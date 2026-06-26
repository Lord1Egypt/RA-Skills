# Deepening Workflow

Wenn ein Plan "vertieft" werden soll, wird jede Section systematisch erweitert.

## Trigger
- "deepen the plan"
- "Plan vertiefen"
- "mehr Details"
- "detaillierter Plan"

## Prozess

### 1. Section identifizieren
Alle Sections durchgehen und markieren welche Vertiefung brauchen.

### 2. Sub-Agent pro Section
Für jede zu vertiefende Section:
```
Task: Vertiefe die Section "[Name]" des Plans "[Plan-Titel]"

Kontext:
- Aktuelle Version der Section
- Workspace-Relevanz

Erweitere um:
- Konkretere Implementierungsdetails
- Fehlende Randfälle
- Test-Szenarien
- Abhängigkeiten
```

### 3. Zusammenführen
Alle vertieften Sections in den Gesamtplan integrieren.

### 4. Review
- Fehlende Verbindungen zwischen Sections?
- Widersprüche?
- Konsistenz der Detailtiefe?

## Wann Deepen?

| Plan-Größe | Deepen nötig? |
|------------|---------------|
| < 10 Steps | Nur wenn gewünscht |
| 10-30 Steps | Empfohlen |
| > 30 Steps | Obligatorisch |

## Output
Ein detaillierterer, implementierungsbereiter Plan mit:
- Konkreten Datei-Inhalten (pseudo-code OK)
- Randfall-Behandlung
- Test-Szenarien pro Step
- Zeitabschätzungen