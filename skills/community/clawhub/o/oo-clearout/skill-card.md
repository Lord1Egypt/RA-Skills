## Description: <br>
Clearout verifies email addresses and checks Clearout account credits through an OOMOL-connected Clearout account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to run Clearout email verification and account-credit checks without calling the Clearout API directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email verification actions may send email addresses to the OOMOL-connected Clearout service. <br>
Mitigation: Use the skill only for explicit Clearout tasks where the user intends to verify the provided email data. <br>
Risk: Clearout verification requests may consume account credits or encounter account limits. <br>
Mitigation: Check available credits and daily verification limits before large or repeated verification workflows. <br>
Risk: The connector contract can change over time. <br>
Mitigation: Inspect the live connector schema before building each action payload. <br>


## Reference(s): <br>
- [Clearout homepage](https://clearout.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub Clearout release page](https://clawhub.ai/oomol/oo-clearout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions may return execution metadata and consume Clearout account credits.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
