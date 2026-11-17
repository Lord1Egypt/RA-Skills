# IA validation and measurement

Read this reference when proposing tests, evaluating an IA, or deciding whether an output can be called validated.

## Match method to question

| Question | Method | Main signals | Does not establish |
|---|---|---|---|
| How might people group and name items? | Open card sort | groupings, labels, disagreement | final IA |
| Do proposed categories make sense? | Closed/hybrid card sort | placement, ambiguity, new categories | full findability |
| Can people find destinations in a hierarchy? | Tree test | success, directness, path, time | interface quality |
| Is the first interface choice promising? | First-click test | first destination, confidence | complete task success |
| Can people complete real tasks? | Usability test | completion, errors, recovery, explanation | population-wide rates without design |
| What happens in production? | Analytics/search logs | paths, reformulation, zero results, exits | why it happens |

## Test tasks

Use realistic goals without copying navigation labels into the task. Include high-frequency, high-risk, cross-role, deep-entry, recovery, and edge-case tasks. Segment results where roles, expertise, language, or device plausibly affect behavior.

## Metrics

Choose a meaningful subset:

- task success;
- direct versus indirect success;
- first destination;
- wrong turns and backtracking;
- time to find;
- confidence and perceived control;
- recovery after error;
- search reformulation and zero results;
- browse versus search by task;
- deep-entry dead ends;
- orphan, duplicate, obsolete, and ownerless content;
- coverage by role, language, expertise, and context.

## Interpretation

Do not optimize click count in isolation. A longer path with clear labels may outperform a shorter ambiguous path. Diagnose label quality, competing choices, depth, task type, user knowledge, and recovery together.

## Evidence layers and claim boundaries

Keep these layers separate so a technically valid artifact is not mistaken for a proven experience:

1. **Representation:** required fields, IDs, references, and syntax are valid.
2. **Structural:** the hierarchy, relationships, destinations, branches, and states are internally coherent.
3. **Cognitive:** intended people understand labels, groupings, choices, and consequences.
4. **Behavioral:** intended people can find information or complete the task under realistic conditions.
5. **Operational:** ownership, permissions, content upkeep, exceptions, and service handoffs work over time.

For every validation statement, write the claim first, name the construct being tested, then choose a method that can actually observe it. A sitemap validator may establish destination integrity; it cannot establish findability. A user-flow validator may establish branch and recovery coverage; it cannot establish task success or comprehension. Package tests establish deterministic packaging properties, not product or mentoring quality.

Do not let an aggregate score hide failure of a critical invariant. A broken permission boundary, missing recovery path, semantic drift, fabricated evidence, or unrequested durable action remains a failure even when other dimensions score well.

## Validation plan template

```markdown
### Claim
What decision or assumption is being tested?

### Participants and segments
Who must be represented, and why?

### Method
Why does this method answer the claim?

### Tasks and materials
What will participants see and do?

### Measures and decision rule
What evidence would retain, revise, or reject the structure?

### Limitations
What will remain unknown?
```

Avoid universal sample-size claims. Select sample size from study purpose, variability, segmentation, risk, and practical constraints.

## Skill-behavior assurance

When evaluating the ProPaymun IA behavior itself, score dimensions separately rather than treating package validity as product quality:

- activation precision and engagement-depth calibration;
- IA decision quality and semantic consistency;
- question utility, interaction burden, and novice comprehension;
- uncertainty calibration, user agency, and memory isolation;
- stage-complete closure, stop compliance, and portable continuation;
- localization discipline and evidence integrity;
- context/token discipline;
- host capability truthfulness and portability;
- IA Reference Lock fidelity in downstream outputs.

Compare representative cases with the last stable release. A deterministic pass proves only the tested structural invariant; it does not prove mentoring quality, cross-host consistency, visual quality, or resistance to every semantic prompt injection.

For conversational tests, record jargon leakage, number and utility of user turns, whether a coherent result arrived before another nonessential question, unsupported product commitments, bilingual duplication, proactive memory retrieval or mutation, whether a pause produced a stage-complete summary, whether continuation remained portable without host memory, and whether an optional next step was presented as optional. Score automatically supplied memory separately from agent-initiated retrieval and mutation so host behavior does not hide or excuse skill behavior. For visual flows, inspect the rendered result at the intended size for overlap, clipped text, mislabeled branches, and ambiguous connector endpoints; source or syntax checks alone do not establish visual legibility.
