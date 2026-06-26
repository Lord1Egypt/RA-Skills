# SOP

1. Check Mac local status: Tailscale, SSH, 5900 listener, local self-test.
2. From Windows, run `Test-NetConnection` for 22 and 5900.
3. If both fail, inspect Tailscale ACL/policy before tuning RealVNC.
4. If 22 works but 5900 fails, restart Screen Sharing and recheck.
5. If both work, continue to VNC/AnyDesk auth and permission troubleshooting.
6. Preserve SSH as break-glass access and AnyDesk as GUI fallback.
