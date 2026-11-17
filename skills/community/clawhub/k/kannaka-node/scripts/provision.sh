#!/usr/bin/env bash
# provision.sh — turn a fresh Linux server into a Kannaka node. Runs ON the
# server (copy it there, or pipe it over ssh). Idempotent: every step checks
# before it changes, and re-running converges to the same state.
#
#   bash provision.sh preflight                     read-only report, exit 0/1
#   bash provision.sh install                       the binaries (no root)
#   bash provision.sh configure --agent-id NAME [--display-name "Name"] \
#        [--nats-url nats://host:4222] [--no-swarm]  writes config, keeps what exists
#   bash provision.sh credentials                   reads NATS_USER/NATS_PASSWORD from env, writes the env file 0600
#   bash provision.sh service [--role member|serve] [--no-dream]   systemd units (root)
#   bash provision.sh verify                        proves the node is alive
#   bash provision.sh report                        the hand-off summary
#   bash provision.sh all --agent-id NAME ...       preflight → install → configure → service → verify → report
#   bash provision.sh uninstall                     stop units, remove units; keeps ~/.kannaka
#
# Environment it honours:
#   KANNAKA_USER   the login user that owns the node (default: the invoking user, or SUDO_USER)
#   NATS_USER / NATS_PASSWORD   swarm credentials from the swarm operator (credentials step)
#   INSTALL_URL    default https://install.ninja-portal.com/kannaka
#   BRAIN          none | hosted | local  (default none); BRAIN_EMAIL for hosted
set -uo pipefail

INSTALL_URL="${INSTALL_URL:-https://install.ninja-portal.com/kannaka}"
NATS_DEFAULT="nats://swarm.ninja-portal.com:4222"
STEP="${1:-}"; shift || true

# ---------------------------------------------------------------- who/where
if [ -n "${KANNAKA_USER:-}" ]; then U="$KANNAKA_USER"
elif [ -n "${SUDO_USER:-}" ] && [ "$SUDO_USER" != "root" ]; then U="$SUDO_USER"
else U="$(id -un)"; fi
H="$(getent passwd "$U" | cut -d: -f6)"
[ -n "$H" ] || { echo "no home for user $U" >&2; exit 1; }
DATA="$H/.kannaka"
CFG="$DATA/config.toml"
NATS_ENV="$H/.kannaka-nats.env"
LOCAL_BIN="$H/.local/bin/kannaka"
SYS_BIN="/usr/local/bin/kannaka"
RUNNER="/usr/local/bin/kannaka-node-run"
UNIT_NODE="/etc/systemd/system/kannaka-node.service"
UNIT_SERVE="/etc/systemd/system/kannaka-serve.service"
UNIT_DREAM="/etc/systemd/system/kannaka-dream.service"
TIMER_DREAM="/etc/systemd/system/kannaka-dream.timer"

say()  { printf '%s\n' "$*"; }
ok()   { printf '  ok    %s\n' "$*"; }
warn() { printf '  WARN  %s\n' "$*"; }
fail() { printf '  FAIL  %s\n' "$*"; FAILED=1; }
have() { command -v "$1" >/dev/null 2>&1; }
as_user() { if [ "$(id -un)" = "$U" ]; then bash -c "$*"; else sudo -u "$U" -H bash -c "$*"; fi; }
# Is this exact file being executed by any process? fuser when present; else walk
# /proc/*/exe (Linux). Unknown platforms answer "not busy" and let the installer decide.
bin_busy() {
  if have fuser; then fuser "$1" >/dev/null 2>&1; return $?; fi
  target="$(readlink -f "$1" 2>/dev/null)" || return 1
  for p in /proc/[0-9]*/exe; do
    [ "$(readlink -f "$p" 2>/dev/null)" = "$target" ] && return 0
  done
  return 1
}

need_root() { if [ "$(id -u)" -ne 0 ]; then if sudo -n true 2>/dev/null; then SUDO="sudo"; else echo "this step needs root (passwordless sudo, or run as root)" >&2; exit 2; fi; else SUDO=""; fi; }

# A value for a TOML key in a table, if the file has it. Crude on purpose: the
# config is small and flat, and this keeps the script dependency-free.
toml_get() { # file table key
  awk -v t="[$2]" -v k="$3" '
    $0 ~ /^\[/ { in_t = ($0 == t) }
    in_t && $1 == k { sub(/^[^=]*=[ \t]*/, ""); gsub(/^"|"$/, ""); print; exit }' "$1" 2>/dev/null
}

# ---------------------------------------------------------------- preflight
preflight() {
  FAILED=0
  say "== preflight on $(hostname) for user $U ($H)"
  . /etc/os-release 2>/dev/null; say "  os    ${PRETTY_NAME:-unknown}"
  arch="$(uname -m)"
  case "$arch" in x86_64|aarch64) ok "arch $arch (a release binary exists)";; *) fail "arch $arch: no release binary; build from source";; esac
  mem_mb=$(awk '/MemTotal/{print int($2/1024)}' /proc/meminfo)
  if [ "$mem_mb" -ge 900 ]; then ok "memory ${mem_mb} MB"; else fail "memory ${mem_mb} MB (< 1 GB)"; fi
  disk_gb=$(df -BG --output=avail "$H" | tail -1 | tr -dc '0-9')
  if [ "$disk_gb" -ge 5 ]; then ok "disk ${disk_gb} GB free under $H"; else fail "disk ${disk_gb} GB free (< 5 GB; the store grows and a full disk strands saves)"; fi
  if have systemctl && [ -d /run/systemd/system ]; then ok "systemd present"; else warn "no systemd: the service step will print units instead of installing them"; fi
  if [ "$(id -u)" -eq 0 ]; then ok "running as root"; elif sudo -n true 2>/dev/null; then ok "passwordless sudo"; else warn "no passwordless sudo: install/configure work; service needs root"; fi
  if have getenforce; then se="$(getenforce 2>/dev/null)"; ok "SELinux $se (the binary is placed in /usr/local/bin for the unit; see references/traps.md)"; else ok "SELinux not present"; fi
  for tool in curl awk tar sha256sum; do have "$tool" && ok "$tool" || fail "$tool missing"; done
  if curl -fsSIL -m 15 -o /dev/null https://github.com; then ok "outbound https"; else fail "outbound https to github.com blocked"; fi
  nats_host="${NATS_DEFAULT#nats://}"; nats_host="${nats_host%%:*}"
  if have timeout && timeout 6 bash -c "exec 3<>/dev/tcp/$nats_host/4222" 2>/dev/null; then ok "outbound 4222 to $nats_host (the swarm bus)"; else warn "cannot reach $nats_host:4222 — a member node needs outbound 4222; standalone does not"; fi
  if [ -x "$LOCAL_BIN" ]; then ok "kannaka already installed: $("$LOCAL_BIN" --version 2>/dev/null | head -1)"; else say "  info  kannaka not installed yet"; fi
  [ -f "$CFG" ] && ok "config exists: $CFG (kept; only missing keys are added)" || say "  info  no config yet"
  [ -f "$NATS_ENV" ] && ok "swarm credentials file exists (kept)" || say "  info  no swarm credentials (anonymous membership; see SKILL.md)"
  systemctl is-active kannaka-node >/dev/null 2>&1 && ok "kannaka-node.service already active" || true
  if [ "$FAILED" = 1 ]; then say "== preflight FAILED"; return 1; fi
  say "== preflight ok"
}

# ---------------------------------------------------------------- install
install_bins() {
  say "== install"
  flags="--skip-statusline"
  case "${BRAIN:-none}" in
    hosted) [ -n "${BRAIN_EMAIL:-}" ] || { echo "BRAIN=hosted needs BRAIN_EMAIL" >&2; return 1; }; flags="$flags --brain hosted --email $BRAIN_EMAIL";;
    local)  flags="$flags --brain local";;
  esac
  # The installer downloads straight onto ~/.local/bin/{kannaka,kannaka-tui,kannaka-hdl}.
  # If one of those files is executing, Linux refuses the write (Text file busy) and the
  # installer removes the destination as if it were a partial download. On 2026-09-11
  # that deleted a user's kannaka, then their kannaka-tui, while the TUI was open
  # (kannaka-plugin #23). Test the FILES, not a process name: the node service runs
  # /usr/local/bin/kannaka, a different file, and must not block an update.
  busy=""
  for b in kannaka kannaka-tui kannaka-hdl; do
    f="$(dirname "$LOCAL_BIN")/$b"
    [ -f "$f" ] && bin_busy "$f" && busy="$busy $b"
  done
  if [ -n "$busy" ]; then
    warn "in use:$busy (under $(dirname "$LOCAL_BIN")). The installer would write onto a running binary and delete it on failure. Close the kannaka-tui / chat that holds it, then re-run install."
    return 1
  fi
  as_user "curl -fsSL '$INSTALL_URL' | sh -s -- $flags" || { echo "installer failed" >&2; return 1; }
  [ -x "$LOCAL_BIN" ] || { echo "installer finished but $LOCAL_BIN is missing" >&2; return 1; }
  ok "$("$LOCAL_BIN" --version 2>/dev/null | head -1) at $LOCAL_BIN"
}

# ---------------------------------------------------------------- configure
configure() {
  AGENT_ID=""; DISPLAY=""; NATS_URL="$NATS_DEFAULT"; SWARM=true
  while [ $# -gt 0 ]; do case "$1" in
    --agent-id) AGENT_ID="$2"; shift;; --display-name) DISPLAY="$2"; shift;;
    --nats-url) NATS_URL="$2"; shift;; --no-swarm) SWARM=false;;
    *) echo "configure: unknown flag $1" >&2; return 1;; esac; shift; done
  say "== configure"
  as_user "mkdir -p '$DATA' && chmod 700 '$DATA'"
  if [ -f "$CFG" ]; then
    have_id="$(toml_get "$CFG" agent id)"
    if [ -n "$have_id" ]; then ok "config has agent id '$have_id' (kept; pass a different --agent-id only by editing the file)"; AGENT_ID="$have_id"; fi
  fi
  [ -n "$AGENT_ID" ] || { echo "configure: --agent-id is required for a new node" >&2; return 1; }
  case "$AGENT_ID" in *[!A-Za-z0-9._-]*) echo "agent id must be [A-Za-z0-9._-]" >&2; return 1;; esac
  [ -n "$DISPLAY" ] || DISPLAY="$AGENT_ID"
  if [ ! -f "$CFG" ]; then
    as_user "cat > '$CFG'" <<EOF
# Kannaka node configuration — written by kannaka-node/provision.sh
[agent]
id = "$AGENT_ID"
display_name = "$DISPLAY"
kind = "agent"

[swarm]
enabled = $SWARM
nats_url = "$NATS_URL"
role = "worker"
EOF
    ok "wrote $CFG (agent '$AGENT_ID', swarm $SWARM → $NATS_URL)"
  else
    # Add only the tables that are missing; never rewrite what a person set.
    grep -q '^\[agent\]' "$CFG" || as_user "printf '\n[agent]\nid = \"%s\"\ndisplay_name = \"%s\"\nkind = \"agent\"\n' '$AGENT_ID' '$DISPLAY' >> '$CFG'"
    grep -q '^\[swarm\]' "$CFG" || as_user "printf '\n[swarm]\nenabled = %s\nnats_url = \"%s\"\nrole = \"worker\"\n' '$SWARM' '$NATS_URL' >> '$CFG'"
    ok "config kept; missing tables added if any"
  fi
  as_user "chmod 600 '$CFG'"
  echo "$AGENT_ID" > /tmp/.kannaka-node-agent-id.$$ 2>/dev/null || true
}

# ---------------------------------------------------------------- credentials
credentials() {
  say "== credentials"
  if [ -z "${NATS_USER:-}" ] || [ -z "${NATS_PASSWORD:-}" ]; then
    if [ -f "$NATS_ENV" ]; then ok "credentials file already present (kept)"; return 0; fi
    warn "NATS_USER/NATS_PASSWORD not in the environment; the node will join anonymously (it still joins, publishes phase and syncs; it cannot create the presence stream or serve recall)"; return 0
  fi
  case "$NATS_PASSWORD" in *"'"*) echo "a password containing a single quote cannot be stored safely by this script" >&2; return 1;; esac
  # Single-quoted on purpose: the file is sourced by a shell, and an unquoted
  # value containing $( ) would execute.
  as_user "umask 077 && printf \"NATS_USER='%s'\nNATS_PASSWORD='%s'\n\" '$NATS_USER' '$NATS_PASSWORD' > '$NATS_ENV' && chmod 600 '$NATS_ENV'"
  ok "wrote $NATS_ENV (0600, single-quoted; value not shown)"
}

# ---------------------------------------------------------------- service
service() {
  ROLE="member"; DREAM=true
  while [ $# -gt 0 ]; do case "$1" in
    --role) ROLE="$2"; shift;; --no-dream) DREAM=false;;
    *) echo "service: unknown flag $1" >&2; return 1;; esac; shift; done
  say "== service (role $ROLE)"
  [ -x "$LOCAL_BIN" ] || { echo "install first: $LOCAL_BIN missing" >&2; return 1; }
  AGENT_ID="$(toml_get "$CFG" agent id)"; [ -n "$AGENT_ID" ] || { echo "configure first: no agent id in $CFG" >&2; return 1; }
  DISPLAY="$(toml_get "$CFG" agent display_name)"; [ -n "$DISPLAY" ] || DISPLAY="$AGENT_ID"

  # The runner: join (announce), then listen with auto-sync, long-running.
  runner_body="$(cat <<EOF
#!/bin/bash
# kannaka-node-run — written by kannaka-node/provision.sh; safe to edit.
export KANNAKA_DATA_DIR="$DATA"
[ -f "$NATS_ENV" ] && { set -a; . "$NATS_ENV"; set +a; }
BIN="$SYS_BIN"
"\$BIN" swarm join --agent-id "$AGENT_ID" --display-name "$DISPLAY"
exec "\$BIN" swarm listen --auto-sync --agent-id "$AGENT_ID"
EOF
)"
  unit_node="$(cat <<EOF
# kannaka-node.service — written by kannaka-node/provision.sh
[Unit]
Description=Kannaka node ($AGENT_ID): swarm join + listen with auto-sync
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$U
WorkingDirectory=$H
Environment=KANNAKA_DATA_DIR=$DATA
EnvironmentFile=-$NATS_ENV
ExecStart=$RUNNER
Restart=always
RestartSec=15
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
)"
  unit_serve="$(cat <<EOF
# kannaka-serve.service — written by kannaka-node/provision.sh
[Unit]
Description=Kannaka remote recall ($AGENT_ID): swarm serve, read-only
After=network-online.target kannaka-node.service
Wants=network-online.target

[Service]
Type=simple
User=$U
WorkingDirectory=$H
Environment=KANNAKA_DATA_DIR=$DATA
Environment=KANNAKA_READONLY=1
EnvironmentFile=-$NATS_ENV
ExecStart=$SYS_BIN swarm serve --agent-id $AGENT_ID
Restart=always
RestartSec=15

[Install]
WantedBy=multi-user.target
EOF
)"
  unit_dream="$(cat <<EOF
# kannaka-dream.service — written by kannaka-node/provision.sh
# The nightly dream stops the node first: the store has one writer at a time.
[Unit]
Description=Kannaka nightly dream ($AGENT_ID)

[Service]
Type=oneshot
ExecStartPre=/bin/systemctl stop kannaka-node.service
ExecStart=/usr/bin/sudo -u $U -H env KANNAKA_DATA_DIR=$DATA $SYS_BIN dream --mode deep
ExecStopPost=/bin/systemctl start kannaka-node.service
TimeoutStartSec=2h
EOF
)"
  timer_dream="$(cat <<EOF
[Unit]
Description=Kannaka nightly dream, 03:17 local with jitter

[Timer]
OnCalendar=*-*-* 03:17:00
RandomizedDelaySec=30m
Persistent=true

[Install]
WantedBy=timers.target
EOF
)"
  if ! have systemctl || [ ! -d /run/systemd/system ]; then
    warn "no systemd here; these are the files to install on a systemd host:"
    printf '\n--- %s\n%s\n--- %s\n%s\n' "$RUNNER" "$runner_body" "$UNIT_NODE" "$unit_node"
    [ "$ROLE" = serve ] && printf -- '--- %s\n%s\n' "$UNIT_SERVE" "$unit_serve"
    return 0
  fi
  need_root
  # The unit runs a copy in /usr/local/bin: on SELinux hosts a binary under a
  # home directory runs confined and cannot read the user's data files.
  if ! cmp -s "$LOCAL_BIN" "$SYS_BIN" 2>/dev/null; then
    [ -f "$SYS_BIN" ] && $SUDO mv "$SYS_BIN" "$SYS_BIN.previous"   # never overwrite a running binary in place
    $SUDO install -m755 "$LOCAL_BIN" "$SYS_BIN"
    have restorecon && $SUDO restorecon "$SYS_BIN" 2>/dev/null || true
    ok "binary copied to $SYS_BIN"; sys_bin_changed=1
  else ok "$SYS_BIN is current"; sys_bin_changed=0; fi
  printf '%s\n' "$runner_body" | $SUDO tee "$RUNNER" >/dev/null && $SUDO chmod 755 "$RUNNER"
  printf '%s\n' "$unit_node" | $SUDO tee "$UNIT_NODE" >/dev/null
  if [ "$ROLE" = serve ]; then printf '%s\n' "$unit_serve" | $SUDO tee "$UNIT_SERVE" >/dev/null; fi
  if [ "$DREAM" = true ]; then printf '%s\n' "$unit_dream" | $SUDO tee "$UNIT_DREAM" >/dev/null; printf '%s\n' "$timer_dream" | $SUDO tee "$TIMER_DREAM" >/dev/null; fi
  $SUDO systemctl daemon-reload
  $SUDO systemctl enable --now kannaka-node.service >/dev/null 2>&1 || $SUDO systemctl restart kannaka-node.service
  # enable --now is a no-op on a unit that is already running; a new binary needs a restart.
  [ "$sys_bin_changed" = 1 ] && $SUDO systemctl restart kannaka-node.service
  [ "$ROLE" = serve ] && $SUDO systemctl enable --now kannaka-serve.service >/dev/null 2>&1
  [ "$DREAM" = true ] && $SUDO systemctl enable --now kannaka-dream.timer >/dev/null 2>&1
  sleep 3
  ok "kannaka-node: $(systemctl is-active kannaka-node)"
  [ "$ROLE" = serve ] && ok "kannaka-serve: $(systemctl is-active kannaka-serve)"
  [ "$DREAM" = true ] && ok "kannaka-dream.timer: $(systemctl is-active kannaka-dream.timer) (next: $(systemctl show -p NextElapseUSecRealtime --value kannaka-dream.timer 2>/dev/null))"
  return 0
}

# ---------------------------------------------------------------- verify
verify() {
  FAILED=0
  say "== verify"
  [ -x "$LOCAL_BIN" ] && ok "binary $("$LOCAL_BIN" --version 2>/dev/null | head -1)" || fail "no binary"
  AGENT_ID="$(toml_get "$CFG" agent id)"; [ -n "$AGENT_ID" ] && ok "agent id $AGENT_ID" || fail "no agent id in config"
  if have systemctl && [ -d /run/systemd/system ] && [ -f "$UNIT_NODE" ]; then
    if systemctl is-active kannaka-node >/dev/null 2>&1; then ok "kannaka-node active"; else fail "kannaka-node not active: $(systemctl is-active kannaka-node)"; fi
    # The journal is readable by root and the adm/systemd-journal groups only.
    if journalctl -u kannaka-node -n 1 >/dev/null 2>&1; then J="journalctl"; elif sudo -n true 2>/dev/null; then J="sudo -n journalctl"; else J=""; fi
    if [ -n "$J" ]; then
      inv="$(systemctl show -p InvocationID --value kannaka-node 2>/dev/null)"
      # This run's journal, not the last N lines: a node up for hours has its join line far back.
      if [ -n "$inv" ]; then log="$($J _SYSTEMD_INVOCATION_ID="$inv" --no-pager 2>/dev/null)"; else log="$($J -u kannaka-node -n 200 --no-pager 2>/dev/null)"; fi
      if printf '%s' "$log" | grep -q "Joined swarm as"; then ok "joined the swarm (journal)"; else warn "no 'Joined swarm' line in this run's journal yet (give it a minute, then: journalctl -u kannaka-node)"; fi
      printf '%s' "$log" | grep -qi "Authorization Violation" && fail "NATS rejected the credentials (Authorization Violation)"
      printf '%s' "$log" | grep -q "presence stream unavailable" && say "  info  anonymous membership: this identity cannot create the presence stream; when the stream already exists on the bus the node is still listed by other hosts (the 'will NOT appear' line is stale then)"
    else warn "cannot read the journal as $U (not in adm/systemd-journal, no sudo); skipping the join check"; fi
  fi
  # A round trip through the store, read-only for status so it never contends
  # with the running node for the single writer.
  st="$(as_user "KANNAKA_DATA_DIR='$DATA' KANNAKA_READONLY=1 '$LOCAL_BIN' status 2>/dev/null")"
  if [ -n "$st" ]; then
    mem="$(printf '%s' "$st" | tr -d ' \n' | grep -o '"active_memories":[0-9]*' | head -1 | tr -dc '0-9')"
    lvl="$(printf '%s' "$st" | tr -d ' \n' | grep -o '"consciousness_level":"[a-z_]*"' | head -1 | cut -d'"' -f4)"
    ok "status: ${mem:-?} memories, level ${lvl:-?} (a new node is dormant until it has memories)"
  else fail "kannaka status returned nothing"; fi
  if [ "$FAILED" = 1 ]; then say "== verify FAILED"; return 1; fi
  say "== verify ok"
}

# ---------------------------------------------------------------- report
report() {
  AGENT_ID="$(toml_get "$CFG" agent id)"
  cat <<EOF
== Kannaka node report — $(hostname), $(date -u +%FT%TZ)
node        $AGENT_ID  (user $U)
binary      $LOCAL_BIN  and  $SYS_BIN  ($("$LOCAL_BIN" --version 2>/dev/null | head -1))
data        $DATA  (store: $DATA/kannaka.hrm; config: $CFG)
credentials $([ -f "$NATS_ENV" ] && echo "$NATS_ENV (0600)" || echo "none — anonymous membership")
units       $([ -f "$UNIT_NODE" ] && echo "kannaka-node.service" ) $([ -f "$UNIT_SERVE" ] && echo "kannaka-serve.service") $([ -f "$TIMER_DREAM" ] && echo "kannaka-dream.timer")
state       $(systemctl is-active kannaka-node 2>/dev/null || echo "n/a")

check       systemctl status kannaka-node; journalctl -u kannaka-node -f
status      KANNAKA_READONLY=1 kannaka status
peers       kannaka swarm peers
update      bash provision.sh install && sudo bash provision.sh service   (manifest-pinned; swaps $SYS_BIN with a move-aside and restarts)
uninstall   bash provision.sh uninstall   (keeps $DATA)
EOF
}

# ---------------------------------------------------------------- uninstall
uninstall() {
  need_root
  say "== uninstall (keeping $DATA)"
  for u in kannaka-dream.timer kannaka-dream.service kannaka-serve.service kannaka-node.service; do
    $SUDO systemctl disable --now "$u" >/dev/null 2>&1 || true
  done
  $SUDO rm -f "$UNIT_NODE" "$UNIT_SERVE" "$UNIT_DREAM" "$TIMER_DREAM" "$RUNNER"
  $SUDO systemctl daemon-reload
  ok "units removed; binaries and $DATA left in place"
}

# ---------------------------------------------------------------- all
all() {
  # split flags between configure and service
  cfg=(); svc=()
  while [ $# -gt 0 ]; do case "$1" in
    --agent-id|--display-name|--nats-url) cfg+=("$1" "$2"); shift;; --no-swarm) cfg+=("$1");;
    --role) svc+=("$1" "$2"); shift;; --no-dream) svc+=("$1");;
    *) echo "all: unknown flag $1" >&2; return 1;; esac; shift; done
  preflight || return 1
  install_bins || return 1
  configure "${cfg[@]}" || return 1
  credentials || return 1
  service "${svc[@]}" || return 1
  verify || return 1
  report
}

case "$STEP" in
  preflight) preflight;;
  install) install_bins;;
  configure) configure "$@";;
  credentials) credentials;;
  service) service "$@";;
  verify) verify;;
  report) report;;
  uninstall) uninstall;;
  all) all "$@";;
  *) sed -n '2,20p' "$0"; exit 1;;
esac
