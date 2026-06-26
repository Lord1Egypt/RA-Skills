## Description: <br>
Maker Hunter helps agents find likely vibe-coding founders across technical communities, review candidate profiles, score fit, and draft personalized outreach messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robinc913](https://clawhub.ai/user/robinc913) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Community builders, recruiters, and founder-facing teams use this skill to discover independent developers or early-stage makers, filter out weak matches, and prepare personalized Chinese or English outreach drafts. It is intended for reviewed outreach workflows rather than unattended messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt users to provide raw platform cookies or automate logged-in social accounts. <br>
Mitigation: Use only accounts you are willing to automate, avoid sharing raw cookies or session tokens, prefer interactive login or scoped APIs, and periodically delete stored credentials. <br>
Risk: Collected candidate details and daily history are stored locally without clear privacy safeguards in the artifact. <br>
Mitigation: Review what is collected, keep only necessary candidate data, delete stale memory files, and handle profile data according to applicable privacy and outreach policies. <br>
Risk: Automated outreach drafts can be inaccurate, overly intrusive, or noncompliant with platform expectations. <br>
Mitigation: Manually review every candidate and message before contact, verify profile evidence, and adjust or discard drafts that are not appropriate. <br>


## Reference(s): <br>
- [DM template guide](references/dm-guide.md) <br>
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0/) <br>
- [ClawHub skill page](https://clawhub.ai/robinc913/maker-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with JSON-shaped candidate records and personalized message drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes platform, username, profile or post links, match score, profile review notes, and complete DM content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
