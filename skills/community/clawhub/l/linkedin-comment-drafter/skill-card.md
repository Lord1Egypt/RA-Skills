## Description: <br>
Drafts high-quality LinkedIn comment options from a post URL, selects a reaction type, and waits for user approval before optional posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to draft concise, voice-aware LinkedIn comments from post URLs, compare 1-3 variants, and approve a reaction/comment before publishing or copying manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved drafts and target LinkedIn URLs may be passed to Publora or a configured custom poster. <br>
Mitigation: Use manual mode unless automated posting is intended, and configure only Publora credentials or custom poster commands that the user trusts. <br>
Risk: Generated comments can affect a user's public LinkedIn reputation if they are inaccurate, off-brand, or posted to the wrong target. <br>
Mitigation: Review the selected draft, target URL, reaction type, and posting mode before approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sergebulaev/linkedin-comment-drafter) <br>
- [Publisher profile](https://clawhub.ai/user/sergebulaev) <br>
- [Comment templates](references/comment-templates.md) <br>
- [Voice rules](references/voice-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown approval prompt with draft comment variants, reaction suggestion, template labels, rationale, and optional posting result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft comments target 200-350 characters, use 1-2 short paragraphs, and require approval before posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
