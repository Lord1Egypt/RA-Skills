## Description: <br>
Tally (tally.so). Use this skill for Tally requests that search, list, and read forms or submissions through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect Tally schemas and run read-only connector actions for forms and submissions through the OOMOL oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned Tally submissions may contain personal or business-sensitive data. <br>
Mitigation: Treat connector responses as sensitive and limit sharing, logging, and storage to the user's intended workflow. <br>
Risk: First-time setup may install or authenticate the OOMOL oo CLI and connect a Tally account. <br>
Mitigation: Run setup commands only after an auth or connection failure and only when the user trusts OOMOL's installer and account connection flow. <br>


## Reference(s): <br>
- [ClawHub Tally Skill](https://clawhub.ai/oomol/oo-tally) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Tally Homepage](https://tally.so) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; returned form submissions may contain sensitive personal or business data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
