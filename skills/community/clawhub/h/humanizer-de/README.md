# Humanizer-DE

**Erster deutscher KI-Text-Detektor fuer OpenClaw.**

> Version 1.2.0 · Autor: OpenClaw · Lizenz: MIT · Sprache: Deutsch

Dieser Skill hat **zwei Betriebsarten:**

| Modus | Was passiert | Umfang |
|-------|-------------|--------|
| **Agent-Modus** (SKILL.md) | OpenClaw fuehrt die vollstaendige 5-Durchgangs-Analyse durch | 24 KI-Muster, 125+ Vokabeln in 3 Tiers, 48 Phrasen, 5 Statistik-Signale, Personality Injection, Stil-Layer |
| **CLI-Modus** (humanize-de.js) | Standalone Node.js-Script, laeuft ohne KI | Tier-1/2-Vokabelcheck (90 Woerter), 48 Phrasen, 16 Chatbot-Artefakte, 5 Statistik-Signale, Co-Occurrence-Cluster, Auto-Fix |

Der **Agent-Modus** nutzt Claude als Analysemotor und hat Zugriff auf alle Reference-Dateien – inklusive 24 KI-Schreibmuster-Erkennung und Personality Injection. Das **CLI-Tool** ist ein regelbasiertes Subset fuer schnelle Checks ohne KI-Kosten.

---

## Was macht dieser Skill?

Du gibst ihm einen deutschen Text. Er sagt dir:

1. **Wie stark** der Text nach KI klingt (Score 0–100)
2. **Wo genau** KI-Muster stecken (markiert + erklaert)
3. **Wie du es besser machst** (konkrete Umschreibvorschlaege)

Score 0 = klingt menschlich. Score 100 = klingt wie ChatGPT auf Autopilot.

---

## Installation

Sag deinem OpenClaw:

> *"Installiere den Skill Tikitackr/humanizer-de"*

OpenClaw laedt den Skill herunter und bestaetigt die Installation. Fertig. Kein Terminal, kein manueller Download – alles laeuft ueber den Chat.

Der Skill wird per Chat-Befehl aufgerufen (z.B. "Check diesen Text") – er laeuft nicht automatisch im Hintergrund.

---

## Befehle

| Befehl | Was passiert |
|--------|-------------|
| `Check diesen Text` | Vollständiger Report: Score + Muster + Vokabeln + Statistik + Vorschläge |
| `Score: [Text]` | Nur der Score (0–100) mit Kurzeinschätzung |
| `Was klingt hier nach KI?` | Nur die problematischen Stellen markiert |
| `Humanisiere das` | Text umschreiben mit Personality Injection (Basis-Stil) |
| `Humanisiere das im Lesch-Stil` | Umschreiben mit Lesch-Layer (Visionär/Mahner/Erklärer) |
| `Mach das menschlicher` | Wie "Humanisiere das" – Synonym |

---

## Was wird analysiert?

### 24 KI-Schreibmuster (nur Agent-Modus)

Der Skill erkennt 24 typische Muster, die KI-generierte deutsche Texte verraten – von Bedeutungsinflation ueber Aufzaehlungs-Sucht bis zu leeren Verstaerkern. Jedes Muster hat einen Schweregrad (HOCH / MITTEL / NIEDRIG) und konkrete Umschreibvorschlaege.

> **Hinweis:** Die 24-Muster-Erkennung laeuft ueber den OpenClaw-Agent (SKILL.md). Das CLI-Tool prueft Vokabeln, Phrasen und Statistik – aber nicht die 24 Muster.

### KI-Vokabeln & Phrasen in 3 Tiers

Die Reference-Datenbank (`references/vokabeln.md`) umfasst 125+ Vokabeln und 48 Phrasen:

- **Tier 1 (VERBOTEN):** 45 Woerter die sofort auffallen ("ermoeglicht", "nahtlos", "massgeblich")
- **Tier 2 (SPARSAM):** 46 Woerter die in Massen okay sind, aber bei Haeufung KI signalisieren (inkl. Nominalstil-Marker wie "Fragestellung", "Zielsetzung")
- **Tier 3 (BEOBACHTEN):** 34 Woerter die nur im Cluster verdaechtig werden (inkl. Anglizismen wie "Benchmark", "Use Case", "Impact")
- **Verbotene Phrasen:** 48 Phrasen die sofort raus muessen ("Es ist wichtig zu beachten", "In der heutigen Welt", "Vor dem Hintergrund")

Das **CLI-Tool** implementiert davon: 45 Tier-1, 45 Tier-2, 48 Phrasen + 16 Chatbot-Artefakte. Tier-3 wird nur im Agent-Modus geprueft.

Plus **7 Co-Occurrence-Sets** – Wort-Cluster die gemeinsam auftreten und KI-Herkunft verraten (inkl. Anglizismen-Cluster und Nominalstil-Cluster). Im CLI und Agent verfuegbar.

### 5 Statistische Signale

| Signal | Was es misst |
|--------|-------------|
| Burstiness | Variation der Satzabstände (KI schreibt gleichmäßig) |
| Type-Token-Ratio | Wortschatz-Vielfalt pro 100-Wort-Fenster |
| Satzlängen-CoV | Variation der Satzlängen (KI = monoton) |
| Trigramm-Wiederholung | Wiederholte 3-Wort-Folgen |
| Flesch-DE | Lesbarkeit (KI-Texte landen oft im Sweetspot 40–50) |

### Personality Injection

5 Techniken machen Texte menschlicher: Einschübe, Rhythmuswechsel, Mini-Abschweifungen, Unsicherheitsmarker und Umgangssprache-Tupfer. Der Skill wählt je nach Kontext (formal vs. locker) die passende Mischung.

### Stil-Layer

- **Basis:** Neutrale Humanisierung ohne besonderen Stil. Funktioniert für jeden Text.
- **Lesch:** Inspiriert vom Erklärstil von Harald Lesch – Tonwechsel (Visionär/Mahner/Erklärer), Analogien, philosophische Anker.

---

## CLI-Tool (Standalone, Subset)

Im Ordner `scripts/` liegt ein Node.js CLI-Tool fuer schnelle Analysen **ohne KI**. Es implementiert:

- **45** Tier-1-Woerter (verboten, +3 Punkte)
- **45** Tier-2-Woerter (sparsam, +1 Punkt ueber Limit von 1x/500 Woerter)
- **48** verbotene Phrasen (+4 Punkte)
- **16** Chatbot-Artefakte (+5 Punkte)
- **5** statistische Signale (Burstiness, TTR, CoV, Trigramm-Rate, Flesch-DE)
- **7** Co-Occurrence-Sets (Cluster-Erkennung)
- **Personality-Bonus** (Abzuege fuer menschliche Stilmittel)

**Nicht im CLI:** 24 KI-Muster-Scan, Tier-3-Vokabeln, Personality Injection, Stil-Layer. Dafuer den Agent-Modus (SKILL.md) nutzen.

```bash
node humanize-de.js score   datei.md    # Nur Score (0-100)
node humanize-de.js analyze datei.md    # Vollstaendiger Report
node humanize-de.js suggest datei.md    # Ersetzungsvorschlaege
node humanize-de.js fix     datei.md    # Auto-Ersetzung (erstellt .bak-Backup)
```

Nur `fs` und `path` als Dependencies – kein Netzwerk, keine externen Pakete.

---

## Kalibrierung

Getestet an 7+ Texten in Session 46–47:

| Texttyp | Score-Bereich | Erwartung | Ergebnis |
|---------|---------------|-----------|----------|
| Menschlich geschrieben | 0–8 | 0–30 | Passt |
| Lesch-Stil (KI-bereinigt) | 2–6 | 0–30 | Passt |
| Subtiler KI-Text | 42 | 30–60 ("Gemischt") | Passt |
| Typischer ChatGPT-Text | 64–92 | 60–100 | Passt |
| Offensichtlicher KI-Text | 98 | 60–100 | Passt |

---

## Dateistruktur

```
humanizer-de/
├── _meta.json                          Skill-Metadaten
├── README.md                           Diese Datei
├── SKILL.md                            Hauptlogik & Workflow
├── references/
│   ├── ki-muster.md                    24 KI-Schreibmuster (deutsch)
│   ├── vokabeln.md                     168 KI-Vokabeln & Phrasen in 3 Tiers
│   ├── statistische-signale.md         5 statistische Signale mit Formeln
│   ├── personality-injection.md        5 Humanisierungs-Techniken
│   ├── examples.md                     6 Vorher/Nachher-Transformationen
│   └── stil-layer/
│       ├── basis.md                    Standard-Humanisierung
│       └── lesch.md                    Lesch-Erweiterung
└── scripts/
    └── humanize-de.js                  Node.js CLI-Tool (960 Zeilen)
```

---

## Teil des OpenClaw-Projekts

Dieser Skill ist eigenständig nutzbar – du brauchst kein Buch und kein Dashboard.

Wenn du mehr willst: Der Skill ist Teil des **OpenClaw Sachbuch-Projekts** ("Agentic Authorship"), das erklärt wie man KI-Agenten baut, betreibt und qualitätssichert. Das Buch nutzt den Humanizer selbst für die eigene Textqualität.

- Dashboard: https://openclaw-buch.de
- Cowan (mobiler Buch-Begleiter): https://openclaw-buch.de/?module=companion

---

## Lizenz

MIT – mach damit was du willst. Wenn du ihn verbesserst, teil es gern auf ClawHub.
