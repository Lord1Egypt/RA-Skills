# MaxBank Skill para OpenClaw

Skill que conecta seu OpenClaw ao MaxBank para consultar saldo, fazer PIX e pagar boletos.

Toda a comunicação é via **MCP** (Model Context Protocol). O MCP roda hospedado — a autenticação (Agent API Key) é injetada diretamente via header no mcporter, sem necessidade de proxy local.

## Ambientes

| Ambiente | Uso | MCP URL |
|----------|-----|---------|
| **prod** | Produção (padrão) | `https://maxbank-mcp.max.com.br/mcp` |
| **homolog** | Validação | `https://mcp-homologacao.maxbank.ai/mcp` |
| **local** | Dev com ngrok | `https://seu-ngrok.ngrok-free.app/mcp` |

Health check do MCP em produção: [https://maxbank-mcp.max.com.br/health](https://maxbank-mcp.max.com.br/health).

## Funcionalidades

| Comando | Descrição |
|---------|-----------|
| `maxbank.sh saldo` | Consulta saldo da conta |
| `maxbank.sh conta` | Exibe dados da conta conectada |
| `maxbank.sh pix CHAVE VALOR` | Cria transferência PIX (chave, e-mail, telefone ou QR) |
| `maxbank.sh pix code=CHAVE amount:N` | PIX com formato nomeado |
| `maxbank.sh billet LINHA_DIGITAVEL` | Paga boleto pela linha digitável |
| `maxbank.sh billet code=LINHA_DIGITAVEL` | Boleto com formato nomeado |
| `maxbank.sh status` | Exibe status da configuração mcporter |
| `maxbank.sh setup <codigo> <env> [url]` | Conecta conta (pareamento + config) |

## Instalação

```bash
clawhub install max-banking
```

Ou copie manualmente para `~/.openclaw/skills/max-banking/`.

## Setup (conectar conta)

O setup pode ser feito via chat ou manualmente:

### Via chat (recomendado)

Diga ao assistente: **"Quero conectar minha conta max, código AX7K-92QF"**

O assistente executa o setup completo: mcporter, pareamento e configuração do header de autenticação.

### Manual

```bash
# Prod (padrão)
bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh setup ABCD-EF12 prod

# Homolog
bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh setup ABCD-EF12 homolog

# Local (requer URL do ngrok)
bash ~/.openclaw/skills/max-banking/scripts/maxbank.sh setup ABCD-EF12 local https://xxx.ngrok-free.app/mcp
```

O setup faz:
1. Instala/verifica mcporter
2. Configura `openclaw.json`
3. Pareia via MCP (tool `pairing_exchange`)
4. Configura mcporter com `Authorization: Bearer <agent_key>` no header

## Pagamentos

### PIX

Aceita formato posicional ou nomeado:

```bash
# Posicional: chave + valor
maxbank.sh pix email@exemplo.com 50.00
maxbank.sh pix 11999998888 100

# Nomeado
maxbank.sh pix code=email@exemplo.com amount:50.00

# QR Code (copia-e-cola)
maxbank.sh pix 00020126...
```

Chaves aceitas: e-mail, telefone (10-11 dígitos), CPF/CNPJ, EVP (aleatória) ou payload QR (começa com `00020`).

### Boleto

Aceita apenas a linha digitável (o valor é extraído automaticamente dela):

```bash
# Posicional
maxbank.sh billet 23793.38128 60000.000003 00000.000008 1 10250000012345

# Nomeado
maxbank.sh billet code="23793.38128 60000.000003 00000.000008 1 10250000012345"
```

> **Importante:** Não envie `amount` ou outros parâmetros para boleto — apenas `code` com a linha digitável completa.

## Arquitetura

```
Usuário → OpenClaw (LLM) → exec maxbank.sh → mcporter → MCP hospedado → Banking API
                                                ↑
                                     Authorization: Bearer <agent_key>
                                     (injetado via header no mcporter config)
```

### Arquivos

```
skills/max-banking/
├── SKILL.md                    # Instruções para a LLM
├── README.md                   # Este arquivo
└── scripts/
    ├── maxbank.sh              # Wrapper unificado (entry point)
    ├── setup.sh                # Setup: pareamento + config mcporter
    └── connect-mcp.js          # Pareamento via MCP JSON-RPC
```

### Armazenamento

Tokens e sessão ficam em `~/.openclaw/secrets/maxbank/` com permissões restritas:

| Arquivo | Conteúdo | Permissão |
|---------|----------|-----------|
| `agent_key` | Agent API Key (longa duração) | `600` |
| `session.json` | Ambiente, telefone, account_id, data de conexão | `600` |

### Configuração mcporter

Após o setup, o mcporter fica configurado assim (equivalente a `mcporter config list`):

```json
{
  "banking": {
    "type": "http",
    "url": "https://maxbank-mcp.max.com.br/mcp",
    "headers": {
      "Authorization": "Bearer max_live_..."
    }
  }
}
```

## Configuração do OpenClaw

O `setup.sh` configura automaticamente. Para referência manual:

```json
{
  "skills": {
    "entries": {
      "mcporter": { "enabled": true },
      "max-banking": { "enabled": true }
    }
  },
  "tools": {
    "allow": ["exec", "process", "read", "write", "edit", "apply_patch"],
    "exec": { "host": "gateway" }
  }
}
```

## Troubleshooting

**"pairing not done"** — Execute o setup com um código de pareamento válido.

**"agent_key invalid"** — Chave revogada ou inválida. Refaça o pareamento com um novo código.

**"servidor 'banking' não encontrado no mcporter"** — O mcporter perdeu a configuração. Execute `maxbank.sh setup` novamente ou reconfigure manualmente:
```bash
mcporter config add banking --http-url https://maxbank-mcp.max.com.br/mcp --header '{"Authorization": "Bearer <sua_agent_key>"}'
```

**Agente não reconhece comandos** — Verifique:
1. Skill está em `~/.openclaw/skills/max-banking/SKILL.md`
2. `openclaw.json` tem `max-banking` habilitada
3. Permissão `exec` está em `tools.allow`
4. Inicie uma nova sessão (`/new`) após alterar configurações

**BILLET_TOO_MANY_ARGS** — O boleto aceita apenas a linha digitável em `code=`. Não envie `amount=`, `description=` ou outros parâmetros extras.
