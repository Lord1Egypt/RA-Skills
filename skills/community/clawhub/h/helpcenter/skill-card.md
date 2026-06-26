## Description: <br>
Helps agents create, update, search, publish, unpublish, and organize Help.Center help center articles through the Help.Center API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shyjal](https://clawhub.ai/user/shyjal) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Support, documentation, and developer-facing teams use this skill to draft, revise, search, publish, and organize knowledge base articles in Help.Center through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API credentials may grant broad access to Help.Center content. <br>
Mitigation: Use the narrowest API key scopes needed and avoid publish or delete permissions unless the task requires them. <br>
Risk: Drafts, publications, deletions, or category changes can alter customer-facing help center content. <br>
Mitigation: Confirm ambiguous requests, default to drafts, and review changes before approving publication or destructive actions. <br>
Risk: Uploaded media or SVG content may introduce unsafe or unwanted assets into articles. <br>
Mitigation: Sanitize SVG and uploaded media before use, and review generated article HTML before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shyjal/helpcenter) <br>
- [Publisher profile](https://clawhub.ai/user/shyjal) <br>
- [Help.Center API base URL](https://api.help.center) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, HTML, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash/curl examples, JSON request bodies, and HTML article content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Help.Center API key and Center ID supplied by the user at runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
