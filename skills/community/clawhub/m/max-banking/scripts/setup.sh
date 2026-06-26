#!/usr/bin/env bash
# Setup MaxBank — conexão + ambiente (prod=padrão, homolog, local).
# Uso: bash setup.sh <pairing_code> [prod|homolog|local] [MCP_URL]
#
# Ambientes:
#   prod    → MCP em https://maxbank-mcp.max.com.br/mcp (default); health: …/health
#   homolog → MCP em mcp-homologacao.maxbank.ai
#   local   → MCP via ngrok — exige MCP_URL como 3º argumento
#
# Armazenamento:
#   ~/.openclaw/secrets/maxbank/agent_key      (Agent API Key de longa duração)
#   ~/.openclaw/secrets/maxbank/session.json   (ambiente, porta, account_id)

set -e

PAIRING_CODE="${1:?Uso: $0 <pairing_code> [prod|homolog|local] [MCP_URL]}"
ENV="${2:-prod}"
MCP_URL_OVERRIDE="${3:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# ── Ambiente ──────────────────────────────────────────────────────────────────

MCP_LOCAL="$MCP_URL_OVERRIDE"
MCP_HOMOLOG="https://mcp-homologacao.maxbank.ai/mcp"
MCP_PROD="https://maxbank-mcp.max.com.br/mcp"

case "$ENV" in
  prod)    MAXBANK_ENV="prod";    MCP_URL="$MCP_PROD" ;;
  homolog) MAXBANK_ENV="homolog"; MCP_URL="$MCP_HOMOLOG" ;;
  local)   MAXBANK_ENV="local";   MCP_URL="$MCP_LOCAL" ;;
  *) echo "ERRO: ENV deve ser prod, homolog ou local"; exit 1 ;;
esac

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
SECRETS_DIR="$HOME/.openclaw/secrets/maxbank"

# ── 1/5 Dependências ─────────────────────────────────────────────────────────

echo "==> 1/5 Verificando mcporter..."
if ! command -v mcporter &>/dev/null; then
  echo "    Instalando mcporter..."
  npm install -g mcporter 2>/dev/null || true
fi
if command -v openclaw &>/dev/null; then
  openclaw skill add steipete/mcporter 2>/dev/null || true
elif command -v clawhub &>/dev/null; then
  clawhub install steipete/mcporter 2>/dev/null || true
fi
echo "    mcporter OK"

echo "==> 1.5/5 Verificando zbar (QR e código de barras)..."
if command -v zbarimg &>/dev/null; then
  echo "    zbarimg OK"
else
  OS_KERNEL="$(uname -s 2>/dev/null || echo unknown)"
  case "$OS_KERNEL" in
    Darwin)
      if command -v brew &>/dev/null; then
        brew install zbar 2>/dev/null || true
      else
        echo "    (aviso: instale Homebrew e execute: brew install zbar)"
      fi
      ;;
    Linux)
      if [[ -f /etc/os-release ]]; then
        # shellcheck source=/dev/null
        . /etc/os-release
        DISTRO_ID="${ID:-}"
        case "$DISTRO_ID" in
          debian|ubuntu|linuxmint|pop|raspbian)
            if command -v apt-get &>/dev/null; then
              sudo apt-get update -qq 2>/dev/null && sudo apt-get install -y zbar-tools 2>/dev/null || true
            fi
            ;;
          fedora|rhel|centos|rocky|almalinux)
            if command -v dnf &>/dev/null; then
              sudo dnf install -y zbar 2>/dev/null || true
            elif command -v yum &>/dev/null; then
              sudo yum install -y zbar 2>/dev/null || true
            fi
            ;;
          arch|manjaro)
            if command -v pacman &>/dev/null; then
              sudo pacman -S --noconfirm zbar 2>/dev/null || true
            fi
            ;;
          alpine)
            if command -v apk &>/dev/null; then
              sudo apk add zbar 2>/dev/null || true
            fi
            ;;
          opensuse-tumbleweed|opensuse-leap|sles|opensuse)
            if command -v zypper &>/dev/null; then
              sudo zypper install -y zbar 2>/dev/null || true
            fi
            ;;
          *)
            echo "    (aviso: instale o pacote zbar ou zbar-tools para sua distribuição)"
            ;;
        esac
      else
        echo "    (aviso: /etc/os-release não encontrado; instale zbar manualmente)"
      fi
      ;;
    *)
      echo "    (aviso: instale zbar para leitura de QR/código de barras neste sistema)"
      ;;
  esac
  if command -v zbarimg &>/dev/null; then
    echo "    zbarimg OK"
  else
    echo "    (aviso: zbarimg indisponível — leitura a partir de imagem pode falhar)"
  fi
fi

# ── 2/5 Skill ────────────────────────────────────────────────────────────────

echo "==> 2/5 Instalando skill max-banking..."
SKILLS_DIR="${CLAWHUB_WORKDIR:-$PWD}/skills"
[[ ! -d "$SKILLS_DIR" ]] && SKILLS_DIR="$OPENCLAW_HOME/skills"
mkdir -p "$SKILLS_DIR"

if command -v clawhub &>/dev/null; then
  (cd "$(dirname "$SKILLS_DIR")" 2>/dev/null || true; clawhub install max-banking --force) 2>/dev/null || true
fi
mkdir -p "$SKILLS_DIR/max-banking"
cp -r "$SKILL_DIR"/* "$SKILLS_DIR/max-banking/" 2>/dev/null || true
echo "    Skill em $SKILLS_DIR/max-banking"

# ── 2.5/5 openclaw.json ──────────────────────────────────────────────────────

echo "==> 2.5/5 Configurando openclaw.json..."
OPENCLAW_CFG="${OPENCLAW_HOME}/openclaw.json"
node -e "
const fs = require('fs');
const p = process.env.OPENCLAW_CFG;
let cfg = {};
try { cfg = JSON.parse(fs.readFileSync(p, 'utf8')); } catch {}
cfg.skills = cfg.skills || {};
cfg.skills.entries = cfg.skills.entries || {};
cfg.skills.entries['mcporter'] = { enabled: true };
cfg.skills.entries['steipete/mcporter'] = { enabled: true };
cfg.skills.entries['max-banking'] = { enabled: true };
cfg.tools = cfg.tools || {};
cfg.tools.allow = cfg.tools.allow || ['exec', 'process', 'read', 'write', 'edit', 'apply_patch'];
if (!cfg.tools.allow.includes('exec')) cfg.tools.allow.push('exec');
cfg.tools.exec = cfg.tools.exec || {};
cfg.tools.exec.host = 'gateway';
fs.mkdirSync(require('path').dirname(p), { recursive: true });
fs.writeFileSync(p, JSON.stringify(cfg, null, 2));
console.log('    openclaw.json OK');
" OPENCLAW_CFG="$OPENCLAW_CFG" 2>/dev/null || echo "    (aviso: configure openclaw.json manualmente se necessário)"

# ── 3/5 MCP (mcporter config) ────────────────────────────────────────────────

echo "==> 3/5 Configurando mcporter (será atualizado após pareamento)..."
# mcporter será configurado após o pareamento (passo 4), quando temos a agent_key

# ── 4/5 Pareamento + Secrets ─────────────────────────────────────────────────

echo "==> 4/5 Pareamento [$ENV]..."

if [[ -z "$MCP_URL" ]]; then
  if [[ "$ENV" == "local" ]]; then
    echo "    ERRO: Para ambiente local, MCP_URL é obrigatório (3º argumento)."
    echo "    Uso: bash setup.sh <codigo> local <MCP_URL_NGROK>"
  else
    echo "    ERRO: MCP_URL não definida para o ambiente '$ENV'."
  fi
  exit 1
fi

mkdir -p "$SECRETS_DIR"
chmod 700 "$HOME/.openclaw/secrets" "$SECRETS_DIR"

echo "    Pareando via MCP (tool pairing_exchange)..."
node "$SCRIPT_DIR/connect-mcp.js" "$PAIRING_CODE" "$MCP_URL" "$MAXBANK_ENV"

# ── 5/5 mcporter config (com header Authorization) ──────────────────────────

echo "==> 5/5 Configurando mcporter com Authorization header..."

AGENT_KEY=""
if [[ -f "$SECRETS_DIR/agent_key" ]]; then
  AGENT_KEY=$(cat "$SECRETS_DIR/agent_key" 2>/dev/null)
fi

if [[ -z "$AGENT_KEY" ]]; then
  echo "    ERRO: agent_key não encontrada após pareamento." >&2
  exit 1
fi

# Configura mcporter diretamente com a URL do MCP e o header de autenticação
mcporter config add banking \
  --http-url "$MCP_URL" \
  --header "{\"Authorization\": \"Bearer $AGENT_KEY\"}" 2>/dev/null \
  && echo "    mcporter: banking → $MCP_URL (com Authorization header)" \
  || {
    # Fallback: configura manualmente via JSON se o comando falhar
    echo "    mcporter config add falhou, configurando manualmente..." >&2
    MCPORTER_CFG="${MCPORTER_CONFIG:-$HOME/.mcporter/mcporter.json}"
    mkdir -p "$(dirname "$MCPORTER_CFG")"
    MCPORTER_CFG="$MCPORTER_CFG" MCP_URL="$MCP_URL" AGENT_KEY="$AGENT_KEY" node -e "
const fs = require('fs');
const p = process.env.MCPORTER_CFG;
let cfg = {};
try { cfg = JSON.parse(fs.readFileSync(p, 'utf8')); } catch {}
cfg.mcpServers = cfg.mcpServers || {};
cfg.mcpServers['banking'] = {
  type: 'http',
  url: process.env.MCP_URL,
  headers: { Authorization: 'Bearer ' + process.env.AGENT_KEY }
};
fs.writeFileSync(p, JSON.stringify(cfg, null, 2));
console.log('    mcporter: banking → ' + process.env.MCP_URL + ' (com Authorization header)');
"
  }

# Limpa proxy antigo se existir
if [[ -f /tmp/maxbank-proxy.pid ]]; then
  kill $(cat /tmp/maxbank-proxy.pid) 2>/dev/null || true
  rm -f /tmp/maxbank-proxy.pid
  echo "    Proxy antigo encerrado (não é mais necessário)"
fi

# ── Output ────────────────────────────────────────────────────────────────────

PHONE=""
if [[ -f "$SECRETS_DIR/session.json" ]]; then
  PHONE=$(node -e "try{const s=JSON.parse(require('fs').readFileSync('$SECRETS_DIR/session.json','utf8'));console.log(s.phone_number||'')}catch{}" 2>/dev/null || true)
fi
[[ -z "$PHONE" ]] && PHONE="conectada"

echo ""
echo "SETUP_OK"
echo "PHONE=$PHONE"
if [[ "$ENV" == "local" || "$ENV" == "homolog" ]]; then
  echo "ENV=teste ($ENV)"
else
  echo "ENV=$ENV"
fi
echo "MCP_URL=$MCP_URL"
