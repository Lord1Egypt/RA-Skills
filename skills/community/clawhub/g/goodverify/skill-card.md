## Description: <br>
Verify emails, phones, and addresses using the goodverify CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[themusicman](https://clawhub.ai/user/themusicman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support teams use this skill to run email, phone, and address verification through the goodverify CLI, including single checks, batch job handling, usage checks, and health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary flags an unverified remote installer for the goodverify CLI. <br>
Mitigation: Review the installer and CLI source before use, prefer a pinned release or verified installer, and install in a controlled environment. <br>
Risk: The skill handles GoodVerify API keys and allows key overrides in CLI commands. <br>
Mitigation: Use least-privileged keys, avoid sharing secrets in chat or command history, and prefer configured environments over inline key arguments. <br>
Risk: Email, phone, and address checks may send personal or contact data to GoodVerify. <br>
Mitigation: Submit only data you are authorized to verify and apply your organization's privacy and compliance requirements before use. <br>


## Reference(s): <br>
- [GoodVerify service](https://goodverify.dev) <br>
- [goodverify CLI installer referenced by the skill](https://raw.githubusercontent.com/agoodway/goodverify_cli/main/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON output from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the goodverify CLI and a GoodVerify API key for authenticated verification.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
