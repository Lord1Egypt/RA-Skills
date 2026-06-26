---
name: guitar-chord
version: 1.1.0
description: |
  Guitar chord toolkit with chord identification, chord diagrams, capo calculation, and more.
  Features:
  - Identify chord from notes (reverse lookup)
  - Look up notes and diagrams from chord name
  - View chord inversions
  - View drop2 voicings
  - View scales and scale diagrams
  - Capo transposition calculator
---

# Guitar Chord Tool

## 1. Forward Lookup (Chord Name → Notes)

```bash
python3 chord_identifier.py <chord_name>
```

Example:
```
python3 chord_identifier.py Cmaj7
→ **Cmaj7**
  Notes: C, E, G, B
```

## 2. With Chord Diagram

```bash
python3 chord_identifier.py <chord_name> --diagram
```

## 3. Reverse Lookup (Notes → Chord Name)

```bash
python3 chord_identifier.py --identify <note1> [note2] ...
```

Example:
```
python3 chord_identifier.py --identify C E G B
→ Result:
  • Cmaj7
```

## 4. Chord Inversions

```bash
python3 chord_identifier.py --inversion <chord_name>
```

Example:
```
python3 chord_identifier.py --inversion C7
→ **C7** inversions:
  Root: C, E, G, A#
  1st: E, G, A#, C
  2nd: G, A#, C, E
  3rd: A#, C, E, G
```

## 5. Drop2 Voicings

```bash
python3 chord_identifier.py --drop2 <chord_name>
```

Drop2 是一种常见的吉他扩展和弦 voicing：把七和弦的第二高音（纯五度）降一个八度，产生更"开阔"的音色。

Example:
```
python3 chord_identifier.py --drop2 Cmaj7
→ **Cmaj7 大七** Drop2 Voicings:
  原位: C, E, G, B
  Drop2: C, G, B, E
  
  常见 Guitar Voicings:
  Root pos.: X-3-2-1-1-0 → C,G,B,E
  1st inv.: X-X-0-2-1-0 → E,C,G,B
  ...
```

## 6. Scale Lookup

```bash
python3 chord_identifier.py --scale "<scale>"
python3 chord_identifier.py --scale "<scale>" --diagram
```

Supported scales:
- `major`, `minor`, `harmonic_minor`, `melodic_minor`
- `pentatonic_major`, `pentatonic_minor`, `blues`
- `dorian`, `phrygian`, `lydian`, `mixolydian`, `locrian`

Example:
```
python3 chord_identifier.py --scale "C major"
→ **C Major**
  Scale: C, D, E, F, G, A, B
```

## 7. Capo Calculator

Formula: **Actual Pitch = Open Chord Pitch + Capo Fret**

Quick Reference:
| Chord | 1st | 2nd | 3rd | 4th |
|-------|-----|-----|-----|-----|
| C | C#/Db | D | D#/Eb | E |
| G | G#/Ab | A | A#/Bb | C |
| Am | A#/Bb | B | C | C#/Db |

## Supported Chord Types

- **Triads**: major, minor, diminished, augmented, sus2, sus4
- **Sevenths**: maj7, 7, m7, m7b5, dim7, aug7, maj7#5, 7#5, 7b5, mMaj7
- **Ninths**: maj9, 9, m9

## Note Formats

Supports:
- Natural: C, D, E, F, G, A, B
- Sharps: C#, D#, F#, G#, A#
- Flats: Db, Eb, Gb, Ab, Bb
- Symbols: ♯ (sharp), ♭ (flat)
- Case insensitive
