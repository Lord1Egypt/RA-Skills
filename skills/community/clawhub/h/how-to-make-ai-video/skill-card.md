## Description:

Finds video making tutorials and matching skills, then presents options and production steps for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

People using coding agents can find a suitable tutorial and skill for a video request, compare suggested creative options, and follow an ordered workflow. For a full video, the guidance includes review checkpoints and cost estimates before paid generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search requests use an external catalog service, and the security assessment flags unclear disclosure of data sharing.

Mitigation: Avoid including sensitive project details in searches until the service's data-sharing practices are clear.

Risk: The workflow recommends install commands without pinned versions and includes a project workflow that stores content in GitHub.

Mitigation: Review and pin skill versions before installation; make GitHub storage optional, private, and explicitly authorized.

Risk: The security scan was partial because some referenced local paths were missing.

Mitigation: Review and scan the complete skill source, including referenced files, before deployment.

## Reference(s):

- [varg how to](https://varg.ai/how-to)
- [Ten-step video workflow](https://varg.ai/how-to/make-a-video-in-ten-steps.md)
- [varg how to MCP server](https://api.varg.ai/v2/skills/mcp)
- [Whole-video prompt](references/whole-video-prompt.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Concise text or Markdown with links, install commands, and workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The output is tailored to a user's video-making request; public search does not require an API key.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata; bundled frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
