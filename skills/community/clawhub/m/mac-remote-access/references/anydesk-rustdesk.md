# AnyDesk / RustDesk notes

Use a third-party GUI remote tool as a fallback so VNC is not the only graphical path.

## AnyDesk on macOS

Recommended setup:

1. Install AnyDesk.
2. Enable unattended access.
3. Set a dedicated unattended-access password.
4. Grant macOS permissions:
   - Accessibility
   - Screen Recording
5. Enable launch at login / startup.

Typical symptoms:

- Can see the desktop but cannot control it → Accessibility is missing.
- Black screen or blank screen → Screen Recording is missing.
- Works once but fails after reboot → launch-at-startup or background permissions are incomplete.

## RustDesk on macOS

Recommended setup is similar:

1. Install RustDesk.
2. Configure permanent password or trusted-device flow.
3. Grant macOS permissions:
   - Accessibility
   - Screen Recording
4. Enable background/startup behavior if supported.

## Positioning

Prefer a layered access model:

1. SSH for break-glass recovery.
2. AnyDesk or RustDesk for primary GUI fallback.
3. VNC / Screen Sharing as secondary GUI path.
