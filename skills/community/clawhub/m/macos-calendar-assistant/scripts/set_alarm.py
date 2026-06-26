#!/usr/bin/env python3
import argparse
import subprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uid", required=True)
    ap.add_argument("--alarm-minutes", type=int, required=True)
    args = ap.parse_args()

    uid = args.uid.replace('"', '\\"')
    minutes_before = int(args.alarm_minutes)

    APPLESCRIPT = f'''
set eventUid to "{uid}"
set minutesBefore to {minutes_before}

tell application "Calendar"
  set foundEvent to missing value
  set foundCal to missing value

  repeat with c in calendars
    try
      set matches to (every event of c whose uid is eventUid)
      if (count of matches) > 0 then
        set foundEvent to item 1 of matches
        set foundCal to c
        exit repeat
      end if
    end try
  end repeat

  if foundEvent is missing value then error "Event not found: " & eventUid

  try
    repeat with a in (every display alarm of foundEvent)
      delete a
    end repeat
  end try

  make new display alarm at end of display alarms of foundEvent with properties {{trigger interval:(-minutesBefore * minutes)}}
  return "OK alarm set: " & minutesBefore & " min before (calendar=" & (name of foundCal) & ")"
end tell
'''

    p = subprocess.run(["osascript"], input=APPLESCRIPT, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr.strip() or p.stdout.strip() or f"osascript failed: {p.returncode}")
    print(p.stdout.strip())


if __name__ == "__main__":
    main()
