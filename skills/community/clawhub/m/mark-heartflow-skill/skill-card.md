## Description:

HeartFlow is a rule-based discriminator that checks AI inputs, drafts, and outputs for safety, honesty, manipulation, contradiction, and completion issues before they reach users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use HeartFlow as a local rule and MCP gate to classify AI text and route it to pass, verify, rewrite, or block decisions before output reaches users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags the skill as suspicious because its local authority and persistence are broader than a simple safety-check framing may suggest.

Mitigation: Review before installing on a real workstation, run only as an unprivileged user, and avoid shared or privileged systems until the highlighted behaviors are removed or made explicit opt-in.

Risk: MCP server use can expose local tool behavior if token and path controls are not configured.

Mitigation: Set HEARTFLOW_MCP_TOKEN manually, set HEARTFLOW_PATH_GUARD=enforce, and restrict deployment to controlled local environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/mark-heartflow-skill)
- [npm package](https://www.npmjs.com/package/@yun520-1/heartflow)
- [README](artifact/README.md)
- [Security guidance](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and structured local rule/MCP outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic gate actions such as pass, verify, rewrite, or block with findings and reasons.]

## Skill Version(s):

6.6.1 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
