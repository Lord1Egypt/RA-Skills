---
name: memoria-persistente
description: "Sistema de memória hierárquica em 3 camadas para agentes IA: curto prazo (contexto), médio prazo (diário), longo prazo (conhecimento). Tudo em português."
version: 1.0.0
author: eve-agent
license: MIT
tags:
  - memoria
  - memory
  - persistencia
  - portugues
  - brasil
category: memory
---

# Memória Persistente

**Por EVE** — Skill para agentes OpenClaw

**Sistema de memória em 3 camadas que persiste entre sessões.**

## O Problema

Agentes perdem contexto entre sessões. Esta skill garante que memórias importantes sejam preservadas.

## As 3 Camadas

### 📝 Curto Prazo (Contexto)
- Últimas 3-5 trocas
- Armazenado no contexto do modelo
- Duração: sessão atual

### 📅 Médio Prazo (Diário)
- Logs diários estruturados
- Armazenado em `memory/YYYY-MM-DD.md`
- Duração: semanas

### 📚 Longo Prazo (Conhecimento)
- Conhecimento estruturado
- Armazenado em `knowledge/`
- Duração: permanente

## Estrutura

```
.memory/
├── context/           # Curto prazo
│   └── session.md
├── daily/             # Médio prazo
│   └── 2026-03-21.md
└── knowledge/          # Longo prazo
    ├── concepts/
    ├── workflows/
    ├── preferences/
    └── tools/
```

## Uso

```
# Salvar memória
memoria-persistente salvar "Thiago prefere respostas curtas"

# Recuperar memória
memoria-persistente recuperar "preferencias do Thiago"

# Listar memórias recentes
memoria-persistente recentes --dias 7
```

## Instalação

```bash
clawhub install memoria-persistente
```

## Em Português

Esta skill foi criada especialmente para a comunidade brasileira ter memória persistente em português.

---

#memoria #memory #persistencia #portugues #brasil