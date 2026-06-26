#!/usr/bin/env bash
# Wrapper unificado para todas as ações do Max Banking.
# Uso: bash maxbank.sh <acao> [args...]
#
# Ações:
#   saldo                         — consulta saldo via MCP
#   conta                         — exibe dados da conta conectada
#   setup <codigo> <env> [url]    — conecta conta (pareamento + proxy)
#   pix-validate-qr CODIGO_QR    — valida QR Code PIX (retorna has_amount, amount, can_modify_final_amount)
#                                 O EMV pode conter espaços: passe o código inteiro entre aspas, ex.:
#                                 pix-validate-qr '00020126...Nome Com Espaço...6304'
#   pix CHAVE VALOR               — PIX por chave (valor obrigatório)
#   pix CODIGO_QR [VALOR]         — PIX por QR copia e cola (valor obrigatório se QR não tem valor embutido);
#                                 QR com espaços: aspas em volta do código, ex. pix '00020126...' 10.50
#   pix code=... amount:N         — formato nomeado
#   billet LINHA_DIGITAVEL        — cria pagamento de boleto (um único argumento: a linha)
#   billet code=LINHA_DIGITAVEL   — formato nomeado (apenas code=; sem outros parâmetros)
#   status                        — exibe status da configuração mcporter

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSION_FILE="$HOME/.openclaw/secrets/maxbank/session.json"
# Função para verificar que mcporter está configurado
check_mcporter_config() {
  # Se não há session, retorna erro
  if [[ ! -f "$SESSION_FILE" ]]; then
    echo "[maxbank] ERRO: Nenhuma conta configurada. Execute: bash maxbank.sh setup <codigo> [env]" >&2
    return 1
  fi

  # Testa se mcporter está instalado
  if ! command -v mcporter &>/dev/null; then
    echo "[maxbank] ERRO: mcporter não está instalado. Execute: npm install -g mcporter" >&2
    return 1
  fi

  # Verifica se o servidor banking está configurado no mcporter
  if ! mcporter config list 2>/dev/null | grep -q banking; then
    echo "[maxbank] AVISO: servidor 'banking' não encontrado no mcporter. Reconfigurando..." >&2

    local AGENT_KEY=""
    local AGENT_KEY_FILE="$HOME/.openclaw/secrets/maxbank/agent_key"
    if [[ -f "$AGENT_KEY_FILE" ]]; then
      AGENT_KEY=$(cat "$AGENT_KEY_FILE" 2>/dev/null)
    fi

    local MCP_URL=$(node -e "
      try {
        const s = JSON.parse(require('fs').readFileSync('$SESSION_FILE', 'utf8'));
        console.log(s.mcp_base_url || '');
      } catch(e) { console.log(''); }
    " 2>/dev/null)

    if [[ -z "$AGENT_KEY" || -z "$MCP_URL" ]]; then
      echo "[maxbank] ERRO: agent_key ou MCP_URL ausente. Execute: bash maxbank.sh setup <codigo> [env]" >&2
      return 1
    fi

    mcporter config add banking \
      --http-url "$MCP_URL" \
      --header "{\"Authorization\": \"Bearer $AGENT_KEY\"}" 2>/dev/null \
      || {
        echo "[maxbank] ERRO: Falha ao configurar mcporter. Execute: bash maxbank.sh setup <codigo> [env]" >&2
        return 1
      }
    echo "[maxbank] mcporter reconfigurado: banking → $MCP_URL" >&2
  fi
}

ACTION="${1:?Uso: bash maxbank.sh <acao> [args...]
Ações disponíveis: saldo, conta, setup, pix, billet, status}"
shift

# Garante configuração antes de qualquer chamada MCP
if [[ "$ACTION" != "setup" && "$ACTION" != "connect" && "$ACTION" != "conectar" && "$ACTION" != "configurar" && "$ACTION" != "instalar" && "$ACTION" != "auth" && "$ACTION" != "login" ]]; then
  check_mcporter_config || exit 1
fi

case "$ACTION" in
  saldo|balance|get-balance)
    echo "[maxbank] Chamando: mcporter call banking.banking_get_balance" >&2
    mcporter call banking.banking_get_balance --output json
    ;;
  conta|account|info|sessao|session)
    if [[ ! -f "$SESSION_FILE" ]]; then
      echo "NO_ACCOUNT"
      exit 0
    fi
    node -e "
      const s = JSON.parse(require('fs').readFileSync('$SESSION_FILE', 'utf8'));
      console.log('ACCOUNT_OK');
      console.log('PHONE=' + (s.phone_number || ''));
      console.log('ENV=' + (s.environment || ''));
      console.log('MCP_URL=' + (s.mcp_base_url || ''));
      console.log('PAIRED_AT=' + (s.paired_at || ''));
    " 2>/dev/null || { echo "NO_ACCOUNT"; exit 0; }
    ;;
  setup|connect|conectar|configurar|instalar|auth|login)
    bash "$SCRIPT_DIR/setup.sh" "$@"
    ;;
  pix-validate-qr|validar-qr)
    CODE=""
    for arg in "$@"; do
      if [[ "$arg" == code=* ]]; then
        CODE="${arg#code=}"
      elif [[ -z "$CODE" ]]; then
        CODE="$arg"
      fi
    done
    CODE="${CODE#"${CODE%%[![:space:]]*}"}"
    if [[ -z "$CODE" ]]; then
      echo "PIX_VALIDATE_QR_INVALID_ARGS: precisa do código QR PIX copia e cola."
      exit 1
    fi
    if [[ ! "$CODE" =~ ^00020 ]]; then
      echo "PIX_VALIDATE_QR_INVALID_ARGS: código informado não é QR Code PIX (deve começar com 00020)."
      exit 1
    fi
    echo "[maxbank] Chamando: mcporter call banking.banking_pix_qrcode_validate code=..." >&2
    mcporter call banking.banking_pix_qrcode_validate "code=$CODE" --output json
    ;;
  pix)
    PIX_ARGS=()
    HAS_NAMED=false
    for arg in "$@"; do
      [[ "$arg" == code=* || "$arg" == amount=* ]] && HAS_NAMED=true
    done
    if [[ "$HAS_NAMED" == true ]]; then
      for arg in "$@"; do
        if [[ "$arg" == amount=* ]]; then
          VAL="${arg#amount=}"
          VAL="${VAL//,/.}"
          PIX_ARGS+=("amount:$VAL")
        else
          PIX_ARGS+=("$arg")
        fi
      done
    else
      CODE=""
      AMOUNT=""
      for arg in "$@"; do
        if [[ "$arg" == *@* ]] || [[ "$arg" =~ ^00020 ]] || [[ "$arg" =~ ^[0-9]{10,11}$ ]]; then
          CODE="$arg"
        elif [[ -n "$arg" && ${#arg} -gt 10 ]]; then
          CODE="$arg"
        elif [[ "$arg" =~ ^[0-9]+([.,][0-9]+)?$ ]]; then
          AMOUNT="$arg"
        fi
      done
      if [[ -z "$CODE" ]]; then
        echo "PIX_INVALID_ARGS: precisa de chave PIX ou código QR (copia e cola)."
        exit 1
      fi
      if [[ "$CODE" =~ ^00020 ]]; then
        PIX_ARGS=(code="$CODE")
        if [[ -n "$AMOUNT" ]]; then
          AMOUNT="${AMOUNT//,/.}"
          PIX_ARGS+=("amount:$AMOUNT")
        fi
      else
        if [[ -z "$AMOUNT" ]]; then
          echo "PIX_INVALID_ARGS: para chave PIX é obrigatório informar o valor."
          exit 1
        fi
        AMOUNT="${AMOUNT//,/.}"
        PIX_ARGS=(code="$CODE" "amount:$AMOUNT")
      fi
    fi
    echo "[maxbank] Chamando: mcporter call banking.banking_pix ${PIX_ARGS[*]}" >&2
    mcporter call banking.banking_pix "${PIX_ARGS[@]}"
    ;;
  billet|boleto)
    # A API banking_billet aceita apenas UM argumento: code=<linha digitável completa>.
    # Se o LLM repassar vários parâmetros nomeados (ex.: code= + amount=), o mcporter envia
    # campos a mais e o backend responde 422.
    if [[ $# -lt 1 ]]; then
      echo "BILLET_INVALID_ARGS: precisa da linha digitável. Exemplos:"
      echo "  billet code=\"23793.38...\""
      echo "  billet 23793.38128 60000.000003..."
      exit 1
    fi

    HAS_CODE_NAMED=false
    for arg in "$@"; do
      [[ "$arg" == code=* ]] && HAS_CODE_NAMED=true && break
    done

    BILLET_SINGLE=""
    if [[ "$HAS_CODE_NAMED" == true ]]; then
      CODE_BUF=""
      SEEN_CODE=false
      for arg in "$@"; do
        if [[ "$arg" == code=* ]]; then
          if [[ "$SEEN_CODE" == true ]]; then
            echo "BILLET_TOO_MANY_ARGS: o boleto aceita apenas UM parâmetro para a API: a linha digitável em code= (sem repetir code=; junte a linha inteira em um único code= ou use aspas)."
            exit 1
          fi
          SEEN_CODE=true
          CODE_BUF="${arg#code=}"
        elif [[ "$arg" == *"="* ]]; then
          echo "BILLET_TOO_MANY_ARGS: o pagamento de boleto usa somente a linha digitável. Não envie outros parâmetros (valor, amount, descrição, etc.). Apenas: code=<linha> ou um único argumento posicional com a linha inteira."
          exit 1
        else
          if [[ "$SEEN_CODE" != true ]]; then
            echo "BILLET_INVALID_ARGS: com code= nomeado, o primeiro argumento deve ser code=<linha digitável>. Demais tokens só podem continuar a linha após o primeiro code=. Use posicional: billet LINHA (várias palavras) se preferir."
            exit 1
          fi
          CODE_BUF="$CODE_BUF $arg"
        fi
      done
      CODE_BUF="${CODE_BUF#"${CODE_BUF%%[![:space:]]*}"}"
      BILLET_SINGLE="code=$CODE_BUF"
    else
      # Posicional: um único argumento code= com toda a linha (espaços preservados em $*)
      BILLET_SINGLE="code=$*"
    fi

    echo "[maxbank] Chamando: mcporter call banking.banking_billet $BILLET_SINGLE" >&2
    mcporter call banking.banking_billet "$BILLET_SINGLE"
    ;;
  debug-token)
    echo "[maxbank] Chamando: mcporter call banking.banking_debug_token" >&2
    mcporter call banking.banking_debug_token --output json
    ;;
  proxy-status|status-proxy|check-proxy|config-status|status)
    echo "=== MaxBank Config Status ==="
    if [[ ! -f "$SESSION_FILE" ]]; then
      echo "Status: NO SESSION ($SESSION_FILE not found)"
      exit 1
    fi

    echo ""
    echo "=== mcporter config ==="
    if command -v mcporter &>/dev/null; then
      mcporter config list 2>/dev/null || echo "mcporter config list failed"
    else
      echo "mcporter NOT INSTALLED"
    fi

    echo ""
    echo "=== session.json ==="
    if [[ -f "$SESSION_FILE" ]]; then
      node -e "
        const s = JSON.parse(require('fs').readFileSync('$SESSION_FILE', 'utf8'));
        console.log(JSON.stringify(s, null, 2));
      " 2>/dev/null || cat "$SESSION_FILE"
    fi

    echo ""
    echo "=== agent_key ==="
    AGENT_KEY_FILE="$HOME/.openclaw/secrets/maxbank/agent_key"
    if [[ -f "$AGENT_KEY_FILE" ]]; then
      node -e "
        const k = require('fs').readFileSync('$AGENT_KEY_FILE', 'utf8').trim();
        const parts = k.split('.');
        if (parts.length >= 2) {
          console.log(parts[0] + '.' + parts[1].slice(0, 4) + '...' + ' (length: ' + k.length + ')');
        } else {
          console.log(k.slice(0, 8) + '...' + ' (length: ' + k.length + ')');
        }
      " 2>/dev/null || echo "EXISTS (could not read)"
    else
      echo "NOT FOUND: $AGENT_KEY_FILE"
    fi
    ;;
  *)
    echo "Ação desconhecida: $ACTION"
    echo "Ações disponíveis: saldo, conta, setup, pix-validate-qr, pix, billet, debug-token, status"
    exit 1
    ;;
esac
