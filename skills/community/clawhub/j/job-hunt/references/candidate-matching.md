# Discovery Candidate Matching

Use this reference in discover mode after a full job detail has been retrieved.
Its purpose is to decide whether a listing deserves the user's default application
effort. It does not predict a screening, interview, or offer result. Those outcomes
depend on information that a CV and posting do not expose, including applicant pool,
timing, recruiter choices, and internal hiring changes.

## Evidence Boundary

Freeze the candidate source first with:

```bash
python3 scripts/snapshot_profile.py --workspace <ws> --profile <master-profile.yaml>
```

Use only `candidate-profile.yaml` as CV evidence in the round. Never update it after
matching begins. A changed CV belongs in a new round.

Use only a successful, journaled `detail` retrieval or an intact browser-detail
capture as job evidence. Search cards establish a lead, source identity, and direct
URL; they do not establish an exhaustive requirement set. Do not derive requirements
from a title, salary, company, tag list, or an unstated assumption.

## Mapping Each Detail

Create exactly one `candidate-match.yaml` entry for every `shortlist.yaml` row.

```yaml
profile_snapshot: candidate-profile.yaml
rows:
  - id: site-source-id
    basis: detail                       # detail | detail_unmapped | card
    recommendation: recommend           # recommend | review
    requirements:
      - id: M1
        text: exact posting requirement phrase
        kind: must_have                 # must_have | responsibility
        screening: weighted             # knockout | weighted | nice_to_have
        match: strong                   # strong | partial | gap | no_evidence
        recency: current                # current | recent | dated | undated
        effort: quick                   # quick | evening | multi_day | not_closable
        job_evidence:
          - file: raw/site-detail-id.json
            quote: exact source phrase containing text
        cv_evidence:
          - path: /experience/0/bullets/1
            quote: exact phrase in the frozen profile leaf
    alignment:
      level_direction: lateral          # step_up | lateral | step_down | unclear
      domain_fit: same_domain           # same_domain | adjacent | cross_over | unclear
      job_evidence: [{file: raw/site-detail-id.json, quote: exact role phrase}]
      cv_evidence: [{path: /experience/0/title, quote: exact role phrase}]
  - id: site-card-id
    basis: card
    recommendation: review
    requirements: []
```

The `path` is an RFC 6901 JSON Pointer into `candidate-profile.yaml`. Point at one
scalar leaf, not a broad section. The quoted CV text must occur in that leaf. For
`no_evidence`, set `cv_evidence: []`; every other match needs one or more exact CV
citations. A job quote must appear in the captured detail and be traceable to the
listing's source ID or direct URL.

Classify requirements conservatively:

- `knockout`: a stated condition that prevents progression when unmet, such as work
  authorization, legally required license, required language, clearance, or a hard
  location rule.
- `weighted`: a core skill, experience, or responsibility the role explicitly uses to
  screen or perform the work.
- `nice_to_have`: a stated preference that can be absent without making the whole
  listing unsuitable.
- `strong`: direct, concrete evidence of comparable work or a current/recent skill.
  A mere skills inventory normally supports `partial`, not `strong`, for a complex
  responsibility.
- `partial`: relevant but narrower, indirect, incomplete, or only modestly stale
  evidence. A `strong` claim that is `dated` is counted as partial.
- `gap`: evidence exists but does not meet the stated depth, scope, or requirement.
- `no_evidence`: the frozen profile provides no support.

Do not turn adjacent technologies into equivalence automatically. Treat them as
strong only when the underlying function is genuinely the same and the frozen profile
shows the comparable work; otherwise use `partial` and explain the short closure.

## Default Recommendation Rule

`recommend` is a strict investment category, not a statement that the user meets every
preference. `scripts/check_candidate_match.py` permits it only when all of these hold:

1. The row has a complete detail retrieval and at least one mapped core requirement.
2. Every knockout has strong evidence; no knockout or weighted core requirement is
   `gap` or `no_evidence`.
3. A partial weighted core item is only `quick` or `evening` to close.
4. At least half of the core requirements have strong evidence not marked `dated`;
   at least one core must-have and one core responsibility, if the posting declares
   each kind, have that strength.
5. Domain is `same_domain` or `adjacent`, and level is assessed.
6. `strong_apply` is narrower still: same domain, no step-up, and strong evidence for
   every core requirement.

Missing `nice_to_have` rows are allowed. A row with a meaningful core gap, ambiguous
level, cross-over domain, incomplete detail, or missing evidence remains `review`.
It can still be shown as a `stretch` if the user wants exploratory options, but it is
not placed ahead of evidence-backed defaults.

## Bounded Review and Rendering

`brief.yaml.max_match_reviews` is an integer from 1 to 5. It limits how many full
details can receive a mapping in one discover round. Follow the source policy's
separate page and row caps too. Reading a description is separate from mapping it to the CV. Read every posting
retained in a complete report, within the source caps. A full description awaiting
that deeper mapping uses `basis: detail_unmapped`, `recommendation: review`, empty
`requirements`, no `alignment`, and `job_evidence` quotes from the successful
row-specific detail capture. The gate checks that evidence without counting the
entry as a mapping or allowing a recommendation. A user-named or final-report
completeness fetch can use the documented exception process; neither bypasses
source limits or the mapping cap. See discover mode for complete versus
explicitly requested preliminary delivery and collection manifests.

Run the render form before writing the shortlist:

```bash
python3 scripts/check_candidate_match.py --workspace <ws> --render --lang <zh|en|ja|ko|es>
```

Copy the exact localized line beside its direct posting link in `shortlist.md`. Then
run the normal gate, followed by `lint_no_prediction.py` and `check_shortlist.py`.
The normal gate verifies the evidence, ordering, localized summary, review cap, and
receipt inputs.

The five native output languages use the same schema and rules. For another report
language, use the skill's existing English or Chinese fallback wording while keeping
the machine keys, raw quotes, IDs, and JSON Pointers unchanged.
