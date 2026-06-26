#!/bin/bash
# LiteLLM Supply Chain Attack Detector
# Checks for compromised litellm versions (1.82.7 / 1.82.8) and related IoCs
# Reference: https://github.com/BerriAI/litellm/issues/24512
# Date: 2026-03-24

set -u

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

FOUND=0

warn()  { echo -e "${RED}[!] $1${NC}"; FOUND=1; }
ok()    { echo -e "${GREEN}[+] $1${NC}"; }
info()  { echo -e "${YELLOW}[*] $1${NC}"; }

echo "============================================"
echo " LiteLLM Supply Chain Attack Detector"
echo " Target: litellm 1.82.7 / 1.82.8 (TeamPCP)"
echo "============================================"
echo ""

# --- 1. Check installed litellm version ---
info "Checking installed litellm version..."
if command -v pip &>/dev/null; then
  VER=$(pip show litellm 2>/dev/null | grep "^Version:" | awk '{print $2}')
  if [ -z "$VER" ]; then
    ok "litellm not installed via pip"
  elif [[ "$VER" == "1.82.7" || "$VER" == "1.82.8" ]]; then
    warn "COMPROMISED version detected: litellm $VER"
  else
    ok "litellm version $VER (not affected)"
  fi
else
  info "pip not found, skipping pip check"
fi

if command -v pip3 &>/dev/null && [ "$(which pip3)" != "$(which pip 2>/dev/null)" ]; then
  VER3=$(pip3 show litellm 2>/dev/null | grep "^Version:" | awk '{print $2}')
  if [[ "$VER3" == "1.82.7" || "$VER3" == "1.82.8" ]]; then
    warn "COMPROMISED version detected via pip3: litellm $VER3"
  fi
fi

if command -v uv &>/dev/null; then
  UV_HIT=$(find ~/.cache/uv -name "litellm_init.pth" 2>/dev/null)
  if [ -n "$UV_HIT" ]; then
    warn "Malicious .pth found in uv cache: $UV_HIT"
  else
    ok "uv cache clean"
  fi
fi

# --- 2. Search for litellm_init.pth ---
info "Searching for litellm_init.pth in Python site-packages..."

# Ask Python for all site-packages paths instead of scanning the entire filesystem
SITE_DIRS=$(python3 -c "import site; print('\n'.join(site.getsitepackages() + [site.getusersitepackages()]))" 2>/dev/null || true)

# Also check common locations: conda, virtualenvs, uv, pip cache
EXTRA_DIRS="$HOME/.cache/pip $HOME/.cache/uv $HOME/anaconda3 $HOME/miniconda3 $HOME/.local/lib ${VIRTUAL_ENV:-}"
SEARCH_DIRS=$(echo -e "$SITE_DIRS\n$EXTRA_DIRS" | sort -u | while read -r d; do [ -d "$d" ] && echo "$d"; done)

PTH_FILES=""
if [ -n "$SEARCH_DIRS" ]; then
  PTH_FILES=$(echo "$SEARCH_DIRS" | xargs -I{} find {} -name "litellm_init.pth" -maxdepth 5 2>/dev/null || true)
fi
if [ -n "$PTH_FILES" ]; then
  warn "Malicious .pth file found:"
  echo "$PTH_FILES" | while read -r f; do echo "       $f"; done
else
  ok "No litellm_init.pth found"
fi

# --- 3. Check for persistence backdoor ---
info "Checking for persistence artifacts..."

BACKDOOR_PATHS=(
  "$HOME/.config/sysmon/sysmon.py"
  "$HOME/.config/systemd/user/sysmon.service"
  "/tmp/.pg_state"
  "/tmp/pglog"
)

BACKDOOR_HIT=0
for f in "${BACKDOOR_PATHS[@]}"; do
  if [ -e "$f" ]; then
    warn "Backdoor artifact found: $f"
    BACKDOOR_HIT=1
  fi
done
[ $BACKDOOR_HIT -eq 0 ] && ok "No persistence artifacts found"

# Check if sysmon service is running
if command -v systemctl &>/dev/null; then
  if systemctl --user is-active sysmon.service &>/dev/null; then
    warn "sysmon.service is ACTIVE — backdoor is running!"
  fi
fi

# --- 4. Check network connections ---
info "Checking for suspicious network connections..."

MALICIOUS_DOMAINS="litellm\.cloud|checkmarx\.zone"
NET_HIT=""

if command -v lsof &>/dev/null; then
  NET_HIT=$(lsof -i -n 2>/dev/null | grep -E "$MALICIOUS_DOMAINS" || true)
elif command -v ss &>/dev/null; then
  NET_HIT=$(ss -tnp 2>/dev/null | grep -E "$MALICIOUS_DOMAINS" || true)
fi

if [ -n "$NET_HIT" ]; then
  warn "Suspicious connection detected:"
  echo "$NET_HIT"
else
  ok "No suspicious connections to known C2 domains"
fi

# --- 5. Check DNS cache / resolver logs ---
info "Checking DNS resolution..."
for domain in models.litellm.cloud checkmarx.zone; do
  if host "$domain" &>/dev/null 2>&1; then
    info "Domain $domain resolves (this is expected — just confirming it exists)"
  fi
done

# --- 6. Check Kubernetes ---
info "Checking Kubernetes environment..."
if command -v kubectl &>/dev/null; then
  K8S_PODS=$(kubectl get pods -n kube-system --no-headers 2>/dev/null | grep "node-setup-" || true)
  if [ -n "$K8S_PODS" ]; then
    warn "Suspicious pods in kube-system namespace:"
    echo "$K8S_PODS"
  else
    ok "No suspicious pods found in kube-system"
  fi

  # Check for privileged pods
  PRIV_PODS=$(kubectl get pods -n kube-system -o json 2>/dev/null | \
    python3 -c "
import sys, json
data = json.load(sys.stdin)
for pod in data.get('items', []):
  for c in pod['spec'].get('containers', []):
    sc = c.get('securityContext', {})
    if sc.get('privileged'):
      print(pod['metadata']['name'])
" 2>/dev/null || true)
  if [ -n "$PRIV_PODS" ]; then
    info "Privileged pods found (review manually): $PRIV_PODS"
  fi
else
  info "kubectl not found, skipping Kubernetes checks"
fi

# --- 7. Check transitive dependencies ---
info "Checking if litellm is a transitive dependency..."
if command -v pip &>/dev/null; then
  DEPENDENTS=$(pip show litellm 2>/dev/null | grep "^Required-by:" | cut -d: -f2 | xargs)
  if [ -n "$DEPENDENTS" ]; then
    info "These packages depend on litellm: $DEPENDENTS"
  fi
fi

# --- Summary ---
echo ""
echo "============================================"
if [ $FOUND -eq 0 ]; then
  echo -e "${GREEN} CLEAN — No indicators of compromise found.${NC}"
else
  echo -e "${RED} ALERT — Indicators of compromise detected!${NC}"
  echo ""
  echo " Recommended actions:"
  echo "   1. Uninstall litellm and delete litellm_init.pth manually"
  echo "   2. Remove backdoor: ~/.config/sysmon/ and sysmon.service"
  echo "   3. Purge caches: pip cache purge / rm -rf ~/.cache/uv"
  echo "   4. ROTATE ALL CREDENTIALS:"
  echo "      - SSH keys"
  echo "      - AWS / GCP / Azure credentials"
  echo "      - Kubernetes configs and service account tokens"
  echo "      - All API keys in .env files"
  echo "      - Database passwords"
  echo "      - Git credentials"
  echo "      - CI/CD secrets"
  echo "   5. Audit cloud IAM logs for unauthorized access"
  echo "   6. If in K8s: delete node-setup-* pods, audit secrets"
fi
echo "============================================"

exit $FOUND
