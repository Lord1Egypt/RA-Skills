---
name: plan
description: "Create structured plans for multi-step tasks -- features, research, automations, events, or any goal that benefits from breakdown. Also deepens existing plans with interactive sub-agent review. Use when the user says 'plan this', 'create a plan', 'break this down', 'how should we build', or when a task is ready for structured planning. Use 'deepen the plan' for the deepening flow. For exploratory requests, prefer /brainstorm first."
argument-hint: "[optional: task description, requirements, or path to deepen]"
---

# Plan Skill

**Denke zuerst. Baue danach.** Der Plan kommt vor der Ausführung.

`/plan` definiert **HOW** — die konkrete Umsetzungsstruktur. Es produziert einen strukturierten Plan, führt keine Implementierung durch.

## Trigger

- "plan this", "create a plan", "break this down"
- "wie sollten wir vorgehen", "erstelle einen Plan"
- "deepen the plan", "Plan vertiefen"
- Direkte Erwähnung von `/plan`

## Was `/plan` leistet

- Zerlegt komplexe Tasks in umsetzbare Steps
- Definiert Abhängigkeiten und Reihenfolge
- Ordnet Dateien, Tools und Verantwortlichkeiten zu
- Testet/Annahmekriterien pro Feature
- Reserviert Entscheidungsspielraum (keine Pseudo-Implementation)

## Workflow

### Phase 0: Input & Scope klären

**Wenn keine Task angegeben:** Nutzer fragen: "Was möchtest du planen?"

**Wenn Input unklar:** Max 1-2 Clarifying-Fragen, dann zur Planning Bootstrap übergehen.

**Grundregel:** Bei direktem `/plan` Aufruf — immer planen. Nie mit "Das ist keine Planungsaufgabe" abbrechen.

### Phase 1: Recherche & Kontext

- Bestehenden Code / Dateien im Workspace prüfen
- Relevante Dokumentation lesen
- Vorherige Pläne oder Learnings aus MEMORY.md einbeziehen
- Falls nötig: Web-Recherche für externe Abhängigkeiten

### Phase 2: Plan erstellen

Einen strukturierten Plan mit diesen Sections:

```
# Plan: [Titel]

## Context & Problem
Was ist die Ausgangslage? Was soll erreicht werden?

## Goals
Konkrete, messbare Ziele dieses Plans.

## Approach
Der gewählte Weg und warum dieser Weg. Entscheidungen mit Begründung.

## Scope
Was ist INCLUDED / ausgeschlossen.

## File Map
Welche Dateien werden erstellt/geändert (repo-relative Pfade).

## Implementation Steps
Nummerierte Steps in korrekter Reihenfolge.
mit Abhängigkeiten und Zeitabschätzungen.

## Acceptance Criteria
Pro Feature/Step: Was muss funktionieren?

## Risks & Mitigations
Was könnte schiefgehen? Wie mildern wir das?

## Test Scenarios
Was muss getestet werden?
```

### Phase 3: Review & Export

- Plan präsentieren
- Feedback einholen
- Auf Wunsch: als `/home/HolBot/plans/YYYY-MM-DD-[slug].md` speichern
- Bei "deepen": Sub-Agent für detaillierte Ausarbeitung jeder Section

## Deepen Flow

Wenn Nutzer "deepen the plan" sagt:

1. Sub-Agent pro Plan-Section starten
2. Section mit konkreten Implementierungsdetails anreichern
3. Fehlende Tests, Randfälle, Edge Cases ergänzen
4. Zusammenführen und präsentieren

## Quality Bar

Ein guter Plan enthält:
- ✅ Klare Problem-Frame und Scope-Grenze
- ✅ Konkrete Requirements-Rückverfolgbarkeit
- ✅ Repo-relative Pfade (keine absoluten Pfade!)
- ✅ Entscheidungen mit Begründung
- ✅ Test-Szenarien pro Feature-Bearing Unit
- ✅ Abhängigkeiten und Sequenzierung

## Dos & Don'ts

| DO | DON'T |
|----|-------|
| Recherche vor Struktur | Sofort coden ohne Plan |
| Entscheidungen erklären | Nur Tasks ohne Kontext |
| Scope explizit machen | Alles auf einmal wollen |
|.small Work = compact Plan | Over-Engineering für triviale Tasks |
| Cliffhanger für Review | Plan ohne User-Feedback abschließen |

---

*Inspiriert von `ce-plan` (Compound Engineering Plugin) — adaptiert für OpenClaw.*