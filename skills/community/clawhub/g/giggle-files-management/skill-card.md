## Description: <br>
Upload files to Giggle asset service and get public/download URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload local files to the Giggle asset service and return public or download URLs when a user asks to host, view, or share a file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files uploaded through this skill are publicly hosted, and broad upload instructions could expose private or sensitive content. <br>
Mitigation: Upload only files explicitly intended for public hosting, avoid secrets or confidential documents, and confirm the target file and API key before running the upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patches429/giggle-files-management) <br>
- [Giggle API](https://api.giggle.pro) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON from the upload script with Markdown links for user-facing previews or downloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a Giggle asset service API key; uploaded files are intended to be publicly accessible.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
