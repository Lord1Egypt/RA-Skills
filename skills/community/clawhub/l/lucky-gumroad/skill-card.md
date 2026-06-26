## Description: <br>
Automates Gumroad seller workflows including product creation, uploads, profile editing, and sales data retrieval using an authenticated Chrome session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents managing the referenced Gumroad store use this skill to create and optimize listings, upload products, edit profile details, and retrieve sales or customer data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a live Gumroad seller account through a saved browser session. <br>
Mitigation: Install only for Gumroad accounts you own or administer, and run the browser profile in an isolated environment. <br>
Risk: Sensitive store actions do not have a clear required approval gate in the skill evidence. <br>
Mitigation: Require explicit confirmation before publishing products, changing profile or account details, uploading files, exporting sales data, or using customer emails. <br>


## Reference(s): <br>
- [Lucky Gumroad Automation on ClawHub](https://clawhub.ai/rmbell09-lang/lucky-gumroad) <br>
- [Gumroad Dashboard](https://gumroad.com/dashboard) <br>
- [Gumroad Best Practices](BEST_PRACTICES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct browser automation against a saved Gumroad session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
