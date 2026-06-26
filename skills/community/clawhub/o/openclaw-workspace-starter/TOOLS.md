# Tools — Your Setup Notes

This file is your cheat sheet for things that are unique to YOUR setup. Your agent reads it to know about your specific devices, accounts, and preferences.

**You don't need to fill this in right away.** Add things as they come up. When your agent asks "what's the camera called?" or "how do you transfer files?" — add the answer here so it remembers next time.

---

## My Devices
[List devices your agent might interact with]

Example:
- Main computer: Windows 11 desktop
- Phone: iPhone, connected via WhatsApp

Your devices:
- [Device 1]
- [Device 2]

## File Transfer
[How do you move files between your computer and the agent's server?]

Example:
- I use WinSCP to download files from /data/.openclaw/media/outbound/

Your method:
- [How you transfer files]

## Preferred Voice
[If your agent can speak (TTS), what voice do you prefer?]
- [e.g., "Something warm and natural", "Deep and calm", "I don't use voice"]

## Accounts & Services
[Things your agent might need to know about — NOT passwords, just what exists]

Example:
- Email: Gmail (agent can check via hooks)
- Calendar: Google Calendar
- Social: Twitter @myhandle

Your accounts:
- [List what's relevant]

---

## Good Default: API Data Safety

When your agent uses external AI services on your behalf, it should:
- Opt out of data retention when possible
- Include "do not store or train on this data" in prompts to external AI
- Add no-data-retention headers where supported
- Check any new API's privacy policy before sending sensitive info

This is already built into the operating rules. Just leaving it here so you know it's happening.

---

**Add whatever helps.** Camera names, SSH hosts, smart home devices, shortcut preferences — if your agent needs to know it, put it here.
