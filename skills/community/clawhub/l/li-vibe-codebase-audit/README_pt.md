# 🔒 Vibe Codebase Audit - Guia de Uso em Português

## 📋 Visão Geral

**Vibe Codebase Audit** é uma ferramenta abrangente de auditoria de segurança projetada para bases de código geradas por IA, com integração nativa de agente, suporte multi-provedor e verificação de segurança de dependências.

> 🎉 **NOVIDADE na v2.0**: Auditoria nativa de agente (sem chave API), suporte multi-provedor, verificação de dependências, auditoria de configuração

---

## ⚡ Início Rápido

### Método 1: Auditoria Nativa de Agente (Recomendado, Sem Configuração!)

```python
# Sem chave API necessária! Usar diretamente o LLM do agente atual
from vibe_audit_enhanced import vibe_audit_enhanced

result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="agent_llm"  # Usar LLM do agente atual
)
```

### Método 2: Com Sua Chave API

```python
# Usar sua própria API OpenAI/Claude/Outra
result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="openai",  # ou "claude", "ollama", "deepseek"
    fallback_provider="claude"
)
```

### Método 3: Uso via CLI

```bash
# Usar LLM do agente (sem chave API)
python vibe_audit_enhanced.py /caminho/para/projeto --provider agent_llm

# Usar OpenAI
python vibe_audit_enhanced.py /caminho/para/projeto --provider openai

# Usar modelo local Ollama
python vibe_audit_enhanced.py /caminho/para/projeto --provider ollama
```

---

## 🆕 Novidades na v2.0

### 1. 🤖 Integração Nativa de Agente
- **Sem configuração** - Nenhuma chave API necessária
- Usa a conexão LLM do seu agente atual
- Integração perfeita com OpenCode, Hermes, OpenClaw
- Menor custo - aproveita assinatura existente do agente

### 2. 🔌 Suporte Multi-Provedor
- **Agent LLM** - Usar agente atual (recomendado)
- **OpenAI** - GPT-4, GPT-4-turbo
- **Claude** - Claude-3 Sonnet/Opus
- **DeepSeek** - Alternativa econômica
- **Qwen/Tongyi** - Modelos Alibaba
- **Ollama** - Executar modelos locais (grátis!)

### 3. 📦 Verificação de Segurança de Dependências
- Verificar vulnerabilidades conhecidas (CVE)
- Detectar dependências desatualizadas
- Verificação de conformidade de licenças
- Suporte: npm, pip, maven, cargo, go mod

### 4. ⚙️ Verificações de Segurança de Configuração
- Detecção de arquivos .env expostos
- Detecção de má configuração CORS
- Detecção de modo depuração
- Verificações SSL

---

## 📊 Comparação de Ferramentas

| Ferramenta | Velocidade | Precisão | Funções | Chave API | Melhor Para |
|------------|------------|----------|---------|-----------|-------------|
| `vibe_audit_enhanced` | Média-Rápida | Alta | Todas | Opcional | **Produção** |
| `vibe_audit_scan` | Rápida | Média | Básicas | Não | Verificações rápidas |
| `vibe_audit_multi_model` | Lenta | Máxima | Consenso AI | Sim | Projetos críticos |
| `vibe_audit_incremental` | Muito Rápida | Média | Git-aware | Opcional | CI/CD |

---

## 🌐 Configuração de Provedores

### Agent LLM (Recomendado)
```python
# Sem configuração! Usar diretamente:
primary_provider="agent_llm"
```

### OpenAI
```bash
export OPENAI_API_KEY="sk-..."
```

### Claude
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Ollama (Local, Grátis)
```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Baixar modelo
ollama pull llama2

# Usar na auditoria
primary_provider="ollama"
```

---

## 🚨 Níveis de Risco

| Nível | Pontuação | Ação |
|-------|-----------|------|
| ✅ SEGURO | 0 | Pronto para publicar |
| 🟢 BAIXO | 1-19 | Problemas menores, revisão recomendada |
| 🟡 MÉDIO | 20-49 | Revisar e corrigir antes de publicar |
| 🟠 ALTO | 50-79 | Problemas significativos, correções necessárias |
| 🔴 CRÍTICO | 80-100 | **NÃO PUBLICAR** |

---

## 🤝 Agentes Suportados

- **OpenCode** - Skill nativa
- **Hermes** - Plugin
- **OpenClaw** - Importação de módulo
- **Clientes MCP** - Suporte de protocolo

---

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/csmoove530/vibe-codebase-audit/issues)
- **Documentação**: Ver SKILL.md
- **Exemplos**: Ver diretório examples/

---

**Publique com confiança. Audite com rigor. Programe em paz.** 🚀
