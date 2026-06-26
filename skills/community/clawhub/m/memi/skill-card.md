## Description: <br>
Personal CRM and relationship intelligence. Extracts contacts from conversations, tracks commitments, detects cooling relationships, delivers morning briefs, preps you before meetings, and gets smarter about your relationships the more you use it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mukund2](https://clawhub.ai/user/Mukund2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use Memi to maintain a local personal CRM, remember relationship context, track commitments, prepare for meetings, and receive timely follow-up suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain broad relationship profiles, commitments, preferences, and inferred behavior patterns in a long-lived local database. <br>
Mitigation: Install only when local retention of relationship data is intended, and periodically review or remove stored contacts, notes, and inferred patterns that are no longer needed. <br>
Risk: Optional Google integrations can scan or use Gmail, Calendar, and Contacts data. <br>
Mitigation: Verify the gog tool source and OAuth scopes before enabling it, and require explicit approval before email, calendar, or contact data is scanned or used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mukund2/memi) <br>
- [Publisher profile](https://clawhub.ai/user/Mukund2) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Concise natural-language responses with occasional markdown and shell commands when setup or local database actions are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses sqlite3 for local storage and can optionally use gog for Google Calendar, Gmail, and Contacts integration.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
