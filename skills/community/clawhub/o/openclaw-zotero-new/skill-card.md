## Description: <br>
Zotero Scholar saves paper metadata, links, tags, abstracts, and optional summaries to a Zotero library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Little-Cat1](https://clawhub.ai/user/Little-Cat1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to add papers to a Zotero library from command-line metadata, with optional abstracts, tags, summaries, and arXiv PDF attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write items, notes, and attachments to the user's Zotero library using a Zotero API key. <br>
Mitigation: Use a least-privilege Zotero API key and review the intended paper metadata before running the skill. <br>
Risk: Paper details, summaries, and downloaded PDFs may be stored in Zotero. <br>
Mitigation: Avoid using the skill with sensitive unpublished papers unless storing that content in Zotero is intended. <br>
Risk: Some setup paths use remote shell installers for uv. <br>
Mitigation: Review the installer source or use a trusted package-manager installation path when available. <br>


## Reference(s): <br>
- [Zotero](https://www.zotero.org) <br>
- [uv install script for Linux](https://astral.sh/uv/install.sh) <br>
- [uv install script for Windows](https://astral.sh/uv/install.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and ZOTERO_CREDENTIALS; may create Zotero library items, notes, and arXiv PDF attachments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
