## Description: <br>
Monitor LinkedIn threads where the user commented for author replies and inbound signals, flag high-value follow-up windows, draft responses, and optionally route dormant warm threads to DM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators, creators, and growth teams use this skill to monitor recent LinkedIn comment threads, identify author replies and inbound-quality signals, prioritize timely public follow-ups, and draft thread-specific responses or DMs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LinkedIn profile and comment activity may be sent to external services. <br>
Mitigation: Verify what HarvestAPI, Publora, and linkedin-reply-handler receive, store, and can do with account data before connecting real LinkedIn or publishing accounts. <br>
Risk: Reply drafting can delegate to a backend that may auto-post without an explicit approval gate. <br>
Mitigation: Use a manual copy-paste backend unless automated posting is explicitly intended, and require approval for every public reply or DM. <br>


## Reference(s): <br>
- [Thread Timing Matrix](references/thread-timing.md) <br>
- [ClawHub release page](https://clawhub.ai/sergebulaev/linkedin-thread-engagement) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown reports with thread classifications, priorities, suggested responses, and DM guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference LinkedIn profile URLs, post URLs, author-reply timing, inbound-quality signals, and downstream reply-drafting behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
