## Description: <br>
People Data Labs lets an agent search and enrich person and company data through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business data teams use this skill to search People Data Labs people and company datasets, or enrich individual person and company records, through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected account and can access credentialed People Data Labs data through the oo CLI. <br>
Mitigation: Install only when the publisher is trusted, inspect the live connector schema before each run, and review payloads before execution. <br>
Risk: The release security verdict is suspicious, with guidance that some workflows can use existing CLI credentials and make real changes. <br>
Mitigation: Follow the release security guidance, avoid full-access automated review modes unless intentionally enabled, and require explicit confirmation before any write or destructive action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-peopledatalabs) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/oomol) <br>
- [People Data Labs homepage](https://www.peopledatalabs.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, an authenticated OOMOL account, and a connected People Data Labs credential.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
