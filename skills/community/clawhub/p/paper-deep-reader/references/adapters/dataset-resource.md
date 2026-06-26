# Adapter: Dataset / Resource

Use this adapter when the paper's main contribution is a dataset, corpus, benchmark resource, annotation scheme, curated collection, or data construction pipeline rather than a single new algorithm.

## What to prioritize

1. The sampling frame and collection pipeline.
2. The intended scientific or engineering use of the resource.
3. Annotation protocol, rubric, and quality control.
4. Split logic, leakage prevention, and artifact risk.
5. Governance issues such as licensing, privacy, or usage constraints.
6. What kinds of capability the resource can and cannot validly measure.

## Questions to answer in the note

- What is the resource, exactly?
- What gap does it fill relative to earlier datasets or corpora?
- How was the data collected, filtered, and cleaned?
- How were labels, annotations, or metadata created?
- What shortcuts, artifacts, or leakage risks are plausible?
- What is the intended use case, and what misuses are easy to imagine?
- Does the resource support the claims the authors make about it?

## Minimum insertions into the note

Add or expand these sections:

### Problem setup

- target task, use case, or scientific question
- scope and population of interest
- what prior resources were missing

### Technical core

- data collection pipeline
- sampling and filtering logic
- annotation or labeling protocol
- split construction
- schema, modalities, or metadata structure when relevant

### Evidence

- quality-control evidence
- inter-annotator agreement or validation checks when relevant
- descriptive statistics and coverage
- baseline results or benchmark usage only insofar as they validate the resource
- leakage, artifact, or shortcut analyses

### Limitations and failure modes

Include discussion of:

- narrow population or coverage
- annotation ambiguity
- governance limitations
- label noise or bias
- ways the dataset could reward the wrong behavior

## Special reading rules

- Do not let baseline model results dominate the note if the real contribution is the resource itself.
- Treat collection and annotation choices as first-class technical design decisions.
- Read data card, appendix, and supplemental material carefully; crucial caveats often live there.
- Ask what the dataset systematically leaves out, not only what it contains.
- Ask whether the dataset measures the target capability directly or only through a proxy task.

## Typical failure patterns to watch for

- unclear or biased sampling frame
- leakage across splits or tasks
- shortcut artifacts that make benchmark scores misleading
- labels whose meaning is underspecified or weakly audited
- strong baseline performance presented as proof of dataset quality without deeper validation
- governance, privacy, or licensing issues treated superficially
- claims of generality that exceed the resource's actual coverage

## Reusable note prompts

- “The resource fills a gap in … by collecting …”
- “The most consequential design choice in the dataset is …”
- “This dataset likely measures … better than …”
- “A major artifact or leakage risk is …”
- “The resource is valuable for … but weak for …”
