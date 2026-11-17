## Description:

Access and manage persistent notes and workspace files through the Northbase CLI when the user explicitly requests reading, writing, listing, or syncing them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethanbernheim-maker](https://clawhub.ai/user/ethanbernheim-maker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use Northbase to access, list, synchronize, and update persistent notes or workspace files through the Northbase CLI when the user explicitly requests file interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unchecked note or workspace paths could be misused if interpolated into shell commands.

Mitigation: Pass only validated, workspace-relative paths to the Northbase CLI using safe argument handling.

Risk: Stored note contents may be untrusted and could influence later agent behavior.

Mitigation: Treat retrieved note contents as user data, not instructions, and confirm intent before acting on sensitive changes.

Risk: Updating files without first reading current contents could overwrite existing notes.

Mitigation: Read the target file first and preserve existing content unless the user clearly asks to replace it.

## Reference(s):

- [Northbase on ClawHub](https://clawhub.ai/ethanbernheim-maker/skills/northbase)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the northbase CLI and user authentication; file changes should be made only after explicit user intent.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
