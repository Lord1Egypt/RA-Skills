#!/usr/bin/env node

import { ICalendarEvents } from 'icalendar-events';
import { DateTime, Interval } from 'luxon';
import { readFile } from 'fs/promises';
import path from 'path';
import { homedir } from 'os';

// ── Extract the core logic into an exported function ────────────────────────
export async function processICalEvents(params) {

  try {
    if (!params?.source) {
      throw new Error('No source param provided');
    }

    let icsContent;
    if (params.source.startsWith('http://') || params.source.startsWith('https://')) {
      const res = await fetch(params.source);
      if (!res.ok) {
        throw new Error(`Failed to fetch ICS: HTTP ${res.status}`);
      }
      icsContent = await res.text();
    } else {
      let filePath = params.source.trim();

      // 1. Effective home (respects OPENCLAW_HOME)
      const effectiveHome = process.env.OPENCLAW_HOME 
        || process.env.HOME 
        || homedir() 
        || '/home/pi';

      // 2. Expand ~
      if (filePath.startsWith('~')) {
        filePath = path.join(effectiveHome, filePath.slice(1));
      }

      const safePath = path.resolve(filePath);

      // 3. Determine workspace (supports default + named profiles)
      let workspaceDir = process.env.OPENCLAW_WORKSPACE;
      if (!workspaceDir) {
        const profile = process.env.OPENCLAW_PROFILE || 'default';
        const base = path.join(effectiveHome, '.openclaw');
        workspaceDir = profile === 'default' 
          ? path.join(base, 'workspace')
          : path.join(base, `workspace-${profile}`);
      }

      // 4. Allowed paths
      const allowedBasePaths = [
        workspaceDir,
        path.resolve('.')   // skill folder itself
      ];

      const isAllowed = allowedBasePaths.some(base => 
        safePath === base || safePath.startsWith(base + path.sep)
      );

      if (!isAllowed) {
        throw new Error(
          `Access restricted by iCalendar Events Parser.\n\n` +
          `This skill can only read files from:\n` +
          `• ${workspaceDir} (your current workspace)\n` +
          `• The skill's own folder\n\n` +
          `Example: "~/openclaw/workspace/my-calendar.ics" or "./my-calendar.ics"`
        );
      }

      icsContent = await readFile(safePath, 'utf-8');
    }

    const timeZone = params.timeZone || params.timezone || 'UTC';

    let range = null;
    if (params.start && params.end) {
      const firstDate = DateTime.fromFormat(params.start, "yyyy-MM-dd", { zone: timeZone }).startOf('day');
      const lastDate  = DateTime.fromFormat(params.end,   "yyyy-MM-dd", { zone: timeZone }).endOf('day');
      range = Interval.fromDateTimes(firstDate, lastDate);
    }

    const calendar = new ICalendarEvents(icsContent, range, {
      withVEvent: false,
      includeDTSTART: false
    });

    let events = calendar.events;

    if (params.filter) {
      const f = params.filter;
      events = events.filter(ev => {
        if (f.titleContains && !ev.summary?.toLowerCase().includes(f.titleContains.toLowerCase())) return false;
        if (f.descriptionContains && !ev.description?.toLowerCase().includes(f.descriptionContains.toLowerCase())) return false;
        if (f.locationContains && !ev.location?.toLowerCase().includes(f.locationContains.toLowerCase())) return false;
        return true;
      });
    }

    return {
      success: true,
      count: events.length,
      events: events.map(ev => ({
        uid: ev.uid,
        title: ev.summary || '(No title)',
        start: ev.dtstart?.setZone(timeZone).toISO({ extendedZone: true }),
        end:   ev.dtend?.setZone(timeZone).toISO({ extendedZone: true }),
        allday: ev.allday || false,
        description: ev.description || '',
        location: ev.location || '',
        recurrenceId: null,
        originalRRule: null
      })),
      message: `${events.length} event(s) found`
    };
  } catch (err) {
    return {
      success: false,
      error: err.message,
      stack: process.env.NODE_ENV === 'development' ? err.stack : undefined
    };
  }
}

// ── CLI entry point ─────────────────────────────────────────────────────────
async function runAsCli() {
  let input = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => { input += chunk; });
  process.stdin.on('end', async () => {
    try {
      if (!input.trim()) {
        throw new Error('No input received on stdin');
      }

      const { params } = JSON.parse(input);

      const result = await processICalEvents(params);

      if (result.success) {
        console.log(JSON.stringify(result, null, 2));
        process.exit(0);
      } else {
        console.error(JSON.stringify(result));
        process.exit(1);
      }
    } catch (err) {
      console.error(JSON.stringify({
        success: false,
        error: err.message,
        stack: process.env.NODE_ENV === 'development' ? err.stack : undefined
      }));
      process.exit(1);
    }
  });
}

// Most reliable cross-project ESM "is main?" check (2024–2026 style)
const isMain = () =>
  process.argv.length > 1 &&
  (import.meta.url.endsWith(process.argv[1]) ||
   import.meta.url.endsWith(process.argv[1] + '.js') ||   // sometimes seen after bundling/tsc
   import.meta.url === `file://${process.argv[1]}`);

if (isMain()) {
  runAsCli().catch(err => {
    console.error(JSON.stringify({ success: false, error: err.message }));
    process.exit(1);
  });
}