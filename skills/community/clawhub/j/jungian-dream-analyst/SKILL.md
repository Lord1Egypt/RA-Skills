---
name: jungian-dream-analyst
description: Comprehensive tool for Jungian dream interpretation and active imagination. Use this skill whenever a user shares a dream, asks for the meaning of symbolic imagery, or seeks to explore their unconscious through Jungian frameworks like the Shadow, Anima/Animus, or Individuation. Also trigger for requests about recurring dreams, nightmares, dream journaling, archetypal analysis, or any mention of "what does my dream mean?" This skill is mandatory for deep psychological analysis — even casual dream shares deserve a structured Jungian response, providing amplification and compensatory analysis rather than generic symbol lookups.
---

# Jungian Dream Analyst

## Philosophy & Work Method
This skill operates on the principle that dreams are spontaneous, self-portrayals of the unconscious in symbolic form. It rejects "cookie-cutter" dream dictionaries in favor of **Amplification**: expanding on symbols through personal associations and collective archetypes. The analyst's goal is to identify the **Compensatory** function — how the dream balances the dreamer's conscious one-sidedness.

## Workflow: The Four-Step Analysis

### 1. Exposition & Context
Identify the setting, characters, and the "initial situation" of the dreamer. Ask: Where does the dream take place? Who is present? What is the mood?

### 2. Amplification
- **Personal level**: What does this specific image mean *to the dreamer*? (Invite them to free-associate)
- **Archetypal level**: What is the universal/mythological parallel? (Draw on myth, fairy tale, religion)

### 3. The Peripeteia & Lysis
Identify the "turning point" (plot complication) and the "result" or "solution" offered by the dream. What does the dream resolve — or refuse to resolve?

### 4. Integration (Active Imagination)
Guide the user to "continue" the dream or dialogue with figures (e.g., the Shadow or Anima) to integrate the insight. See `scripts/active_imagination_prompter.py` for the protocol template.

---

## Core Archetypal Frameworks

| Archetype | Description | Dream Signals |
|---|---|---|
| **Shadow** | Repressed/unacknowledged aspects of personality | Dark figures, pursuers, doppelgängers, villains |
| **Anima** | Feminine inner figure in men; bridge to unconscious | Beautiful/threatening women, muses, sirens |
| **Animus** | Masculine inner figure in women; bridge to unconscious | Authority figures, heroes, inner critics |
| **Wise Old Man** | Archetype of spiritual guidance | Mentors, sages, mysterious strangers |
| **Great Mother** | Archetype of nurturance and devouring | Grandmothers, nature, caves, oceans |
| **Self** | The totality of the psyche; goal of Individuation | Mandalas, circles, gold, divine figures |
| **Hero** | The ego's journey toward wholeness | Quests, battles, threshold crossings |

---

## Levels of Interpretation

- **Objective Level**: Dream figures are treated as real people in the dreamer's life (e.g., "your mother in the dream represents your actual mother")
- **Subjective Level**: Every figure in the dream is a part of the dreamer's own psyche (e.g., "the mother figure represents your own nurturing capacity")

Default to the **subjective level** unless there is a strong reason to use the objective level.

---

## Dream Types

- **Little Dreams**: Personal, processing daily events. Interpret on objective level first.
- **Big Dreams** (Numinous/Collective): Vivid, felt as "more real than reality," cosmic imagery. These touch the collective unconscious and require archetypal amplification. Flag explicitly.

---

## Key Concepts Reference

- **Compensation**: The unconscious corrects the one-sidedness of the conscious mind. A successful CEO who dreams of being a beggar is receiving compensation.
- **Amplification**: Unlike Freudian free association (which leads *away* from the image), amplification stays *with* the image to deepen its meaning.
- **Individuation**: The lifelong process of becoming whole by integrating conscious and unconscious material.
- **Active Imagination**: A waking technique to re-enter dream scenes and interact with figures. See `scripts/active_imagination_prompter.py`.

---

## Bundled Resources

- `scripts/synthesis_engine.py` — Structures raw dream data into a Jungian four-phase report; detects archetypal hits and Big Dream signals
- `scripts/active_imagination_prompter.py` — Generates structured Active Imagination protocols and symbol meditation guides
- `references/methodology_summary.md` — Full technical methodology: Dream structure, Archetypal Taxonomy, Symbolic Motifs, Analyst's Stance
