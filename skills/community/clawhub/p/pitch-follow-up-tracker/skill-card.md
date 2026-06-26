## Description: <br>
Track outreach pitches and draft contextual follow-up emails by checking a Google Sheet or markdown tracker, reviewing Gmail activity, flagging stale pitches, and drafting tiered follow-ups that reference the original pitch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexa853](https://clawhub.ai/user/alexa853) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Talent managers, PR professionals, agency teams, sales reps, and other outbound campaign operators use this skill to review pitch status, identify contacts who have not replied, and prepare contextual follow-up drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect sensitive Gmail messages, drafts, full email threads, pitch tracker data, and recent memory or off-channel context. <br>
Mitigation: Run it only on accounts and trackers the user approves, and limit contacts, date ranges, Gmail searches, draft access, thread reads, and memory/context sources before use. <br>
Risk: Generated follow-up drafts may be inaccurate, overly broad, or inappropriate for the relationship. <br>
Mitigation: Review and personalize every draft before creating it in Gmail or sending it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown outreach report with draft email text and optional Gmail draft creation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Gmail account, pitch tracker, sender details, and explicit approval before creating Gmail drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
