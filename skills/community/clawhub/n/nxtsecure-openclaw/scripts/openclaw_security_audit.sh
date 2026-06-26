#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

CONFIG_FILE="${OPENCLAW_AUDIT_CONFIG:-}"
if [[ -z "${CONFIG_FILE}" ]]; then
  for candidate in \
    "/etc/openclaw-security-audit.conf" \
    "${SKILL_DIR}/references/openclaw-security-audit.conf" \
    "${SKILL_DIR}/references/openclaw-security-audit.conf.example"
  do
    if [[ -f "${candidate}" ]]; then
      CONFIG_FILE="${candidate}"
      break
    fi
  done
fi

EXPECTED_TCP_PORTS="80 443 2222"
EXPECTED_UDP_PORTS=""
SSH_EXPECTED_PORT="2222"
SSH_PORT_IN_USE=1
SSH_REQUIRE_KEYS_ONLY=1
ENABLE_SSH_PORT_REMEDIATION=0
VIRUSTOTAL_ENABLED=0
VIRUSTOTAL_ALLOW_UPLOADS=0
VIRUSTOTAL_URLS=""
VIRUSTOTAL_FILES=""
ALLOWED_DOCKER_CONTAINERS=""
DISK_THRESHOLD_PERCENT=80
MAX_FAILED_LOGIN_ATTEMPTS=25
AUTO_SECURITY_UPDATES_REQUIRED=1
AUTO_REMEDIATE=1
REMEDIATE_UNEXPECTED_PORTS=0
ALLOW_DOCKER_PRUNE=0

if [[ -n "${CONFIG_FILE}" && -f "${CONFIG_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${CONFIG_FILE}"
fi

declare -a ISSUES=()
declare -a ACTIONS=()
declare -a WARNINGS=()

log() {
  printf '[INFO] %s\n' "$*"
}

warn() {
  WARNINGS+=("$*")
  printf '[WARN] %s\n' "$*"
}

issue() {
  ISSUES+=("$*")
  printf '[FAIL] %s\n' "$*"
}

action() {
  ACTIONS+=("$*")
  printf '[FIX] %s\n' "$*"
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

is_root() {
  [[ "${EUID}" -eq 0 ]]
}

run_privileged() {
  if is_root; then
    "$@"
  elif command_exists sudo && sudo -n true >/dev/null 2>&1; then
    sudo "$@"
  else
    return 126
  fi
}

contains_word() {
  local needle="$1"
  local haystack="$2"
  local item
  for item in ${haystack}; do
    if [[ "${item}" == "${needle}" ]]; then
      return 0
    fi
  done
  return 1
}

if [[ "${SSH_PORT_IN_USE}" -eq 1 ]] && ! contains_word "${SSH_EXPECTED_PORT}" "${EXPECTED_TCP_PORTS}"; then
  EXPECTED_TCP_PORTS="${EXPECTED_TCP_PORTS} ${SSH_EXPECTED_PORT}"
fi

service_is_active() {
  local service="$1"
  command_exists systemctl && systemctl is-active --quiet "${service}"
}

safe_systemctl_enable_now() {
  local service="$1"
  if run_privileged systemctl enable --now "${service}" >/dev/null 2>&1; then
    action "Enabled ${service}."
    return 0
  fi
  return 1
}

detect_firewall_backend() {
  if command_exists ufw; then
    echo "ufw"
    return 0
  fi
  if command_exists firewall-cmd; then
    echo "firewalld"
    return 0
  fi
  if command_exists nft; then
    echo "nftables"
    return 0
  fi
  echo "none"
}

check_firewall() {
  local backend
  backend="$(detect_firewall_backend)"

  case "${backend}" in
    ufw)
      if ufw status 2>/dev/null | grep -q "^Status: active"; then
        log "Firewall active via ufw."
      elif [[ "${AUTO_REMEDIATE}" -eq 1 ]] && run_privileged ufw --force enable >/dev/null 2>&1; then
        action "Enabled ufw."
      else
        issue "ufw is installed but not active."
      fi
      ;;
    firewalld)
      if service_is_active firewalld; then
        log "Firewall active via firewalld."
      elif [[ "${AUTO_REMEDIATE}" -eq 1 ]] && safe_systemctl_enable_now firewalld; then
        :
      else
        issue "firewalld is installed but not active."
      fi
      ;;
    nftables)
      if nft list ruleset 2>/dev/null | grep -q "table"; then
        log "Firewall appears active via nftables."
      else
        issue "nftables is present but no active ruleset was found."
      fi
      ;;
    *)
      issue "No supported firewall manager was found."
      ;;
  esac
}

fail2ban_banned_total() {
  local total=0
  local jail
  local jails

  if ! command_exists fail2ban-client; then
    echo "0"
    return 0
  fi

  jails="$(fail2ban-client status 2>/dev/null | sed -n 's/.*Jail list:[[:space:]]*//p' | tr ',' ' ')"
  if [[ -z "${jails}" ]]; then
    echo "0"
    return 0
  fi

  for jail in ${jails}; do
    local count
    count="$(fail2ban-client status "${jail}" 2>/dev/null | sed -n 's/.*Total banned:[[:space:]]*//p' | tail -n1)"
    if [[ "${count}" =~ ^[0-9]+$ ]]; then
      total=$((total + count))
    fi
  done

  echo "${total}"
}

check_fail2ban() {
  if ! command_exists fail2ban-client && ! service_is_active fail2ban; then
    issue "fail2ban is not installed or not available."
    return 0
  fi

  if service_is_active fail2ban; then
    log "fail2ban is active. Total banned IPs: $(fail2ban_banned_total)."
  elif [[ "${AUTO_REMEDIATE}" -eq 1 ]] && safe_systemctl_enable_now fail2ban; then
    log "fail2ban is active. Total banned IPs: $(fail2ban_banned_total)."
  else
    issue "fail2ban is installed but inactive."
  fi
}

ssh_effective_value() {
  local key="$1"
  if command_exists sshd; then
    sshd -T 2>/dev/null | awk -v target="${key}" '$1 == target { print $2; exit }'
    return 0
  fi
  awk -v target="${key}" '
    BEGIN { IGNORECASE=1 }
    $1 == target { value = $2 }
    END { if (value != "") print tolower(value) }
  ' /etc/ssh/sshd_config 2>/dev/null
}

remediate_ssh_password_auth() {
  local drop_in="/etc/ssh/sshd_config.d/99-openclaw-hardening.conf"
  local tmp_file

  tmp_file="$(mktemp)"
  cat >"${tmp_file}" <<'EOF'
PasswordAuthentication no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
EOF

  if run_privileged mkdir -p /etc/ssh/sshd_config.d \
    && run_privileged install -m 0644 "${tmp_file}" "${drop_in}" \
    && run_privileged sshd -t \
    && (run_privileged systemctl reload sshd >/dev/null 2>&1 || run_privileged systemctl reload ssh >/dev/null 2>&1); then
    rm -f "${tmp_file}"
    action "Disabled SSH password authentication with ${drop_in}."
    return 0
  fi

  rm -f "${tmp_file}"
  return 1
}

ssh_effective_ports() {
  if command_exists sshd; then
    sshd -T 2>/dev/null | awk '$1 == "port" { print $2 }'
    return 0
  fi

  awk '
    BEGIN { IGNORECASE=1 }
    $1 == "Port" { print $2 }
  ' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null
}

ssh_key_auth_enabled() {
  local key_auth
  key_auth="$(ssh_effective_value pubkeyauthentication)"
  [[ -z "${key_auth}" || "${key_auth}" == "yes" ]]
}

remediate_ssh_port() {
  local desired_port="$1"
  local drop_in="/etc/ssh/sshd_config.d/98-openclaw-port.conf"
  local tmp_file

  if [[ -z "${desired_port}" || "${desired_port}" == "22" ]]; then
    return 1
  fi

  tmp_file="$(mktemp)"
  cat >"${tmp_file}" <<EOF
Port ${desired_port}
EOF

  if ! run_privileged mkdir -p /etc/ssh/sshd_config.d; then
    rm -f "${tmp_file}"
    return 1
  fi

  if ! run_privileged install -m 0644 "${tmp_file}" "${drop_in}"; then
    rm -f "${tmp_file}"
    return 1
  fi

  rm -f "${tmp_file}"

  if ! run_privileged sshd -t; then
    return 1
  fi

  if ! run_privileged systemctl reload sshd >/dev/null 2>&1 \
    && ! run_privileged systemctl reload ssh >/dev/null 2>&1; then
    return 1
  fi

  action "Configured SSH to listen on port ${desired_port}. Verify access with: ssh -p ${desired_port} <user>@<host>"
  return 0
}

check_ssh() {
  local password_auth
  local ports
  local port_ok=1
  password_auth="$(ssh_effective_value passwordauthentication)"

  if [[ "${SSH_REQUIRE_KEYS_ONLY}" -eq 1 ]]; then
    if [[ "${password_auth}" != "no" ]]; then
      if [[ "${AUTO_REMEDIATE}" -eq 1 ]] && remediate_ssh_password_auth; then
        password_auth="$(ssh_effective_value passwordauthentication)"
      fi
    fi

    if [[ "${password_auth}" != "no" ]]; then
      issue "SSH password authentication is still enabled."
    elif ! ssh_key_auth_enabled; then
      issue "SSH public key authentication is not enabled."
    else
      log "SSH is configured for key-based authentication only."
    fi

  else
    log "SSH key-only enforcement is disabled by configuration."
  fi

  if [[ "${SSH_PORT_IN_USE}" -ne 1 ]]; then
    log "SSH port policy skipped because SSH_PORT_IN_USE is disabled."
    return 0
  fi

  ports="$(ssh_effective_ports | sort -u | tr '\n' ' ')"
  if [[ -z "${ports}" ]]; then
    warn "Unable to determine SSH listening ports from configuration."
    return 0
  fi

  if contains_word "22" "${ports}"; then
    port_ok=0
    if [[ "${AUTO_REMEDIATE}" -eq 1 && "${ENABLE_SSH_PORT_REMEDIATION}" -eq 1 ]] \
      && remediate_ssh_port "${SSH_EXPECTED_PORT}"; then
      ports="$(ssh_effective_ports | sort -u | tr '\n' ' ')"
      if contains_word "22" "${ports}"; then
        issue "SSH still exposes port 22 after remediation attempt."
      else
        log "SSH no longer uses port 22."
      fi
    else
      issue "SSH is configured on port 22. Migrate to a non-default port such as ${SSH_EXPECTED_PORT}, allow it in the firewall, then verify with: ssh -p ${SSH_EXPECTED_PORT} <user>@<host>"
    fi
  fi

  if ! contains_word "${SSH_EXPECTED_PORT}" "${ports}"; then
    port_ok=0
    issue "SSH is not configured on the expected port ${SSH_EXPECTED_PORT}. Current configured ports: ${ports}"
  fi

  if [[ "${port_ok}" -eq 1 ]]; then
    log "SSH uses the expected non-default port ${SSH_EXPECTED_PORT}."
  fi
}

list_listening_ports() {
  ss -lntuH 2>/dev/null | awk '
    {
      split($5, parts, ":")
      port = parts[length(parts)]
      if (port ~ /^[0-9]+$/) {
        print tolower($1) " " port
      }
    }
  ' | sort -u
}

block_port() {
  local proto="$1"
  local port="$2"
  local backend
  backend="$(detect_firewall_backend)"

  case "${backend}" in
    ufw)
      run_privileged ufw deny "${port}/${proto}" >/dev/null 2>&1
      ;;
    firewalld)
      run_privileged firewall-cmd --permanent --remove-port="${port}/${proto}" >/dev/null 2>&1 \
        && run_privileged firewall-cmd --reload >/dev/null 2>&1
      ;;
    *)
      return 1
      ;;
  esac
}

check_ports() {
  local proto
  local port
  local unexpected=0
  local current

  while read -r proto port; do
    [[ -z "${proto}" || -z "${port}" ]] && continue

    if [[ "${proto}" == udp* ]]; then
      current="${EXPECTED_UDP_PORTS}"
      proto="udp"
    else
      current="${EXPECTED_TCP_PORTS}"
      proto="tcp"
    fi

    if contains_word "${port}" "${current}"; then
      continue
    fi

    unexpected=1
    if [[ "${AUTO_REMEDIATE}" -eq 1 && "${REMEDIATE_UNEXPECTED_PORTS}" -eq 1 ]] && block_port "${proto}" "${port}"; then
      action "Blocked unexpected ${proto} port ${port} at the firewall."
    else
      issue "Unexpected listening ${proto} port detected: ${port}."
    fi
  done < <(list_listening_ports)

  if [[ "${unexpected}" -eq 0 ]]; then
    log "No unexpected listening ports detected."
  fi
}

check_docker() {
  local running
  local name
  local unexpected=0

  if ! command_exists docker; then
    log "Docker is not installed."
    return 0
  fi

  if ! docker info >/dev/null 2>&1; then
    warn "Docker is installed but unavailable to the current user."
    return 0
  fi

  running="$(docker ps --format '{{.Names}}' 2>/dev/null)"
  if [[ -z "${running}" ]]; then
    log "No running Docker containers."
    return 0
  fi

  if [[ -z "${ALLOWED_DOCKER_CONTAINERS}" ]]; then
    issue "Running Docker containers found but ALLOWED_DOCKER_CONTAINERS is not configured."
    printf '%s\n' "${running}" | sed 's/^/[INFO] Running container: /'
    return 0
  fi

  while read -r name; do
    [[ -z "${name}" ]] && continue
    if contains_word "${name}" "${ALLOWED_DOCKER_CONTAINERS}"; then
      continue
    fi

    unexpected=1
    if [[ "${AUTO_REMEDIATE}" -eq 1 ]] && docker stop "${name}" >/dev/null 2>&1; then
      action "Stopped unexpected Docker container ${name}."
    else
      issue "Unexpected Docker container detected: ${name}."
    fi
  done <<< "${running}"

  if [[ "${unexpected}" -eq 0 ]]; then
    log "Docker containers match the allowlist."
  fi
}

cleanup_disk_space() {
  command_exists journalctl && run_privileged journalctl --vacuum-time=7d >/dev/null 2>&1 || true
  command_exists apt-get && run_privileged apt-get clean >/dev/null 2>&1 || true
  command_exists dnf && run_privileged dnf clean all >/dev/null 2>&1 || true
  command_exists yum && run_privileged yum clean all >/dev/null 2>&1 || true
  if [[ "${ALLOW_DOCKER_PRUNE}" -eq 1 ]] && command_exists docker; then
    docker system prune -af >/dev/null 2>&1 || true
  fi
}

enable_auto_security_updates_apt() {
  local periodic_file="/etc/apt/apt.conf.d/20auto-upgrades"
  local origin_file="/etc/apt/apt.conf.d/52openclaw-unattended-upgrades"
  local distro_id version_codename tmp_file

  distro_id="$(. /etc/os-release 2>/dev/null; printf '%s' "${ID:-Ubuntu}")"
  version_codename="$(. /etc/os-release 2>/dev/null; printf '%s' "${VERSION_CODENAME:-}")"
  [[ -n "${version_codename}" ]] || version_codename="stable"

  if ! command_exists apt-get; then
    return 1
  fi

  run_privileged apt-get update >/dev/null 2>&1 || true
  if ! dpkg -s unattended-upgrades >/dev/null 2>&1; then
    run_privileged apt-get install -y unattended-upgrades >/dev/null 2>&1 || return 1
  fi

  tmp_file="$(mktemp)"
  cat >"${tmp_file}" <<'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
EOF
  run_privileged install -m 0644 "${tmp_file}" "${periodic_file}" || { rm -f "${tmp_file}"; return 1; }

  cat >"${tmp_file}" <<EOF
Unattended-Upgrade::Origins-Pattern {
        "origin=${distro_id},codename=${version_codename},label=${distro_id}-Security";
        "origin=${distro_id},codename=${version_codename},suite=${version_codename}-security";
        "origin=Debian,codename=${version_codename},label=Debian-Security";
        "origin=Debian,codename=${version_codename},suite=${version_codename}-security";
        "origin=Ubuntu,codename=${version_codename},archive=${version_codename}-security";
};
EOF
  run_privileged install -m 0644 "${tmp_file}" "${origin_file}" || { rm -f "${tmp_file}"; return 1; }
  rm -f "${tmp_file}"

  if command_exists systemctl; then
    run_privileged systemctl enable --now unattended-upgrades >/dev/null 2>&1 || true
  fi

  action "Enabled unattended-upgrades for security updates."
  return 0
}

enable_auto_security_updates_dnf() {
  local config_file="/etc/dnf/automatic.conf"
  local timer_service=""
  local tmp_file

  if ! command_exists dnf; then
    return 1
  fi

  run_privileged dnf -y install dnf-automatic >/dev/null 2>&1 || return 1

  if command_exists systemctl; then
    if systemctl list-unit-files 2>/dev/null | grep -q '^dnf-automatic-install.timer'; then
      timer_service="dnf-automatic-install.timer"
    elif systemctl list-unit-files 2>/dev/null | grep -q '^dnf-automatic.timer'; then
      timer_service="dnf-automatic.timer"
    fi
  fi

  if [[ -f "${config_file}" ]]; then
    tmp_file="$(mktemp)"
    awk '
      /^\s*upgrade_type\s*=/ { print "upgrade_type = security"; next }
      /^\s*apply_updates\s*=/ { print "apply_updates = yes"; next }
      { print }
    ' "${config_file}" > "${tmp_file}"
    run_privileged install -m 0644 "${tmp_file}" "${config_file}" || { rm -f "${tmp_file}"; return 1; }
    rm -f "${tmp_file}"
  fi

  [[ -n "${timer_service}" ]] || return 1
  run_privileged systemctl enable --now "${timer_service}" >/dev/null 2>&1 || return 1
  action "Enabled dnf-automatic security updates."
  return 0
}

check_auto_security_updates() {
  if [[ "${AUTO_SECURITY_UPDATES_REQUIRED}" -ne 1 ]]; then
    log "Automatic security updates check is disabled by configuration."
    return 0
  fi

  if command_exists apt-config || command_exists apt-get; then
    if [[ -f /etc/apt/apt.conf.d/20auto-upgrades ]] \
      && grep -Eq 'APT::Periodic::Unattended-Upgrade "1"' /etc/apt/apt.conf.d/20auto-upgrades 2>/dev/null \
      && dpkg -s unattended-upgrades >/dev/null 2>&1; then
      log "Automatic security updates are enabled via unattended-upgrades."
      return 0
    fi

    if [[ "${AUTO_REMEDIATE}" -eq 1 ]] && enable_auto_security_updates_apt; then
      return 0
    fi

    issue "Automatic security updates are not enabled on this APT host."
    return 0
  fi

  if command_exists dnf; then
    if command_exists systemctl \
      && (systemctl is-enabled --quiet dnf-automatic-install.timer 2>/dev/null || systemctl is-enabled --quiet dnf-automatic.timer 2>/dev/null) \
      && grep -Eq '^\s*upgrade_type\s*=\s*security' /etc/dnf/automatic.conf 2>/dev/null; then
      log "Automatic security updates are enabled via dnf-automatic."
      return 0
    fi

    if [[ "${AUTO_REMEDIATE}" -eq 1 ]] && enable_auto_security_updates_dnf; then
      return 0
    fi

    issue "Automatic security updates are not enabled on this DNF host."
    return 0
  fi

  warn "Automatic security update verification is not implemented for this package manager."
}

check_disk() {
  local line
  local usage
  local mountpoint
  local over_limit=0

  while read -r line; do
    usage="$(awk '{print $5}' <<< "${line}" | tr -d '%')"
    mountpoint="$(awk '{print $6}' <<< "${line}")"
    [[ "${usage}" =~ ^[0-9]+$ ]] || continue

    if (( usage < DISK_THRESHOLD_PERCENT )); then
      continue
    fi

    over_limit=1
    if [[ "${AUTO_REMEDIATE}" -eq 1 ]]; then
      cleanup_disk_space
      usage="$(df -P "${mountpoint}" | awk 'NR==2 {gsub("%","",$5); print $5}')"
    fi

    if [[ "${usage}" =~ ^[0-9]+$ ]] && (( usage < DISK_THRESHOLD_PERCENT )); then
      action "Reduced disk usage on ${mountpoint} to ${usage}%."
    else
      issue "Disk usage on ${mountpoint} is ${usage}% (threshold ${DISK_THRESHOLD_PERCENT}%)."
    fi
  done < <(df -P -x tmpfs -x devtmpfs 2>/dev/null | awk 'NR>1')

  if [[ "${over_limit}" -eq 0 ]]; then
    log "Disk usage is below ${DISK_THRESHOLD_PERCENT}% on persistent filesystems."
  fi
}

failed_login_count() {
  local count=0

  if command_exists journalctl; then
    count="$(journalctl --since '-24 hours' --no-pager 2>/dev/null | grep -Eci 'Failed password|authentication failure|Invalid user|Failed publickey')"
    echo "${count}"
    return 0
  fi

  if command_exists lastb; then
    count="$(lastb -s -24hours 2>/dev/null | awk 'NF > 0 && $1 != "btmp" { total++ } END { print total + 0 }')"
    echo "${count}"
    return 0
  fi

  if [[ -f /var/log/auth.log ]]; then
    count="$(find /var/log -maxdepth 1 -name 'auth.log*' -mtime -1 -print0 2>/dev/null | xargs -0 zgrep -Ehi 'Failed password|authentication failure|Invalid user|Failed publickey' 2>/dev/null | wc -l | tr -d ' ')"
    echo "${count:-0}"
    return 0
  fi

  echo "0"
}

check_failed_logins() {
  local count
  count="$(failed_login_count)"
  log "Failed login attempts in the last 24 hours: ${count}."

  if [[ "${count}" =~ ^[0-9]+$ ]] && (( count > MAX_FAILED_LOGIN_ATTEMPTS )); then
    issue "Failed login attempts exceed the threshold (${count} > ${MAX_FAILED_LOGIN_ATTEMPTS})."
  fi
}

check_virustotal() {
  local helper
  local item
  local any_item=0

  if [[ "${VIRUSTOTAL_ENABLED}" -ne 1 ]]; then
    log "VirusTotal checks are disabled."
    return 0
  fi

  helper="${SCRIPT_DIR}/openclaw_virustotal_check.sh"
  if [[ ! -x "${helper}" ]]; then
    issue "VirusTotal helper script is missing or not executable: ${helper}"
    return 0
  fi

  for item in ${VIRUSTOTAL_URLS}; do
    any_item=1
    if VIRUSTOTAL_ALLOW_UPLOADS="${VIRUSTOTAL_ALLOW_UPLOADS}" \
      "${helper}" --url "${item}"; then
      log "VirusTotal browser review prepared for URL: ${item}"
    else
      issue "VirusTotal browser workflow failed for URL: ${item}"
    fi
  done

  for item in ${VIRUSTOTAL_FILES}; do
    any_item=1
    if VIRUSTOTAL_ALLOW_UPLOADS="${VIRUSTOTAL_ALLOW_UPLOADS}" \
      "${helper}" --file "${item}"; then
      log "VirusTotal browser review prepared for file: ${item}"
    else
      issue "VirusTotal browser workflow failed for file: ${item}"
    fi
  done

  if [[ "${any_item}" -eq 0 ]]; then
    warn "VirusTotal is enabled but no VIRUSTOTAL_URLS or VIRUSTOTAL_FILES were configured."
  fi
}

main() {
  log "Starting OpenClaw security audit."
  [[ -n "${CONFIG_FILE}" ]] && log "Using configuration file: ${CONFIG_FILE}"

  check_firewall
  check_fail2ban
  check_ssh
  check_ports
  check_docker
  check_disk
  check_failed_logins
  check_auto_security_updates
  check_virustotal

  if (( ${#ISSUES[@]} == 0 )); then
    printf 'audit de sécurité réussi\n'
    exit 0
  fi

  printf '\nSecurity audit found %d issue(s).\n' "${#ISSUES[@]}"
  printf '%s\n' "${ISSUES[@]}" | sed 's/^/- /'

  if (( ${#ACTIONS[@]} > 0 )); then
    printf '\nRemediation actions applied:\n'
    printf '%s\n' "${ACTIONS[@]}" | sed 's/^/- /'
  fi

  if (( ${#WARNINGS[@]} > 0 )); then
    printf '\nWarnings:\n'
    printf '%s\n' "${WARNINGS[@]}" | sed 's/^/- /'
  fi

  exit 1
}

main "$@"
