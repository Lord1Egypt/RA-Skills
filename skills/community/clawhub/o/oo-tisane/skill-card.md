## Description: <br>
Tisane connects an agent to Tisane through the OOMOL oo CLI for text analysis, language detection, translation, paraphrasing, text extraction, similarity scoring, and entity comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tisane language and content-analysis actions through an OOMOL-connected account without handling raw Tisane API tokens directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup instructions include a one-line remote installer for the oo CLI. <br>
Mitigation: Use OOMOL's official installation guide, review the installer before running it, and verify checksums or signatures where available. <br>
Risk: The skill requires an OOMOL-connected Tisane account and server-side credentials. <br>
Mitigation: Install only when the publisher and connected service are trusted, and review requested actions and payloads before execution. <br>


## Reference(s): <br>
- [Tisane homepage](https://tisane.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-tisane) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OOMOL server-side credentials through the oo CLI; action responses may include JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
