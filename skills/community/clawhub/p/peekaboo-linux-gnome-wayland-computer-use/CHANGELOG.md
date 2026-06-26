# Changelog

## 1.0.2
- Correct the "local VPN swallows RDP" entry: it's stateful/intermittent (NordVPN AND Tailscale on the box), not a deterministic Threat-Protection NEFilter rule. Reliable recovery is bouncing the VPN helper(s), not a single toggle.

## 1.0.1
- RDP diagnosis: document the "local VPN / endpoint-security content filter swallows RDP" root cause (NordVPN Threat Protection, Cloudflare WARP, etc.) — zero packets reach the server from one client while other clients/hosts work. Common "works from machine A not B" cause.

## 1.0.0
- Initial public release.
- Screenshot on GNOME 49+/Wayland via the `allow-gnome-screenshot` extension (scoped, no global unsafe_mode).
- Per-display and per-window capture via Mutter DisplayConfig + the Window Calls extension (`screenshot-display`).
- Input injection via `ydotool`/`/dev/uinput` (rootless persistent user service).
- Click-by-element (SOM) via hybrid coordinates — AT-SPI WINDOW-relative extents + Window Calls window origin (`locate-element`), with a vision fallback for elements that zero even WINDOW extents.
- Window actions (focus/move/resize/maximize/close) via Window Calls.
- Optional GNOME Remote Desktop (Remote Login) setup + an authoritative server-side RDP auth-failure diagnosis guide.
