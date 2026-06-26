#!/usr/bin/env python3
import argparse
import subprocess
import datetime as dt


def parse_iso(s: str) -> dt.datetime:
    # Python 3.11+ supports fromisoformat with timezone offset
    try:
        d = dt.datetime.fromisoformat(s)
    except Exception as e:
        raise SystemExit(f"Invalid --start/--end ISO datetime: {s} ({e})")
    if d.tzinfo is None:
        raise SystemExit(f"Timezone required in ISO string: {s}")
    return d


def to_applescript_date(d: dt.datetime) -> str:
    # Convert to local time components (Calendar expects local 'date' object)
    local = d.astimezone()
    return (
        f"set _d to (current date)\n"
        f"set year of _d to {local.year}\n"
        f"set month of _d to {local.month}\n"
        f"set day of _d to {local.day}\n"
        f"set hours of _d to {local.hour}\n"
        f"set minutes of _d to {local.minute}\n"
        f"set seconds of _d to {local.second}\n"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--calendar", default="")
    ap.add_argument("--notes", default="")
    ap.add_argument("--location", default="")
    ap.add_argument("--alarm-minutes", type=int, default=None)
    args = ap.parse_args()

    start = parse_iso(args.start)
    end = parse_iso(args.end)
    if end <= start:
        raise SystemExit("--end must be after --start")

    # Escape quotes for AppleScript string literals
    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    cal_name = esc(args.calendar)
    title = esc(args.title)
    notes = esc(args.notes)
    location = esc(args.location)

    alarm_block = ""
    if args.alarm_minutes is not None:
        alarm_block = (
            "\n"
            "  -- Remove existing display alarms to avoid duplicates\n"
            "  try\n"
            "    repeat with a in (every display alarm of newEvent)\n"
            "      delete a\n"
            "    end repeat\n"
            "  end try\n"
            f"  make new display alarm at end of display alarms of newEvent with properties {{trigger interval:(-{int(args.alarm_minutes)} * minutes)}}\n"
        )

    start_as = to_applescript_date(start) + "set startDate to _d\n"
    end_as = to_applescript_date(end) + "set endDate to _d\n"

    APPLESCRIPT = f'''
set eventTitle to "{title}"
set eventNotes to "{notes}"
set eventLocation to "{location}"
set desiredCalendarName to "{cal_name}"

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

  set newEvent to make new event at end of events of targetCal with properties {{summary:eventTitle, start date:startDate, end date:endDate, description:eventNotes, location:eventLocation}}
{alarm_block}
  set calName to name of targetCal
  set eventId to uid of newEvent
end tell

return "OK calendar=" & calName & " uid=" & eventId
'''

    p = subprocess.run(["osascript"], input=APPLESCRIPT, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr.strip() or p.stdout.strip() or f"osascript failed: {p.returncode}")

    print(p.stdout.strip())


if __name__ == "__main__":
    main()
