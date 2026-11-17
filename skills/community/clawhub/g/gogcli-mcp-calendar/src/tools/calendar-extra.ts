import { McpServer } from '@modelcontextprotocol/server';
import { z } from 'zod';
import {
  accountParam,
  runOrDiagnose,
  pageTokenParam,
  pageAliasParam,
  resolvePageToken,
  pos,
  CONFIRM_FALLBACK_DESCRIPTION,
  confirmTokenParam,
  eventSnapshot,
  requireDispatchConfirmation,
  resultText,
} from '../../../gogcli-mcp/src/lib.js';
import type { GogArg } from '../../../gogcli-mcp/src/lib.js';

const meetAccess = z.enum(['open', 'trusted', 'restricted']);

// gog >= 0.44: per-space meeting settings. Each is a negatable gog flag
// (--recording / --no-recording) and tri-state here: true and false are sent,
// omitted is not, so create falls back to the account default and update
// leaves that setting alone (gog builds a per-field update mask).
const MEET_SETTINGS = [
  ['recording', 'recording', 'Auto-record when someone allowed to record joins'],
  ['transcription', 'transcription', 'Auto-transcribe when someone allowed to transcribe joins'],
  ['smartNotes', 'smart-notes', 'Auto-generate Gemini smart notes'],
  ['attendanceReport', 'attendance-report', 'Generate an attendance report'],
  ['moderation', 'moderation', 'Host management (moderation)'],
  ['restrictChat', 'restrict-chat', 'Only hosts can chat (turning it on enables moderation)'],
  ['restrictPresent', 'restrict-present', 'Only hosts can share their screen (turning it on enables moderation)'],
  ['restrictReactions', 'restrict-reactions', 'Only hosts can send reactions (turning it on enables moderation)'],
  ['joinAsViewer', 'join-as-viewer', 'Participants join as viewers by default (turning it on enables moderation)'],
] as const;

type MeetSettingKey = typeof MEET_SETTINGS[number][0];
type MeetSettings = Partial<Record<MeetSettingKey, boolean>>;

function meetSettingsSchema(omitted: string) {
  return Object.fromEntries(MEET_SETTINGS.map(([key, , help]) => [
    key, z.boolean().optional().describe(`${help}. true turns it on, false turns it off, omit to ${omitted}.`),
  ])) as Record<MeetSettingKey, z.ZodOptional<z.ZodBoolean>>;
}

function appendMeetSettings(args: GogArg[], settings: MeetSettings): void {
  for (const [key, flag] of MEET_SETTINGS) {
    const value = settings[key];
    if (value !== undefined) args.push(value ? `--${flag}` : `--no-${flag}`);
  }
}

/** A calendar by name, for a delete's prompt; `etag` apart as the token's revision. Unreadable output names nothing. */
export function calendarSnapshot(raw: string, calendarId: string): { id: string; summary?: string; etag?: string } {
  let cal: { summary?: unknown; etag?: unknown } | undefined;
  try {
    const parsed = JSON.parse(raw) as ({ result?: typeof cal } & NonNullable<typeof cal>) | null;
    cal = parsed?.result ?? parsed ?? undefined;
  } catch {
    cal = undefined;
  }
  return {
    id: calendarId,
    ...(typeof cal?.summary === 'string' ? { summary: cal.summary } : {}),
    ...(typeof cal?.etag === 'string' ? { etag: cal.etag } : {}),
  };
}

// Meet spaces are the conferencing surface attached to calendar events,
// so they live in the calendar sub-package.
export function registerExtraCalendarTools(server: McpServer): void {
  server.registerTool('gog_meet_create', {
    description: 'Create a Google Meet space and return its meeting code. Optionally configure recording, transcription, smart notes, attendance reports and host moderation; any setting left out uses the account default.',
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({
      access: meetAccess.optional().describe('Access type (default: trusted)'),
      open: z.boolean().optional().describe('Open the meeting in a browser after creation'),
      ...meetSettingsSchema('use the account default'),
      account: accountParam,
    }),
  }, async ({ access, open, account, ...settings }) => {
    const args: GogArg[] = ['meet', 'create'];
    if (access) args.push(`--access=${access}`);
    if (open) args.push('--open');
    appendMeetSettings(args, settings);
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_meet_get', {
    description: 'Get a Google Meet space by its meeting code.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      meetingCode: z.string().describe('Meeting code (e.g. abc-defg-hij)'),
      account: accountParam,
    }),
  }, async ({ meetingCode, account }) => {
    return runOrDiagnose(['meet', 'get', pos(meetingCode)], { account });
  });

  server.registerTool('gog_meet_update', {
    description: 'Update a Google Meet space configuration: access type, recording, transcription, smart notes, attendance reports and host moderation. Only the settings you pass change; every other one keeps its current value.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      meetingCode: z.string().describe('Meeting code'),
      access: meetAccess.optional().describe('Access type'),
      ...meetSettingsSchema('keep the current value'),
      account: accountParam,
    }),
  }, async ({ meetingCode, access, account, ...settings }) => {
    const args: GogArg[] = ['meet', 'update', pos(meetingCode)];
    if (access) args.push(`--access=${access}`);
    appendMeetSettings(args, settings);
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_meet_end', {
    description: 'End the active conference in a Google Meet space.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      meetingCode: z.string().describe('Meeting code'),
      account: accountParam,
    }),
  }, async ({ meetingCode, account }) => {
    return runOrDiagnose(['meet', 'end', pos(meetingCode), '--force'], { account }); // gog gates this op; without --force the runner's --no-input makes it refuse
  });

  server.registerTool('gog_meet_history', {
    description: 'List past calls (conferences) in a Google Meet space.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      meetingCode: z.string().describe('Meeting code'),
      max: z.number().optional().describe('Max results (default: 20)'),
      pageToken: pageTokenParam,
      page: pageAliasParam,
      all: z.boolean().optional().describe('Fetch all pages'),
      account: accountParam,
    }),
  }, async ({ meetingCode, max, pageToken, page, all, account }) => {
    const args: GogArg[] = ['meet', 'history', pos(meetingCode)];
    if (max !== undefined) args.push(`--max=${max}`);
    const token = resolvePageToken({ pageToken, page });
    if (token) args.push(`--page=${token}`);
    if (all) args.push('--all');
    return runOrDiagnose(args, { account });
  });

  // Zoom S2S OAuth credentials are scoped to Zoom-as-calendar-conferencing
  // today (the `--with-zoom` flag on calendar create/update), so the auth
  // helpers live in the calendar extras alongside meet space management.
  server.registerTool('gog_zoom_auth_setup', {
    description: 'Store Zoom Server-to-Server (S2S) OAuth credentials so calendar events can be attached to Zoom meetings via the --with-zoom flag on gog_calendar_create / gog_calendar_update. Credentials are saved in gogcli\'s keyring under the given alias.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      accountId: z.string().describe('Zoom S2S OAuth account ID'),
      clientId: z.string().describe('Zoom S2S OAuth client ID'),
      clientSecret: z.string().describe('Zoom S2S OAuth client secret'),
      alias: z.string().optional().describe('Zoom credential alias (default: "default")'),
      skipValidate: z.boolean().optional().describe('Store credentials without calling Zoom /users/me to validate'),
    }),
  }, async ({ accountId, clientId, clientSecret, alias, skipValidate }) => {
    const args: GogArg[] = ['zoom', 'auth', 'setup'];
    if (alias) args.push(`--alias=${alias}`);
    args.push(`--account-id=${accountId}`);
    args.push(`--client-id=${clientId}`);
    args.push(`--client-secret=${clientSecret}`);
    if (skipValidate) args.push('--skip-validate');
    return runOrDiagnose(args, {});
  });

  server.registerTool('gog_zoom_auth_doctor', {
    description: 'Validate stored Zoom S2S OAuth credentials by calling Zoom /users/me.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      alias: z.string().optional().describe('Zoom credential alias to check (default: "default")'),
    }),
  }, async ({ alias }) => {
    const args: GogArg[] = ['zoom', 'auth', 'doctor'];
    if (alias) args.push(`--alias=${alias}`);
    return runOrDiagnose(args, {});
  });

  // --- gog 0.19.0 calendar reads & CRUD ---

  server.registerTool('gog_calendar_calendars', {
    description: 'List the calendars in your calendar list (id, summary, access role, primary flag).',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      max: z.number().optional().describe('Max results (default: 100)'),
      pageToken: pageTokenParam,
      page: pageAliasParam,
      all: z.boolean().optional().describe('Fetch all pages'),
      account: accountParam,
    }),
  }, async ({ max, pageToken, page, all, account }) => {
    const args: GogArg[] = ['calendar', 'calendars'];
    if (max !== undefined) args.push(`--max=${max}`);
    const token = resolvePageToken({ pageToken, page });
    if (token) args.push(`--page=${token}`);
    if (all) args.push('--all');
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_calendar_search', {
    description: 'Full-text search for events matching a query string, with optional time filters. '
      + 'Describe the window ONE way only (gog >= 0.36.0 rejects the rest as ambiguous instead of discarding a flag): one of today / tomorrow / week on its own, '
      + 'or from + to, or from + days, or days on its own. The fixed presets cannot be combined with from, to or days, and days cannot be combined with to.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      query: z.string().describe('Search query'),
      from: z.string().optional().describe('Start time (RFC3339, date, or relative: now, today, tomorrow, monday)'),
      to: z.string().optional().describe('End time (RFC3339, date, or relative: now, today, tomorrow, monday). Mutually exclusive with days.'),
      today: z.boolean().optional().describe('Today only. A complete window on its own — not combinable with from/to/days.'),
      tomorrow: z.boolean().optional().describe('Tomorrow only. A complete window on its own — not combinable with from/to/days.'),
      week: z.boolean().optional().describe('This week (uses weekStart, default Mon). A complete window on its own — not combinable with from/to/days.'),
      // gog >= 0.36.0 (openclaw/gogcli#981) anchors --days at --from. It used
      // to mean "next N days from today" no matter what --from said, which is
      // why the old description here read that way.
      days: z.number().optional().describe('Window LENGTH in days, measured from `from` when one is given and from today otherwise — NOT always "the next N days".'),
      weekStart: z.string().optional().describe('Week start day for week (sun, mon, ...)'),
      calendar: z.string().optional().describe('Calendar ID (default: primary)'),
      max: z.number().optional().describe('Max results (default: 25)'),
      account: accountParam,
    }),
  }, async ({ query, from, to, today, tomorrow, week, days, weekStart, calendar, max, account }) => {
    const args: GogArg[] = ['calendar', 'search', pos(query)];
    if (from) args.push(`--from=${from}`);
    if (to) args.push(`--to=${to}`);
    if (today) args.push('--today');
    if (tomorrow) args.push('--tomorrow');
    if (week) args.push('--week');
    if (days !== undefined) args.push(`--days=${days}`);
    if (weekStart) args.push(`--week-start=${weekStart}`);
    if (calendar) args.push(`--calendar=${calendar}`);
    if (max !== undefined) args.push(`--max=${max}`);
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_calendar_changed', {
    description: 'List most recently changed events (including cancellations/deletions) across one or more calendars, ordered by last-modification time. Requires gog >= 0.31.1.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      calendarId: z.string().optional().describe('Calendar ID (default: primary)'),
      calendarIds: z.string().optional().describe('Comma-separated calendar IDs, names, or indices'),
      since: z.string().optional().describe('Lower bound for last-modification time (RFC3339, date, or Go duration like 24h, 168h; default: 720h / 30 days). Google rejects windows too far in the past (410 updatedMinTooLongAgo) — retry with a shorter duration if that happens'),
      max: z.number().optional().describe('Max results (default: 10)'),
      all: z.boolean().optional().describe('Fetch from all calendars'),
      account: accountParam,
    }),
  }, async ({ calendarId, calendarIds, since, max, all, account }) => {
    const args: GogArg[] = ['calendar', 'changed'];
    if (calendarId) args.push(pos(calendarId));
    if (calendarIds) args.push(`--calendars=${calendarIds}`);
    if (since) args.push(`--since=${since}`);
    if (max !== undefined) args.push(`--max=${max}`);
    if (all) args.push('--all');
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_calendar_freebusy', {
    description: 'Query free/busy intervals for one or more calendars over a time window.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      from: z.string().describe('Start time (RFC3339, required)'),
      to: z.string().describe('End time (RFC3339, required)'),
      calendarIds: z.string().optional().describe('Comma-separated calendar IDs, names, or indices'),
      all: z.boolean().optional().describe('Query all calendars'),
      account: accountParam,
    }),
  }, async ({ from, to, calendarIds, all, account }) => {
    const args: GogArg[] = ['calendar', 'freebusy'];
    if (calendarIds) args.push(pos(calendarIds));
    args.push(`--from=${from}`);
    args.push(`--to=${to}`);
    if (all) args.push('--all');
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_calendar_colors', {
    description: 'Show the available calendar and event color palette (color IDs to hex values).',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      account: accountParam,
    }),
  }, async ({ account }) => {
    return runOrDiagnose(['calendar', 'colors'], { account });
  });

  server.registerTool('gog_calendar_acl', {
    description: 'List the access control list (sharing rules) for a calendar.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      calendarId: z.string().describe('Calendar ID'),
      max: z.number().optional().describe('Max results (default: 100)'),
      pageToken: pageTokenParam,
      page: pageAliasParam,
      all: z.boolean().optional().describe('Fetch all pages'),
      account: accountParam,
    }),
  }, async ({ calendarId, max, pageToken, page, all, account }) => {
    const args: GogArg[] = ['calendar', 'acl', pos(calendarId)];
    if (max !== undefined) args.push(`--max=${max}`);
    const token = resolvePageToken({ pageToken, page });
    if (token) args.push(`--page=${token}`);
    if (all) args.push('--all');
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_calendar_move', {
    description: 'Move an event from one calendar to another; the destination calendar becomes the organizer. With '
      + 'sendUpdates all or externalOnly Google emails the guests, so this reads the event and asks the MCP host to '
      + 'show the user a confirmation prompt with the event, its guests and the destination first; a move that '
      + 'notifies nobody (the default) is made without asking.' + CONFIRM_FALLBACK_DESCRIPTION,
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({
      calendarId: z.string().describe('Source calendar ID'),
      eventId: z.string().describe('Event ID'),
      destinationCalendarId: z.string().describe('Destination calendar ID that becomes the event organizer'),
      sendUpdates: z.enum(['all', 'externalOnly', 'none']).optional().describe('Notification mode (default: none). all / externalOnly email the guests and ask the user first.'),
      account: accountParam,
      confirmToken: confirmTokenParam,
    }),
  }, async ({ calendarId, eventId, destinationCalendarId, sendUpdates, account, confirmToken }, ctx) => {
    const args: GogArg[] = ['calendar', 'move', pos(calendarId), pos(eventId), pos(destinationCalendarId)];
    if (sendUpdates) args.push(`--send-updates=${sendUpdates}`);
    if (sendUpdates === 'all' || sendUpdates === 'externalOnly') {
      const got = await runOrDiagnose(['calendar', 'event', pos(calendarId), pos(eventId)], { account });
      if (got.isError) return got;
      const { etag, ...event } = eventSnapshot(resultText(got));
      const view = { calendarId, eventId, event, destinationCalendarId, emails: sendUpdates === 'all' ? 'every guest' : 'guests outside your domain' };
      const confirmation = await requireDispatchConfirmation(ctx, {
        action: 'calendar.move',
        message: 'Review and confirm moving this event — Google will email the guests:',
        confirmationLabel: 'Confirm that this event should be moved and the guests notified now.',
        details: view,
        unsupportedNote: 'Move it with sendUpdates none instead, which notifies nobody.',
        fallback: {
          args: { calendarId, eventId, destinationCalendarId, sendUpdates, account },
          tool: 'gog_calendar_move',
          account,
          confirmToken,
          subject: () => ({ target: `${calendarId}/${eventId}`, revision: etag, payload: view, preview: view }),
        },
      });
      if (confirmation) return confirmation;
    }
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_calendar_out_of_office', {
    description: 'Create an Out of Office event that auto-declines invitations during the block. gog auto-declines '
      + 'EVERY conflicting meeting by default (autoDecline all), and each organizer is notified, so unless autoDecline '
      + 'is none this asks the MCP host to show the user a confirmation prompt with the window, the decline mode and '
      + 'the message first; nothing is created unless they accept.' + CONFIRM_FALLBACK_DESCRIPTION,
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      from: z.string().describe('Start date or datetime (RFC3339 or YYYY-MM-DD)'),
      to: z.string().describe('End date or datetime (RFC3339 or YYYY-MM-DD)'),
      calendarId: z.string().optional().describe('Calendar ID (default: primary)'),
      summary: z.string().optional().describe('Out of office title (default: "Out of office")'),
      autoDecline: z.enum(['none', 'all', 'new']).optional().describe('Auto-decline mode (default: all — declines existing AND new conflicting meetings; none notifies nobody and does not ask)'),
      declineMessage: z.string().optional().describe('Message for declined invitations'),
      allDay: z.boolean().optional().describe('Create as an all-day event'),
      account: accountParam,
      confirmToken: confirmTokenParam,
    }),
  }, async ({ from, to, calendarId, summary, autoDecline, declineMessage, allDay, account, confirmToken }, ctx) => {
    const args: GogArg[] = ['calendar', 'out-of-office'];
    if (calendarId) args.push(pos(calendarId));
    args.push(`--from=${from}`);
    args.push(`--to=${to}`);
    if (summary) args.push(`--summary=${summary}`);
    if (autoDecline) args.push(`--auto-decline=${autoDecline}`);
    if (declineMessage) args.push(`--decline-message=${declineMessage}`);
    if (allDay) args.push('--all-day');
    if (autoDecline !== 'none') {
      const mode = autoDecline ?? 'all';
      const view = {
        calendarId: calendarId ?? 'primary',
        from,
        to,
        allDay: Boolean(allDay),
        summary: summary ?? 'Out of office',
        declines: mode === 'all' ? 'every existing and new conflicting meeting' : 'new conflicting invitations',
        declineMessage,
      };
      const confirmation = await requireDispatchConfirmation(ctx, {
        action: 'calendar.out-of-office',
        message: 'Review and confirm this Out of Office block — conflicting meetings are declined and their organizers notified:',
        confirmationLabel: 'Confirm that meetings in this window should be auto-declined.',
        details: view,
        unsupportedNote: 'Create it with autoDecline none instead; the user can turn on auto-decline in Google Calendar.',
        fallback: {
          args: { from, to, calendarId, summary, autoDecline, declineMessage, allDay, account },
          tool: 'gog_calendar_out_of_office',
          account,
          confirmToken,
          subject: () => ({ target: view.calendarId, payload: view, preview: view }),
        },
      });
      if (confirmation) return confirmation;
    }
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_calendar_unsubscribe', {
    description: 'Remove a calendar from your calendar list (the underlying calendar is not deleted — you can re-subscribe). For deleting a secondary calendar you own, use gog_calendar_delete_calendar.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      calendarId: z.string().describe('Calendar ID or alias to remove from your calendar list'),
      account: accountParam,
    }),
  }, async ({ calendarId, account }) => {
    return runOrDiagnose(['calendar', 'unsubscribe', pos(calendarId)], { account });
  });

  server.registerTool('gog_calendar_delete_calendar', {
    description: 'Permanently delete an owned secondary calendar and all its events. Cannot delete your primary calendar. '
      + 'To merely remove a calendar you do not own from your list, use gog_calendar_unsubscribe. Reads the calendar and '
      + 'asks the MCP host to show the user a confirmation prompt naming it first; nothing is deleted unless they accept.'
      + CONFIRM_FALLBACK_DESCRIPTION,
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      calendarId: z.string().describe('Owned secondary calendar ID or alias'),
      account: accountParam,
      confirmToken: confirmTokenParam,
    }),
  }, async ({ calendarId, account, confirmToken }, ctx) => {
    const got = await runOrDiagnose(
      ['api', 'call', 'calendar', 'v3', 'calendars.get', `--params=${JSON.stringify({ calendarId })}`], { account });
    if (got.isError) return got;
    const { etag, ...calendar } = calendarSnapshot(resultText(got), calendarId);
    const view = { calendar, deletes: 'the calendar and every event on it, for good' };
    const confirmation = await requireDispatchConfirmation(ctx, {
      action: 'calendar.delete-calendar',
      message: 'Review and confirm PERMANENTLY deleting this calendar and all of its events:',
      confirmationLabel: 'Confirm that this calendar should be deleted now.',
      details: view,
      unsupportedNote: 'Ask the user to delete it from Google Calendar\'s settings, or use gog_calendar_unsubscribe to only hide it.',
      fallback: {
        args: { calendarId, account },
        tool: 'gog_calendar_delete_calendar',
        account,
        confirmToken,
        subject: () => ({ target: calendarId, revision: etag, payload: view, preview: view }),
      },
    });
    if (confirmation) return confirmation;
    return runOrDiagnose(['calendar', 'delete-calendar', pos(calendarId), '--force'], { account }); // gog gates this op; without --force the runner's --no-input makes it refuse
  });

  server.registerTool('gog_meet_participants', {
    description: 'List participants from the latest (or a specific) Meet call.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      meetingCode: z.string().describe('Meeting code'),
      conference: z.string().optional().describe('Specific conference ID (default: most recent)'),
      max: z.number().optional().describe('Max results (default: 50)'),
      pageToken: pageTokenParam,
      page: pageAliasParam,
      all: z.boolean().optional().describe('Fetch all pages'),
      account: accountParam,
    }),
  }, async ({ meetingCode, conference, max, pageToken, page, all, account }) => {
    const args: GogArg[] = ['meet', 'participants', pos(meetingCode)];
    if (conference) args.push(`--conference=${conference}`);
    if (max !== undefined) args.push(`--max=${max}`);
    const token = resolvePageToken({ pageToken, page });
    if (token) args.push(`--page=${token}`);
    if (all) args.push('--all');
    return runOrDiagnose(args, { account });
  });
}
