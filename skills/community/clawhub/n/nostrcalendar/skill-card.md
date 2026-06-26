## Description: <br>
Time awareness for sovereign entities: manage availability, book meetings, and negotiate schedules over Nostr relays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vveerrgg](https://clawhub.ai/user/vveerrgg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to give an agent calendar capabilities over Nostr relays, including publishing availability, checking free slots, booking meetings, and negotiating meeting times. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: NOSTR_NSEC is a sensitive private key used to sign calendar events. <br>
Mitigation: Use a dedicated Nostr key for the calendar identity and keep it out of logs, hardcoded examples, and shared shells. <br>
Risk: Nostr relays may expose scheduling metadata such as times and participant public keys even when event details are encrypted. <br>
Mitigation: Choose trusted relays and avoid placing sensitive information in public calendar metadata. <br>
Risk: The workflow installs and uses the third-party nostrcalendar Python package. <br>
Mitigation: Install only if the package source is trusted and review the package before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vveerrgg/nostrcalendar) <br>
- [NostrCalendar source repository](https://github.com/HumanjavaEnterprises/nostrcalendar.app.OC-python.src) <br>
- [NostrCalendar PyPI package](https://pypi.org/project/nostrcalendar/) <br>
- [NIP-52 calendar events](https://github.com/nostr-protocol/nips/blob/master/52.md) <br>
- [NostrKey prerequisite skill](https://clawhub.ai/vveerrgg/nostrkey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.2.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
