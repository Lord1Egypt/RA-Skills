## Description: <br>
Create, fetch, and validate me.txt personal identity files for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollsmorr1](https://clawhub.ai/user/rollsmorr1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create public me.txt identity files, place them on websites, fetch existing files, and validate that they follow the expected markdown structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public me.txt files can expose private contact details, location information, secrets, or other sensitive personal information. <br>
Mitigation: Review generated content before publishing and omit anything that should not be publicly indexed. <br>
Risk: Optional npx helper commands and the metxt.org lookup fallback rely on external packages or services. <br>
Mitigation: Use the helper only when the npm package is trusted, and avoid external lookup fallbacks for private or sensitive domains. <br>


## Reference(s): <br>
- [me.txt homepage](https://metxt.org) <br>
- [me.txt specification](https://metxt.org/spec) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and me.txt file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a me.txt file body, validation checklist, fetch URLs, and optional npx commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
