## Description: <br>
Crustdata (crustdata.com). Use this skill for ANY Crustdata request - searching and reading data. Whenever a task involves Crustdata, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search, identify, and enrich Crustdata company records through an OOMOL-connected account without handling raw Crustdata API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence flags the package as suspicious because bundled maintainer helpers may run with broad authority or perform credentialed account actions. <br>
Mitigation: Install only from the trusted publisher account, review the skill before use, and avoid full-access nested agent execution unless explicitly intended. <br>
Risk: This skill requires sensitive credentials through an OOMOL-connected Crustdata account. <br>
Mitigation: Use the OOMOL connection flow so credentials remain server-side, and reconnect or rotate credentials when scope or expiration errors occur. <br>
Risk: Connector actions depend on live schemas and may fail or behave differently if the connected service changes. <br>
Mitigation: Inspect the live action schema before constructing payloads and confirm any action marked write or destructive before execution. <br>


## Reference(s): <br>
- [Crustdata homepage](https://crustdata.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Skill page](https://clawhub.ai/oomol/oo-crustdata) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action payload construction; connector responses include data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
