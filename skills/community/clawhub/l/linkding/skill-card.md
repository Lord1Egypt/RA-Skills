## Description: <br>
Manage bookmarks with Linkding via the Linkding REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmagar](https://clawhub.ai/user/jmagar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to search, create, update, archive, delete, tag, and organize bookmarks in a Linkding instance from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Linkding API token that can access the user's bookmark data. <br>
Mitigation: Install only if the publisher is trusted, use the narrowest Linkding token available, and store credentials only in the documented config file or environment variables. <br>
Risk: Update, archive, delete, and bundle-delete commands can change or remove bookmark data. <br>
Mitigation: Confirm bookmark or bundle IDs before executing mutating commands, and review returned JSON where available. <br>


## Reference(s): <br>
- [Linkding Skill Page](https://clawhub.ai/jmagar/linkding) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; Linkding API helper responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Linkding base URL and API token. Some commands modify or delete server-side bookmark data.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
