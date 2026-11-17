# Common Fingering Errors

Check these after generation and before rendering. Evidence, priorities, and exceptions are in [professional-fingering-rules.md](professional-fingering-rules.md). Prefer relaxed, simple shapes that preserve musical connections.

| Failure | Check or correction |
| --- | --- |
| A plausible fingering is generated for a wrong pitch | Validate staff geometry, clef, and spelling first. Confidence and successful export do not bypass recognition. |
| Adjacent chord heads merge into one note | Enlarge the crop; bind each head, including heads on opposite stem sides. Match digits to visible heads. |
| Equivalent transposed dyads arbitrarily change fingers | Review the whole sequence. Preserve a comfortable mapping unless key geometry, voice connection, reach, or landing changes. |
| A movable fixed dyad is repeatedly refingered | Prefer translating the hand over arbitrary 1–3 → 1–4 → 1–5 changes. |
| A connected scale skips an available finger | Prefer adjacent fingers, such as 5–4 over 5–3, unless later preparation justifies a skip. |
| Different connected pitches reuse one finger | Prepare adjacent fingers, a crossing, or an explained reposition. Detached/nonlegato attacks can differ. |
| Every dyad receives 1–5 | Match finger span to interval: seconds adjacent, thirds often 1–3, fourths 1–4, fifths/wider 1–5; mirror LH order. Context may justify other pairs. |
| Bass and following chord compete for one finger | Check single-to-chord and chord-to-single transitions. An outer LH bass normally prepares 5 → 3–1 for a third. |
| An unverified pattern is copied through repetitions | Verify one full cell before propagating. A wide descending three-note RH figure often favors 5–3–1 over 5–4–1. |
| Repeated accompaniment pitches silently change fingers | Keep the finger by default. Explain rotation, substitution, or preparation using transition metadata. |
| Tied continuations change fingers | Preserve one tie_group/finger. Substitution needs transition_type=substitution, rule_id=A4, exception_reason, and exception_verified=true after review. |
| Immediately repeated single notes silently change fingers | Keep the finger for contiguous attacks without rest/detachment. Do not apply blindly to gapped repetitions or chord members. |
| Bass–dyad–dyad accompaniment has no prepared shape | Review the unit: LH outer bass usually 5, second dyad 2–1, third dyad 3–1. Deviations need reviewed evidence. |
| Five heads produce six digits | Independently count page/measure/hand heads. Stems, beams, barlines, and dots are not notes. Global counts cannot hide local discrepancies. |
| A rest becomes a note and affects the next measure | Verify an open/filled ellipse. Rectangular rests and quarter-rest strokes stay outside notes. Check sparse symbols and recompute affected/next measures after deleting false events. |
| A chord member is inferred from an accompaniment pattern | Locate each real ellipse. Record origin=direct_visual_notehead and chord_member_verified=true. Never create a member from page_y ± a fixed gap or a copied prior chord. |
| Keyboard coordinates reverse pitch order | Compute keyboard_x_cm with keypos_midi. Coordinates strictly increase through black keys and octave boundaries. |

Automatically generated explanations do not themselves verify exceptions.
