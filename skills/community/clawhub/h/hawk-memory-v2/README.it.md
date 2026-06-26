# 🦅 Context-Hawk

> **Guardiano della Memoria Contestuale IA** — Smetti di perdere il filo, inizia a ricordare ciò che conta.

*Dai a qualsiasi agente IA una memoria che funziona davvero — attraverso sessioni, argomenti e tempo.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## Cosa fa

La maggior parte degli agenti IA soffre di **amnesia** — ogni nuova sessione parte da zero. Context-Hawk risolve questo con un sistema di gestione della memoria di livello produzione che cattura automaticamente ciò che conta, fa svanire il rumore e richiama il ricordo giusto al momento giusto.

**Senza Context-Hawk:**
> "Te l'ho già detto — preferisco risposte concise!"
> (sessione successiva, l'agente dimentica di nuovo)

**Con Context-Hawk:**
> (applica silenziosamente le tue preferenze di comunicazione dalla sessione 1)
> ✅ Risposta concisa e diretta ogni volta

---

## ✨ 10 Funzionalità Principali

| # | Funzionalità | Descrizione |
|---|---------|-------|
| 1 | **Persistenza Stato Attività** | `hawk resume` — persiste lo stato, riprendi dopo riavvio |
| 2 | **Memoria a 4 Livelli** | Working → Short → Long → Archive con decadimento Weibull |
| 3 | **JSON Strutturato** | Punteggio di importanza (0-10), categoria, livello, strati L0/L1/L2 |
| 4 | **Punteggio Importanza IA** | Assegna automaticamente punteggio ai ricordi, scarta contenuto a basso valore |
| 5 | **5 Strategie di Iniezione** | A(alta-imp) / B(collegata attività) / C(recente) / D(top5) / E(completa) |
| 6 | **5 Strategie di Compressione** | summarize / extract / delete / promote / archive |
| 7 | **Auto-Introspezione** | Verifica chiarezza attività, info mancanti, rilevamento loop |
| 8 | **Ricerca Vettoriale LanceDB** | Opzionale — ricerca ibrida vettoriale + BM25 |
| 9 | **Fallback Memoria Pura** | Funziona senza LanceDB, persistenza JSONL |
| 10 | **Auto-Deduplicazione** | Unisce automaticamente i ricordi duplicati |

---

## 📦 Memoria Stato Attività (Funzionalità Più Preziosa)

Anche dopo riavvio, interruzione di corrente o cambio sessione, Context-Hawk riprende esattamente da dove aveva lasciato.

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "Completare la documentazione API",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["Rivedi template architettura", "Riporta all'utente"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["Copertura deve raggiungere il 98%", "Le API devono essere versionate"],
  "resumed_count": 3
}
```

```bash
hawk task "Completa la documentazione"  # Crea attività
hawk task --step 1 done             # Segna passo completato
hawk resume                           # Riprendi dopo riavvio ← FONDAMENTALE!
```

---

## 🧠 Memoria Strutturata

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "Contenuto originale completo",
  "summary": "Riepilogo in una riga",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### Punteggio di Importanza

| Punteggio | Tipo | Azione |
|-------|------|--------|
| 0.9-1.0 | Decisioni/regole/errori | Permanente, decadimento più lento |
| 0.7-0.9 | Attività/preferenze/conoscenze | Memoria a lungo termine |
| 0.4-0.7 | Dialogo/discussione | Breve termine, decadimento verso archivio |
| 0.0-0.4 | Chat/saluti | **Scartare, mai memorizzare** |

---

## 🎯 5 Strategie di Iniezione Contestuale

| Strategia | Trigger | Risparmio |
|----------|---------|--------|
| **A: Alta Importanza** | `importanza ≥ 0.7` | 60-70% |
| **B: Collegata all'Attività** | scope corrisponde | 30-40% ← predefinito |
| **C: Recente** | ultimi 10 turni | 50% |
| **D: Top5 Richiamo** | top 5 `access_count` | 70% |
| **E: Completa** | nessun filtro | 100% |

---

## 🗜️ 5 Strategie di Compressione

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 Sistema di Avviso a 4 Livelli

| Livello | Soglia | Azione |
|-------|--------|--------|
| ✅ Normale | < 60% | Silenzioso |
| 🟡 Osservazione | 60-79% | Suggerisci compressione |
| 🔴 Critico | 80-94% | Metti in pausa scrittura auto, forza suggerimento |
| 🚨 Pericolo | ≥ 95% | Blocca scritture, compressione obbligatoria |

---

## 🚀 Avvio Rapido

```bash
# Installa plugin LanceDB (consigliato)
openclaw plugins install memory-lancedb-pro@beta

# Attiva skill
openclaw skills install ./context-hawk.skill

# Inizializza
hawk init

# Comandi essenziali
hawk task "La mia attività"    # Crea attività
hawk resume             # Riprendi ultima attività ← MOLTO IMPORTANTE
hawk status            # Visualizza utilizzo contesto
hawk compress          # Comprimi memoria
hawk strategy B        # Passa a modo collegato all'attività
hawk introspect         # Report di auto-introspezione
```

---

## Auto-Trigger: Ogni N Turni

Ogni **10 turni** (predefinito, configurabile), Context-Hawk automaticamente:

1. Controlla livello contesto
2. Valuta importanza dei ricordi
3. Ti riporta lo stato
4. Suggerisce compressione se necessario

```bash
# Configurazione (memory/.hawk/config.json)
{
  "auto_check_rounds": 10,          # controlla ogni N turni
  "keep_recent": 5,                 # preserva ultimi N turni
  "auto_compress_threshold": 70      # comprimi quando > 70%
}
```

---

## Struttura File

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Strumento CLI Python
└── references/
    ├── memory-system.md           # Architettura a 4 livelli
    ├── structured-memory.md      # Formato memoria e importanza
    ├── task-state.md           # Persistenza stato attività
    ├── injection-strategies.md  # 5 strategie di iniezione
    ├── compression-strategies.md # 5 strategie di compressione
    ├── alerting.md             # Sistema di avviso
    ├── self-introspection.md   # Auto-introspezione
    ├── lancedb-integration.md  # Integrazione LanceDB
    └── cli.md                  # Riferimento CLI
```

---

## Specifiche Tecniche

- **Persistenza**: File JSONL locali, nessun database richiesto
- **Ricerca vettoriale**: LanceDB (opzionale), fallback automatico su file
- **Cross-Agent**: Universale, nessuna logica di business, funziona con qualsiasi agente IA
- **Zero-Config**: Funziona out-of-the-box con valori predefiniti intelligenti
- **Estendibile**: Strategie di iniezione personalizzate, politiche di compressione, regole di scoring

---

## Licenza

MIT — libero di utilizzare, modificare e distribuire.
