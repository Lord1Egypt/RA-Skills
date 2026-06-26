## Description: <br>
Search 1+ million free high-quality AI stock photos. Generate up to 240 free AI images daily. No API key, no tokens, no cost. 235+ niches and growing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tompltw](https://clawhub.ai/user/tompltw) <br>

### License/Terms of Use: <br>
NK Images License <br>


## Use Case: <br>
External users, content creators, designers, and developers use this skill to search NK Images for stock-style AI images, request custom generated images when search results are insufficient, and report search or generation quality issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image searches, generation prompts, feedback descriptions, and optional email addresses are sent to NK Images. <br>
Mitigation: Do not include confidential client data, sensitive personal details, or private prompts unless the user intends to share them with NK Images. <br>
Risk: Generated or returned image links may be incorrect if an agent fabricates URLs instead of using API response fields. <br>
Mitigation: Use the `viewUrl`, `downloadUrl`, and `thumbnailUrl` values exactly as returned by the NK Images API. <br>
Risk: Feedback submissions can disclose user issue descriptions or contact information to the service. <br>
Mitigation: Submit feedback only with user consent and include optional email addresses only when the user chooses follow-up. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tompltw/nk-images-search) <br>
- [NK Images](https://nkimages.com) <br>
- [NK Images License](https://nkimages.com/license) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline curl commands, image links, and concise user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NK Images API response URLs directly for viewing and downloading images; may include search results, generation status, quota information, and feedback submission guidance.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
