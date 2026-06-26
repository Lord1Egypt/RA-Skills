# 🔍 li_sentry_check - Habilidade de Inspeção de Servidores

> Habilidade multiplataforma de inspeção e verificação de saúde de servidores. Acesso SSH a servidores Linux remotos por meio de autenticação por chave, execução de comandos de inspeção somente leitura e geração de relatórios estruturados em Markdown.

[![Versão](https://img.shields.io/badge/versão-0.1.0-blue.svg)](https://clawhub.ai/skills/li_sentry_check)
[![Plataformas](https://img.shields.io/badge/plataformas-nanobot%20%7C%20OpenClaw%20%7C%20Hermes-green.svg)]()
[![Licença](https://img.shields.io/badge/licença-MIT-green.svg)](LICENSE)

## 📋 Visão Geral

`li_sentry_check` é uma habilidade de inspeção de servidores multiplataforma que suporta **nanobot**, **OpenClaw** e **Hermes agent**. Ele se conecta a servidores Linux remotos por meio de autenticação por chave SSH, executa comandos de inspeção somente leitura (CPU, memória, disco, rede, serviços, segurança) e gera relatórios Markdown estruturados com destaque automático de anomalias.

## ✨ Funcionalidades Principais

| Funcionalidade | Descrição |
|----------------|-----------|
| 🔐 Autenticação por Chave SSH | Somente autenticação por chave, acesso por senha desabilitado, segurança reforçada |
| 📊 Inspeção de Hardware | CPU, memória, disco, uso de rede |
| 🖥️ Inspeção de Serviços | Estado de serviços-chave, logs de erros |
| 🛡️ Inspeção de Segurança | Logins SSH anômalos, alertas de firewall, erros do kernel |
| 📝 Relatórios Estruturados | Formato Markdown/JSON, anomalias prioritárias |
| 🌐 Multiplataforma | Suporta nanobot, OpenClaw, Hermes |

## 🚀 Início Rápido

### 1. Instalar a Habilidade

```bash
# nanobot
./manage.sh skill install li_sentry_check

# OpenClaw
npx clawhub@latest install li_sentry_check

# Hermes
hermes skill install li_sentry_check
```

### 2. Configurar Chaves SSH

```bash
# Gerar par de chaves
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# Copiar chave pública para o servidor remoto
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@<IP_SERVIDOR>

# Testar conexão
ssh -i ~/.ssh/li_sentry_check inspector@<IP_SERVIDOR>
```

### 3. Configurar Servidores Alvo

Editar `references/targets.yaml`:

```yaml
targets:
  produção-web:
    host: SEU_IP_SERVIDOR
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - nginx
      - docker
      - sshd
```

### 4. Executar Inspeção

```bash
# Inspeção básica (recursos de hardware)
python3 scripts/inspect.py --target produção-web --checks basic

# Inspeção de serviços
python3 scripts/inspect.py --target produção-web --checks services

# Inspeção completa (básica + serviços + segurança + logs)
python3 scripts/inspect.py --target produção-web --checks daily

# Saída em formato JSON
python3 scripts/inspect.py --target produção-web --checks daily --format json

# Saída para arquivo
python3 scripts/inspect.py --target produção-web --checks daily --output relatorio.md
```

## 📖 Grupos de Verificação de Inspeção

| Grupo | Conteúdo | Comandos |
|-------|----------|----------|
| `basic` | CPU, memória, disco, rede | 8 |
| `services` | Estado de serviços + logs de erros (dinâmico) | 3×N |
| `daily` | Inspeção completa (básica + serviços + segurança + logs) | 26 |

## 📊 Exemplo de Relatório

```markdown
# 🔍 Relatório de Inspeção de Servidor

- Alvo: produção-web
- Host: SEU_IP_SERVIDOR
- Usuário: inspector
- Verificações: daily
- Iniciado: 2026-04-26T09:00:00+00:00
- Total de verificações: 26
- ⚠️ Anomalias: 3

## Estado Geral: ⚠️ AVISO

## ⚠️ Anomalias (Prioridade)

### ⚠️ systemd_failed_units
Comando: `systemctl --failed --no-pager`
Estado: OK (contém anomalias)

Saída:
```
UNIT          LOAD   ACTIVE SUB    DESCRIPTION
mcelog.service loaded failed failed Machine Check Exception Logging Daemon
```
```

## 🔧 Opções de Linha de Comando

| Opção | Descrição | Padrão |
|-------|-----------|--------|
| `--target` | Nome do servidor alvo (definido em targets.yaml) | (obrigatório) |
| `--checks` | Grupo de verificação: `basic`, `services`, `daily` | `basic` |
| `--format` | Formato de saída: `markdown`, `json` | `markdown` |
| `--output` | Saída para arquivo (padrão: stdout) | stdout |

## 🌐 Suporte Multiplataforma

| Plataforma | Runtime | Script | Comando |
|------------|---------|--------|---------|
| **OpenClaw** | Node.js 24+ | `scripts/inspect.mjs` | `node scripts/inspect.mjs --target bogon --checks daily` |
| **NanoBot** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |
| **Hermes** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |

## 📁 Estrutura de Arquivos

```
li_sentry_check/
├── SKILL.md                  # Documentação da habilidade
├── _meta.json                # Metadados da habilidade
├── design.md                 # Documentação de design
├── references/
│   ├── targets.yaml          # Configuração de servidores alvo
│   └── checks.yaml           # Lista branca de comandos de inspeção
└── scripts/
    ├── inspect.mjs           # Implementação Node.js (OpenClaw)
    └── inspect.py            # Implementação Python (NanoBot/Hermes)
```

## 🔒 Melhores Práticas de Segurança

- **Permissões de chave**: `chmod 600 ~/.ssh/li_sentry_check`
- **Verificação de host**: Para produção, pré-preencha `known_hosts` em vez de usar `accept-new`
- **Nomes de serviços**: Apenas alfanumérico, hífens, sublinhados permitidos (validados antes do uso)
- **Lista branca de comandos**: Nunca modifique `checks.yaml` com comandos que alterem o estado
- **Manuseio de relatórios**: Os relatórios podem conter dados do sistema — não compartilhe publicamente

## 🔧 Guia de Extensão

### Adicionar um Novo Servidor Alvo

Editar `references/targets.yaml`:

```yaml
targets:
  servidor-banco-dados:
    host: SEU_IP_SERVIDOR
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - mysql
      - redis
```

### Adicionar um Novo Grupo de Verificação

Editar `references/checks.yaml`:

```yaml
checks:
  banco-dados:
    description: Inspeção de banco de dados
    commands:
      - id: mysql_status
        cmd: "systemctl status mysql --no-pager | sed -n '1,20p'"
        timeoutSec: 10
      - id: mysql_connections
        cmd: "mysql -e 'SHOW STATUS LIKE \"Threads_connected\"' || true"
        timeoutSec: 15
```

## 📝 Histórico de Versões

| Versão | Data | Alterações |
|--------|------|------------|
| 0.1.0 | 2026-04-26 | Versão inicial: inspeção básica, de serviços e completa |

## 📄 Licença

Licença MIT
