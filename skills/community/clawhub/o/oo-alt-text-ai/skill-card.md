## Description: <br>
AltText.ai (alttext.ai). Use this skill for ANY AltText.ai request - reading, creating, updating, and deleting data. Whenever a task involves AltText.ai, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and operators use this skill to manage AltText.ai image records and generate alt text through an OOMOL-connected account without handling raw API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting AltText.ai through OOMOL and uses account credentials through the oo CLI. <br>
Mitigation: Before installation, confirm the user is comfortable with the OOMOL connection and the AltText.ai credential posture. <br>
Risk: Image creation and deletion actions change the user's AltText.ai library. <br>
Mitigation: Review the exact payload, target asset, and expected effect with the user before approving write or destructive actions. <br>
Risk: Create and scrape actions may submit public image URLs or page content for alt-text generation. <br>
Mitigation: Confirm the source URLs or HTML scope are intended for processing before running create_image or scrape_page. <br>


## Reference(s): <br>
- [AltText.ai homepage](https://alttext.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
