## Description: <br>
Newsletter Curation helps agents plan and draft curated newsletters with content sourcing, editorial structure, issue formats, commentary patterns, sending cadence, and subscriber growth guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, marketers, and editorial operators use this skill to curate newsletter issues, select content formats, write value-added commentary, plan sending cadence, and draft growth-oriented distribution material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party inference.sh CLI installer and command workflow. <br>
Mitigation: Install only if the publisher and inference.sh are trusted, and review the installer or use the documented checksum verification path before running commands. <br>
Risk: Generated infsh commands may search external services or publish public social posts. <br>
Mitigation: Review every proposed command before execution, especially x/post-create or any command that could post publicly. <br>
Risk: Newsletter topics, subscriber details, or business plans could be sent to external search or generation apps. <br>
Mitigation: Avoid sending confidential topics, subscriber data, or sensitive business plans to external apps. <br>


## Reference(s): <br>
- [Newsletter Curation on ClawHub](https://clawhub.ai/okaris/newsletter-curation) <br>
- [okaris ClawHub Publisher Profile](https://clawhub.ai/user/okaris) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI Installer](https://cli.inference.sh) <br>
- [inference.sh CLI Checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and newsletter templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include suggested inference.sh commands for content search, image generation, and public social post drafting.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
