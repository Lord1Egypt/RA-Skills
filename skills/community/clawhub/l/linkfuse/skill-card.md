## Description: <br>
Create a Linkfuse affiliate short link from any URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oliverw](https://clawhub.ai/user/oliverw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create Linkfuse affiliate short links from supplied URLs through the Linkfuse REST API. It is intended for workflows where an agent should validate token availability, call the helper script, and return the created short URL and title. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Linkfuse API token and sends user-provided URLs to Linkfuse. <br>
Mitigation: Install only when this data sharing is acceptable, keep LINKFUSE_TOKEN in the environment, and avoid shortening secret-bearing private URLs. <br>
Risk: Unescaped URLs or unintended clipboard copy commands could expose or mishandle sensitive link data. <br>
Mitigation: Use proper shell quoting for URLs and copy the generated short URL to the clipboard only after explicit user approval. <br>


## Reference(s): <br>
- [ClawHub Linkfuse Skill Page](https://clawhub.ai/oliverw/linkfuse) <br>
- [Linkfuse](https://www.linkfuse.net) <br>
- [Linkfuse External Token Page](https://app.linkfuse.net/user/external-token) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, network access, and LINKFUSE_TOKEN. The helper returns JSON with url and title on success.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
