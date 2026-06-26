## Description: <br>
Orchestrate screenshot and Chinese instruction inputs into PSD batch edits with transaction rollback by reusing psd-automator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhrxy](https://clawhub.ai/user/dhrxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Design automation users and developers use this skill to turn Chinese edit instructions, screenshot context, or pre-parsed tasks into PSD/PSB text-edit batches, dry-run previews, PNG exports, and rollback-aware execution through psd-automator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says rollback and local-copy safety promises are weaker than documented for important PSD/PSB files. <br>
Mitigation: Start with dry-run, keep independent backups outside the tool, and verify outputs before using real file changes. <br>
Risk: Low-confidence edits or forced execution can apply incorrect text changes to PSD/PSB files. <br>
Mitigation: Avoid force on low-confidence edits and require review when task confidence falls below the configured threshold. <br>
Risk: The skill depends on psd-automator behavior for actual file changes and exports. <br>
Mitigation: Review the referenced psd-automator dependency before allowing production file edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dhrxy/main-image-editor) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [JSON results and command-line execution output, with generated PSD/PNG/ZIP file paths when execution succeeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run, confidence thresholds, force execution, rollback_all behavior, and optional bundle ZIP output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
