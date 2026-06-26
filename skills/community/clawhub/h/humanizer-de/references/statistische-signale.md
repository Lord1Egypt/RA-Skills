# Statistische Signale – KI-Erkennung durch Textstatistik

> Fuenf messbare Signale die zwischen menschlichem und KI-generiertem Text unterscheiden.
> Jedes Signal hat: Formel, Schwellenwerte, Beispielberechnung, Interpretation.

---

## Warum Statistik?

Vokabeln und Muster kann eine gute KI vermeiden. Aber die statistische Struktur eines Textes ist schwerer zu fälschen. Menschen schreiben in Schüben: mal kurze Sätze, mal lange. KI schreibt gleichmäßig. Das lässt sich messen.

---

## Signal 1: Burstiness

**Was es misst:** Wie ungleichmäßig die Satzlängen im Text verteilt sind. Menschen schreiben in "Bursts" – drei kurze Sätze, dann ein langer, dann ein mittlerer. KI produziert gleichmäßige Sätze.

### Formel

```
B = (σ_τ - μ_τ) / (σ_τ + μ_τ)

Wobei:
  τ = Vektor der Satzlängen (in Wörtern)
  μ_τ = Mittelwert der Satzlängen
  σ_τ = Standardabweichung der Satzlängen
```

### Schwellenwerte

| Burstiness | Interpretation | Punkte |
|-----------|----------------|--------|
| 0.5 – 1.0 | Menschlich: Starke Variation, natürlicher Rhythmus | 0 |
| 0.3 – 0.5 | Grenzbereich: Leichte Variation | 0 |
| 0.1 – 0.3 | KI-typisch: Zu gleichmäßig | +10 |
| < 0.1 | Stark KI: Fast roboterhaft gleichmäßig | +10 |

### Beispielberechnung

**Text (5 Sätze):**
> "OpenClaw routet Anfragen. Das ist der Kern. Aber wie genau funktioniert das, wenn drei verschiedene Modelle gleichzeitig verfügbar sind und jedes seine eigenen Stärken mitbringt? Einfach. Der Router entscheidet."

**Satzlängen (Wörter):** [3, 4, 17, 1, 3]

```
μ = (3 + 4 + 17 + 1 + 3) / 5 = 5.6
σ = √[((3-5.6)² + (4-5.6)² + (17-5.6)² + (1-5.6)² + (3-5.6)²) / 5]
σ = √[(6.76 + 2.56 + 129.96 + 21.16 + 6.76) / 5]
σ = √[33.44] = 5.78

B = (5.78 - 5.6) / (5.78 + 5.6) = 0.18 / 11.38 = 0.016
```

Hmm, das ist niedrig. Aber: Bei nur 5 Sätzen ist die Stichprobe zu klein. Burstiness braucht mindestens 20 Sätze für zuverlässige Werte. Bei kürzeren Texten liefert die Formel fast immer negative Werte – egal ob Mensch oder Maschine.

**Minimum:** 20 Sätze. Bei weniger: Signal überspringen.

---

## Signal 2: Type-Token-Ratio (TTR)

**Was es misst:** Wortschatz-Vielfalt. Wie viele verschiedene Wörter verwendet werden im Verhältnis zur Gesamtzahl. KI wiederholt Wörter häufiger als Menschen.

### Formel

```
TTR = |V| / N

Wobei:
  V = Menge der einzigartigen Tokens (Types)
  N = Gesamtanzahl Tokens

Berechnung: Pro 100-Wort-Fenster (gleitend), dann Mittelwert.
```

### Warum 100-Wort-Fenster?

TTR sinkt natürlich mit der Textlänge (längere Texte wiederholen zwangsläufig mehr Wörter). Deshalb messen wir in festen Fenstern und mitteln.

### Schwellenwerte

| TTR | Interpretation | Punkte |
|-----|----------------|--------|
| 0.65 – 0.80 | Menschlich: Reicher Wortschatz | 0 |
| 0.50 – 0.65 | Normal: Ausreichende Variation | 0 |
| 0.35 – 0.50 | KI-typisch: Eingeschränkter Wortschatz | +5 |
| < 0.35 | Stark KI: Sehr repetitiv | +5 |

### Beispielberechnung

**100-Wort-Fenster (gekürzt auf 20 Wörter für Demo):**
> "Der Agent verarbeitet die Anfrage und der Agent leitet die Anfrage weiter und der Agent liefert das Ergebnis"

**Tokens:** [der, agent, verarbeitet, die, anfrage, und, der, agent, leitet, die, anfrage, weiter, und, der, agent, liefert, das, ergebnis]
**N** = 18
**V** = {der, agent, verarbeitet, die, anfrage, und, leitet, weiter, liefert, das, ergebnis} = 11

```
TTR = 11 / 18 = 0.61
```

Das ist grenzwertig. "Agent" 3x, "der" 3x, "die" 2x, "anfrage" 2x – die Wiederholungen ziehen den Wert runter.

### Hinweise

- **Stoppwörter:** "der", "die", "das", "und", "ist" werden NICHT herausgefiltert. Sie sind Teil des natürlichen Rhythmus.
- **Groß/Klein:** Alles wird lowercase für die Zählung.
- **Satzzeichen:** Werden entfernt vor der Zählung.
- **Komposita:** "Sprachmodell" und "Sprachmodelle" zählen als zwei Types (keine Stemming).

---

## Signal 3: Satzlängen-Variation (CoV)

**Was es misst:** Wie stark die Satzlängen variieren. Der Variationskoeffizient (Coefficient of Variation) normalisiert die Standardabweichung durch den Mittelwert. Menschen variieren stark, KI ist monoton.

### Formel

```
CoV = σ_L / μ_L

Wobei:
  L = Vektor der Satzlängen (in Wörtern)
  μ_L = Mittelwert der Satzlängen
  σ_L = Standardabweichung der Satzlängen
```

### Schwellenwerte

| CoV | Interpretation | Punkte |
|-----|----------------|--------|
| > 0.6 | Sehr menschlich: Starke Satzlängen-Variation | 0 |
| 0.4 – 0.6 | Menschlich: Normale Variation | 0 |
| 0.3 – 0.4 | Grenzbereich | 0 |
| < 0.3 | KI-typisch: Zu gleichmäßige Sätze | +5 |

### Beispielberechnung

**KI-typischer Text (10 Sätze):**
Satzlängen: [14, 16, 15, 13, 16, 14, 15, 14, 16, 15]

```
μ = 14.8
σ = √[Varianz] = √[((14-14.8)² + (16-14.8)² + ... ) / 10] ≈ 0.98
CoV = 0.98 / 14.8 = 0.066
```

CoV von 0.066 – extrem niedrig. Alle Sätze sind fast gleich lang. Klares KI-Signal.

**Menschlicher Text (10 Sätze):**
Satzlängen: [3, 22, 8, 5, 31, 2, 14, 7, 19, 4]

```
μ = 11.5
σ ≈ 9.6
CoV = 9.6 / 11.5 = 0.83
```

CoV von 0.83 – hohe Variation. Kurze und lange Sätze wechseln sich ab. Menschlich.

### Unterschied zu Burstiness

- **CoV** misst die *Menge* der Variation (wie stark schwanken die Satzlängen insgesamt?)
- **Burstiness** misst die *Ungleichmäßigkeit* der Variation (gibt es Cluster von kurzen/langen Sätzen?)

Beide zusammen geben ein besseres Bild als jedes Signal allein.

---

## Signal 4: Trigramm-Wiederholung

**Was es misst:** Wie oft sich 3-Wort-Sequenzen wiederholen. KI recycelt bestimmte Phrasenmuster. "in der Lage", "auf der anderen Seite", "es ist wichtig" – diese Trigramme tauchen bei KI häufiger auf.

### Formel

```
TR = R / T

Wobei:
  T = Gesamtanzahl der Trigramme im Text
  R = Anzahl der Trigramme die mehr als einmal vorkommen

Ein Trigramm = 3 aufeinanderfolgende Wörter (lowercase, ohne Satzzeichen).
```

### Schwellenwerte

| Trigramm-Rate | Interpretation | Punkte |
|---------------|----------------|--------|
| < 0.03 | Menschlich: Kaum Wiederholung | 0 |
| 0.03 – 0.05 | Normal | 0 |
| 0.05 – 0.10 | Grenzbereich: Etwas repetitiv | 0 |
| > 0.10 | KI-typisch: Deutliche Phrasen-Wiederholung | +5 |

### Beispielberechnung

**Text:**
> "Es ist wichtig zu verstehen, dass KI-Modelle auf der Grundlage von Daten arbeiten. Es ist wichtig, dass die Daten sauber sind. Auf der Grundlage dieser Erkenntnis entwickeln wir das System."

**Trigramme (Auswahl):**
- "es ist wichtig" → 2x
- "ist wichtig zu" → 1x
- "wichtig zu verstehen" → 1x
- "auf der grundlage" → 2x
- "der grundlage von" → 1x
- ... (insgesamt ~25 Trigramme)

**Wiederholte Trigramme:** 2 ("es ist wichtig", "auf der grundlage")

```
TR = 2 / 25 = 0.08
```

0.08 – Grenzbereich, aber bei einem so kurzen Text schon auffällig.

### Hinweise

- **Stoppwort-Trigramme:** "in der die", "und die von" – werden MITGEZÄHLT. KI nutzt diese Muster häufiger.
- **Satzgrenzen:** Trigramme gehen NICHT über Satzgrenzen hinweg.
- **Minimum:** Mindestens 100 Wörter für zuverlässige Werte.

---

## Signal 5: Lesbarkeit (Flesch-DE)

**Was es misst:** Wie leicht ein Text zu lesen ist. KI-Text landet typischerweise in einem mittleren Lesbarkeitsbereich (Flesch 40–60). Menschlicher Text variiert stärker – er ist entweder einfacher (Blog, Sachbuch) oder komplexer (Fachtext, Jura).

### Formel (Deutsche Anpassung)

Die Flesch-Formel für Deutsch verwendet andere Koeffizienten als die englische Version:

```
FRE_DE = 180 - L - (58.5 × S)

Wobei:
  L = durchschnittliche Satzlänge in Wörtern (Wörter / Sätze)
  S = durchschnittliche Silbenanzahl pro Wort (Silben / Wörter)
```

### Schwellenwerte

| Flesch-DE | Interpretation | KI-Verdacht |
|-----------|----------------|-------------|
| 70–100 | Sehr leicht (Kinderbuch, SMS) | Niedrig |
| 50–70 | Leicht (Blog, Sachbuch) | Niedrig |
| 40–50 | KI-Sweetspot | +3 Punkte |
| 30–40 | Schwierig (Fachtext) | Niedrig |
| 0–30 | Sehr schwierig (Jura, Wissenschaft) | Niedrig |

### Warum der KI-Sweetspot?

KI-Modelle sind darauf trainiert, "verständlich aber gebildet" zu schreiben. Das ergibt konsistent mittlere Lesbarkeit. Menschen schreiben entweder einfacher (wenn sie für ein breites Publikum schreiben) oder komplexer (wenn sie Fachleute adressieren). Der Bereich 40–50 ist verdächtig, weil er "zu ausbalanciert" ist.

### Silbenzählung (Deutsch)

Deutsche Silbenzählung ist komplexer als englische:

```
Regeln:
1. Jeder Vokal-Cluster = 1 Silbe (a, e, i, o, u, ä, ö, ü)
2. Diphthonge zählen als 1 Silbe: ei, ai, au, eu, äu, ie
3. Stummes -e am Ende zählt als eigene Silbe
4. Minimum: 1 Silbe pro Wort
```

### Beispielberechnung

**Text (3 Sätze):**
> "OpenClaw routet Anfragen automatisch. Das spart Zeit. Die Architektur wächst mit deinen Anforderungen."

**Wörter:** 12 | **Sätze:** 3 | **Silben:** ~22

```
L = 12 / 3 = 4.0
S = 22 / 12 = 1.83
FRE_DE = 180 - 4.0 - (58.5 × 1.83) = 180 - 4 - 107.1 = 68.9
```

Flesch 68.9 – leicht lesbar, typisch für Sachbuch. Kein KI-Verdacht.

---

## Gesamt-Statistik-Score

Die fuenf Signale addieren sich zum statistischen Teil des Gesamt-Scores:

| Signal | Max-Punkte |
|--------|-----------|
| Burstiness < 0.3 | +10 |
| TTR < 0.5 | +5 |
| CoV < 0.3 | +5 |
| Trigramm-Rate > 0.10 | +5 |
| Flesch-DE 40–50 (KI-Sweetspot) | +3 |
| **Maximum aus Statistik** | **+28** |

### Report-Format für Statistik

```
  STATISTIK
  ─────────────────────────────
  Burstiness:       0.42  ✓ menschlich (>0.3)    [nur bei >=20 Saetzen]
  TTR:              0.58  ✓ menschlich (>0.5)
  Satzlaengen-CoV:  0.21  ✗ KI-typisch (<0.3)    → +5
  Trigramm-Rate:    0.04  ✓ normal (<0.10)
  Flesch-DE:        45.2  ✗ KI-Sweetspot (40-50)  → +3

  Statistik-Score: +8
```

---

## Einschränkungen

1. **Kurze Texte (<100 Wörter):** Statistische Signale sind unzuverlässig. Warnung ausgeben, aber trotzdem berechnen.
2. **Fachtexte:** Juristische, medizinische und wissenschaftliche Texte haben von Natur aus niedrigere Burstiness und CoV. Das ist okay – der Muster-Scan fängt die KI-Signale dort.
3. **Listen-Texte:** Texte mit vielen Aufzählungen haben verzerrte Satzlängen. Statistik mit Vorsicht interpretieren.
4. **Übersetzungen:** Übersetzte Texte können KI-ähnliche Statistikwerte haben ohne KI zu sein. Im Report erwähnen.
