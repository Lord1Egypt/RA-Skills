"""
send_email.py — Send email via macOS Mail.app using osascript.
No SMTP credentials required. Mail.app must be configured with the sender account.
"""

import subprocess


def send_email(subject: str, body: str, to: str, cc: str = None, sender: str = None) -> None:
    """
    Send an email via Mail.app on macOS.

    Args:
        subject: Email subject line
        body: Plain text email body
        to: Primary recipient address
        cc: Optional CC address
        sender: Optional sender address (must match a Mail.app account)

    Raises:
        RuntimeError: If osascript returns a non-zero exit code
    """
    # Escape for AppleScript string literals
    body_esc = body.replace("\\", "\\\\").replace('"', '\\"')
    subj_esc = subject.replace('"', '\\"')

    # Build sender property if provided
    sender_prop = f', sender:"{sender}"' if sender else ""

    # Build CC block
    cc_block = ""
    if cc:
        cc_esc = cc.replace('"', '\\"')
        cc_block = f'\n    make new to recipient with properties {{address:"{cc_esc}"}}'

    script = f'''tell application "Mail"
  set m to make new outgoing message with properties {{subject:"{subj_esc}", content:"{body_esc}", visible:false{sender_prop}}}
  tell m
    make new to recipient with properties {{address:"{to}"}}{cc_block}
  end tell
  send m
end tell
return "sent"'''

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"osascript-email failed (exit {result.returncode}): {result.stderr.strip()}"
        )

    print(f"✅ Email sent: {subject}")


if __name__ == "__main__":
    # Quick test — update addresses before running
    send_email(
        subject="Test from osascript-email skill",
        body="This is a test email sent via Mail.app + osascript.",
        to="your@example.com",
        cc="backup@example.com",
    )
