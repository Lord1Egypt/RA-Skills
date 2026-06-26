## Description: <br>
A browser automation CLI for AI agents that uses a persistent Chromium instance to manage tabs, preserve sessions, map page elements to interaction tags, and extract web content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaThanMiThun1999](https://clawhub.ai/user/MaThanMiThun1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to drive Chromium through shell commands for web navigation, tagged interaction, session reuse, multi-tab workflows, and content extraction from complex sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent login sessions and exported cookies can retain sensitive account access after automation finishes. <br>
Mitigation: Use a dedicated non-sensitive browser profile in an isolated environment and delete chrome_profile, session.json, recordings, and learning files when finished. <br>
Risk: The skill supports arbitrary in-page JavaScript through eval. <br>
Mitigation: Review every eval script before running it and only use scripts from trusted sources. <br>
Risk: Bot-evasion behavior and automatic confirmations can automate sites in ways that may violate permissions or policies. <br>
Mitigation: Only automate sites where the user has permission and avoid important accounts or unauthorized access workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MaThanMiThun1999/god-of-all-browsers) <br>
- [Puppeteer documentation](https://pptr.dev/) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, CLI text output, JSON-like tag maps, screenshots, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses persistent browser profile, session files, recordings, and optional in-page JavaScript execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact package metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
