# openclaw-memory-transfer

> **Migrazione della memoria senza attrito per OpenClaw.** Porta i tuoi ricordi da ChatGPT, Claude, Gemini, Copilot e altri — in meno di 10 minuti.

[![Powered by MyClaw.ai](https://img.shields.io/badge/Powered%20by-MyClaw.ai-blue)](https://myclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[English](README.md) | [中文](README.zh-CN.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Español](README.es.md)

---

Hai passato mesi (o anni) con ChatGPT. Conosce il tuo stile di scrittura, i tuoi progetti, le tue preferenze. Quando passi a OpenClaw, niente di tutto ciò dovrebbe ricominciare da zero.

**Memory Transfer** estrae tutto ciò che il tuo vecchio assistente AI sa di te, pulisce i dati e li importa nel sistema di memoria di OpenClaw.

## Utilizzo

Di' al tuo agente OpenClaw:

```
Vengo da ChatGPT
```

## Fonti supportate

| Fonte | Metodo | Azione richiesta |
|-------|--------|-----------------|
| **ChatGPT** | Esportazione ZIP | Clicca Esporta nelle impostazioni, carica lo ZIP |
| **Claude.ai** | Guidato da prompt | Copia un prompt, incolla il risultato |
| **Gemini** | Guidato da prompt | Copia un prompt, incolla il risultato |
| **Copilot** | Guidato da prompt | Copia un prompt, incolla il risultato |
| **Claude Code** | Scansione automatica | Niente — automatico |
| **Cursor** | Scansione automatica | Niente — automatico |
| **Windsurf** | Scansione automatica | Niente — automatico |

## Cosa viene migrato

| Categoria | Destinazione | Esempi |
|-----------|-------------|--------|
| Identità | `USER.md` | Nome, professione, lingua, fuso orario |
| Stile comunicativo | `USER.md` | Tono di scrittura, preferenze di formattazione |
| Conoscenze | `MEMORY.md` | Progetti, competenze, intuizioni |
| Pattern comportamentali | `MEMORY.md` | Workflow, abitudini, correzioni |
| Preferenze strumenti | `TOOLS.md` | Stack tecnologico, piattaforme |

## Installazione

```bash
clawhub install openclaw-memory-transfer
```

## Licenza

MIT

---

**Powered by [MyClaw.ai](https://myclaw.ai)**
