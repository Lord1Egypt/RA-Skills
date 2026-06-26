# Brainstorm Skill

**Trigger:** `/brainstorm` oder "brainstorm", "sammle Ideen", "was sind die Möglichkeiten?"

## Was es leistet

`/brainstorm` sammelt und strukturiert Ideen — bevor ein Plan erstellt wird.
Es definiert **WHAT** zu bauhen ist, nicht **HOW**.

## Wann brainstorm?

- Nutzer hat ein vages Ziel
- Mehrere Lösungswege möglich
- Kreativität gefragt
- Keine klare Richtung

## Wann NICHT brainstorm?

- Anforderungen sind bereits klar
- Nutzer fragt direkt nach Plan
- Es gibt nur einen offensichtlichen Weg

## Workflow

### 1. Ziel verstehen
- Was ist das Problem/die Opportunity?
- Wer sind die Stakeholder?
- Was sind die Constraints?

### 2. Ideen sammeln (Diverging)
- Quantity over Quality
- Keine Kritik during Brainstorm
- Ungewöhnliche Ideen ermutigen
- Verwandte Domains einbeziehen

### 3. Clustern & Strukturieren
- Ähnliche Ideen gruppieren
- Themen identifizieren
- Prioritäten setzen (MoSCoW, RICE, etc.)

### 4. Fokus-Setzung (Converging)
- Top 3-5 Ansätze identifizieren
- Pro/Contra analysieren
- Empfehlung aussprechen

### 5. Output
Format:
```
# Brainstorm: [Thema]

## Ziel
## Constraints
## Ideen ( clustered )
## Top-Ansätze
## Empfehlung
## Nächste Schritte
```

## Integration mit /plan

Brainstorm output → Input für `/plan`

> `/brainstorm` defines WHAT to build. `/plan` defines HOW to build it. `ce-work` executes the plan.