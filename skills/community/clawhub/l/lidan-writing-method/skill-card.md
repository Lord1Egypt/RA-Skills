## Description: <br>
A Chinese writing-style skill that helps agents turn explanations of complex topics into smooth long-form articles using a hidden seven-step framework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whyischen](https://clawhub.ai/user/whyischen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to write approachable Chinese explanatory articles about complex topics in areas such as philosophy, business, AI, linguistics, and sociology. It is best suited for long-form explanation and teaching rather than short news, notices, or pure technical documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for broad writing or explanation requests and steer outputs into this specific long-form style. <br>
Mitigation: Use it only when the requested output benefits from the hidden seven-step explanatory article structure. <br>
Risk: The local quality-check script reads article files supplied to it. <br>
Mitigation: Run the checker only on article files intended for review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/whyischen/lidan-writing-method) <br>
- [Publisher Profile](https://clawhub.ai/user/whyischen) <br>
- [Quality Check Guide](artifact/scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text article prose, with optional terminal quality-check output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated article should hide framework section titles; the bundled checker reads a user-supplied article file and reports whether it matches the style checklist.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
