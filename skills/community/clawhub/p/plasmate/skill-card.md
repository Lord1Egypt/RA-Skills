## Description:

Browse the web via Plasmate, a fast headless browser engine for agents that compiles HTML into a Semantic Object Model (SOM), supports AWP, and offers CDP compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builder-nc](https://clawhub.ai/user/builder-nc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to browse, extract, and interact with web pages through Plasmate's local AWP workflow or CDP-compatible server mode. It is most useful for speed-sensitive scraping, batch page processing, token-sensitive extraction, and structured data collection when visual browser rendering is not required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer commands can execute remote code or build dependencies that alter the local environment.

Mitigation: Prefer a pinned, signed, or checksum-verified Plasmate release and review installer behavior before running it.

Risk: The helper script may install the websockets Python package at runtime and start a local Plasmate server.

Mitigation: Install dependencies ahead of time in an isolated environment and review process changes before execution.

Risk: AWP or browser interactions can expose sensitive input or perform account-changing actions on visited sites.

Mitigation: Keep connections on 127.0.0.1 unless the server and network are trusted, and require separate confirmation before entering secrets or making state-changing actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/builder-nc/skills/plasmate)
- [Plasmate Homepage](https://plasmate.app)
- [Plasmate Documentation](https://docs.plasmate.app)
- [Plasmate Source Repository](https://github.com/plasmate-labs/plasmate)
- [Plasmate Privacy Policy](https://plasmate.app/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands, Python helper usage, JavaScript CDP examples, and SOM JSON returned by Plasmate commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the plasmate binary and may use a local AWP or CDP server on 127.0.0.1:9222.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
