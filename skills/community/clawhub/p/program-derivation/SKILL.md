---
name: program-derivation
description: Formale Programmableitung / Formal Program Derivation: Architektur-Ermittlung, Abstraktionsschichten, Metriken (CC, LCOM, Kopplung, Kohäsion, Vendor Lock-in, SoC, Leaky Abstractions). Lade diesen Skill wenn der Nutzer eine Architekturanalyse, Programmableitung, formale Ableitung, Abstraktionsschichten, Interface-Design, Komplexitätsmessung, Refactoring-Planung oder Software-Qualitätsbewertung anfordert. / Load this skill when the user requests architecture analysis, program derivation, formal derivation, abstraction layers, interface design, complexity measurement, refactoring planning or software quality assessment.
---
# Programmableitung / Program Derivation

## Wann dieser Skill geladen werden soll / When to Load

**Deutsch:** Lade diesen Skill bei:
- Architekturanalyse eines bestehenden oder neuen Systems
- Formale Programmableitung / Program Derivation
- Abstraktionsschichten-Design (Interfaces, Wrappers, Facades)
- Komplexitätsmessung (CC, LCOM, Kopplung, Kohäsion)
- Vendor Lock-in Analyse
- Refactoring-Planung und Entkopplungspunkte
- Software-Qualitätsbewertung

**English:** Load this skill for:
- Architecture analysis of existing or new systems
- Formal program derivation
- Abstraction layer design (Interfaces, Wrappers, Facades)
- Complexity measurement (CC, LCOM, Coupling, Cohesion)
- Vendor Lock-in analysis
- Refactoring planning and decoupling points
- Software quality assessment

---

## Arbeitsanweisung / Work Instructions

Führe die Analyse in drei Phasen durch. Sprache der Ausgabe: Sprache des Nutzers (de/en).

---

## Phase 1: Architektur-Ermittlung / Architecture Discovery

### 1.1 Grenzschichten-Check / Boundary Analysis
Identifiziere alle Schnittstellen zu externen Systemen.

**Ausgabe-Tabelle / Output table:**
| Schnittstelle | Typ | Protokoll | Authentifizierung | Fehlerbehandlung |
|---|---|---|---|---|
| ... | REST-API / DB / Browser-API / FS | HTTPS/JSON / SQLite / In-Process | Bearer / Key / keine | ja (Retry) / teilweise / nein |

### 1.2 Austauschbarkeits-Check / Replaceability Check
Bewerte jede externe Abhängigkeit: Ist sie austauschbar ohne Core-Code-Änderungen?

**Skala:** 1 = hardgecoded, kein Interface | 3 = Interface vorhanden, aber spezifische Typen | 5 = vollständig abstrakt, Provider-agnostisch

### 1.3 Komplexitäts-Check / Complexity Check
- Zeilenzahl und Funktionsanzahl pro Modul
- Geschachtelte Async-Strukturen / fire-and-forget Patterns
- Kritische Pfade identifizieren

### 1.4 Vendor Lock-in Analyse
Bewertung: **HOCH** (hardgecoded URL + Model + Response-Parsing) | **MITTEL** (teilweise abstrahiert) | **NIEDRIG** (Web-Standard oder austauschbar)

### 1.5 Separation of Concerns (SoC)
Identifiziere Verletzungen: Business-Logik in Routing-Schicht, duplizierte Logik mit abweichenden Konstanten, Datenbankzugriff ohne Interface-Nutzung.

### 1.6 Kopplung & Kohäsion / Coupling & Cohesion
- **Ca** (Afferente Kopplung): Wie viele Module hängen von diesem ab?
- **Ce** (Efferente Kopplung): Von wie vielen Modulen hängt dieses ab?
- **I** (Instabilitäts-Index): `I = Ce / (Ca + Ce)` — 0 = stabil, 1 = instabil
- **Kohäsionstyp:** Funktional (hoch) → Logisch → Sequentiell → Kommunikativ → Prozedural → Zeitlich → Koinzidentell (niedrig)

### 1.7 Leckende Abstraktionen / Leaky Abstractions
Identifiziere konkrete Fälle:
- ORM-/DB-spezifische Typen im Interface
- Raw HTTP-Status-Codes oder Exception-Typen in der UI
- Unstrukturierte LLM-Rohantworten in DB-Spalten
- Plattform-spezifische APIs direkt in Business-Hooks
- Zwei Verbindungen auf dieselbe Ressource (Architekturleck)

---

## Phase 2: Abstraktionsschichten-Design / Abstraction Layer Design

### 2.1 Wrapper & Facade-Ermittlung
Welche Wrappers/Facades fehlen? Für jeden Vorschlag:
- Name und Zweck
- TypeScript/Python/Java Interface-Definition
- Konkrete Implementierungen die das Interface erfüllen sollen

### 2.2 Strategische Entkopplungspunkte / Strategic Decoupling Points
Priorisiere die 3–5 wichtigsten Stellen nach:
- Häufigkeit der erwarteten Änderung (hoch = höhere Priorität)
- Anzahl betroffener Module (viele = höhere Priorität)
- Vendor Lock-in Stärke

### 2.3 Interface-Definitionen / Interface Definitions
Erstelle vollständige Interface-Definitionen in der Zielsprache (TypeScript / Python ABC / Java Interface). Muster:

```typescript
// Beispiel: Austauschbarer Vision-Provider
export interface IVisionProvider {
  readonly providerName: string;
  isAvailable(config: ApiKeyConfig): boolean;
  analyze(inputs: AnalysisInput[], prompt: string, config: ApiKeyConfig): Promise<AnalysisResult>;
}
// Konkrete Implementierungen: OpenAIProvider, AnthropicProvider, FallbackProvider
```

---

## Phase 3: Metriken / Metrics

### 3.1 Zyklomatische Komplexität / Cyclomatic Complexity (CC)
`CC = Entscheidungspunkte + 1`

Zähle als Entscheidungspunkt: `if`, `else if`, `for`, `while`, `do-while`, `case`, `catch`, `&&`, `||`, ternärer Operator, `??`.

**Bewertung:**
| CC | Testbarkeit |
|---|---|
| 1–4 | Sehr gut — einfach unit-testbar |
| 5–7 | Gut — testbar mit wenigen Cases |
| 8–10 | Mittel — refactoring empfohlen |
| 11–15 | Schlecht — aufteilen |
| >15 | **Kritisch** — sofortiger Refactoring-Bedarf |

### 3.2 LCOM (Lack of Cohesion of Methods)
`LCOM4`: Anzahl der unverbundenen Komponentengruppen in einer Klasse/Modul.

- **LCOM4 = 1**: Kohärent — alle Methoden teilen Zustand/Daten
- **LCOM4 = 2–3**: Kandidat für Aufspaltung
- **LCOM4 > 3**: **Aufspaltung dringend empfohlen**

### 3.3 Zusammenfassung / Summary Table

| Modul | CC (max) | LCOM4 | I-Index | SoC-Verletzungen | Priorität |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | Hoch/Mittel/Niedrig |

---

## Ausgabeformat / Output Format

Strukturiere die Ausgabe immer so:

1. **Kritische Befunde** (sofortiger Handlungsbedarf) — mit konkreten Code-Beispielen
2. **Hohe Befunde** (nächster Sprint) — mit Interface-Vorschlägen
3. **Mittlere Befunde** (Backlog) — mit kurzer Begründung
4. **Positive Aspekte** — was bereits gut strukturiert ist
5. **Priorisierte Refactoring-Reihenfolge** — Tabelle mit Aufwand und Nutzen

Für jedes Interface immer vollständige TypeScript/Python/Java-Definition, nicht nur den Namen.

---

## Referenzen / References

Detaillierte Checklisten und Beispiele:
- `references/boundary-checklist.md` — Grenzschichten-Checkliste
- `references/interface-templates.md` — Interface-Vorlagen für häufige Muster
- `references/metrics-examples.md` — CC/LCOM Berechnungsbeispiele

---

## Beispiel-Trigger / Example Triggers

- "Führe eine Architekturanalyse durch"
- "Erstelle eine Programmableitung für [System]"
- "Welche Abstraktionsschichten fehlen?"
- "Berechne die zyklomatische Komplexität"
- "Analysiere den Vendor Lock-in"
- "Wo sind die strategischen Entkopplungspunkte?"
- "Perform a program derivation / architecture analysis"
- "What interfaces are missing?"
- "Analyze coupling and cohesion"
