## Description: <br>
MetatextAI (metatext.ai) operates a connected MetatextAI account through the OOMOL oo CLI connector for reading, creating, and updating guardrail-related data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect MetatextAI connector schemas, manage guardrail policies, evaluate chat transcripts against configured guardrails, and run selected red-team test scans for a connected application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected MetatextAI account through OOMOL. <br>
Mitigation: Install it only when you intend the agent to operate that account, and keep account connection and billing state under user control. <br>
Risk: Policy creation changes MetatextAI guardrail configuration. <br>
Mitigation: Review the exact policy payload and expected effect with the user before running write actions. <br>
Risk: First-time setup may require installing the oo CLI from a shell command. <br>
Mitigation: Verify the oo CLI installer source before running setup commands. <br>


## Reference(s): <br>
- [MetatextAI ClawHub page](https://clawhub.ai/oomol/oo-metatextai) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [MetatextAI homepage](https://metatext.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; action responses are JSON from the oo CLI.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
