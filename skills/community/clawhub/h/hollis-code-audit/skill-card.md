## Description: <br>
Runs a read-only, evidence-backed code audit for repositories, pull requests, security reviews, regression-risk reviews, and intent-alignment checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollis9087](https://clawhub.ai/user/hollis9087) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit code changes, modules, repositories, and prior review findings for concrete security, correctness, regression, and intent-alignment risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit snapshots and packets can expose repository metadata such as local paths, branch names, changed-file names, and diff statistics. <br>
Mitigation: Use .auditignore or configured skip paths for confidential or noisy files, and review packet contents before sharing them. <br>
Risk: External reviewer routes can share code or metadata outside the local agent environment. <br>
Mitigation: Use external reviewers only when repository policy and user instructions allow it, and redact secrets, customer data, private documents, and unreleased business material first. <br>
Risk: A same-model audit can miss issues because it shares blind spots with the development model. <br>
Mitigation: For high-stakes changes, use a strong non-current-model reviewer or human reviewer and validate candidate findings locally before relying on the audit. <br>


## Reference(s): <br>
- [Audit Checklist](references/audit-checklist.md) <br>
- [Independent Reviewer Prompt](references/independent-reviewer-prompt.md) <br>
- [ClawHub Release Page](https://clawhub.ai/hollis9087/hollis-code-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown audit report with optional shell command blocks, JSON snapshots, and review packet text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only by default; helper scripts can produce repository snapshots, audit packets, reviewer-route inventories, and eval summaries.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
