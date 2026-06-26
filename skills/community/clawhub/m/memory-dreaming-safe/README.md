# Memory Dreaming (Safe Edition)

Autonomous memory consolidation ("dreaming") for OpenClaw agents — mit verbesserten Safety-Regeln.

## Was ist anders?

Diese Version ergänzt den originalen memory-dreaming Skill mit:
- **Expliziter Bestätigungspflicht:** Keine automatischen Änderungen mehr
- **Safety & Boundaries:** Klare NEVER/ALWAYS/WHEN IN DOUBT Regeln
- **3 konkrete Examples:** Mustererkennung, Konsolidierung, Sensitive Data
- **Core Principles:** Read-before-Write, Diff-before-Apply, Interpretation-Not-Fact
- **Workflow mit Confirmation Gate:** 7 Schritte, Schritt 4 ist die Sicherheitskontrolle

## Sicherheitsverbesserungen

| Original | Diese Version |
|----------|---------------|
| Keine Safety-Sektion | NEVER/ALWAYS/WHEN IN DOUBT |
| Keine Beispiele | 3 konkrete Szenarien |
| Keine Trigger-Doku | When to Use + When NOT to Use |
| Kein Confirmation Gate | Diff → Bestätigung → Apply |

## Installation

```bash
clawhub install memory-dreaming-safe --registry "https://clawhub.ai"
```

Oder den Original-Skill ersetzen durch Kopieren der SKILL.md.

## Fork Hinweis

Dies ist ein Fork von @oryanmoshe/memory-dreaming mit ergänzten Safety-Regeln.
Alle originale Funktionalität bleibt erhalten.
