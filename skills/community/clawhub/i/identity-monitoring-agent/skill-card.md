## Description: <br>
An OSINT sentinel that monitors the public web for email exposure, username footprint, and identity leaks without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[assix](https://clawhub.ai/user/assix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security and privacy practitioners use this skill to check authorized identifiers for public exposure, account registration signals, username footprints, and leak mentions across public web sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send searched emails, usernames, phone numbers, or other identifiers to external services through third-party OSINT tools. <br>
Mitigation: Use only for owned identities or authorized investigations, review the required packages before installation, and run the tooling in an isolated environment. <br>
Risk: OSINT checks may be affected by rate limits, service terms, or incomplete public-source coverage. <br>
Mitigation: Treat results as investigative leads, confirm findings independently, and respect applicable service terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/assix/identity-monitoring-agent) <br>
- [Publisher profile](https://clawhub.ai/user/assix) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may query third-party OSINT tools and public search services for user-provided identifiers.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
