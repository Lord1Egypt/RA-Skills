## Description: <br>
Hermes-only runtime security attestation and drift detection skill for operator-managed Hermes infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hermes operators and security engineers use this skill to generate deterministic runtime posture attestations, verify attestation integrity, compare trusted baselines for drift, and run advisory-aware guarded verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated attestations can expose host identity, Hermes paths, security toggles, feed state, and watched-file or trust-anchor hashes. <br>
Mitigation: Treat attestation files as sensitive operational records and review watch_files and trust_anchor_files before generation or scheduling. <br>
Risk: Recurring jobs can be added to the user's crontab when scheduler helpers are run with --apply. <br>
Mitigation: Use print-only previews first and run --apply only when the operator intentionally wants managed recurring attestation or advisory checks. <br>
Risk: Unsigned advisory feed bypass weakens the default fail-closed verification posture. <br>
Mitigation: Keep signed advisory verification enabled and use unsigned bypass only for short, audited emergency recovery windows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/hermes-attestation-guardian) <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for operator-managed Hermes environments and may describe generated attestation JSON, checksum files, advisory verification state, and cron configuration.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter, skill.json, changelog, server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
