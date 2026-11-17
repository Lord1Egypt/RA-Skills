import { describe, it, expect, vi, beforeEach } from 'vitest';
import { registerExtraCalendarTools } from '../../src/tools/calendar-extra.js';
import * as lib from '../../../gogcli-mcp/src/lib.js';
import { createTestHarness, type TestHarness } from '@chrischall/mcp-utils/test';
import { rawTextResult } from '@chrischall/mcp-utils';
import { pos } from '../../../gogcli-mcp/src/argv.js';

vi.mock('../../../gogcli-mcp/src/lib.js', async (importOriginal) => {
  const actual = await importOriginal<typeof lib>();
  return {
    ...actual,
    runOrDiagnose: vi.fn(),
  };
});

let harness: TestHarness;

beforeEach(async () => {
  vi.clearAllMocks();
  vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{}'));
  // The gated tools (move with sendUpdates, out-of-office, delete-calendar) are
  // exercised prompt-by-prompt in calendar-extra-gates.test.ts; here the user accepts.
  harness = await createTestHarness(registerExtraCalendarTools, {
    elicitation: async () => ({ action: 'accept', content: { confirmed: true } }),
  });
});

describe('gog_meet_create', () => {
  it('calls runOrDiagnose with no flags', async () => {
    await harness.callTool('gog_meet_create', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['meet', 'create'], { account: undefined });
  });

  it('passes --access and --open when provided', async () => {
    await harness.callTool('gog_meet_create', { access: 'open', open: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['meet', 'create', '--access=open', '--open'],
      { account: undefined },
    );
  });

  it('omits --open when false', async () => {
    await harness.callTool('gog_meet_create', { open: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['meet', 'create'], { account: undefined });
  });

  it('passes each meeting setting as --flag / --no-flag, omitting unset ones', async () => {
    await harness.callTool('gog_meet_create', {
      recording: true, transcription: false, smartNotes: true, attendanceReport: false,
      moderation: true, restrictChat: true, restrictPresent: false, restrictReactions: true, joinAsViewer: false,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith([
      'meet', 'create',
      '--recording', '--no-transcription', '--smart-notes', '--no-attendance-report',
      '--moderation', '--restrict-chat', '--no-restrict-present', '--restrict-reactions', '--no-join-as-viewer',
    ], { account: undefined });
  });
});

describe('gog_meet_get', () => {
  it('calls runOrDiagnose with meetingCode', async () => {
    await harness.callTool('gog_meet_get', { meetingCode: 'abc-defg-hij' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['meet', 'get', pos('abc-defg-hij')], { account: undefined });
  });
});

describe('gog_meet_update', () => {
  it('calls runOrDiagnose with meetingCode and --access', async () => {
    await harness.callTool('gog_meet_update', { meetingCode: 'abc-defg-hij', access: 'restricted' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['meet', 'update', pos('abc-defg-hij'), '--access=restricted'],
      { account: undefined },
    );
  });

  it('omits --access when not provided', async () => {
    await harness.callTool('gog_meet_update', { meetingCode: 'abc-defg-hij' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['meet', 'update', pos('abc-defg-hij')], { account: undefined });
  });

  it('sends only the settings supplied, so gog leaves the rest untouched', async () => {
    await harness.callTool('gog_meet_update', { meetingCode: 'abc-defg-hij', recording: false, restrictChat: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['meet', 'update', pos('abc-defg-hij'), '--no-recording', '--restrict-chat'],
      { account: undefined },
    );
  });
});

describe('gog_meet_end', () => {
  it('calls runOrDiagnose with meetingCode', async () => {
    await harness.callTool('gog_meet_end', { meetingCode: 'abc-defg-hij' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['meet', 'end', pos('abc-defg-hij'), '--force'], { account: undefined });
  });
});

describe('gog_meet_history', () => {
  it('calls runOrDiagnose with meetingCode', async () => {
    await harness.callTool('gog_meet_history', { meetingCode: 'abc-defg-hij' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['meet', 'history', pos('abc-defg-hij')], { account: undefined });
  });

  it('passes pagination flags', async () => {
    await harness.callTool('gog_meet_history', {
      meetingCode: 'abc-defg-hij',
      max: 50,
      page: 'tok',
      all: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['meet', 'history', pos('abc-defg-hij'), '--max=50', '--page=tok', '--all'],
      { account: undefined },
    );
  });

  it('omits --all when false', async () => {
    await harness.callTool('gog_meet_history', { meetingCode: 'abc-defg-hij', all: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['meet', 'history', pos('abc-defg-hij')], { account: undefined });
  });
});

// --- gog 0.18.0 Zoom S2S OAuth (Zoom is calendar conferencing — lives here) ---

describe('gog_zoom_auth_setup', () => {
  it('passes credentials and uses default alias when omitted', async () => {
    await harness.callTool('gog_zoom_auth_setup', {
      accountId: 'acct',
      clientId: 'cid',
      clientSecret: 'csecret',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'zoom', 'auth', 'setup',
        '--account-id=acct', '--client-id=cid', '--client-secret=csecret',
      ],
      { account: undefined },
    );
  });

  it('passes --alias and --skip-validate when provided', async () => {
    await harness.callTool('gog_zoom_auth_setup', {
      accountId: 'acct', clientId: 'cid', clientSecret: 'csecret',
      alias: 'work', skipValidate: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'zoom', 'auth', 'setup',
        '--alias=work',
        '--account-id=acct', '--client-id=cid', '--client-secret=csecret',
        '--skip-validate',
      ],
      { account: undefined },
    );
  });
});

describe('gog_zoom_auth_doctor', () => {
  it('validates default alias', async () => {
    await harness.callTool('gog_zoom_auth_doctor', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['zoom', 'auth', 'doctor'], { account: undefined });
  });

  it('passes --alias when provided', async () => {
    await harness.callTool('gog_zoom_auth_doctor', { alias: 'work' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['zoom', 'auth', 'doctor', '--alias=work'],
      { account: undefined },
    );
  });
});

// --- gog 0.19.0 calendar reads & CRUD ---

describe('gog_calendar_calendars', () => {
  it('calls runOrDiagnose with no flags', async () => {
    await harness.callTool('gog_calendar_calendars', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['calendar', 'calendars'], { account: undefined });
  });

  it('passes pagination flags', async () => {
    await harness.callTool('gog_calendar_calendars', { max: 50, page: 'tok', all: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'calendars', '--max=50', '--page=tok', '--all'],
      { account: undefined },
    );
  });

  it('omits --all when false', async () => {
    await harness.callTool('gog_calendar_calendars', { all: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['calendar', 'calendars'], { account: undefined });
  });
});

describe('gog_calendar_search', () => {
  it('calls runOrDiagnose with just the query', async () => {
    await harness.callTool('gog_calendar_search', { query: 'standup' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['calendar', 'search', pos('standup')], { account: undefined });
  });

  // One case per LEGAL window, not one case passing every flag at once. gog
  // >= 0.36.0 (openclaw/gogcli#981) rejects a fixed preset alongside
  // from/to/days, and days alongside to, with exit 2 — so the all-flags array
  // this used to assert is one gog will not run, and a mocked test asserting
  // it would keep passing forever while the tool was broken in the field.
  it('passes an explicit from/to range with the non-window filters', async () => {
    await harness.callTool('gog_calendar_search', {
      query: 'standup',
      from: 'today',
      to: 'tomorrow',
      calendar: 'primary',
      max: 10,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'calendar', 'search', pos('standup'),
        '--from=today', '--to=tomorrow',
        '--calendar=primary', '--max=10',
      ],
      { account: undefined },
    );
  });

  it('anchors --days at --from when both are given', async () => {
    await harness.callTool('gog_calendar_search', { query: 'standup', from: '2026-09-25', days: 7 });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'search', pos('standup'), '--from=2026-09-25', '--days=7'],
      { account: undefined },
    );
  });

  it('passes each fixed preset on its own', async () => {
    for (const [param, flag] of [['today', '--today'], ['tomorrow', '--tomorrow'], ['week', '--week']] as const) {
      vi.mocked(lib.runOrDiagnose).mockClear();
      await harness.callTool('gog_calendar_search', { query: 'standup', [param]: true });
      expect(lib.runOrDiagnose).toHaveBeenCalledWith(
        ['calendar', 'search', pos('standup'), flag],
        { account: undefined },
      );
    }
  });

  it('passes --week-start alongside --week', async () => {
    await harness.callTool('gog_calendar_search', { query: 'standup', week: true, weekStart: 'sun' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'search', pos('standup'), '--week', '--week-start=sun'],
      { account: undefined },
    );
  });

  it('omits boolean flags when false', async () => {
    await harness.callTool('gog_calendar_search', {
      query: 'standup', today: false, tomorrow: false, week: false,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['calendar', 'search', pos('standup')], { account: undefined });
  });
});

describe('gog_calendar_changed', () => {
  it('calls runOrDiagnose with no flags by default', async () => {
    await harness.callTool('gog_calendar_changed', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['calendar', 'changed'], { account: undefined });
  });

  it('passes calendarId positionally and all flags', async () => {
    await harness.callTool('gog_calendar_changed', {
      calendarId: 'primary',
      calendarIds: 'work,personal',
      since: '48h',
      max: 25,
      all: true,
      account: 'me@example.com',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'changed', pos('primary'), '--calendars=work,personal', '--since=48h', '--max=25', '--all'],
      { account: 'me@example.com' },
    );
  });

  it('omits --all when false', async () => {
    await harness.callTool('gog_calendar_changed', { all: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['calendar', 'changed'], { account: undefined });
  });
});

describe('gog_calendar_freebusy', () => {
  it('calls runOrDiagnose with required from/to only', async () => {
    await harness.callTool('gog_calendar_freebusy', { from: 'A', to: 'B' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'freebusy', '--from=A', '--to=B'],
      { account: undefined },
    );
  });

  it('passes calendarIds and --all when provided', async () => {
    await harness.callTool('gog_calendar_freebusy', {
      from: 'A', to: 'B', calendarIds: 'primary,team@x.com', all: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'freebusy', pos('primary,team@x.com'), '--from=A', '--to=B', '--all'],
      { account: undefined },
    );
  });

  it('omits --all when false', async () => {
    await harness.callTool('gog_calendar_freebusy', { from: 'A', to: 'B', all: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'freebusy', '--from=A', '--to=B'],
      { account: undefined },
    );
  });
});

describe('gog_calendar_colors', () => {
  it('calls runOrDiagnose with the colors subcommand', async () => {
    await harness.callTool('gog_calendar_colors', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['calendar', 'colors'], { account: undefined });
  });
});

describe('gog_calendar_acl', () => {
  it('calls runOrDiagnose with calendarId only', async () => {
    await harness.callTool('gog_calendar_acl', { calendarId: 'primary' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['calendar', 'acl', pos('primary')], { account: undefined });
  });

  it('passes pagination flags', async () => {
    await harness.callTool('gog_calendar_acl', { calendarId: 'primary', max: 25, page: 'tok', all: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'acl', pos('primary'), '--max=25', '--page=tok', '--all'],
      { account: undefined },
    );
  });

  it('omits --all when false', async () => {
    await harness.callTool('gog_calendar_acl', { calendarId: 'primary', all: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['calendar', 'acl', pos('primary')], { account: undefined });
  });
});

describe('gog_calendar_move', () => {
  it('calls runOrDiagnose with the three positionals', async () => {
    await harness.callTool('gog_calendar_move', {
      calendarId: 'primary', eventId: 'ev1', destinationCalendarId: 'team@x.com',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'move', pos('primary'), pos('ev1'), pos('team@x.com')],
      { account: undefined },
    );
  });

  it('passes --send-updates when provided', async () => {
    await harness.callTool('gog_calendar_move', {
      calendarId: 'primary', eventId: 'ev1', destinationCalendarId: 'team@x.com',
      sendUpdates: 'all',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'move', pos('primary'), pos('ev1'), pos('team@x.com'), '--send-updates=all'],
      { account: undefined },
    );
  });
});

describe('gog_calendar_out_of_office', () => {
  it('calls runOrDiagnose with required from/to only', async () => {
    await harness.callTool('gog_calendar_out_of_office', { from: '2026-06-01', to: '2026-06-05' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'out-of-office', '--from=2026-06-01', '--to=2026-06-05'],
      { account: undefined },
    );
  });

  it('passes calendarId and all optional flags when provided', async () => {
    await harness.callTool('gog_calendar_out_of_office', {
      from: '2026-06-01', to: '2026-06-05',
      calendarId: 'primary',
      summary: 'Vacation',
      autoDecline: 'new',
      declineMessage: 'Away',
      allDay: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'calendar', 'out-of-office', pos('primary'),
        '--from=2026-06-01', '--to=2026-06-05',
        '--summary=Vacation', '--auto-decline=new',
        '--decline-message=Away', '--all-day',
      ],
      { account: undefined },
    );
  });

  it('omits --all-day when false', async () => {
    await harness.callTool('gog_calendar_out_of_office', { from: '2026-06-01', to: '2026-06-05', allDay: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'out-of-office', '--from=2026-06-01', '--to=2026-06-05'],
      { account: undefined },
    );
  });
});

describe('gog_meet_participants', () => {
  it('calls runOrDiagnose with meetingCode', async () => {
    await harness.callTool('gog_meet_participants', { meetingCode: 'abc-defg-hij' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['meet', 'participants', pos('abc-defg-hij')],
      { account: undefined },
    );
  });

  it('passes --conference and pagination flags', async () => {
    await harness.callTool('gog_meet_participants', {
      meetingCode: 'abc-defg-hij',
      conference: 'conf123',
      max: 100,
      page: 'tok',
      all: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'meet', 'participants', pos('abc-defg-hij'),
        '--conference=conf123',
        '--max=100',
        '--page=tok',
        '--all',
      ],
      { account: undefined },
    );
  });

  it('omits --all when false', async () => {
    await harness.callTool('gog_meet_participants', { meetingCode: 'abc-defg-hij', all: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['meet', 'participants', pos('abc-defg-hij')],
      { account: undefined },
    );
  });
});

describe('gog_calendar_unsubscribe', () => {
  it('calls runOrDiagnose with calendarId', async () => {
    await harness.callTool('gog_calendar_unsubscribe', { calendarId: 'cal@group.calendar.google.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'unsubscribe', pos('cal@group.calendar.google.com')],
      { account: undefined },
    );
  });

  it('passes account through', async () => {
    await harness.callTool('gog_calendar_unsubscribe', { calendarId: 'cal', account: 'me@x.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'unsubscribe', pos('cal')],
      { account: 'me@x.com' },
    );
  });
});

describe('gog_calendar_delete_calendar', () => {
  it('calls runOrDiagnose with calendarId', async () => {
    await harness.callTool('gog_calendar_delete_calendar', { calendarId: 'cal' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'delete-calendar', pos('cal'), '--force'],
      { account: undefined },
    );
  });

  it('passes account through', async () => {
    await harness.callTool('gog_calendar_delete_calendar', { calendarId: 'cal', account: 'me@x.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['calendar', 'delete-calendar', pos('cal'), '--force'],
      { account: 'me@x.com' },
    );
  });
});
