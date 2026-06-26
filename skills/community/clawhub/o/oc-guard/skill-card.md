## Description: <br>
Safe OpenClaw config planning/apply workflow with bilingual execution receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmond-ai](https://clawhub.ai/user/edmond-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use OC Guard to plan, validate, and apply OpenClaw configuration changes with receipts, backups, rollback behavior, and post-apply checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make high-impact OpenClaw configuration changes from generated proposals. <br>
Mitigation: Review the generated plan before applying changes, use apply only with explicit confirmation, and verify receipt and post-apply checks. <br>
Risk: Requirements, proposals, logs, or backups may expose sensitive operational details if handled carelessly. <br>
Mitigation: Avoid placing secrets in requirements or proposals, keep backup and diagnostic directories private, and review outputs for secret masking. <br>
Risk: Apply operations may restart OpenClaw services and send live canary messages. <br>
Mitigation: Run apply operations during an appropriate maintenance window and confirm rollback readiness before making changes. <br>
Risk: This slug is deprecated in favor of oc-guard-skill. <br>
Mitigation: Prefer the maintained oc-guard-skill release when available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edmond-ai/oc-guard) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/edmond-ai) <br>
- [README](artifact/README.md) <br>
- [Safety notes](artifact/docs/SAFETY.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples, JSON proposal inputs, and bilingual execution receipts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, openclaw, and opencode; receipt output includes operation, request id, status, and signature.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact changelog contains 1.0.2 entry) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
