## Description: <br>
Manage Helmet library accounts in the Helsinki capital region from an AI agent, including renewals, holds, fines, and catalog search for one card or family profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vijaykodam](https://clawhub.ai/user/vijaykodam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to inspect Helmet library account status, triage overdue loans and pickup-ready holds, renew eligible loans, place or cancel holds, view fines, and search the catalog. It supports single-card and family-profile workflows through the Helmet CLI with JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on locally stored library card numbers, PINs, and session cookies. <br>
Mitigation: Install only if the user trusts the @helmet-ai/helmet package and keep Helmet configuration files private on the local machine. <br>
Risk: The skill can perform account-changing actions such as renewing loans, placing holds, and canceling holds. <br>
Mitigation: Ask before state-changing actions, especially when shared or family profiles are configured. <br>
Risk: Expired or invalid sessions can cause partial failures across multiple profiles. <br>
Mitigation: Run helmet status with --json before multi-step workflows and stop for user re-authentication if AUTH_REQUIRED is returned. <br>


## Reference(s): <br>
- [Helmet ClawHub listing](https://clawhub.ai/vijaykodam/helmet) <br>
- [vijaykodam publisher profile](https://clawhub.ai/user/vijaykodam) <br>
- [@helmet-ai/helmet npm package](https://www.npmjs.com/package/@helmet-ai/helmet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Helmet CLI commands and JSON-output handling notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the helmet CLI with --json output; requires local Helmet login configuration at ~/.config/helmet/config.json.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
