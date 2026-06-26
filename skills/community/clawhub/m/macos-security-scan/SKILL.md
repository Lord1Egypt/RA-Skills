---
name: macos-security-scan
description: >
  Scans a macOS computer for signs of tampering, malware, keyloggers, and
  suspicious activity — especially useful after a device has been sent for
  repair or handled by a third party. Use this skill whenever the user asks
  to check their Mac for security threats, spyware, keyloggers, suspicious
  processes, unexpected network connections, unknown startup items, or
  recently installed software. Also trigger when the user says things like
  "is my Mac safe?", "check my computer after repair", "was my Mac tampered
  with?", or "scan for malware". Always use this skill for any post-repair
  security check on macOS, even if the user doesn't use the word "scan".
compatibility:
  os: macOS 12 (Monterey) or later
  tools: bash, python3 (built-in on macOS)
  permissions: Standard user account (some checks need sudo for full results)
---

# macOS Security Scan Skill

This skill runs a comprehensive, read-only security scan of a macOS machine
and produces a detailed report. It is safe to run — it only reads system
state and never modifies anything.

---

## Workflow

### Step 1 — Explain to the user what will happen

Tell the user:
- The scan is read-only and safe. Nothing will be changed or deleted.
- Some checks (marked with ⚠️) produce richer results when run with `sudo`,
  but all checks work without it.
- The scan takes about 30–60 seconds.
- A report file will be saved when done.

Ask: "Ready to run the scan? And do you want to run it with sudo for deeper
results, or without sudo to keep it simple?"

### Step 2 — Run the scan script

Once the user confirms, run:

```bash
python3 scripts/scan.py [--sudo] --out ~/Desktop/security_report.md
```

Pass `--sudo` only if the user agreed to it. The script handles all checks
and writes the report file.

### Step 3 — Summarise findings in chat

After the script finishes, read the report and give the user a plain-English
verdict in chat:

- ✅ **Looks clean** — No significant threats found. Briefly note what was
  checked.
- ⚠️ **Needs attention** — List the specific findings that look suspicious,
  explain what each one means in plain language, and recommend next steps.
- 🚨 **Serious concern** — If any high-confidence indicators are found
  (active keylogger, known malware process, suspicious kernel extension),
  say so clearly and recommend they contact Apple Support or a security
  professional before using the device for sensitive tasks.

Always remind the user: this scan is a good first check, but it is not a
replacement for dedicated antivirus software.

### Step 4 — Point the user to the report file

Tell them the report has been saved to `~/Desktop/security_report.md` and
they can open it in any text editor or share it with a professional.

---

## What the Scan Checks

| Category | What is checked |
|---|---|
| Keyloggers & input monitors | Processes with Accessibility / Input Monitoring permissions; IOHIDFamily kernel extensions |
| Suspicious background processes | Running processes cross-referenced against a known-bad list; processes with no bundle ID hiding in temp folders |
| Launch agents & daemons | Startup items in all LaunchAgent / LaunchDaemon directories, flagging unknown or recently added items |
| Network connections | Active connections, listening ports, and processes making outbound connections to non-Apple IPs |
| Recently installed software | Apps and packages installed in the last 14 days |
| Login items | Items set to launch at login via System Settings |
| Kernel extensions (kexts) | Third-party kexts loaded into the kernel |
| Browser extensions | Installed extensions for Safari, Chrome, and Firefox |
| Privacy permissions | Apps with Camera, Microphone, Screen Recording, Accessibility, Full Disk Access |
| System Integrity Protection | Whether SIP is enabled (disabled SIP is a red flag) |
| Gatekeeper | Whether Gatekeeper is enforcing app signing |
| FileVault | Whether disk encryption is active |

---

## Interpreting Results

Guide the user using these thresholds:

**Green (normal)**
- SIP enabled, Gatekeeper on, FileVault on
- No unknown kexts
- No processes in `/tmp`, `/var/folders`, or home-directory hidden folders
- Launch agents all belong to known software the user recognises
- No unusual Accessibility or Screen Recording permissions

**Yellow (worth investigating)**
- Apps with Screen Recording or Accessibility access the user doesn't recognise
- Launch agents with random-looking names or paths in unusual locations
- Software installed in the days around the repair that the user didn't install
- Open ports the user doesn't expect

**Red (act now)**
- SIP disabled
- Unknown kernel extensions
- Processes actively keylogging (IOHIDFamily hooks from unknown processes)
- Known malware process names (see `scripts/scan.py` bad-list)
- Outbound connections from hidden processes to non-standard IPs

---

## Notes for the Agent

- Never make the user feel panicked unnecessarily. Many yellow flags are
  legitimate (e.g. Logi Options has Accessibility access, Zoom has Screen
  Recording). Always say "check whether you recognise this" before calling
  something suspicious.
- If the user asks what a specific process or item is, look it up or explain
  it — don't just say "unknown".
- If the user wants to remove something, do NOT do so automatically. Guide
  them to System Settings or explain the manual removal steps. The scan is
  read-only; remediation is a separate, deliberate action.
