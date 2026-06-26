## Description: <br>
Typeform lets agents search and read data from a connected Typeform account through the OOMOL oo connector instead of calling the Typeform API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve Typeform account, workspace, form, and response data from an OOMOL-connected Typeform account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can read data from the connected Typeform account, including submitted form responses. <br>
Mitigation: Use a Typeform account whose data is appropriate for the agent workflow, and review returned data before sharing or storing it elsewhere. <br>
Risk: The skill requires OAuth or other sensitive credentials through the OOMOL connector. <br>
Mitigation: Connect only the intended Typeform account and rerun setup steps only after an authentication or connection failure. <br>
Risk: Future connector versions may expose write or destructive Typeform actions. <br>
Mitigation: Confirm the exact payload, target, and expected effect with the user before running any action marked write or destructive. <br>


## Reference(s): <br>
- [ClawHub Typeform skill](https://clawhub.ai/oomol/oo-typeform) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Typeform homepage](https://www.typeform.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live Typeform connector schema before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
