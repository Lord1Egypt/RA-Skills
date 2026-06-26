# 🦅 Context-Hawk

> **KI-Kontext-Gedächtnis-Wächter** — Hör auf, den Faden zu verlieren, und fang an, dich an das Wichtige zu erinnern.

*Gib jedem KI-Agenten ein Gedächtnis, das wirklich funktioniert — über Sessions, Themen und Zeit hinweg.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## Was es macht

Die meisten KI-Agenten leiden an **Amnesie** — jede neue Sitzung beginnt bei Null. Context-Hawk löst das mit einem produktionsreifen Gedächtnisverwaltungssystem, das automatisch erfasst, was wichtig ist, Rauschen verblassen lässt und die richtige Erinnerung zum richtigen Zeitpunkt abruft.

**Ohne Context-Hawk:**
> "Ich habe es dir schon gesagt — ich mag kurze Antworten!"
> (nächste Sitzung, der Agent vergisst es wieder)

**Mit Context-Hawk:**
> (wendet stillschweigend deine Kommunikationspräferenzen aus Sitzung 1 an)
> ✅ Liefert jedes Mal eine präzise, direkte Antwort

---

## ✨ 10 Kernfunktionen

| # | Funktion | Beschreibung |
|---|---------|-------|
| 1 | **Aufgabenstatus-Persistenz** | `hawk resume` — Status speichern, nach Neustart fortsetzen |
| 2 | **4-stufiges Gedächtnis** | Working → Short → Long → Archive mit Weibull-Abfall |
| 3 | **Strukturiertes JSON** | Wichtigkeitsbewertung (0-10), Kategorie, Ebene, L0/L1/L2-Schichten |
| 4 | **KI-Wichtigkeitsbewertung** | Erinnerungen automatisch bewerten, minderwertige Inhalte verwerfen |
| 5 | **5 Injektionsstrategien** | A(high-imp) / B(aufgabenbezogen) / C(rezent) / D(top5) / E(voll) |
| 6 | **5 Kompressionsstrategien** | summarize / extract / delete / promote / archive |
| 7 | **Selbst-Introspektion** | Prüft Aufgabenklarheit, fehlende Informationen, Schleifenerkennung |
| 8 | **LanceDB-Vektorsuche** | Optional — hybride Vektor + BM25-Suche |
| 9 | **Reines Gedächtnis-Fallback** | Funktioniert ohne LanceDB, JSONL-Datei-Persistenz |
| 10 | **Auto-Deduplizierung** | Führt doppelte Erinnerungen automatisch zusammen |

---

## 🏗️ Architektur

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── Aktuelle Sitzung (letzte 5-10 Runden)  │
│       ↓ Weibull-Abfall                                        │
│  Short-term      ←── 24h Inhalt, zusammengefasst            │
│       ↓ access_count ≥ 10 + Wichtigkeit ≥ 0.7             │
│  Long-term       ←── Permanentes Wissen, vektorindiziert   │
│       ↓ >90 Tage oder decay_score < 0.15                    │
│  Archive          ←── Historie, bei Bedarf geladen         │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── Über Neustarts hinweg persistent (Schlüssel!)│
│  - Aktuelle Aufgabe / nächste Schritte / Fortschritt / Ausgaben│
├──────────────────────────────────────────────────────────────┤
│  Injektions-Engine  ←── Strategie A/B/C/D/E bestimmt Abruf │
│  Selbst-Introspektion ←── Jede Antwort prüft Kontext       │
│  Auto-Trigger        ←── Alle 10 Runden (konfigurierbar)    │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Aufgabenstatus-Gedächtnis (Wertvollste Funktion)

Selbst nach Neustart, Stromausfall oder Sitzungswechsel setzt Context-Hawk genau dort fort, wo es aufgehört hat.

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "API-Dokumentation abschließen",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["Architekturvorlage überprüfen", "Benutzer Bericht erstatten"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["Abdeckung muss 98% erreichen", "APIs müssen versioniert sein"],
  "resumed_count": 3
}
```

```bash
hawk task "Dokumentation abschließen"  # Aufgabe erstellen
hawk task --step 1 done             # Schritt als erledigt markieren
hawk resume                           # Nach Neustart fortsetzen ← KERN!
```

---

## 🧠 Strukturiertes Gedächtnis

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "Vollständiger Originalinhalt",
  "summary": "Einzeilige Zusammenfassung",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### Wichtigkeitsbewertung

| Bewertung | Typ | Aktion |
|-------|------|--------|
| 0.9-1.0 | Entscheidungen/Regeln/Fehler | Permanent, langsamster Abfall |
| 0.7-0.9 | Aufgaben/Präferenzen/Wissen | Langzeitgedächtnis |
| 0.4-0.7 | Dialog/Diskussion | Kurzzeit, Abfall zu Archiv |
| 0.0-0.4 | Chat/Begrüßungen | **Verwerfen, niemals speichern** |

---

## 🎯 5 Kontextinjektionsstrategien

| Strategie | Auslöser | Einsparung |
|----------|---------|-----------|
| **A: Hohe Wichtigkeit** | `Wichtigkeit ≥ 0.7` | 60-70% |
| **B: Aufgabenbezogen** | Scope-Treffer | 30-40% ← Standard |
| **C: Aktuell** | letzte 10 Runden | 50% |
| **D: Top5 Abruf** | Top 5 `access_count` | 70% |
| **E: Voll** | kein Filter | 100% |

---

## 🗜️ 5 Kompressionsstrategien

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 4-stufiges Alarm-System

| Stufe | Schwellenwert | Aktion |
|-------|---------|--------|
| ✅ Normal | < 60% | Still |
| 🟡 Beobachten | 60-79% | Kompression vorschlagen |
| 🔴 Kritisch | 80-94% | Auto-Schreiben pausieren, Vorschlag erzwingen |
| 🚨 Gefahr | ≥ 95% | Schreiben blockieren, Kompression Pflicht |

---

## 🚀 Schnellstart

```bash
# LanceDB-Plugin installieren (empfohlen)
openclaw plugins install memory-lancedb-pro@beta

# Skill aktivieren
openclaw skills install ./context-hawk.skill

# Initialisieren
hawk init

# Kernbefehle
hawk task "Meine Aufgabe"    # Aufgabe erstellen
hawk resume             # Letzte Aufgabe fortsetzen ← SEHR WICHTIG
hawk status            # Kontextnutzung anzeigen
hawk compress          # Gedächtnis komprimieren
hawk strategy B        # Zum aufgabenbezogenen Modus wechseln
hawk introspect         # Selbst-Introspektionsbericht
```

---

## Auto-Trigger: Alle N Runden

Alle **10 Runden** (Standard, konfigurierbar) führt Context-Hawk automatisch aus:

1. Kontext-Wasserstand prüfen
2. Gedächtniswichtigkeit bewerten
3. Status an Benutzer melden
4. Kompression vorschlagen, wenn nötig

```bash
# Konfiguration (memory/.hawk/config.json)
{
  "auto_check_rounds": 10,          # alle N Runden prüfen
  "keep_recent": 5,                 # letzte N Runden bewahren
  "auto_compress_threshold": 70      # komprimieren wenn > 70%
}
```

---

## Dateistruktur

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Python CLI-Werkzeug
└── references/
    ├── memory-system.md           # 4-Ebenen-Architektur
    ├── structured-memory.md      # Gedächtnisformat und Wichtigkeit
    ├── task-state.md           # Aufgabenstatus-Persistenz
    ├── injection-strategies.md  # 5 Injektionsstrategien
    ├── compression-strategies.md # 5 Kompressionsstrategien
    ├── alerting.md             # Alarmsystem
    ├── self-introspection.md   # Selbst-Introspektion
    ├── lancedb-integration.md  # LanceDB-Integration
    └── cli.md                  # CLI-Referenz
```

---

## Technische Daten

- **Persistenz**: JSONL lokale Dateien, keine Datenbank erforderlich
- **Vektorsuche**: LanceDB (optional), automatisches Fallback auf Dateien
- **Cross-Agent**: Universell, keine Geschäftslogik, funktioniert mit jedem KI-Agenten
- **Null-Konfiguration**: Sofort einsatzbereit mit intelligenten Standardwerten
- **Erweiterbar**: Benutzerdefinierte Injektionsstrategien, Kompressionsrichtlinien, Bewertungsregeln

---

## Lizenz

MIT — frei verwendbar, änderbar und verteilbar.
