## Description: <br>
Svix helps agents read, create, update, and delete Svix data through an OOMOL-connected account using the oo CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Svix applications, endpoints, event types, and messages from an agent workflow. It supports read operations as well as confirmed write and destructive actions against a connected Svix account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected account and sensitive credentials are injected server-side. <br>
Mitigation: Use it only in environments where the OOMOL account and Svix connection are approved, and avoid exposing raw credentials in prompts, files, or logs. <br>
Risk: Write actions can create or update Svix applications, endpoints, event types, and messages. <br>
Mitigation: Fetch the live action schema first, review the exact JSON payload and expected effect, and obtain user confirmation before running write actions. <br>
Risk: Destructive actions can delete Svix applications or endpoints. <br>
Mitigation: Confirm the target application or endpoint identifier explicitly with the user before running destructive commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-svix) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Svix Homepage](https://www.svix.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before running actions and returns connector responses as JSON when commands are executed with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
