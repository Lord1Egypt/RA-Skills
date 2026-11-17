# AI Trace Rubric

## Aim

Locate machine-shaped prose and rank repairs.

One span, one owner: `cliche` = stock wording; `formulaic` =
contrast/structure; `surface` = format/range/headings; `prose-progress` =
stasis/uptake; `narrative-naturalness` = six-plus-beat recipe.

Score each dimension from 0 to 3:

- 0: not a problem
- 1: mild issue
- 2: visible issue
- 3: dominant issue

## Dimensions

| Dimension | Warning Sign | Repair Direction |
| --- | --- | --- |
| Cognitive smoothness | Transitions conceal a real gap or uncertainty | Expose the evidenced gap; do not manufacture doubt or drift |
| Generic diction | Sentences fit any topic | Use specific objects, places, actions, or voice |
| Cliche phrase cluster | Stock phrases, cues, or transitions recur | Use scene evidence, specific action, or plain speech |
| Formulaic structure | Neat threes, repeated contrast frames, chained "比", identical cadence | Use owner evidence |
| Polished stagnation | Paragraphs restate one premise | Cut, merge, or change the state |
| Emotional flatness | The wording loses an evidenced emotional distinction | Restore the distinction; use embodiment only when the scene needs it |
| Rhythm monotony | One speed throughout | Vary breath, brakes, and cadence |
| Context drift | Facts, stakes, or timeline blur | Obey the ledger |
| Relationship stance drift | A reference conflicts with speaker, listener, or audience | Audit the triad; motivate, code, redirect, or add consequence |
| Weak beat bridge | Adjacent beats do not cause each other | Carry residue into a turn and exit pressure |
| Orphaned interaction | Consequential speech or action gets no uptake | Use owner evidence |
| Relationship reset | Trust, secrets, boundaries, or leverage reset | Track knowledge, wants, debts, refusals, and exit rights |
| False precision | Unmeasured micro-actions get exact numbers | Keep useful facts; use felt or plot-relevant scale elsewhere |
| Physical drift | Position, clothing, props, or injuries jump | Restore state or a change gate |
| Occupancy conflict | A resource has impossible or unclear occupants | Establish capacity, transformation, zones, or movement |
| Cultural vacuum | Relevant supplied cultural context disappears | Restore the supported context; do not invent local color |
| Over-clean prose | Editing removes meaningful source roughness | Restore evidenced voice; do not add hesitation by quota |
| Closure addiction | Every thought resolves | Leave useful pressure open |
| Sentence incompleteness | A verb, connector, parallel clause, or reference loses a required slot | Restore recoverable words; report ambiguity |

## Output Format

```text
AI Trace Review
- Cognitive smoothness: 2 -- transitions over-explain cause and effect.
- Emotional flatness: 1 -- one embodied detail is present, but the final sentence summarizes.
- Highest-priority repair: replace the final explanation with action.
```

## Revision Check

Keep genre-valid friction; do not optimize every dimension to zero.
Scores are subjective editing leads, not measured AI probabilities. A smooth,
formal, or clearly resolved passage can need no change. Evidence and author intent
outrank scores; do not praise a revision simply because it is newer.
