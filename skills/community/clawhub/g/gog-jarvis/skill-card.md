## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingze00000](https://clawhub.ai/user/bingze00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to set up and use the gog CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows through an authorized Google account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires installing and trusting the external gog CLI package. <br>
Mitigation: Install only from a trusted source, verify the package before use, and keep the CLI updated according to the publisher's guidance. <br>
Risk: OAuth authorization can grant access to sensitive Gmail, Calendar, Drive, Contacts, Sheets, and Docs data. <br>
Mitigation: Review requested Google OAuth scopes, authorize only the intended account and services, and revoke access when it is no longer needed. <br>
Risk: Generated commands can send email, create events, update contacts, or modify Drive, Sheets, or Docs content. <br>
Mitigation: Require explicit approval before executing data-changing commands and prefer dry-run, read-only, JSON, or no-input modes when validating workflows. <br>


## Reference(s): <br>
- [Gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub release page](https://clawhub.ai/bingze00000/gog-jarvis) <br>
- [Publisher profile](https://clawhub.ai/user/bingze00000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides OAuth setup and gog CLI usage; commands may read or modify authorized Google Workspace data when executed by the user or agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
