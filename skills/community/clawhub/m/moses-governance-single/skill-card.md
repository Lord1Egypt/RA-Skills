## Description: <br>
MOSES Governance Single provides single-agent constitutional controls for behavioral modes, posture controls, role awareness, and a SHA-256 chained local audit trail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add a local governance layer that tracks an agent's active mode, posture, and role while recording governed actions in a tamper-evident audit ledger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes persistent local governance and audit state that can contain operational details. <br>
Mitigation: Treat ~/.openclaw/audits/moses and ~/.openclaw/governance as sensitive local data and avoid logging secrets or private details. <br>
Risk: MOSES_OPERATOR_SECRET is an optional local HMAC signing secret. <br>
Mitigation: Set MOSES_OPERATOR_SECRET only in a trusted shell and never paste it into chat or expose it to agents. <br>
Risk: Unrestricted or offense modes can reduce behavioral constraints while retaining audit logging. <br>
Mitigation: Use unrestricted and offense modes deliberately, and review the active mode, posture, and role before consequential actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sunrisesillneversee/moses-governance-single) <br>
- [MOSES DOI record](https://zenodo.org/records/18792459) <br>
- [MOSES website](https://mos2es.io) <br>
- [Governance modes reference](references/modes.md) <br>
- [Posture controls reference](references/postures.md) <br>
- [Role hierarchy reference](references/roles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON or JSONL state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local governance state and audit ledger files under ~/.openclaw when its helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
