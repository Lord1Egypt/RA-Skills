## Description: <br>
Mev Engine provides an OpenClaw-native workflow framework for Mission-Environment-Verification reasoning, delivery gates, sign-off expectations, and lesson lifecycle management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meta-evo-creator](https://clawhub.ai/user/meta-evo-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to structure agent work with MEV reasoning layers, delivery checks, sign-off expectations, and learning capture. When configured, it can guide IMA delivery workflows that require explicit credentialed upload steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is marked for review because it under-discloses a bundled helper that can upload local Markdown or text files to an external IMA knowledge base using credentials. <br>
Mitigation: Review before installing, keep IMA credentials unset unless needed, require explicit confirmation before any upload or push, and verify the exact file path and knowledge-base ID before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/meta-evo-creator/mev-engine) <br>
- [Eval Loop for Self-Improvement](references/eval-loop.md) <br>
- [Promotion Guide](references/promotion-guide.md) <br>
- [Learning Schema](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklist text, command examples, and optional JSON status from the IMA upload helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Credentialed IMA upload behavior is optional and should require explicit user confirmation.] <br>

## Skill Version(s): <br>
8.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
