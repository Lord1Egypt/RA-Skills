## Description: <br>
Audit and correct LinkedIn experience descriptions for overclaims, fabricated metrics, and inaccuracies using browser automation + LLM accuracy review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to review LinkedIn experience descriptions before job searches, AI-assisted rewrites, reference checks, or background screening. It flags potentially inaccurate claims, asks targeted clarification questions, and helps apply corrected wording through the user's authenticated browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and edit LinkedIn profile content through the user's logged-in browser session. <br>
Mitigation: Install only if comfortable with that automation, keep the browser session local, and review proposed edits before saving. <br>
Risk: Profile descriptions and local review notes may contain sensitive personal career details. <br>
Mitigation: Keep backups of original descriptions and delete local review or memory files when they are no longer needed. <br>
Risk: Automated corrections could still leave inaccurate or misleading career claims if the user provides incomplete context. <br>
Mitigation: Answer targeted clarification questions role by role and manually verify final wording against actual work, ownership, and measured outcomes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/linkedin-profile-audit) <br>
- [LinkedIn experience edit URL pattern](https://www.linkedin.com/in/{profile}/edit/forms/position/{position_id}/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with corrected profile text, local review notes, and Playwright script snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update LinkedIn descriptions in the user's logged-in browser session and write a local fact/data log for later review.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
