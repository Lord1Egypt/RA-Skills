#!/usr/bin/env python3
import argparse, json, os, subprocess


def run_osascript(script, env=None):
    result = subprocess.run(['osascript', '-'], input=script, text=True, capture_output=True, env=env)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def cmd_count(_args):
    script = r'''
with timeout of 20 seconds
  tell application "Contacts"
    return count of people
  end tell
end timeout
'''
    print(json.dumps({"ok": True, "people_count": int(run_osascript(script))}, ensure_ascii=False, indent=2))


def cmd_exists(args):
    env = os.environ.copy()
    env.update({
        'FN': args.first_name or '',
        'LN': args.last_name or '',
        'PHONE': args.phone or '',
        'EMAIL': args.email or '',
    })
    script = r'''
on run
  set fn to system attribute "FN"
  set ln to system attribute "LN"
  set phoneVal to system attribute "PHONE"
  set emailVal to system attribute "EMAIL"
  tell application "Contacts"
    set matches to {}
    repeat with p in people
      set hit to false
      if fn is not "" then
        if first name of p is fn then set hit to true
      end if
      if ln is not "" then
        if last name of p is ln then set hit to true
      end if
      if phoneVal is not "" then
        try
          if (value of every phone of p) contains phoneVal then set hit to true
        end try
      end if
      if emailVal is not "" then
        try
          if (value of every email of p) contains emailVal then set hit to true
        end try
      end if
      if hit then
        set nm to name of p
        try
          set phs to value of every phone of p
        on error
          set phs to {}
        end try
        try
          set ems to value of every email of p
        on error
          set ems to {}
        end try
        set end of matches to {nm, phs, ems}
      end if
    end repeat
    return matches
  end tell
end run
'''
    out = run_osascript(script, env=env)
    print(json.dumps({'ok': True, 'raw': out}, ensure_ascii=False, indent=2))


def cmd_create(args):
    env = os.environ.copy()
    env.update({
        'FN': args.first_name or '',
        'LN': args.last_name or '',
        'PHONE': args.phone or '',
        'EMAIL': args.email or '',
        'ORG': args.organization or '',
        'TITLE': args.job_title or '',
    })
    # duplicate detection must happen on Contacts API side, not SQLite side
    precheck = r'''
on run
  set fn to system attribute "FN"
  set ln to system attribute "LN"
  set phoneVal to system attribute "PHONE"
  set emailVal to system attribute "EMAIL"
  tell application "Contacts"
    repeat with p in people
      set hit to false
      if fn is not "" and first name of p is fn then set hit to true
      if ln is not "" and last name of p is ln then set hit to true
      if phoneVal is not "" then
        try
          if (value of every phone of p) contains phoneVal then set hit to true
        end try
      end if
      if emailVal is not "" then
        try
          if (value of every email of p) contains emailVal then set hit to true
        end try
      end if
      if hit then
        set nm to name of p
        try
          set phs to value of every phone of p
        on error
          set phs to {}
        end try
        try
          set ems to value of every email of p
        on error
          set ems to {}
        end try
        return "DUPLICATE" & linefeed & nm & linefeed & (phs as string) & linefeed & (ems as string)
      end if
    end repeat
    return "OK"
  end tell
end run
'''
    pre = run_osascript(precheck, env=env).splitlines()
    if pre and pre[0] == 'DUPLICATE':
        print(json.dumps({
            'ok': False,
            'created': False,
            'reason': 'duplicate_detected',
            'match': {
                'name': pre[1] if len(pre) > 1 else '',
                'phones': [x.strip() for x in (pre[2].split(',') if len(pre) > 2 and pre[2] else []) if x.strip()],
                'emails': [x.strip() for x in (pre[3].split(',') if len(pre) > 3 and pre[3] else []) if x.strip()],
            }
        }, ensure_ascii=False, indent=2))
        return

    script = r'''
on run
  set fn to system attribute "FN"
  set ln to system attribute "LN"
  set phoneVal to system attribute "PHONE"
  set emailVal to system attribute "EMAIL"
  set orgVal to system attribute "ORG"
  set titleVal to system attribute "TITLE"
  tell application "Contacts"
    set newPerson to make new person with properties {first name:fn, last name:ln}
    tell newPerson
      if orgVal is not "" then set organization to orgVal
      if titleVal is not "" then set job title to titleVal
      if phoneVal is not "" then make new phone with properties {label:"mobile", value:phoneVal}
      if emailVal is not "" then make new email with properties {label:"work", value:emailVal}
    end tell
    save
    set outName to name of newPerson
    set outPhones to value of every phone of newPerson
    set outEmails to value of every email of newPerson
    return outName & linefeed & (outPhones as string) & linefeed & (outEmails as string)
  end tell
end run
'''
    out = run_osascript(script, env=env).splitlines()
    print(json.dumps({
        'ok': True,
        'created': True,
        'name': out[0] if len(out) > 0 else '',
        'phones': [x.strip() for x in (out[1].split(',') if len(out) > 1 and out[1] else []) if x.strip()],
        'emails': [x.strip() for x in (out[2].split(',') if len(out) > 2 and out[2] else []) if x.strip()],
    }, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)

    p = sp.add_parser('count')
    p.set_defaults(func=cmd_count)

    p = sp.add_parser('exists')
    p.add_argument('--first-name')
    p.add_argument('--last-name')
    p.add_argument('--phone')
    p.add_argument('--email')
    p.set_defaults(func=cmd_exists)

    p = sp.add_parser('create')
    p.add_argument('--first-name', required=True)
    p.add_argument('--last-name', default='')
    p.add_argument('--phone')
    p.add_argument('--email')
    p.add_argument('--organization')
    p.add_argument('--job-title')
    p.set_defaults(func=cmd_create)

    args = ap.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
