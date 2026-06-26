---
version: 1.0.0
name: lena-learning
description: Lena lernt aus jeder Konversation und verbessert sich automatisch
---

<objective>
Der Agent lernt kontinuierlich aus jeder Konversation und verbessert sich automatisch. Speichert Erkenntnisse, Korrekturen und Präferenzen für bessere future Responses.
</objective>

<principles>
## Wie Selbst-Verbesserung funktioniert

### 1. Nach jeder Session
- Key Insights extrahieren
- Fehler dokumentieren
- Präferenzen aktualisieren
- Learnings speichern

### 2. Memory System
- daily logs: memory/YYYY-MM-DD.md
- long-term: MEMORY.md
- preferences: USER.md, TOOLS.md

### 3. Feedback Loop
- Korrekturen sofort speichern
- recurring patterns merken
- bessere prompts entwickeln
</principles>

<process>
## Verbesserungs-Routine nach jeder Konversation

<step>
<action>Identifiziere neue Learnings</action>
<details>
- Was habe ich heute Neues gelernt?
- Welche Insights sollte ich mir merken?
- Gab es Fehler die ich nicht wiederholen soll?
</details>
</step>

<step>
<action>Aktualisiere Memory Files</action>
<details>
- memory/YYYY-MM-DD.md: Raw notes
- MEMORY.md: Langzeit-Wissen
- USER.md: Präferenzen
- TOOLS.md: Environment-Notes
</details>
</step>

<step>
<action>Skill-Updates</action>
<details>
- Check ob Skills verbessert werden müssen
- Neue Patterns dokumentieren
- Best Practices teilen
</details>
</step>

<step>
<action>Feedback-Loop</action>
<details>
- Wenn Thomas mich korrigiert -> sofort speichern
- Wenn etwas nicht funktioniert -> dokumentieren
- Wenn etwas gut funktioniert -> merken
</details>
</step>
</process>

<triggers>
## Wann aktivieren?

- Am Ende jeder Session
- Nach jeder Korrektur durch Thomas
- Bei signifikanten Entscheidungen
- Täglich (Heartbeat-Routine)
</triggers>

<success_criteria>
- Keine Wiederholung alter Fehler
- BessereResponses durch Memory
- Thomas' Präferenzen genau kennen
- Kontinuierliches Lernen ohne manuelles Setup
</success_criteria>