## Description: <br>
Zotero Scholar saves paper metadata, links, optional abstracts, tags, and AI-generated summaries into a user's Zotero library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Little-Cat1](https://clawhub.ai/user/Little-Cat1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research assistants use this skill to add paper records, summaries, tags, and arXiv PDF attachments to a Zotero library from command-line inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Zotero API key that can add library items and attachments. <br>
Mitigation: Use a minimally scoped Zotero key and install only if account writes are acceptable. <br>
Risk: ZOTERO_CREDENTIALS contains sensitive account access material. <br>
Mitigation: Keep ZOTERO_CREDENTIALS out of logs, shared terminals, screenshots, and committed files. <br>
Risk: User-supplied URLs and AI-generated summaries are written into Zotero records. <br>
Mitigation: Run the skill only with trusted paper URLs and reviewed summary text. <br>


## Reference(s): <br>
- [Zotero](https://www.zotero.org) <br>
- [ClawHub release page](https://clawhub.ai/Little-Cat1/openclaw-zotero-scholar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and ZOTERO_CREDENTIALS in userid:apiKey format; writes user-supplied paper information to Zotero through the Zotero API.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence, created 2026-03-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
