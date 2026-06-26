# Humanizer-DE – Session-Log

> **Sessions:** 46 (Skill-Bau) + 47 (Phase 4 – Tests & Kalibrierung) + 196 (Cleanup, Morphologie & v1.1.0) + 209 (Gedankenstrich-Erkennung & v1.2.0)
> **Datum:** 05.03.2026 (erstellt), 07.04.2026 (aktualisiert)
> **Gesamtumfang:** 10 Dateien, ~2.300 Zeilen Code/Doku
> **Status:** Phase 1–5 fertig. Auf ClawHub veroeffentlicht (`Tikitackr/humanizer-de`). v1.2.0.
>
> **v1.2.0 Aenderungen (Session 209):**
> - Muster #13 (Gedankenstrich-Seuche) im CLI implementiert: countGedankenstriche()
> - En-Dashes (–) im Fliesstext zaehlen, Code-Bloecke/Inline-Code/QR-Platzhalter filtern
> - Scoring: >3 pro ~250 Woerter = +5 Punkte pro Ueberschreitung, max +25
> - Neuer Abschnitt im Analyse-Report: "GEDANKENSTRICHE" mit Treffer-Anzahl, Dichte und Bewertung
> - Version 1.1.2 → 1.2.0 in _meta.json, SKILL.md, README.md
>
> **v1.1.0 Aenderungen (Session 196):**
> - README geschaerft: Klare Trennung Agent-Modus vs. CLI-Modus
> - Tier-1 Vokabeln synchronisiert (35 → 45, jetzt identisch mit vokabeln.md)
> - Fix-Befehl: Morphologisch korrekte Ersetzung (Adjektiv-/Substantiv-Suffixe)
> - Fix-Befehl: .bak-Backup vor Ueberschreiben
> - TIER1-Array um Wortart-Feld erweitert (adj/noun/verb/adv)
> - Chatbot-Artefakte in vokabeln.md dokumentiert
> - statistische-signale.md: "4 Signale" → "5 Signale" korrigiert, Report-Beispiel ergaenzt
> - SKILL.md: Kapitelverweise und Dashboard-Links aktualisiert
> - SESSION-LOG: Tier-2-Bug als gefixt markiert, Zahlen aktualisiert
> - _meta.json: Version 1.0.1 → 1.1.0, Description aktualisiert
> - Morphologische Ersetzung im Fix-Befehl: Adjektiv-Suffixe, Substantiv-Suffixe, Artikel-Korrektur
> - TIER1-Array um Wortart-Feld erweitert (adj/noun/verb/adv) + Genus-Mapping fuer Substantive
> - Artikel-Korrektur mit Praepositions-Heuristik (Dativ-Praep → dem/der, sonst Genitiv)

---

## Was wurde gebaut

Ein kompletter **deutscher KI-Text-Detektor & Humanisierer** als OpenClaw Skill.

### Dateistruktur (10 Dateien)

```
humanizer-de/
├── SKILL.md                              (223 Zeilen) – Hauptlogik, 6 Befehle, 5-Pass-Workflow, Scoring
├── SESSION-LOG.md                        (diese Datei)
├── references/
│   ├── ki-muster.md                      (446 Zeilen) – 24 KI-Muster, Vorher/Nachher, Schweregrade
│   ├── vokabeln.md                       (224 Zeilen) – 3-Tier-System + Co-Occurrence-Sets
│   ├── statistische-signale.md           (316 Zeilen) – 5 Signale mit Formeln + Schwellenwerte
│   ├── personality-injection.md          (259 Zeilen) – 5 Techniken, je 5+ Beispiele
│   ├── examples.md                       (279 Zeilen) – 6 Vorher/Nachher-Transformationen
│   └── stil-layer/
│       ├── basis.md                      (110 Zeilen) – Neutral-Humanisierung
│       └── lesch.md                      (175 Zeilen) – Lesch-Stil (3 Hüte)
└── scripts/
    └── humanize-de.js                    (927 Zeilen) – Node.js CLI-Tool
```

---

## Features im Detail

### Scoring-System (0–100)

**Punkt-Quellen (Score erhöhen):**
| Quelle | Punkte |
|--------|--------|
| Tier-1-Wörter (verboten) | +3 pro Treffer |
| Tier-2-Wörter (Überschuss) | +1 pro Treffer über Limit |
| Verbotene Phrasen | +4 pro Treffer |
| Chatbot-Artefakte | +5 pro Treffer |
| Burstiness < 0.3 (nur ≥20 Sätze) | +10 |
| TTR < 0.5 | +5 |
| CoV < 0.3 | +5 |
| Trigramm-Rate > 0.10 | +5 |
| Flesch-DE 40–50 (KI-Sweetspot) | +3 |
| Co-Occurrence-Alarm (3+ Wörter aus Set) | +5 pro Cluster |

**Bonus-Abzüge (Score senken):**
| Quelle | Bonus |
|--------|-------|
| Einschübe in Klammern | -3 |
| Variabler Satzrhythmus | -5 |
| Kontraktionen (gibt's, ist's) | -2 |
| Konkrete Zahlen/Einheiten | -3 |
| Abschweifungen/Anekdoten | -3 |
| Satzfragmente | -2 |
| Lesch-Layer (optional) | bis -12 |

### Score-Skala
| Score | Bewertung |
|-------|-----------|
| 0–20 | Klingt menschlich |
| 21–40 | Leicht maschinell |
| 41–60 | Gemischt |
| 61–80 | Offensichtlich KI |
| 81–100 | ChatGPT-Standard |

### CLI-Tool (humanize-de.js)

4 Befehle: `score`, `analyze`, `suggest`, `fix`

```bash
node humanize-de.js score   datei.md    # Nur Score
node humanize-de.js analyze datei.md    # Vollständiger Report
node humanize-de.js suggest datei.md    # Ersetzungsvorschläge
node humanize-de.js fix     datei.md    # Automatische Tier-1/Phrasen-Ersetzung
```

**Keine Dependencies** außer `fs` und `path` (kein Netzwerk, kein npm install nötig).

### Funktionen im JS-Script

| Funktion | Zweck |
|----------|-------|
| `splitSentences(text)` | Text in Sätze aufteilen |
| `tokenize(text)` | Text in Wörter aufteilen |
| `findTier1(text)` | Tier-1-Woerter finden (45 Paare, v1.1.0 sync mit vokabeln.md) |
| `findTier2(text)` | Tier-2-Woerter finden (45 Woerter, v1.1-Erweiterung) |
| `findVerbotenePhrasen(text)` | 48 verbotene Phrasen scannen (v1.1-Erweiterung) |
| `findChatbotArtefakte(text)` | 16 Chatbot-Artefakte scannen |
| `calcBurstiness(sentences)` | Burstiness-Score berechnen |
| `calcTTR(text)` | Type-Token-Ratio (100-Wort-Fenster) |
| `calcCoV(sentences)` | Satzlängen-Variationskoeffizient |
| `calcTrigramRepeat(text)` | Trigramm-Wiederholungsrate |
| `countSyllablesDE(word)` | Deutsche Silbenzählung |
| `calcFleschDE(text)` | Flesch-DE Lesbarkeit (deutsche Formel) |
| `findCoOccurrences(text)` | Co-Occurrence-Cluster in Absätzen |
| `calcPersonalityBonus(text)` | Menschliche Stilmittel erkennen |
| `calculateScore(text)` | Gesamtscore berechnen |
| `fixText(text)` | Automatische Tier-1/Phrasen-Ersetzung |
| `formatScore/Analyze/Suggest` | Report-Formatierung |

---

## Test-Ergebnisse (Kalibrierung)

| Text | Score | Bewertung | Flesch-DE | Co-Occurrence |
|------|-------|-----------|-----------|---------------|
| Kapitel 1 (Entwurf) | 19 | Klingt menschlich | 60.3 (ok) | 0 Alarme |
| Vorwort v1 | 6 | Klingt menschlich | – | 0 Alarme |
| Vorwort v2 (Lesch) | 2 | Klingt menschlich | – | 0 Alarme |
| Synthetischer KI-Text | 98 | ChatGPT-Standard | 31.0 (ok) | 3 Alarme (+15) |

**Kalibrierung bestätigt:** Menschliche Texte 2–19, KI-Text 98. Klare Trennung.

### Session 47 – Erweiterte Tests (Phase 4)

| Text | Score | Bewertung |
|------|-------|-----------|
| ChatGPT-1 (KI & Gesellschaft, buzzword-heavy) | 92 | ChatGPT-Standard |
| ChatGPT-2 (Nachhaltigkeit, subtiler) | 42 | Gemischt |
| ChatGPT-3 (Digitale Bildung) | 64 | Offensichtlich KI |
| Mensch-1 (Stefan & Sensoren, Anekdote) | 0 | Klingt menschlich |
| Mensch-2 (Kaffee-Ritual, 26 Sätze) | 8 | Klingt menschlich |
| Mensch-3 (Flohmarkt Berlin) | 0 | Klingt menschlich |

**Anpassung:** Burstiness-Mindest-Satzanzahl von 10 auf 20 erhöht. Signal feuerte bei kurzen Texten (<20 Sätze) immer – egal ob Mensch oder KI. War reine Rauschquelle. Nach Fix: Menschliche Texte 0–8, KI-Texte 42–92.

**ChatGPT-2 bei 42 – Begründung:** Der Text ist subtiler (weniger Buzzwords, mehr Alltagssprache). "Gemischt" ist ein ehrliches Label – nicht jeder ChatGPT-Output ist ein Buzzword-Feuerwerk.

---

## Vergleich mit Original (Operator Humanizer)

Das englische Original (`Kevjade/operator-humanizer`) wurde als ZIP analysiert. Ergebnis:

### Was wir übernommen haben (als Idee, nicht als Code):
- Modulare Dateistruktur (SKILL.md + references/)
- 24-Muster-Konzept → ins Deutsche übersetzt + erweitert
- Tier-System für Vokabeln
- Statistische Signale (Burstiness, TTR, CoV)
- Personality-Injection-Techniken
- Scoring-System (0–100)

### Was wir aus dem Vergleich nachgebaut haben:
1. **examples.md** – 6 deutsche Vorher/Nachher-Transformationen (Original hatte 5 englische)
2. **Flesch-DE (Signal 5)** – Deutsche Lesbarkeitsformel (Original hatte englische Flesch-Kincaid)
3. **Co-Occurrence-Sets** – 5 Wortgruppen-Cluster (Original hatte 6 englische Sets)

### Was wir bewusst NICHT übernommen haben:
- **Strategic Misspellings** – Im Deutschen nicht sinnvoll (Duden-Regel)
- **Curly Quotes** – Im Deutschen irrelevant (wir nutzen „Anführungszeichen")
- Keinen Code aus dem Original
- Keine Unicode-Steuerzeichen

---

## Erledigte Phasen (aus STARTBEFEHL-HUMANIZER.md)

### ✅ Phase 1: Kern-Dateien (komplett)
- [x] SKILL.md
- [x] references/ki-muster.md
- [x] references/vokabeln.md
- [x] references/statistische-signale.md
- [x] references/personality-injection.md

### ✅ Phase 2: Stil-Layer (komplett)
- [x] references/stil-layer/basis.md
- [x] references/stil-layer/lesch.md

### ✅ Phase 3: CLI-Tool (komplett)
- [x] scripts/humanize-de.js (inkl. Flesch-DE + Co-Occurrence)

### ✅ Phase 3b: Vergleich mit Original (komplett)
- [x] examples.md hinzugefügt
- [x] Flesch-DE (Signal 5) integriert
- [x] Co-Occurrence-Sets integriert
- [x] Re-Test und Kalibrierung bestätigt

### ✅ Phase 4: Externe Tests & Kalibrierung (ERLEDIGT – Session 47)
- [x] 3 ChatGPT-Texte getestet → 92, 42, 64
- [x] 3 menschliche Texte getestet → 0, 8, 0
- [x] Burstiness-Schwelle angepasst (10 → 20 Sätze)

### ⬜ Phase 5: Veröffentlichung & Integration (OFFEN)
- [ ] Auf ClawHub veröffentlichen unter `OpenClaw/humanizer-de`
- [ ] `_meta.json` erstellen (Name, Version, Autor, Description)
- [ ] README für ClawHub schreiben
- [ ] QR-Code `HUMANIZER-INSTALL` im QR-Code-Plan ergänzen
- [ ] STARTBEFEHL-BUCH.md updaten: Humanizer als neues Asset
- [ ] Überarbeitungs-Notizen ergänzen

---

## Bekannte Einschraenkungen

1. **Burstiness-Berechnung** liefert manchmal negative Werte (z.B. -0.240 bei Kapitel 1). Mathematisch korrekt per Formel, aber ungewoehnlich. **Fix Session 47:** Mindest-Satzanzahl auf 20 erhoeht – bei kurzen Texten wird das Signal jetzt uebersprungen.
2. ~~**Tier-2-Zaehlung** zaehlte jedes Vorkommen als Ueberschuss, statt das Limit von 1 pro 500 Woerter zu beruecksichtigen.~~ **Gefixt (v1.1):** `findTier2()` prueft jetzt korrekt `count > maxAllowed` und zaehlt nur Ueberschuss-Treffer.
3. **Muster-Scan (24 KI-Muster)** ist nur in der SKILL.md als Workflow dokumentiert, NICHT im JS-Script implementiert. Das ist **by design**: Die 24-Muster-Erkennung braucht semantisches Verstaendnis und laeuft ueber den OpenClaw-Agent. Das CLI-Tool ist ein regelbasiertes Subset. README.md dokumentiert diese Trennung seit v1.1.0.
4. **Fix-Befehl** ersetzt Tier-1-Woerter (morphologisch korrekt) und verbotene Phrasen. Kein Rewriting ganzer Saetze. **Seit v1.1.0:** Morphologische Ersetzung mit 3 Ebenen: (a) Adjektiv-Suffixe -e/-en/-em/-er/-es werden aufs Ersatzwort uebertragen. (b) Substantiv-Suffixe (Genitiv-s, Plural) werden intelligent gehandhabt (kein doppeltes -s bei "Basis" etc.). (c) Artikel-Korrektur bei Genus-Wechsel mit Praepositions-Heuristik fuer Dativ/Genitiv-Unterscheidung. Erstellt automatisch ein `.bak`-Backup vor dem Ueberschreiben. **Bekannte Einschraenkungen:** (1) Komposita mit Bindestrich ("KI-Landschaft") → Artikel-Suche findet Artikel manchmal nicht. (2) Phrasen-Ersetzungen ("Meilenstein" → "wichtiger Schritt") → Gross/Kleinschreibung des Adjektivs im Ersatz nicht immer korrekt.
5. **Tier-3 nicht im CLI.** Reference-Dateien: 45 Tier-1, 46 Tier-2, 34 Tier-3, 48 Phrasen. CLI (v1.1.0): 45 Tier-1, 45 Tier-2, 48 Phrasen + 16 Chatbot-Artefakte. Tier-3 nur im Agent-Modus (braucht Kontext-Verstaendnis).

---

## Nächster Schritt im neuen Chat

```
Lies STARTBEFEHL-HUMANIZER.md und dann humanizer-de/SESSION-LOG.md.
Phase 1–4 sind fertig. Mach weiter mit Phase 5 (Veröffentlichung & Integration).
Erste Aufgabe: README.md für ClawHub schreiben.
```
