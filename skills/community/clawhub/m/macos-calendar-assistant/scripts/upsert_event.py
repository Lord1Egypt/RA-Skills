#!/usr/bin/env python3
import argparse
import datetime as dt
import subprocess
import sys


def parse_iso(s: str) -> dt.datetime:
    try:
        d = dt.datetime.fromisoformat(s)
    except Exception as e:
        raise SystemExit(f"Invalid ISO datetime: {s} ({e})")
    if d.tzinfo is None:
        raise SystemExit(f"Timezone required: {s}")
    return d


def to_applescript_date(var_name: str, d: dt.datetime) -> str:
    local = d.astimezone()
    return (
        f"set {var_name} to (current date)\n"
        f"set year of {var_name} to {local.year}\n"
        f"set month of {var_name} to {local.month}\n"
        f"set day of {var_name} to {local.day}\n"
        f"set hours of {var_name} to {local.hour}\n"
        f"set minutes of {var_name} to {local.minute}\n"
        f"set seconds of {var_name} to {local.second}\n"
    )


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def run_osascript(script: str) -> str:
    p = subprocess.run(["osascript"], input=script, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr.strip() or p.stdout.strip() or f"osascript failed: {p.returncode}")
    return (p.stdout or "").strip()


def main():
    ap = argparse.ArgumentParser(description="Idempotent calendar upsert (create/update/skip).")
    ap.add_argument("--title", required=True)
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--calendar", default="")
    ap.add_argument("--notes", default="")
    ap.add_argument("--location", default="")
    ap.add_argument("--alarm-minutes", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    start = parse_iso(args.start)
    end = parse_iso(args.end)
    if end <= start:
        raise SystemExit("--end must be after --start")

    cal_name = esc(args.calendar)
    title = esc(args.title.strip())
    notes = esc(args.notes)
    location = esc(args.location)

    alarm_block_create = ""
    alarm_block_update = ""
    if args.alarm_minutes is not None:
        mins = int(args.alarm_minutes)
        alarm_block_create = (
            "\n"
            "  try\n"
            "    repeat with a in (every display alarm of newEvent)\n"
            "      delete a\n"
            "    end repeat\n"
            "  end try\n"
            f"  make new display alarm at end of display alarms of newEvent with properties {{trigger interval:(-{mins} * minutes)}}\n"
        )
        alarm_block_update = (
            "\n"
            "      try\n"
            "        repeat with a in (every display alarm of foundEvent)\n"
            "          delete a\n"
            "        end repeat\n"
            "      end try\n"
            f"      make new display alarm at end of display alarms of foundEvent with properties {{trigger interval:(-{mins} * minutes)}}\n"
        )

    start_as = to_applescript_date("startDate", start)
    end_as = to_applescript_date("endDate", end)

    dry = "true" if args.dry_run else "false"

    script = f'''
set eventTitle to "{title}"
set eventNotes to "{notes}"
set eventLocation to "{location}"
set desiredCalendarName to "{cal_name}"
set isDryRun to {dry}

{start_as}
{end_as}

tell application "Calendar"
  set targetCal to missing value

  if desiredCalendarName is not "" then
    repeat with c in calendars
      try
        if (name of c is desiredCalendarName) and (writable of c is true) then
          set targetCal to c
          exit repeat
        end if
      end try
    end repeat
  end if

  if targetCal is missing value then
    repeat with c in calendars
      try
        if writable of c is true then
          set targetCal to c
          exit repeat
        end if
      end try
    end repeat
  end if

  if targetCal is missing value then set targetCal to calendar 1

  -- Idempotency key: same calendar + same startDate + same summary
  set foundEvent to missing value
  set candidates to (every event of targetCal whose start date = startDate)
  repeat with e in candidates
    try
      if (summary of e) is eventTitle then
        set foundEvent to e
        exit repeat
      end if
    end try
  end repeat

  set calName to name of targetCal

  if foundEvent is missing value then
    if isDryRun then
      return "DRYRUN action=create calendar=" & calName
    end if

    set newEvent to make new event at end of events of targetCal with properties {{summary:eventTitle, start date:startDate, end date:endDate, description:eventNotes, location:eventLocation}}
{alarm_block_create}
    return "CREATED calendar=" & calName & " uid=" & (uid of newEvent)
  else
    set needUpdate to false

    try
      if (end date of foundEvent) is not endDate then set needUpdate to true
    end try
    try
      if (description of foundEvent) is not eventNotes then set needUpdate to true
    end try
    try
      if (location of foundEvent) is not eventLocation then set needUpdate to true
    end try

    if needUpdate is false then
      return "SKIPPED calendar=" & calName & " uid=" & (uid of foundEvent)
    end if

    if isDryRun then
      return "DRYRUN action=update calendar=" & calName & " uid=" & (uid of foundEvent)
    end if

    set end date of foundEvent to endDate
    set description of foundEvent to eventNotes
    set location of foundEvent to eventLocation
{alarm_block_update}
    return "UPDATED calendar=" & calName & " uid=" & (uid of foundEvent)
  end if
end tell
'''

    out = run_osascript(script)
    print(out)


if __name__ == "__main__":
    main()
