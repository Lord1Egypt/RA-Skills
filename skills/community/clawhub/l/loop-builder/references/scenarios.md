# Scenario Defaults

These are starting points, not fixed iteration counts. Always calibrate the
design with the user's evidence, environment, risk, and budget.

## Content Production

Primary pattern: `Explore-Narrow`

Typical phases:

1. define audience, platform, and claim boundary;
2. collect a bounded evidence set;
3. narrow to one angle;
4. draft;
5. verify claims and platform fit;
6. present the publish decision to a person;
7. record performance evidence for the next lifecycle review.

Feedback:

- source coverage;
- claim verification;
- reader or platform fit;
- structural review;
- later performance data with clear measurement limits.

Human gates:

- sensitive claims;
- final editorial judgment;
- external publication.

Stop when the evidence cannot support the angle, another revision does not
change reviewer findings, or publication approval is missing.

## Skill Maintenance

Primary pattern: `Plan-Execute-Verify`

Typical phases:

1. inspect the current package and repository rules;
2. reproduce the behavior or validation failure;
3. plan one bounded change;
4. edit the smallest necessary files;
5. run skill-specific and repository validation;
6. review the diff for public boundaries;
7. request separate commit or publication approval.

Feedback:

- validator results;
- expected example behavior;
- package structure;
- diff and leak scan;
- installed-source or registry verification after publication.

Human gates:

- behavior-contract changes;
- global installation;
- commit, push, or registry publication.

Stop when the requested behavior conflicts with repository policy, required
evidence is missing, or validation can pass only by weakening checks.

## Learning Review

Primary pattern: `Lifecycle Loop`

Typical phases:

1. define the learning question;
2. capture sources and uncertainty;
3. extract concepts in the learner's own structure;
4. turn one concept into an action or experiment;
5. review the result;
6. update the durable note or method.

Feedback:

- ability to explain or apply the concept;
- observed experiment result;
- contradiction with later evidence;
- retrieval and reuse in another context.

Human gates:

- interpretation;
- personal goal;
- adoption into a long-term system.

Stop when the input has not been understood well enough to act, when no
observable practice is available, or when the review produces no new decision.

## UI Visual Match

Primary pattern: `Plan-Execute-Verify`

Typical phases:

1. inspect screenshots, current UI, viewport, and code boundary;
2. identify the largest visual mismatch;
3. plan one visual work package;
4. implement the bounded change;
5. render the same viewport;
6. compare structure, spacing, typography, color, and imagery;
7. continue only if the comparison produces a clear next correction.

Feedback:

- same-viewport screenshots;
- layout and spacing delta;
- typography and color delta;
- visual regression in already-correct regions;
- human acceptance for subjective details.

Human gates:

- design intent not visible in the reference;
- brand or asset choice;
- final subjective acceptance.

Stop when the target or current screenshot is missing, the render environment
cannot reproduce the viewport, two iterations show no meaningful improvement,
or changes would require expanding outside the confirmed component boundary.

## CI Repair

Primary pattern: `Plan-Execute-Verify`

Use Retry only for a known transient infrastructure step.

Typical phases:

1. read the failing job and exact error;
2. reproduce with the narrowest safe command;
3. identify root cause and affected boundary;
4. change one coherent work package;
5. run the narrow check, then relevant broader checks;
6. report remaining environment limitations separately.

Feedback:

- original failure no longer reproduces;
- related tests, build, lint, or type checks;
- diff scope;
- absence of weakened assertions or bypasses.

Stop when the failure cannot be reproduced, required dependencies or permission
are unavailable, the same diagnosis repeats without new evidence, or the
proposed fix hides rather than resolves the cause.
