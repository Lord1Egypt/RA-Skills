## Description: <br>
L2S (l2s.is) lets an agent read, create, and update shortened-link data through an OOMOL-connected L2S account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage L2S shortened links from an agent session, including retrieving stored link details, creating shortened URLs, and updating link metadata after reviewing write payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an OOMOL-connected L2S account. <br>
Mitigation: Install it only when the agent is expected to use that account, and review account connection or authentication failures before retrying. <br>
Risk: Write actions can create or update short links with unintended destinations, custom keys, titles, or UTM tags. <br>
Mitigation: Review the exact payload and intended effect before running create or update actions. <br>
Risk: Connector input contracts may change over time. <br>
Mitigation: Inspect the live action schema before constructing a payload for an L2S action. <br>


## Reference(s): <br>
- [ClawHub L2S skill page](https://clawhub.ai/oomol/oo-l2s) <br>
- [L2S homepage](https://www.l2s.is) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target the OOMOL oo CLI and may return JSON responses from L2S connector actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
