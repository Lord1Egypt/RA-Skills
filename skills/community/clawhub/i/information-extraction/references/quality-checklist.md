# Quality Checklist

Review these questions before finalizing extraction results.

## Entities

- Did you miss any central entity?
- Are repeated mentions merged correctly?
- Are entity types conservative and defensible?

## Relations

- Is each relation directional where needed?
- Are predicates normalized?
- Did you invent a predicate unnecessarily?
- Should any weak predicate be downgraded to `related_to`?

## Attributes

- Is each attribute attached to the right entity?
- Should any attribute actually be a relation?
- Are values normalized consistently?

## Events

- Did you preserve event structure when time or place matters?
- Did you avoid flattening a complex event too early?
- Are participant roles explicit?

## Evidence and confidence

- Does each important record have evidence?
- Did you separate explicit text from inference?
- Are low-confidence cases marked as ambiguity?

## Final output

- Are duplicates removed?
- Is the requested export format correct?
- Is JSON the default unless the user asked for JSONL or TSV?
