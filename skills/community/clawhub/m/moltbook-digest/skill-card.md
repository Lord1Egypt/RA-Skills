## Description:

Collect Moltbook posts and comments, build an evidence pack, and interpret it through either the calling agent or LiteLLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtics](https://clawhub.ai/user/mtics)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users use this skill to collect Moltbook posts and comments for topic research, feed digests, monitoring, and evidence-grounded reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A weak Moltbook URL check may expose a bearer token if the API base URL is changed.

Mitigation: Use the skill without a Moltbook API key unless authentication is required, and keep MOLTBOOK_API_BASE or --base-url set only to the real Moltbook API origin.

Risk: Dependency installation is not reproducible from the provided artifact.

Mitigation: Run the skill in an isolated environment and prefer a reviewed lock file before enabling LiteLLM or provider credentials.

Risk: Provider credentials can be used during LiteLLM interpretation.

Mitigation: Grant only the required provider credentials and run with limited filesystem and environment access.

## Reference(s):

- [Moltbook](https://www.moltbook.com)
- [Moltbook API Notes](references/api.md)
- [ClawHub skill page](https://clawhub.ai/mtics/skills/moltbook-digest)
- [Publisher profile](https://clawhub.ai/user/mtics)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON evidence packs, configuration guidance, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes fixed output filenames including digest.md, evidence.json, analysis_input.md, agent_handoff.md, and analysis_report.md depending on analysis mode.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
