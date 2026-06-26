---
name: mac-remote-access
description: Diagnose, configure, and recover remote access to a macOS machine over Tailscale. Use when setting up or troubleshooting Mac SSH, Screen Sharing/VNC, RealVNC, AnyDesk, RustDesk, Tailscale ACLs, or remote-access baselines, especially for Windows-to-Mac access, unreachable port 22/5900 issues, visible-in-tailnet-but-not-connectable cases, or break-glass remote recovery planning.
---

# Mac Remote Access

Set up or troubleshoot remote access to a Mac over Tailscale.

## Workflow

1. Check the Mac side first.
2. Verify TCP reachability from the remote client.
3. Check Tailscale ACLs before tuning VNC clients.
4. Preserve at least one command-line recovery path (SSH).
5. Recommend a layered setup: SSH fallback, AnyDesk primary GUI fallback, VNC secondary.

## Mac-side checks

Run these first when local access to the Mac exists:

```bash
tailscale status
tailscale ip -4
sudo systemsetup -getremotelogin
sudo /usr/sbin/netstat -anv -p tcp | grep '\.5900 .*LISTEN'
nc -vz <Mac-IP> 5900
```

If Screen Sharing looks stuck, restart it:

```bash
sudo launchctl kickstart -k system/com.apple.screensharing
```

## Windows-side checks

Use PowerShell and prefer TCP tests over ping:

```powershell
Test-NetConnection <Mac-IP> -Port 22
Test-NetConnection <Mac-IP> -Port 5900
```

Interpretation:

- 22=False and 5900=False → check Tailscale ACL / policy first
- 22=True and 5900=False → check Mac Screen Sharing / VNC service
- 22=True and 5900=True → move to client auth/compatibility

## ACL guidance

Prefer explicit ACLs during troubleshooting.

Read `references/acl-template.md` for a minimal working example.

## References

- `references/acl-template.md` — minimal ACL template
- `references/checklist.md` — baseline checklist
- `references/sop.md` — end-to-end operating procedure
- `references/anydesk-rustdesk.md` — GUI fallback setup and troubleshooting notes
