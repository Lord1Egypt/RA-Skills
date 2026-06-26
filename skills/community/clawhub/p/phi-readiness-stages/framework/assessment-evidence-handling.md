# Assessment Evidence Handling

Use these rules whenever a PRS review requests, copies, stores, or summarizes assessment evidence.

Last reviewed against official source registry: March 18, 2026.

## Purpose

PRS reviews should evaluate evidence without creating a new PHI handling problem in the assessment process itself.

## Default handling rule

- collect the minimum evidence necessary to support the stage decision
- prefer evidence location pointers, record identifiers, and redacted excerpts over raw exports
- do not copy full logs, screenshots, tickets, or datasets into the final assessment unless necessary to explain a blocker

## Prohibited handling

- do not place raw PHI into AI prompts, chat tools, issue trackers, pull requests, or public documentation
- do not paste raw PHI into `README.md`, assessment reports, or example artifacts
- do not create local working copies of raw PHI unless there is no reasonable alternative and the storage location is approved

## Required reviewer behavior

- ask for redacted screenshots, redacted log excerpts, or evidence pointers first
- record where durable evidence lives instead of duplicating it into the report
- label any evidence that contains or may contain PHI
- use approved storage locations and approved access paths only
- restrict access to reviewers and approvers with a stated need to know

## Minimum handling expectations by evidence type

- screenshots: redact names, dates of birth, account numbers, medical record numbers, message bodies, and free-text fields
- logs: request event metadata, control identifiers, timestamps, and actor types before asking for full payloads
- tickets and documents: link to the internal record and summarize only the control-relevant point
- exports and datasets: use field lists, counts, or sample schemas unless raw records are required for the review
- contracts and approvals: capture the effective date, scope, approver, and record location before copying full text

## If raw PHI is unexpectedly received

1. stop normal review handling
2. move the artifact only into an approved controlled location if it is not already there
3. avoid re-sharing it through chat, tickets, or prompts
4. record that unexpected PHI was received and how it was secured
5. continue the review using a redacted or pointer-based substitute whenever possible

## Retention and deletion

- keep only the assessment notes and evidence pointers needed to support the PRS decision
- do not retain duplicate raw PHI artifacts longer than necessary for the review
- follow the organization's approved retention and deletion path for assessment materials
- if retention requirements are unclear, record that as a process gap

## Output requirements

Every PRS assessment must include:

- an assessment evidence handling note
- whether any PHI-bearing evidence was reviewed directly, redacted, or avoided
- the storage or record-location approach used for durable evidence

## Assessment rule

If the review process itself cannot handle evidence safely, reduce confidence and record the evidence-handling gap as a blocker or follow-up action.
