## Description: <br>
An intelligent event finder that searches for meetups and events based on your interests, tracks them, and reminds you before they happen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apresmoi](https://clawhub.ai/user/apresmoi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to collect event preferences, find relevant public meetups and events through their configured search and scraping tools, track interesting events, and receive reminders before events they plan to attend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Preference-derived search queries, event page URLs, IP address, and credentials used by configured search or scraping tools may be sent to third-party event or search services. <br>
Mitigation: Install only if this data sharing is acceptable, use trusted search and scraping tools, and avoid adding sensitive personal details to event preferences. <br>
Risk: Optional daily automation can create persistent scheduled tasks for event searches and reminders. <br>
Mitigation: Enable daily searches only when recurring automation is desired, and review scheduler or crontab entries when pausing, changing, or uninstalling the skill. <br>
Risk: The skill stores event interests, location, schedule preferences, tracked events, and reminders locally. <br>
Mitigation: Keep the workspace directory private, review stored files periodically, and delete local preference or event files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/apresmoi/meetup-planner) <br>
- [GitHub Repository](https://github.com/apresmoi/meetup-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces event summaries, local configuration and tracking files, reminder guidance, and scheduled-search setup instructions.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
