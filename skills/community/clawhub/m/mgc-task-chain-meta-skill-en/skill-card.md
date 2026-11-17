## Description:

A single-device multi-agent task-chain methodology for coordinating Master, Script, and Executor agents through MGC to handle sensitive resources with reduced exposure, adapted to MGC 1.4.10.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure single-device multi-agent task chains where scripts and credentials are handled through MGC. It provides prompt templates and operating guidance for orchestration, script storage, MGC execution, and result handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill coordinates agents around local secrets and script execution.

Mitigation: Install only from a trusted MGC package, pin and isolate the dependency, and require approval for each script save and run.

Risk: Scripts may retrieve secrets or sensitive records through broad local MGC access.

Mitigation: Allow only the specific secrets needed for each script and review scripts before storing or running them.

Risk: Reusable scripts may write plaintext results to ~/mgc_outputs.

Mitigation: Treat result files as sensitive, restrict access, remove them after use, and avoid writing raw customer data when a desensitized result is sufficient.

Risk: The best-practice document can persist user history and operational details.

Mitigation: Review or disable automatic best-practice updates before using the skill with real credentials, customer data, or confidential workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zkeviny/skills/mgc-task-chain-meta-skill-en)
- [MGC Core Repository](https://github.com/zkeviny/MGC-Blackbox)
- [Artifact README](artifact/README.md)
- [Master Agent Prompt Template](artifact/prompts/master_agent.md)
- [Script Agent Prompt Template](artifact/prompts/script_agent.md)
- [Executor Agent Prompt Template](artifact/prompts/executor_agent.md)
- [Cooperation Best Practices](artifact/prompts/cooperation_best_practice.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown prompt templates with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific prompt guidance for Master, Script, and Executor agents; MGC-run scripts may write local result files for downstream handoff.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
