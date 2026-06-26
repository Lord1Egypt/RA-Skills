## Description: <br>
Uploads self-contained HTML games, apps, or generative art to PaperBox and returns a shareable link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felixdaga](https://clawhub.ai/user/felixdaga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to publish AI-generated HTML games, apps, and generative art to PaperBox, then share the returned live URL with users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload generated HTML to PaperBox without a clear final confirmation. <br>
Mitigation: Require explicit user confirmation before upload and review the HTML for secrets or private content. <br>
Risk: Published projects receive shareable links, so visibility, retention, and deletion expectations may affect sensitive work. <br>
Mitigation: Check PaperBox visibility, retention, and deletion behavior before publishing private or commercial content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/felixdaga/paperbox) <br>
- [PaperBox](https://paperbox-beta.vercel.app) <br>
- [PaperBox Games API](https://paperbox-beta.vercel.app/api/games) <br>
- [PaperBox login](https://paperbox-beta.vercel.app/login) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Text response containing the shareable URL, with JSON parsed from the PaperBox API response.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PaperBox API key and outbound network access; uploads complete HTML content to PaperBox.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
