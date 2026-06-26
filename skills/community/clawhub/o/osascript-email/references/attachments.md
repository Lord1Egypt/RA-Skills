# Sending Attachments via osascript-email

Attaching files requires adding an `attach` command inside the `tell m` block.

## AppleScript pattern

```applescript
tell application "Mail"
  set m to make new outgoing message with properties {subject:"Report", content:"See attached.", visible:false}
  tell m
    make new to recipient with properties {address:"recipient@example.com"}
    make new attachment with properties {file name:(POSIX file "/path/to/file.pdf") as alias}
  end tell
  send m
end tell
```

**Important:** The file path must be an absolute POSIX path. Use `as alias` to convert it.

## Python helper with attachment

```python
import subprocess

def send_email_with_attachment(subject, body, to, attachment_path):
    body_esc = body.replace('\\', '\\\\').replace('"', '\\"')
    subj_esc = subject.replace('"', '\\"')
    script = f'''tell application "Mail"
  set m to make new outgoing message with properties {{subject:"{subj_esc}", content:"{body_esc}", visible:false}}
  tell m
    make new to recipient with properties {{address:"{to}"}}
    make new attachment with properties {{file name:(POSIX file "{attachment_path}") as alias}}
  end tell
  send m
end tell
return "sent"'''
    r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Failed: {r.stderr}")
    print(f"✅ Sent with attachment: {attachment_path}")
```

## Limitations
- File must exist at send time
- Large files (>25MB) may be blocked by the receiving mail server
- Multiple attachments: add multiple `make new attachment` lines
