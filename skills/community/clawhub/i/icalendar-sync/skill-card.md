## Description: <br>
Secure iCloud Calendar operations for OpenClaw with CalDAV and macOS native bridge providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h8kxrfp68z-lgtm](https://clawhub.ai/user/h8kxrfp68z-lgtm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to let agents list, retrieve, create, update, and delete iCloud Calendar events, including recurring event changes, through CalDAV or the macOS Calendar bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make irreversible calendar changes, including event deletes and recurring event updates. <br>
Mitigation: Require the agent to show the event details and obtain explicit user approval before delete operations or recurring update modes. <br>
Risk: Credential handling can expose sensitive iCloud access if secrets are stored or logged carelessly. <br>
Mitigation: Use an app-specific iCloud password, prefer system keyring storage, and use file storage only with strict permissions in trusted runtimes. <br>
Risk: Debug HTTP output and custom CalDAV endpoints can reveal sensitive diagnostics or send credentials to an untrusted service. <br>
Mitigation: Keep debug output private, leave ICALENDAR_SYNC_CALDAV_URL unset unless the endpoint is trusted, and review logs before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h8kxrfp68z-lgtm/icalendar-sync) <br>
- [README](artifact/README.md) <br>
- [Security policy](artifact/SECURITY.md) <br>
- [Apple ID app-specific passwords](https://appleid.apple.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON event payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent actions may read or modify external calendar data through iCloud credentials.] <br>

## Skill Version(s): <br>
2.4.1 (source: evidence release metadata and changelog, released 2026-03-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
