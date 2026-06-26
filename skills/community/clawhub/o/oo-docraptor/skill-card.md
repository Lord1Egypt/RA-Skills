## Description: <br>
DocRaptor helps agents create hosted PDF or Excel documents from raw HTML or public URLs through an OOMOL-connected DocRaptor account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to create DocRaptor-hosted PDF or Excel documents from HTML content or a public URL without handling raw DocRaptor credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or invoking the external oo CLI can introduce supply-chain and local execution risk. <br>
Mitigation: Prefer the official install guide or inspect the installer before running it, install only from a trusted OOMOL CLI source, and avoid elevated privileges unless official documentation requires them. <br>
Risk: The create_hosted_document action changes DocRaptor state by creating a hosted PDF or Excel document. <br>
Mitigation: Fetch the live connector schema before building the payload and confirm the exact payload and expected effect with the user before running the write action. <br>


## Reference(s): <br>
- [DocRaptor homepage](https://docraptor.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-docraptor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON payload expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include DocRaptor-hosted document download URLs returned by oo CLI connector responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
