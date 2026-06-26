## Description: <br>
Convert Markdown files to properly formatted Google Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, writers, and operators use this skill to convert local Markdown documents into Google Docs while preserving headings, bold text, code blocks, lists, links, blockquotes, and tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The document may be created under the wrong Google account or Drive folder. <br>
Mitigation: Confirm the authenticated gog account before use and pass --account and --parent when the destination matters. <br>
Risk: Markdown content intended to stay local may be uploaded to Google Docs and Drive. <br>
Mitigation: Convert only Markdown files intended for storage in the selected Google Workspace account. <br>
Risk: An untrusted or over-permissioned gog installation could expose Google Workspace access. <br>
Mitigation: Install gog only from a trusted source and review its Google permissions before authenticating. <br>


## Reference(s): <br>
- [gog Google Workspace CLI](https://github.com/tychohq/gog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and a Google Doc URL on successful conversion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated gog CLI session and a Markdown input file.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
