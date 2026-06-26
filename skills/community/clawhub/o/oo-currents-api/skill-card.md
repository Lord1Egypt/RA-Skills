## Description: <br>
Currents API lets agents search and read Currents API news data through the OOMOL-connected `currents_api` connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Currents API news data through the OOMOL `currents_api` connector, including latest news, article search, supported categories, languages, and regions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary marks the release suspicious and reports high-impact moderation commands plus a review helper that can run nested Codex with full access by default. <br>
Mitigation: Install only in trusted maintainer or development environments, disable YOLO autoreview unless full local access is intentional, and check the exact target, reason, credentials, and audit expectations before moderation commands run. <br>
Risk: The skill requires sensitive credentials through the connected Currents API account. <br>
Mitigation: Use the OOMOL-managed connector path rather than handling raw API tokens, and reconnect credentials only when an auth or connection error requires it. <br>


## Reference(s): <br>
- [Currents API homepage](https://currentsapi.services) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-currents-api) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to inspect live connector schemas before running read-only Currents API actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
