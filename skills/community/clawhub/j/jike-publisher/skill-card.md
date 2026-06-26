## Description: <br>
Publish posts to Jike using browser automation, including text posts with emoji, hashtags, topics, and links without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maoruibin](https://clawhub.ai/user/maoruibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to draft and publish Jike posts through a managed browser session when they want browser-guided posting workflows rather than a direct API integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports the skill may mark posts as successful without actually publishing or verifying them. <br>
Mitigation: Manually confirm the final Jike post in the browser before relying on success output or downstream state. <br>
Risk: The skill can persist posted content in a local JSON state file. <br>
Mitigation: Avoid posting sensitive content, and clear or disable local state when stored post text should not remain on disk. <br>
Risk: The skill operates a real Jike account through an active browser session. <br>
Mitigation: Use only an intended account and confirm each publish action before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maoruibin/jike-publisher) <br>
- [Jike web app](https://web.okjike.com/) <br>
- [Quick Reference](QUICK_REFERENCE.md) <br>
- [Examples](references/EXAMPLES.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [Unicode Escape Guide](references/UNICODE_ESCAPE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline browser automation and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local JSON state file with the last publish time and post content when the bundled script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
