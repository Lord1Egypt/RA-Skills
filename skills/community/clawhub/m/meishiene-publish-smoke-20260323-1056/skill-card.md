## Description: <br>
Verify ClawHub login, dry-run sync state, one-off publish success, and cleanup for a local skill workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meishiene](https://clawhub.ai/user/meishiene) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release operators use this skill to confirm ClawHub authentication, dry-run behavior, temporary publish success, and cleanup without modifying existing production skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup commands can hide or delete the temporary test skill. <br>
Mitigation: Confirm the active ClawHub account, use a unique temporary slug, inspect the published test item, and prefer hiding over deleting unless the slug is confirmed to be temporary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/meishiene/meishiene-publish-smoke-20260323-1056) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for validating and cleaning up a temporary ClawHub publish.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
