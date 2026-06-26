## Description: <br>
Searches and browses Pinterest pins, gets pin details, and sends selected Pinterest images through supported messaging tools instead of only links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xs4m1337](https://clawhub.ai/user/0xs4m1337) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search Pinterest for visual inspiration, inspect pins, and share selected images directly in chat. Developers can optionally use the helper script with Pinterest OAuth for read-only board and pin access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can install Python packages at runtime. <br>
Mitigation: Review the script before running it and install dependencies deliberately in a controlled environment. <br>
Risk: OAuth use can expose Pinterest access tokens or grant broader access than needed. <br>
Mitigation: Use only read-only Pinterest scopes, protect the token, and rotate or revoke credentials when they are no longer needed. <br>
Risk: The skill can send Pinterest screenshots or media through messaging tools. <br>
Mitigation: Send media only when it is clearly the requested Pinterest content and verify the selected image before sharing. <br>


## Reference(s): <br>
- [Pinterest OAuth Setup](references/oauth-setup.md) <br>
- [Pinterest API v5 Reference](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with browser and message tool examples, shell commands, and optional JSON from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include direct image media messages, Pinterest pin metadata, and OAuth-backed API results when configured.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
