## Description: <br>
API2PDF converts raw Markdown into PDF output through an OOMOL-connected API2PDF account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert Markdown content into PDF files and receive the generated PDF URL plus conversion metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PDF-generation action is presented as an untagged read, but it may send provided Markdown to API2PDF through OOMOL. <br>
Mitigation: Treat markdown_to_pdf as an external conversion action, review the payload before execution, and avoid confidential content unless the connected service and account setup are acceptable. <br>
Risk: The skill requires connected account credentials and service access. <br>
Mitigation: Use the server-managed OOMOL connection flow and avoid exposing raw API keys or tokens in prompts, files, or command arguments. <br>


## Reference(s): <br>
- [ClawHub API2PDF listing](https://clawhub.ai/oomol/oo-api2pdf) <br>
- [API2PDF homepage](https://www.api2pdf.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL connection setup for API2PDF](https://console.oomol.com/app-connections?provider=api2pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON response expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The connector action returns a generated PDF URL and conversion metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
