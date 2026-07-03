---
title: Aquila Hermes-Fähigkeiten — Memory Management & Learning Loop
type: reference
created: 2026-06-12
permalink: aquila/hermes-features
---

# Aquila Hermes-Fähigkeiten — Memory Management & Learning Loop

## Übersicht

Aquila hat die Kernfähigkeiten von Hermes Agent nativ integriert — ohne Hermes selbst zu installieren. Drei Säulen bilden die Selbstverbesserung:

1. **Geschlossene Lernschleife** — Periodischer Self-Review, Pattern-Extraktion, Skill-Erstellung
2. **Skill-System** — Automatische Skill-Erstellung aus Erfahrungen, Progressive Disclosure
3. **Persistentes Gedächtnis** — Kapazitätsbeschränkt mit hartem Write-Block und Overflow-Archiv

---

## 1. Geschlossene Lernschleife

### Cron: `hermes-style-self-review`
- **Frequenz:** Alle 30 Minuten (00:00, 06:00, 12:00, 18:00)
- **Session-Target:** Isoliert (eigener Task)
- **Modell:** `openai/gpt-5.5` mit `thinking: high`
- **Timeout:** 600 Sekunden

### Ablauf
1. **REVIEW:** Nutze `sessions_list(activeMinutes=360)` um kürzliche Sessions zu finden. Wähle 1-2 relevante aus.
2. **EXTRACT:** Identifiziere aus den Sessions:
   - Wiederkehrende Aufgaben/Muster (mind. 2x gesehen)
   - Erfolgreiche Lösungswege nach Fehlversuchen
   - Korrekturen durch den Nutzer
   - Neue Tools/APIs die entdeckt wurden
   - Nicht-triviale Workflows (5+ Tool-Calls)
3. **CREATE/UPDATE:**
   - Wiederverwendbarer Workflow → Skill via `skill_workshop(action=create)`
   - Neue Erkenntnis →MEMORY.md (via `edit`)
   - Bestehender Skill → Update via `skill_workshop(action=update)`
4. **CONSOLIDATE:**
   - MEMORY.md prüfen → Entfernen, Zusammenführen, Auslagern
   - MEMORY.md >5.000 → Aufräumen
5. **LOG:** Schreibe Zusammenfassung in `vault/10-journal/YYYY-MM-DD.md` unter `## Self-Review`

### Trigger
- Nach Abschluss komplexer Tasks (5+ Tool-Calls)
- Nach Fehlversuchen mit erfolgreichem Lösungsweg
- Bei Nutzer-Korrekturen
- Bei wiederkehrenden Mustern (3x in 30 Tagen)
- Bei expliziten "merke dir"-Anfragen

---

## 2. Skill-System

### Skill: `auto-skill-builder`
- **Zweck:** Erkennt wann ein Workflow als Skill gespeichert werden sollte
- **Trigger:**
  - 5+ Tool-Calls in einer Session
  - Fehlversuch → erfolgreicher Weg
  - Nutzer-Korrektur
  - Wiederkehrende Aufgabe (3x in 30 Tagen)
- **Prozess:**
  1. Erkennung nach komplexen Tasks
  2. Extraktion: Name, Beschreibung, Trigger, Prozedur, Pitfalls, Verifikation
  3. Erstellung via `skill_workshop(action=create)`
  4. Als pending proposal speichern
  5. Nutzer bestätigt mit `skill_workshop(action=apply)` oder nach 24h automatisch

### Progressive Disclosure
- **Level 0:** `available_skills` listet Name + Beschreibung (~3K tokens)
- **Level 1:** SKILL.md wird nur bei Bedarf geladen (via `read`)
- **Level 2:** Referenzdateien nur bei explizitem Aufruf

### Qualität-Gates
- Lösung ist getestet und funktioniert
- Beschreibung ist ohne Original-Kontext verständlich
- Keine Secrets/Passwörter enthalten
- Keine projekt-spezifischen Hardcodes
- Skill-Name folgt Konvention (lowercase, hyphens)

---

## 3. Persistentes Gedächtnis

### Limits (Hermes-kompatibel mit Aquila-Optimierung)

| Datei | Zweck | Prompt-Limit | Overflow | Status |
|-------|-------|-------------|----------|--------|
| **MEMORY.md** | Agent's Langzeitgedächtnis | 5.000 Zeichen | `vault/30-knowledge/MEMORY-overflow.md` | ✅ 2.818 (56%) |
| **USER.md** | Nutzer-Profil | 1.375 Zeichen | `vault/30-knowledge/USER-overflow.md` | ✅ 1.310 (95%) |
| **memory/YYYY-MM-DD.md** | Tägliches Journal | 3.000 Zeichen | `vault/10-journal/YYYY-MM-DD.md` | ⚠️ 06-12: 2.121 (71%) |
| **working-buffer.md** | Aktiver Arbeitspuffer | 1.000 Zeichen | `vault/30-knowledge/working-buffer-overflow.md` | ✅ 333 (33%) |

### Harter Write-Block (HERMES-STYLE)

**Vor JEDEM Schreibzugriff auf eine der 4 Dateien:**

#### Step 1: Größe prüfen
```powershell
$current = Get-Content "<path>" -Raw
$newContent.Length
```

#### Step 2: Overflow-Check
Wenn `$newContent.Length > LIMIT`:
→ **BLOCKIERT** — Kürzen oder aufteilen.

#### Step 3: Near-Limit-Check (>80%)
Wenn `$current.Length > SOFT_LIMIT`:
→ **KONSOLIDIEREN MIT OVERFLOW** vor dem Schreiben:
1. Datei einlesen und alle Sektionen analysieren
2. Veraltete Einträge identifizieren (>30 Tage)
3. **Details auslagern statt löschen:**
   - Tabellen, Listen → Overflow/Vault (Niemals löschen!)
   - Projekt-Details → `vault/20-projects/<projekt>/`
4. Gekürzte Version schreiben (nur Kernfakten)
5. Erst DANN den neuen Eintrag hinzufügen

#### Step 4: Schreiben
Erst wenn `$newContent.Length <= LIMIT` → `write` ausführen.

### Was in MEMORY.md (Kernfakten)
- Umgebungs-Fakten (OS, Tools, Projektstruktur)
- Projekt-Konventionen und Konfiguration
- Tool-Eigenheiten und Workarounds
- Abgeschlossene Tasks (kurz!)
- Skills und Techniken die funktioniert haben
- Korrekturen durch Nutzer
- Explizite "merke dir"-Anfragen

### Was NICHT in MEMORY.md (→ Overflow auslagern)
- Raw Data Dumps (Code-Blöcke, Logs, Tabellen)
- Session-spezifische Ephemera (temp paths)
- Secrets/Passwörter/Token

### Was in USER.md (Kernfakten)
- Name, Rolle, Zeitzone
- Kommunikations-Präferenzen
- Pet Peeves und No-Gos
- Workflow-Gewohnheiten
- Technisches Skill-Level
- Aktive Projekte (Übersicht — Details → Overflow)

### Was im Overflow-Archiv
- `vault/30-knowledge/MEMORY-overflow.md` — Komplett-Backup aller ausgelagertenMEMORY.md-Details
- `vault/30-knowledge/USER-overflow.md` — Komplett-Backup aller ausgelagerten USER.md-Details
- `vault/30-knowledge/working-buffer-overflow.md` — Komplett-Backup aller ausgelagerten working-buffer-Details
- `vault/20-projects/<projekt>/` — Projekt-spezifische Details (Switch-Tabellen, API-Docs, etc.)

### Vorteil des Overflow-Systems
- **Keine Token-Kosten:** Overflow wird NIE in System-Prompt injiziert
- **Keine Datenverluste:** Alles wird ausgelagert, niemals gelöscht
- **Aquila lädt bei Bedarf:** `read vault/30-knowledge/MEMORY-overflow.md` — alle Details sofort verfügbar

---

## Integration mit Heartbeat

### HEARTBEAT.md — Ergänzung um Hermes-Style Nudge

```markdown
## Hermes-Style Nudge (bei jedem Heartbeat)
- Letzte 1-2 Sessions seit letztem Heartbeat reviewen (sessions_list activeMinutes=30)
- Neue Patterns erkennen? → skill_workshop create oder MEMORY.md update
- MEMORY.md >4.000 chars? → Konsolidieren
- USER.md >1.100 chars? → Konsolidieren
```

### Cron + Heartbeat — Zwei Nudge-Mechanismen

| Stufe | Mechanismus | Frequenz | Was passiert |
|-------|-------------|----------|-------------|
| **Cron-Nudge** | `hermes-style-self-review` | Alle 30 Min | Isolierter GPT-5.5 Run: Sessions reviewen → Patterns extrahieren → Skills/Memory erstellen |
| **Heartbeat-Nudge** | HEARTBEAT.md Integration | Bei jeder Interaktion mit dir | Inline im Haupt-Session-Kontext: Letzte Sessions checken, Patterns erkennen, MEMORY.md prüfen |

---

## Memory-Tool-Aktionen (Hermes-kompatibel)

| Aktion | Beschreibung |
|--------|-------------|
| `add` | Neuen Eintrag hinzufügen (mit Limit-Check + Write-Block + Overflow) |
| `replace` | Eintrag ersetzen (substring-matching via old_text) |
| `remove` | Eintrag entfernen (substring-matching via old_text) |

Kein `read` — Memory wird automatisch in System-Prompt injiziert.

---

## Session-Suche (FTS5-Äquivalent)

OpenClaw bietet `sessions_list` + `sessions_history` als Äquivalent zu Hermes' FTS5-Session-Suche:
- `sessions_list(search="keyword")` → Sessions finden
- `sessions_history(sessionKey)` → Inhalt lesen
- Kein LLM-Call nötig, direkter DB-Zugriff

---

## Status & Next Steps

### Aktueller Status
- ✅ Geschlossene Lernschleife: Cron + Heartbeat-Nudge aktiv
- ✅ Skill-System: Auto-Erstellung + Progressive Disclosure
- ✅ Persistentes Gedächtnis: 4 Dateien mit Kapazitätslimits + Write-Block + Overflow
- ✅ Konsolidierung: Bei >80% automatisch, Details in Overflow
- ✅ Keine Datenverluste: Alles wird ausgelagert, niemals gelöscht

### Nächste Schritte (optional)
- Integriere `learning-loop` Skill von ClawHub (yoder-bawt)
- Aktiviere Confidence Decay für Rules
- Aktiviere Cross-Agent Sharing
- Integriere 3-Tier-System (Events→Lessons→Rules)

---

## Related

- `vault/30-knowledge/MEMORY-overflow.md`
- `vault/30-knowledge/USER-overflow.md`
- `vault/30-knowledge/working-buffer-overflow.md`
- `vault/20-projects/idoit/switch-inventar.md`
- `vault/20-projects/cisco-backup/`
- `vault/10-journal/`

---

*Created: 2026-06-12 | Updated: 2026-06-12*  
*Author: Aquila 🦅*  
*Status: Active*