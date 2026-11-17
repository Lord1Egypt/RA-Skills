import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { registerExtraCalendarTools, calendarSnapshot } from '../../src/tools/calendar-extra.js';
import * as lib from '../../../gogcli-mcp/src/lib.js';
import { createTestHarness } from '@chrischall/mcp-utils/test';
import { rawTextResult } from '@chrischall/mcp-utils';
import type { ElicitRequest, ElicitResult } from '@modelcontextprotocol/server';
import { pos } from '../../../gogcli-mcp/src/argv.js';
import { resetConfirmTokenState } from '../../../gogcli-mcp/src/send-confirm-token.js';

vi.mock('../../../gogcli-mcp/src/lib.js', async (importOriginal) => {
  const actual = await importOriginal<typeof lib>();
  return { ...actual, runOrDiagnose: vi.fn() };
});

// ============================================================================
// Fleet audit 2026-09-24 SEC-6: a move that emails the guests, an Out of Office
// block that auto-declines (and notifies) every conflicting organizer, and a
// calendar delete all ask first — prompted, refused, and via the token fallback.
// ============================================================================

const ORIGINAL_ENV = { ...process.env };
beforeEach(() => {
  vi.clearAllMocks();
  process.env = { ...ORIGINAL_ENV };
  delete process.env.MCP_CONFIRM_MODE;
  process.env.GOG_ACCOUNT = 'me@example.com';
  resetConfirmTokenState();
});
afterEach(() => { process.env = ORIGINAL_ENV; });

const json = (r: { content: Array<{ text?: string }> }) => JSON.parse(r.content[0]!.text as string);

async function prompted(answer: ElicitResult = { action: 'accept', content: { confirmed: true } }) {
  const seen: ElicitRequest[] = [];
  const harness = await createTestHarness(registerExtraCalendarTools, { elicitation: async (r) => { seen.push(r); return answer; } });
  const details = () => JSON.parse(seen[0]!.params.message.split('\n').slice(1).join('\n')).details;
  return { harness, seen, details };
}
const unprompted = () => createTestHarness(registerExtraCalendarTools);

/** Answer reads keyed by their command words; a `failing` prefix returns an error result. */
function stub(reads: Record<string, string>, failing?: string) {
  vi.mocked(lib.runOrDiagnose).mockImplementation(async (args) => {
    const key = args.filter((a): a is string => typeof a === 'string' && !a.startsWith('--')).join(' ');
    if (failing && key.startsWith(failing)) return { content: [{ type: 'text', text: 'Error: not found' }], isError: true };
    for (const [prefix, out] of Object.entries(reads)) if (key.startsWith(prefix)) return rawTextResult(out);
    return rawTextResult('{"ok":true}');
  });
}
const callsTo = (...words: string[]) => vi.mocked(lib.runOrDiagnose).mock.calls.filter(([args]) =>
  words.every((w, i) => args[i] === w));

describe('gog_calendar_move', () => {
  const EVENT = (etag = '"v1"') => JSON.stringify({ event: {
    id: 'e1', etag, summary: 'Budget review', start: { dateTime: '2026-09-30T14:00:00-04:00' },
    end: { dateTime: '2026-09-30T15:00:00-04:00' }, organizer: { email: 'me@example.com' },
    attendees: [{ email: 'me@example.com', self: true }, { email: 'boss@example.com' }],
  } });
  const ARGS = { calendarId: 'primary', eventId: 'e1', destinationCalendarId: 'team@example.com', sendUpdates: 'all' as const };

  it.each([undefined, 'none'] as const)('moves without reading or asking when sendUpdates is %s', async (sendUpdates) => {
    stub({});
    const { harness, seen } = await prompted();
    await harness.callTool('gog_calendar_move', { ...ARGS, sendUpdates });
    expect(seen).toHaveLength(0);
    expect(callsTo('calendar', 'event')).toHaveLength(0);
    expect(callsTo('calendar', 'move')).toHaveLength(1);
  });

  it('reads the event and asks, naming it, its guests and who is emailed', async () => {
    stub({ 'calendar event': EVENT() });
    const { harness, details } = await prompted();
    await harness.callTool('gog_calendar_move', { ...ARGS, sendUpdates: 'externalOnly' });
    expect(details()).toEqual({
      calendarId: 'primary', eventId: 'e1', destinationCalendarId: 'team@example.com',
      event: { summary: 'Budget review', start: '2026-09-30T14:00:00-04:00', end: '2026-09-30T15:00:00-04:00', organizer: 'me@example.com', guests: ['boss@example.com'] },
      emails: 'guests outside your domain',
    });
    expect(callsTo('calendar', 'move')[0]![0]).toEqual(
      ['calendar', 'move', pos('primary'), pos('e1'), pos('team@example.com'), '--send-updates=externalOnly']);
  });

  it('moves nothing when the user declines, or when the read fails', async () => {
    stub({ 'calendar event': EVENT() });
    const declined = await prompted({ action: 'decline' });
    expect(json(await declined.harness.callTool('gog_calendar_move', ARGS))).toMatchObject({ cancelled: true, action: 'calendar.move' });
    stub({}, 'calendar event');
    const { harness, seen } = await prompted();
    expect((await harness.callTool('gog_calendar_move', ARGS)).isError).toBe(true);
    expect(seen).toHaveLength(0);
    expect(callsTo('calendar', 'move')).toHaveLength(0);
  });

  it('refuses a client that cannot be prompted, pointing at sendUpdates none', async () => {
    process.env.MCP_CONFIRM_MODE = 'refuse';
    stub({ 'calendar event': EVENT() });
    const r = json(await (await unprompted()).callTool('gog_calendar_move', ARGS));
    expect(r).toMatchObject({ reason: 'confirmation-unsupported', action: 'calendar.move' });
    expect(r.note).toMatch(/sendUpdates none/);
  });

  it('token fallback: an event edited between the phases (etag rotated) is DRAFT_CHANGED', async () => {
    process.env.MCP_CONFIRM_MODE = 'ask-user';
    stub({ 'calendar event': EVENT() });
    const harness = await unprompted();
    const p1 = json(await harness.callTool('gog_calendar_move', ARGS));
    expect(p1.preview).toMatchObject({ event: { summary: 'Budget review', guests: ['boss@example.com'] }, emails: 'every guest' });
    stub({ 'calendar event': EVENT('"v2"') });
    expect(json(await harness.callTool('gog_calendar_move', { ...ARGS, confirmToken: p1.confirmToken })))
      .toMatchObject({ error: 'DRAFT_CHANGED' });
    stub({ 'calendar event': EVENT() });
    await harness.callTool('gog_calendar_move', { ...ARGS, confirmToken: p1.confirmToken });
    expect(callsTo('calendar', 'move')).toHaveLength(1);
  });
});

describe('gog_calendar_out_of_office', () => {
  const ARGS = { from: '2026-10-01', to: '2026-10-05' };

  it('creates a block that declines nothing without asking', async () => {
    stub({});
    const { harness, seen } = await prompted();
    await harness.callTool('gog_calendar_out_of_office', { ...ARGS, autoDecline: 'none' });
    expect(seen).toHaveLength(0);
    expect(callsTo('calendar', 'out-of-office')).toHaveLength(1);
  });

  it("asks by default, because gog's default declines every conflicting meeting", async () => {
    stub({});
    const { harness, details } = await prompted();
    await harness.callTool('gog_calendar_out_of_office', ARGS);
    expect(details()).toEqual({
      calendarId: 'primary', from: '2026-10-01', to: '2026-10-05', allDay: false,
      summary: 'Out of office', declines: 'every existing and new conflicting meeting',
    });
    expect(callsTo('calendar', 'out-of-office')).toHaveLength(1);
  });

  it('asks for new-only declines too, showing the message', async () => {
    stub({});
    const { harness, details } = await prompted({ action: 'decline' });
    await harness.callTool('gog_calendar_out_of_office', { ...ARGS, calendarId: 'work', summary: 'Leave', autoDecline: 'new', declineMessage: 'Back Monday', allDay: true });
    expect(details()).toEqual({
      calendarId: 'work', from: '2026-10-01', to: '2026-10-05', allDay: true,
      summary: 'Leave', declines: 'new conflicting invitations', declineMessage: 'Back Monday',
    });
    expect(callsTo('calendar', 'out-of-office')).toHaveLength(0);
  });

  it('refuses a client that cannot be prompted, pointing at autoDecline none', async () => {
    process.env.MCP_CONFIRM_MODE = 'refuse';
    const r = json(await (await unprompted()).callTool('gog_calendar_out_of_office', ARGS));
    expect(r).toMatchObject({ reason: 'confirmation-unsupported', action: 'calendar.out-of-office' });
    expect(r.note).toMatch(/autoDecline none/);
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('token fallback: a changed message is DRAFT_CHANGED; the same call creates', async () => {
    process.env.MCP_CONFIRM_MODE = 'ask-user';
    stub({});
    const harness = await unprompted();
    const args = { ...ARGS, declineMessage: 'Away' };
    const p1 = json(await harness.callTool('gog_calendar_out_of_office', args));
    expect(p1.status).toBe('confirmation-required');
    expect(json(await harness.callTool('gog_calendar_out_of_office', { ...args, declineMessage: 'Gone', confirmToken: p1.confirmToken })))
      .toMatchObject({ error: 'DRAFT_CHANGED' });
    await harness.callTool('gog_calendar_out_of_office', { ...args, confirmToken: p1.confirmToken });
    expect(callsTo('calendar', 'out-of-office')).toHaveLength(1);
  });
});

describe('gog_calendar_delete_calendar', () => {
  const CAL = (etag = '"c1"') => JSON.stringify({ id: 'cal1', summary: 'Team offsite', etag });

  it('reads the calendar and asks by name', async () => {
    stub({ 'api call calendar': CAL() });
    const { harness, details, seen } = await prompted();
    await harness.callTool('gog_calendar_delete_calendar', { calendarId: 'cal1' });
    expect(seen[0]!.params.message).toMatch(/PERMANENTLY/);
    expect(details()).toEqual({ calendar: { id: 'cal1', summary: 'Team offsite' }, deletes: 'the calendar and every event on it, for good' });
    expect(callsTo('api', 'call')[0]![0]).toEqual(['api', 'call', 'calendar', 'v3', 'calendars.get', '--params={"calendarId":"cal1"}']);
    expect(callsTo('calendar', 'delete-calendar')).toHaveLength(1);
  });

  it('deletes nothing when the user declines, or when the read fails', async () => {
    stub({ 'api call calendar': CAL() });
    await (await prompted({ action: 'decline' })).harness.callTool('gog_calendar_delete_calendar', { calendarId: 'cal1' });
    stub({}, 'api call calendar');
    expect((await (await prompted()).harness.callTool('gog_calendar_delete_calendar', { calendarId: 'cal1' })).isError).toBe(true);
    expect(callsTo('calendar', 'delete-calendar')).toHaveLength(0);
  });

  it('refuses a client that cannot be prompted', async () => {
    process.env.MCP_CONFIRM_MODE = 'refuse';
    stub({ 'api call calendar': CAL() });
    const r = json(await (await unprompted()).callTool('gog_calendar_delete_calendar', { calendarId: 'cal1' }));
    expect(r).toMatchObject({ reason: 'confirmation-unsupported', action: 'calendar.delete-calendar' });
    expect(r.note).toMatch(/gog_calendar_unsubscribe/);
  });

  it('token fallback: a calendar changed between the phases (etag rotated) is DRAFT_CHANGED', async () => {
    process.env.MCP_CONFIRM_MODE = 'ask-user';
    stub({ 'api call calendar': CAL() });
    const harness = await unprompted();
    const p1 = json(await harness.callTool('gog_calendar_delete_calendar', { calendarId: 'cal1' }));
    expect(p1.preview.calendar).toEqual({ id: 'cal1', summary: 'Team offsite' });
    stub({ 'api call calendar': CAL('"c2"') });
    expect(json(await harness.callTool('gog_calendar_delete_calendar', { calendarId: 'cal1', confirmToken: p1.confirmToken })))
      .toMatchObject({ error: 'DRAFT_CHANGED' });
    stub({ 'api call calendar': CAL() });
    await harness.callTool('gog_calendar_delete_calendar', { calendarId: 'cal1', confirmToken: p1.confirmToken });
    expect(callsTo('calendar', 'delete-calendar')).toHaveLength(1);
  });

  it('calendarSnapshot reads a bare or result-wrapped calendar and tolerates unreadable output', () => {
    expect(calendarSnapshot(JSON.stringify({ result: { summary: 'X', etag: 'e' } }), 'c')).toEqual({ id: 'c', summary: 'X', etag: 'e' });
    expect(calendarSnapshot('{"summary":7}', 'c')).toEqual({ id: 'c' });
    expect(calendarSnapshot('null', 'c')).toEqual({ id: 'c' });
    expect(calendarSnapshot('nope', 'c')).toEqual({ id: 'c' });
  });
});
