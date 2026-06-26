#!/usr/bin/env bash
# Headless RDP-server health probe for gnome-remote-desktop Remote Login.
# A native agent can't SEE a GUI RDP session, so this verifies the SERVER side
# instead: config sane, listener bound, and (optionally) that an inbound connect
# is being processed by NTLM/credssp (proves creds+cert are wired, regardless of
# whether your particular RDP *client* completes the handshake).
#
# Run ON the box (or wrap in ssh). Needs sudo for grdctl --system + journal.
#
# Usage:
#   check-rdp-server.sh                 # static checks only
#   check-rdp-server.sh --watch 12      # also tail grd logs for N seconds while
#                                       # you trigger a connect from a client
set -u
echo "== gnome-remote-desktop system service =="
systemctl is-active gnome-remote-desktop.service 2>&1
systemctl is-enabled gnome-remote-desktop.service 2>&1

echo "== grdctl --system status =="
sudo grdctl --system status 2>&1 | grep -viE 'TPM'   # TPM-fallback line is harmless noise

echo "== listener on 3389 =="
sudo ss -tlnp 2>/dev/null | grep ':3389' || echo "NO LISTENER on 3389 (service not bound)"

echo "== UFW rule (should be LAN-scoped, never any-source) =="
sudo ufw status 2>/dev/null | grep 3389 || echo "(no explicit 3389 ufw rule)"

if [ "${1:-}" = "--watch" ]; then
  SECS="${2:-12}"
  echo "== watching grd logs for ${SECS}s — trigger an RDP connect now =="
  echo "   interpret: 'NTLM'/'credssp'/'AcceptSecurityContext' lines = creds ARE being"
  echo "   processed (server good). 'Couldn't retrieve RDP username' = creds NOT set."
  echo "   'MIC verification failed'/'SEC_E_MESSAGE_ALTERED' = client-side FreeRDP-CLI"
  echo "   interop bug (FreeRDP #7722), NOT a server problem — use MS Remote Desktop/Remmina."
  sudo timeout "$SECS" journalctl -u gnome-remote-desktop.service -f -n 0 2>&1 \
    | grep -iE 'ntlm|credssp|AcceptSecurityContext|username|session|MIC|MESSAGE_ALTERED|connect|reject|accept'
fi
