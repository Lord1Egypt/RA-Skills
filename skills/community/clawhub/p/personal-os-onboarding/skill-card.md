## Description: <br>
Set up a Personal OS through a conversational interview that creates SOUL.md, USER.md, IDENTITY.md, AGENTS.md, and MEMORY.md for future agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[borodich](https://clawhub.ai/user/borodich) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to onboard a new personal agent workspace, capture working preferences, and create local foundation files that future sessions can read. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local plaintext files that may contain personal profile details and working preferences. <br>
Mitigation: Run it only in a trusted workspace, review the generated SOUL.md, USER.md, IDENTITY.md, AGENTS.md, and MEMORY.md files, and redact sensitive information before reuse or sharing. <br>
Risk: Broad trigger phrases such as setup or identity prompts could invoke onboarding when the user did not intend to create persistent local context. <br>
Mitigation: Use an explicit setup command or clear onboarding request, and confirm before creating or replacing existing foundation files. <br>


## Reference(s): <br>
- [Onboarding on ClawHub](https://clawhub.ai/borodich/personal-os-onboarding) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with conversational text and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local profile and memory files after a guided interview; users should review and redact sensitive details.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
