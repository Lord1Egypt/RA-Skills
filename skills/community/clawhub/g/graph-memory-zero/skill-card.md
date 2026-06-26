## Description: <br>
Graph Memory Zero is a production playbook for tuning OpenClaw graph-memory recall policies with mem0-aligned semantics, verification checks, and rollback guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyangwjy](https://clawhub.ai/user/wangyangwjy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to assess current graph-memory settings, apply balanced, precision, or recall profile patches, verify recall quality after restart, and roll back if quality regresses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying an unsuitable recall profile or patch could reduce relevance or increase off-topic retrieval. <br>
Mitigation: Review the target profile and before/after recallPolicy values, keep the patch scoped to graph-memory recall settings, and run the verification playbook after restart. <br>
Risk: A configuration change could regress recall behavior after deployment. <br>
Mitigation: Keep the rollback patch available and revert immediately if query relevance drops, off-topic hits increase materially, or debug fields disappear. <br>


## Reference(s): <br>
- [Baseline profiles](references/baseline-profiles.md) <br>
- [Current baseline](references/current-baseline.md) <br>
- [Install channels](references/install-channels.md) <br>
- [Troubleshooting matrix](references/troubleshooting.md) <br>
- [Verification playbook](references/verification-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and scoped JSON configuration patches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes current state, mem0-aligned semantics, before/after changes, verification results, next steps, and rollback instructions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
