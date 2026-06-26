## Description: <br>
Browserbase (browserbase.com). Use this skill for Browserbase requests that read, create, update, or delete Browserbase data through the OOMOL connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Browserbase projects, sessions, contexts, and usage through an OOMOL-connected account. It supports read operations, state-changing session and context creation, credential refresh, and context deletion with confirmation guidance for write and destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Browserbase account and sensitive credentials are handled by the OOMOL connection. <br>
Mitigation: Install only when you trust the publisher and intend to operate Browserbase through the connected account. <br>
Risk: Write and destructive actions can create sessions or contexts, refresh upload credentials, request session release, or delete Browserbase contexts. <br>
Mitigation: Confirm the exact payload, target identifiers, and expected effect with the user before running write or destructive actions. <br>
Risk: The authoritative security verdict is suspicious and recommends review before use. <br>
Mitigation: Review the skill and security guidance before deployment, and restrict use to the intended account and maintenance workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-browserbase) <br>
- [Browserbase Homepage](https://www.browserbase.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON when actions are run with the documented --json flag.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
