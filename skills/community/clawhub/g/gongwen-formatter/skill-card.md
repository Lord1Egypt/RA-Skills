## Description: <br>
Converts Markdown documents into Word .docx files formatted for the GB/T 9704-2012 Chinese official-document layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to turn generated or supplied Markdown reports into standardized Word documents with government-style page, font, heading, table, link, image, and list formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports that Markdown image URLs are fetched automatically without network or size safeguards. <br>
Mitigation: Use this skill only with Markdown you control or trust, or run it with restricted outbound network access until image fetching is constrained by allowlists, private-network blocking, and download size limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edwardwason/gongwen-formatter) <br>
- [Publisher profile](https://clawhub.ai/user/edwardwason) <br>
- [Project homepage from artifact metadata](https://github.com/EdwardWason/official-doc) <br>


## Skill Output: <br>
**Output Type(s):** [files, text] <br>
**Output Format:** [Word .docx file plus a success flag and output path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts Markdown content and an output path; supported Markdown includes headings, paragraphs, lists, tables, links, images, bold, italic, and code blocks.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
