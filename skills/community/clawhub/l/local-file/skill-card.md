## Description:

Reads, summarizes, and searches local text, Markdown, JSON, DOCX, and PDF files from authorized paths for agent use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhouqing](https://clawhub.ai/user/zhouhouqing)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to inspect, extract, summarize, and search local document contents within a workspace or explicitly authorized path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak path validation could allow reads outside the intended workspace or authorized folders.

Mitigation: Install only in a sandboxed workspace and require canonical realpath containment checks before granting broad local-folder access.

Risk: The documented 10MB file-size limit is not enforced by the artifact behavior.

Mitigation: Add explicit size checks before reading or parsing files, especially DOCX and PDF inputs.

Risk: Hard-coded authorized paths may expose unintended local files.

Mitigation: Remove hard-coded local directories or make authorized roots explicit, reviewable configuration.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhouhouqing/skills/local-file)
- [Publisher profile](https://clawhub.ai/user/zhouhouqing)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or structured error object returned to the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text, Markdown, JSON, DOCX, and PDF inputs; documented file-size and path controls should be verified before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
