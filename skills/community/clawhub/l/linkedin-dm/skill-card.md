## Description:

Sends AI-personalized LinkedIn direct messages to existing 1st-degree connections via browser automation, using a provided contact list, approved pitch, profile-based opener, and outreach status tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[10madh](https://clawhub.ai/user/10madh)

### License/Terms of Use:


## Use Case:

External users and business teams use this skill to message existing LinkedIn connections with personalized outreach for lead nurturing, event follow-up, reconnection, or announcements. The skill helps prepare profile-aware openers, reuse an approved pitch, send messages through the browser, and track outreach status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send LinkedIn messages from the user's authenticated account.

Mitigation: Require explicit approval of the pitch and full batch preview before sending, keep per-message review available, and stop immediately if LinkedIn warns about messaging rate.

Risk: The skill reads LinkedIn profile information and can store identifiable outreach records.

Mitigation: Store only necessary outreach fields, limit retention of full message text and relationship notes, and use a controlled Google Sheet or local file with appropriate access controls.

Risk: The security summary flags anti-detection guidance and broad personal-data logging.

Mitigation: Review platform-policy, anti-spam, and privacy compliance before installing or running the skill.

## Reference(s):

- [Browser Automation Workflow](references/browser-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/10madh/skills/linkedin-dm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with personalized message drafts, browser action steps, and optional Google Sheets shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one personalized opener and one approved pitch message per contact, with outreach status records for Google Sheets or a local JSON sidecar.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
