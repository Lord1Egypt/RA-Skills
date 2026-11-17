## Description:

GSAP动画生成工具 helps developers generate, explain, debug, optimize, and package GSAP animation code through an AI-backed external API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn natural-language animation requests, GSAP API questions, setup needs, debugging reports, performance issues, and production pattern requests into GSAP-oriented guidance and code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Animation prompts and submitted code snippets are sent to an external Xiaobenyang API.

Mitigation: Use the skill only with data suitable for that service, avoid secrets or proprietary code, and review generated GSAP output before use.

Risk: The API key is stored in plaintext in a local .env file.

Mitigation: Treat the key as sensitive, restrict access to the workspace, and delete or protect the .env file after use.

Risk: The artifact includes unrelated gaokao configuration references, making the release scope unclear.

Mitigation: Require publisher cleanup or review before routine deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/gsap-animation-generate)
- [ALinkLab publisher profile](https://clawhub.ai/user/alinklab)
- [Xiaobenyang API key site](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown or structured text with code snippets derived from external API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key; tool calls return raw API data with success and message fields.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
