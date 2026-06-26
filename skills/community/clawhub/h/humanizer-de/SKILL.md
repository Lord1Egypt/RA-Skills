# Humanizer-DE

**Erster deutscher KI-Text-Detektor für OpenClaw.**

5-Durchgang-Analyse: Erkennt 24 KI-Schreibmuster, flaggt 125+ deutsche KI-Vokabeln in 3 Tiers + 48 Phrasen + 16 Chatbot-Artefakte, misst 5 statistische Signale (Burstiness, TTR, Flesch-DE) und schreibt Texte mit Personality Injection um. Inklusive Lesch-Stil-Layer.

> **Version:** 1.2.0
> **Autor:** OpenClaw
> **Sprache:** Deutsch
> **Lizenz:** MIT
> **ClawHub:** `Tikitackr/humanizer-de`

---

## Was macht dieser Skill?

Du gibst ihm einen deutschen Text. Er sagt dir:
1. **Wie stark** der Text nach KI klingt (Score 0–100)
2. **Wo genau** KI-Muster stecken (markiert + erklärt)
3. **Wie du es besser machst** (konkrete Umschreibvorschläge)

Score 0 = klingt menschlich. Score 100 = klingt wie ChatGPT auf Autopilot.

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

## Workflow (5 Durchgänge)

Wenn ein Text gecheckt wird, durchläuft er 5 Analyse-Schritte. Jeder Schritt hat eine eigene Reference-Datei mit allen Details.

### Durchgang 1: KI-Muster-Scan
**Reference:** `references/ki-muster.md`

Prüfe den Text auf alle 24 KI-Schreibmuster. Für jedes gefundene Muster:
- Markiere die betroffene Stelle
- Nenne das Muster (z.B. "Muster #1: Bedeutungsinflation")
- Zeige Schweregrad: HOCH / MITTEL / NIEDRIG
- Gib einen konkreten Umschreibvorschlag

**Punkte-Vergabe:**
- HOCH-Muster: +5 Punkte pro Treffer
- MITTEL-Muster: +3 Punkte pro Treffer
- NIEDRIG-Muster: +1 Punkt pro Treffer

### Durchgang 2: Vokabel-Check
**Reference:** `references/vokabeln.md`

Scanne den Text auf KI-typische Wörter und Phrasen aus der deutschen KI-Marker-Datenbank.

**Tier-System:**
- **Tier 1 (VERBOTEN):** Jedes Vorkommen = +3 Punkte. Immer ersetzen.
- **Tier 2 (SPARSAM):** Erlaubt max 1x pro 500 Wörter. Jedes Vorkommen über Limit = +1 Punkt.
- **Tier 3 (BEOBACHTEN):** Nur zählen. Wenn Dichte > 3 pro 500 Wörter = +1 Punkt pro überzähligem.
- **Verbotene Phrasen:** Jedes Vorkommen = +4 Punkte. Immer ersetzen.

Für jedes geflaggerte Wort: Zeige das Wort, den Tier, und einen konkreten Ersetzungsvorschlag.

### Durchgang 3: Statistische Analyse
**Reference:** `references/statistische-signale.md`

Berechne fünf statistische Signale:

| Signal | Formel | KI-Alarm wenn |
|--------|--------|---------------|
| Burstiness | B = (σ_τ - μ_τ) / (σ_τ + μ_τ) | B < 0.3 |
| Type-Token-Ratio (TTR) | Unique Tokens / Total Tokens (pro 100-Wort-Fenster) | TTR < 0.5 |
| Satzlängen-Variation (CoV) | σ / μ der Satzlängen in Wörtern | CoV < 0.3 |
| Trigramm-Wiederholung | Wiederholte Trigramme / Gesamt-Trigramme | Rate > 0.10 |
| Flesch-DE (Lesbarkeit) | 180 - L - (58.5 × S) | Flesch 40–50 (KI-Sweetspot) |

**Punkte-Vergabe:**
- Burstiness unter 0.3: +10 Punkte (nur bei ≥20 Sätzen)
- TTR unter 0.5: +5 Punkte
- Satzlängen-CoV unter 0.3: +5 Punkte
- Trigramm-Rate über 0.10: +5 Punkte
- Flesch-DE im KI-Sweetspot (40–50): +3 Punkte

### Durchgang 3b: Co-Occurrence-Check
**Reference:** `references/vokabeln.md` (Abschnitt Co-Occurrence-Sets)

Prüfe ob in einzelnen Absätzen 3+ Wörter aus derselben KI-Wortgruppe auftauchen. 5 Sets definiert (Bedeutungsinflation, Techno-Superlative, Akademisch-Abstrakt, Passiv-Verben, Floskel-Ketten).

**Punkte-Vergabe:**
- Pro Cluster-Alarm (3+ Treffer aus einem Set in einem Absatz): +5 Punkte

### Durchgang 4: Personality-Check
**Reference:** `references/personality-injection.md`

Prüfe ob menschliche Stilmittel vorhanden sind. Wenn ja: Bonus-Abzüge.

**Bonus-Abzüge (reduzieren den Score):**
- Authentische Einschübe in Klammern vorhanden: -3 Punkte
- Satzrhythmus variiert (keine 3+ gleich langen Sätze): -5 Punkte
- Kontraktionen verwendet (gibt's, ist's, hat's): -2 Punkte
- Konkrete Zahlen/Quellen statt vager Aussagen: -3 Punkte
- Echte Abschweifungen/Anekdoten: -3 Punkte
- Satzfragmente (bewusst unvollständig): -2 Punkte

### Durchgang 5: Stil-Layer (optional)
**Reference:** `references/stil-layer/basis.md` oder `references/stil-layer/lesch.md`

Wenn der Benutzer "Humanisiere" oder "Mach menschlicher" sagt:
1. Wende den **Basis-Stil** an (Standard, für alle geeignet)
2. Oder wende den **Lesch-Stil** an (wenn explizit gewünscht)
3. Erstelle eine Vorher/Nachher-Gegenüberstellung

---

## Score-Berechnung

### Gesamt-Score = Rohpunkte - Bonus-Abzüge

**Clamp:** Minimum 0, Maximum 100.

### Score-Skala

| Score | Bewertung | Empfehlung |
|-------|-----------|------------|
| 0–20 | Klingt menschlich | Keine Änderung nötig. Gut gemacht. |
| 21–40 | Leicht maschinell | Ein paar Stellen polieren. Siehe markierte Muster. |
| 41–60 | Gemischt | Überarbeitung empfohlen. Vokabeln ersetzen, Rhythmus variieren. |
| 61–80 | Offensichtlich KI | Deutliche Überarbeitung nötig. Personality Injection einsetzen. |
| 81–100 | ChatGPT-Standard | Komplett umschreiben. Dieser Text besteht keinen KI-Detektor. |

### Report-Format

Wenn der Benutzer einen vollständigen Check will, gib den Report in diesem Format aus:

```
═══════════════════════════════════════════
  HUMANIZER-DE · Analyse-Report
═══════════════════════════════════════════

  SCORE: [XX] / 100  →  [Bewertung]

───────────────────────────────────────────
  1. KI-MUSTER ([Anzahl] gefunden)
───────────────────────────────────────────

  ▸ Muster #X: [Name] (SCHWERE)
    Stelle: "[Zitat aus dem Text]"
    Vorschlag: [Umschreibung]

───────────────────────────────────────────
  2. VOKABEL-CHECK ([Anzahl] geflaggert)
───────────────────────────────────────────

  ▸ "[Wort]" (Tier X) → Vorschlag: "[Ersetzung]"

───────────────────────────────────────────
  3. STATISTIK
───────────────────────────────────────────

  Burstiness:       [Wert] ([menschlich/KI-typisch])
  TTR:              [Wert] ([menschlich/KI-typisch])
  Satzlängen-CoV:   [Wert] ([menschlich/KI-typisch])
  Trigramm-Rate:    [Wert] ([menschlich/KI-typisch])
  Flesch-DE:        [Wert] ([ok/KI-Sweetspot])

  Co-Occurrence:    [Anzahl] Cluster-Alarme

───────────────────────────────────────────
  4. PERSONALITY-BONUS
───────────────────────────────────────────

  [Liste der erkannten menschlichen Stilmittel]
  Bonus: -[X] Punkte

───────────────────────────────────────────
  5. TOP-3-EMPFEHLUNGEN
───────────────────────────────────────────

  1. [Wichtigste Verbesserung]
  2. [Zweitwichtigste]
  3. [Drittwichtigste]

═══════════════════════════════════════════
```

---

## Regeln

1. **Score ehrlich berechnen.** Kein Gefälligkeits-Score. Wenn ein Text nach KI klingt, sag es.
2. **Immer Vorschläge machen.** Nicht nur Probleme zeigen, sondern konkrete Lösungen.
3. **Kontext beachten.** Ein Förderantrag darf formaler sein als ein Blogpost. Passe die Bewertung an.
4. **Deutsch.** Alle Muster, Vokabeln und Vorschläge sind auf Deutsch. Englische Fachbegriffe nur wo nötig.
5. **Kein Netzwerk.** Dieser Skill macht keine HTTP-Calls. Alles funktioniert offline.
6. **Modular.** Stil-Layer sind optional. Der Basis-Check funktioniert für jeden Text.

---

## Reference-Dateien

| Datei | Inhalt |
|-------|--------|
| `references/ki-muster.md` | 24 KI-Schreibmuster mit Beispielen, Schweregrad, Erkennungsregeln |
| `references/vokabeln.md` | 125+ KI-Vokabeln in 3 Tiers + 48 verbotene Phrasen + 16 Chatbot-Artefakte + 7 Co-Occurrence-Cluster + Ersetzungen |
| `references/statistische-signale.md` | Formeln für Burstiness, TTR, CoV, Trigramm-Rate, Flesch-DE + Schwellenwerte |
| `references/personality-injection.md` | 5 Techniken zur Vermenschlichung + Regeln + deutsche Beispiele |
| `references/examples.md` | 6 deutsche Vorher/Nachher-Transformationen (Blogpost, E-Mail, Social Media, Tech Doku, Sachbuch, Förderantrag) |
| `references/stil-layer/basis.md` | Standard-Humanisierung ohne besonderen Stil |
| `references/stil-layer/lesch.md` | Lesch-Stil-Erweiterung (Tonwechsel, Analogien, Lesch-ismen) |

---

## Integration

Dieser Skill funktioniert **eigenständig** – du brauchst kein Buch, kein Dashboard, keinen Cowan.

### Installation

Sag deinem OpenClaw:

> *"Installiere den Skill Tikitackr/humanizer-de"*

### Im OpenClaw-Ökosystem

- **Im Buch:** Kapitel 9 (Agent-Architektur) erklaert die Theorie hinter Skills. Kap 13 zeigt den Humanizer als Praxis-Beispiel.
- **Im Dashboard:** https://openclaw-buch.de
- **In Cowan:** "Hey Cowan, check diesen Text" – per Sprache oder Kamera (OCR).
