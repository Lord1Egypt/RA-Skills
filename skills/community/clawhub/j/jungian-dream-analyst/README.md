# Jungian Dream Analyst

A Claude skill that interprets dreams through the lens of Analytical Psychology. Rejects generic symbol dictionaries in favor of Amplification — expanding symbols through personal associations and collective archetypes to reveal the unconscious message the dream is trying to deliver.

---

## What it does

- **Four-Phase Analysis** — Structures every dream through Exposition, Development, Peripeteia (turning point), and Lysis (resolution or refusal to resolve)
- **Archetypal Detection** — Identifies Shadow, Anima/Animus, Wise Old Man, Great Mother, Self, and Hero patterns from dream imagery
- **Big Dream Flagging** — Detects numinous/collective dreams (cosmic imagery, god figures, mandalas) and treats them with the appropriate weight
- **Active Imagination Protocol** — Generates a step-by-step waking practice to re-enter dream scenes and dialogue with archetypal figures
- **Symbol Amplification** — Guides the dreamer through personal and archetypal layers of each symbol without imposing meaning
- **Compensation Analysis** — Identifies how the dream balances the dreamer's conscious one-sidedness

---

## Files

```
jungian-dream-analyst/
├── SKILL.md                              # Main skill instructions
├── scripts/
│   ├── synthesis_engine.py               # Structures dream data into four-phase Jungian report
│   └── active_imagination_prompter.py    # Generates Active Imagination & symbol meditation protocols
└── references/
    └── methodology_summary.md            # Full methodology: Dream structure, Archetypal Taxonomy,
                                          # Symbolic Motifs, Analyst's Stance
```

---

## Installation

1. Download `jungian-dream-analyst.skill`
2. Go to Claude.ai → Settings → Skills
3. Upload the `.skill` file

---

## Usage

Once installed, trigger with phrases like:

- "I had a strange dream last night..."
- "What does it mean to dream about [symbol]?"
- "I keep having a recurring nightmare about..."
- "Can you analyze this dream for me?"
- "I dreamed about my shadow / a dark figure / a wise old man"
- "Help me do active imagination with a figure from my dream"

---

## Example output

**Input dream:** *"I'm in an old library with no exits. A dark figure is burning the books. I find a golden key hidden inside one of them."*

**`synthesis_engine.py` output:**
```
Dream Type: Little Dream (Personal)
Interpretation Level: Subjective

EXPOSITION: Old library with no exits
PERIPETEIA: Dark figure burning the books
LYSIS: Discovery of a golden key inside a hollowed book

ARCHETYPAL HITS:
  • Dark figure → Shadow
  • Golden key → Self

AMPLIFICATION MAP:
  Symbol: Dark figure
    Personal: [Ask dreamer: What does this figure mean to you personally?]
    Archetypal: [Shadow — repressed vitality, unacknowledged potential]

  Symbol: Golden key
    Personal: [Ask dreamer: What does a key represent to you?]
    Archetypal: [Self — access to hidden wholeness; transitional object]
```

**Active Imagination protocol** generated for "The Shadow" figure — includes 5-step guided protocol with ethical commitment step.

---

## Core Archetypal Frameworks

| Archetype | Dream Signals |
|---|---|
| **Shadow** | Dark figures, pursuers, doppelgängers, villains |
| **Anima** | Beautiful/threatening women, muses, sirens |
| **Animus** | Authority figures, heroes, inner critics |
| **Wise Old Man** | Mentors, sages, mysterious strangers |
| **Great Mother** | Grandmothers, nature, caves, oceans |
| **Self** | Mandalas, circles, gold, divine figures |
| **Hero** | Quests, battles, threshold crossings |

---

## Key Principles

**Amplification over association** — Unlike Freudian free association (which leaps *away* from the image), this skill stays *with* the image, enriching it from the dreamer's personal world and from mythology, religion, and folklore.

**Subjective level by default** — Every figure in the dream is treated as an aspect of the dreamer's own psyche unless there is a compelling reason to interpret it as a real external person.

**Compensation** — The dream corrects the one-sidedness of the conscious mind. A rigid intellectual who dreams of chaos is not being warned — they are being balanced.

**Active Imagination is not passive** — The protocol requires an ethical commitment step: one concrete real-world action to honor what the unconscious revealed. Without this, the work stays inflation.

---

## Cautions

- Active Imagination is psychologically significant work. The protocol includes a caution not to engage during acute emotional crisis.
- This skill is a reflective and educational tool — it is not a replacement for professional psychotherapy or clinical analysis.
- Big Dreams (numinous, collective) are flagged explicitly and handled with appropriate gravity.

---

## Built with

[Claude Skills](https://claude.ai) · Python · C.G. Jung's Analytical Psychology
