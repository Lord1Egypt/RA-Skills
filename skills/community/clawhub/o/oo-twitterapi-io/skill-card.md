## Description: <br>
TwitterAPI.io connector skill for querying X/Twitter data and managing TwitterAPI.io monitoring and filter-rule state through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect TwitterAPI.io connector schemas, run account-backed X/Twitter lookups, and manage monitoring or filter rules after user confirmation for state-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected TwitterAPI.io account. <br>
Mitigation: Install only when the agent should use that account, and rely on server-injected credentials rather than exposing raw tokens. <br>
Risk: Monitoring and filter-rule actions can change or remove TwitterAPI.io state. <br>
Mitigation: Confirm the exact payload, target, and expected effect with the user before any write or destructive action. <br>
Risk: Setup commands can install or authenticate the oo CLI. <br>
Mitigation: Run setup or authentication steps only after a command fails with the matching install, auth, connection, or billing error. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-twitterapi-io) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [TwitterAPI.io Homepage](https://twitterapi.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector command responses are JSON when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
