# Professional Piano Fingering Rules

Use this reference for generation, musical review, and explanations. common-fingering-errors.md contains counterexamples. These are paraphrases of accessible full papers and upstream source code; paper texts and tables are not distributed.

## Evidence

- **[P97]** Richard Parncutt, John A. Sloboda, Eric F. Clarke, Matti Raekallio, Peter Desain. *An Ergonomic Model of Keyboard Fingering for Melodic Fragments*. Music Perception 14(4), 1997, 341–382. https://static.uni-graz.at/fileadmin/_Persoenliche_Webseite/parncutt_richard/Pdfs/PaSlClRaDe97_FingeringModel.pdf
  Covers practical/comfortable spans, stretch/compression, movement, weak fingers, key colors, crossings, rhythm, tempo, articulation, register, repetition, and phrase boundaries. Primarily a monophonic legato model; its average adult-male starting spans and exploratory weights are not universal prescriptions.
- **[AK07]** Alia Al Kasimi, Eric Nichols, Christopher Raphael. *A Simple Algorithm for Automatic Generation of Polyphonic Piano Fingerings*. ISMIR 2007, 355–356. https://archives.ismir.net/ismir2007/paper/000355.pdf
  Supports polyphonic hard constraints, vertical chord comfort plus horizontal transitions, and hand-specific comfort zones. The paper does not model substitutions, key-color differences, or automatic hand assignment.
- **[N14]** Eita Nakamura, Nobutaka Ono, Shigeki Sagayama. *Merged-output HMM for Piano Fingering of Both Hands*. ISMIR 2014. https://eita-nakamura.github.io/articles/Nakamura_etal_MergedOutputHMMForPianoFingering_ISMIR2014.pdf
  Supports continuous within-hand/voice dependencies rather than instantaneous pitch splitting; it supplies statistical architecture rather than a teaching rulebook.
- **[N19]** Eita Nakamura, Yasuyuki Saito, Kazuyoshi Yoshii. *Statistical Learning and Estimation of Piano Fingering*. Information Sciences 517, 2020; 2019 preprint: https://arxiv.org/pdf/1904.10237
  Supports multi-note context, systematic individual differences, simultaneous/sustained chord constraints, and evaluation with multiple reasonable answers. Statistical agreement does not equal musical quality; phrase boundaries and inter-hand dependence remain limitations.
- **[PP]** Marco Musy, *PianoPlayer*. https://github.com/marcomusy/pianoplayer
  Engineering baseline for the bundled hand model, movement/time costs, bounded lookahead, and anchors. It is an implementation source rather than a teaching authority; independent-hand, ornament, and crossing limitations remain.

Abstract-only access to *Talking Fingers*, paid books with previews only, and secondhand blog summaries are excluded as formal evidence.

## Priority order

1. Locked user fingers, explicit composer instructions, and established musical intent.
2. Playability and hard constraints.
3. Articulation, voices, sustained notes, and phrase continuity.
4. Relaxed shapes, movement, and preparation.
5. Repeated-pattern consistency.
6. General preferences for weak fingers, black keys, and conventional patterns.

Lower priorities cannot override higher ones. Optimize a repeatable complete phrase, not isolated minimum effort. [P97][N19]

## A. Hard constraints and reviewed connections

**A1 — One finger, one simultaneous key.** Distinct simultaneous keys in one hand need distinct fingers. Enforced by generation and validation. [AK07][N19]

**A2 — Ordered chord fingers.** Ascending pitches normally use increasing RH fingers and decreasing LH fingers. Avoid crossed shapes. Enforced by generation and validation. [AK07][N19]

**A3 — Practical reach.** Reject candidates beyond MinPrac/MaxPrac before scoring comfort. Adapt span to hand size and ability. XXS–XXL presets are supported. [P97][AK07]

**A4 — Sustained occupation.** A finger holding a key cannot concurrently play another. Preserve fingers on ties unless a reviewed substitution is needed. Identified tie_group continuity is enforced; other cross-event sustained occupations still require review. A substitution needs explicit metadata and verified evidence. [AK07][N19]

**A5 — Connected different pitches.** Avoid unexplained reuse of one finger for finger-legato attacks. Use adjacent fingers, a prepared crossing, or repositioning. Staccato, pedal connection, phrase breaks, and special tone intentions may justify exceptions. Validator warnings require musical review. [P97]

## B. Context-sensitive preferences

**B1 — Match interval and finger span.** Avoid spreading a small interval or squeezing a large interval into weak adjacent fingers. Dyad defaults are seconds adjacent, thirds RH 1–3/LH 3–1, fourths 1–4, and fifths/wider 1–5/5–1. Key geometry, voices, and surrounding notes can override defaults with explanation. Basic semitone-distance choice is implemented; context still matters. [P97][AK07]

**B2 — Penalize both stretch and compression.** Reachable does not mean comfortable for repetition. Non-thumb pairs are particularly sensitive to crowding and stretch. Maximum hand span and movement costs are implemented; detailed per-pair comfort zones require review. [P97][AK07]

**B3 — Minimize unnecessary repositioning.** Compare number/distance of shifts and preparation at the landing. A locally convenient finger must not create the next beat's avoidable leap. Bounded lookahead and review implement this partially. [P97][PP]

**B4 — Use multi-note context.** Consider at least three events and see beyond turning points in fast runs, arpeggios, and crossings. Core lookahead supports multiple events; the production default is four, with reviewed 5–7-event candidates. [N19][PP]

**B5 — Natural stepwise sequences.** Prefer adjacent fingers unless that sequence would strand the hand, exhaust finger 5, or spoil a crossing. Algorithm costs and review apply. [P97]

**B6 — Crossing direction and key height.** Thumb crossings are not categorically forbidden. White/black transitions differ; avoid a crowded thumb landing on a black key in an unfavorable direction. Pedal or speed may justify exceptions. Basic key-color/crossing costs are implemented; complex combinations need review. [P97][AK07]

**B7 — Weak-finger preferences serve the music.** Consider 4/5 independence and 3–4–5 coordination without banning them. Accent, voicing, stability, and tempo can favor a particular finger. Tempo/accent adaptation remains a review task. [P97]

**B8 — Repeated and transposed patterns.** Preserve mappings when interval structure, key shape, and later context agree. Explain changes from the complete group. Identical-measure consistency is implemented; section-level pattern recognition remains incomplete. [P97]

**B9 — Shift at appropriate boundaries.** Favor rests, articulation breaks, phrase boundaries, structural accents, or pedal coverage. Legato and staccato may need different solutions. Review the score rather than deciding by distance alone. [P97][N19]

**B10 — Vertical and horizontal chord costs.** Score internal interval comfort and transitions to adjacent chords together. Stable outer-bass/dyad connections are checked; larger chords, sustained voices, and complete harmonic transitions still need review. [AK07][N19]

**B11 — Preserve hand/voice continuity.** Do not split hands by middle C or an instantaneous pitch boundary. Respect voice, rhythm, and movement continuity. Input staff/voice routing is primary; redistribution requires review. [N14][N19]

**B12 — Individual and editorial alternatives.** Preserve locked anchors, hand size, skill, tempo, and user preferences. Professionals can choose different playable fingers. Provide alternatives/review status where uncertain. Hand presets and locked anchors are implemented; interpretive alternatives need explanation. [P97][AK07][N19][PP]

**B13 — Complete LH arpeggio landing.** Ordinary broken triads can use 5–3–2. A wide lower skip followed by a minor third, or a diminished 3+3 cell immediately resetting to the bass, often favors 5–3–1. Apply only to the guarded complete context; other patterns remain solver/review decisions. Implemented with transposed regressions. [P97][PP]

**B14 — Held lower note, leap, then descent.** For the guarded RH context of a held lower note followed across a barline by a fourth-or-larger leap and three descending steps in one bar, favor centered 4–3–2 rather than edge 5–4–3. Do not apply to ordinary scales, short detached attacks, or locked anchors. Implemented with regressions. [P97][N19][PP]

**B15 — Held-start descending tetrachord.** For a same-measure RH four-note phrase beginning with a dotted-quarter-or-longer value and descending within a seventh, consider 4–3–2–1. Exclude equal-duration scale fragments, wider spans, crossed voices, and locked anchors. Implemented for the guarded shape. [P97][N19][PP]

**B16 — Complete arpeggio/arch contour.** A same-measure RH third–third–fourth arpeggio closing an octave favors 1–2–3–5. A seven-note, strictly mirrored arch rising in 2–4-semitone steps favors 1–2–3–5–3–2–1. Do not force arbitrary contours into these patterns; retain span/rhythm/voice/anchor guards. Implemented with regressions. [P97][N19][PP]

**B17 — Slow cross-bar phrase entry.** A new RH phrase after a real rest/voice gap, with two long-value notes per measure and a compact descending contour, may favor centered 4–3–1–3 and a following 1–2–1–2 lower-neighbor response. This is a narrow guarded context, not a rule for all descending lines. Implemented with regressions. [P97][N19][PP]

## C. Generation and review

Lock existing fingers, voices, articulation, ties, and coordinate identities. Remove impossible A1–A4 candidates; A5 creates explained warnings. Score local and lookahead preferences. Review complete phrases/patterns for repetition, boundaries, and hand routing. Preserve user anchors and stable alternatives. Explain retained exceptions by articulation, voice, speed, hand size, or later preparation.

## D. Exit checks

- No duplicate simultaneous fingers or crossed chord order.
- Reach suits hand size; small intervals do not mechanically use 1–5.
- Sustained notes, substitutions, and reused fingers match articulation.
- Crossings/shifts are explained by at least three surrounding events.
- Repeated patterns remain consistent unless context changes.
- Shifts fit phrase/rest/articulation/pedal opportunities.
- Chords are comfortable alone and reachable from neighbors.
- Hand transfers preserve voices and avoid conflicts.
- Fast passages penalize unnecessary movement.
- Locked user fingers and individual preferences remain respected.

## E. Implementation boundaries

Phrase recognition, accent, pedal, articulation, section similarity, and cross-hand redistribution are not fully integrated into one optimizer. The host must review these against the complete score and distinguish algorithm enforcement from musical review.
