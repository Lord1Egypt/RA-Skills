## Description: <br>
Pear Apple lets agents manage iCloud calendars, reminders, contacts, daily briefings, and AI-assisted scheduling through Pear using CalDAV and CardDAV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AshtonAU](https://clawhub.ai/user/AshtonAU) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent read and update their iCloud Calendar, Reminders, and Contacts through Pear-backed tools. It supports schedule review, event and reminder management, contact lookup and updates, daily briefings, and meeting-time suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive iCloud calendars, reminders, and contacts. <br>
Mitigation: Install only when the user accepts Pear-backed read and write access to those data types. <br>
Risk: Delete and batch operations can permanently remove or change personal data. <br>
Mitigation: Confirm destructive or bulk actions with the user, including item names and counts, before execution. <br>
Risk: PEAR_API_KEY grants access to Pear-backed tools. <br>
Mitigation: Store PEAR_API_KEY only as a secret environment variable and never reveal it in agent output. <br>
Risk: A custom PEAR_MCP_URL or untrusted contact-photo URL can route data to an untrusted endpoint. <br>
Mitigation: Use the default Pear endpoint unless the replacement is trusted, and avoid untrusted or internal URLs for contact photos. <br>


## Reference(s): <br>
- [Pear Documentation](https://pearmcp.com/docs) <br>
- [Pear Homepage](https://pearmcp.com) <br>
- [Apple App-Specific Passwords](https://support.apple.com/en-us/102654) <br>
- [CalDAV Protocol (RFC 4791)](https://www.rfc-editor.org/rfc/rfc4791) <br>
- [CardDAV Protocol (RFC 6352)](https://www.rfc-editor.org/rfc/rfc6352) <br>
- [IANA Time Zone Database](https://www.iana.org/time-zones) <br>
- [ClawHub Skill Page](https://clawhub.ai/AshtonAU/pear-apple) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration] <br>
**Output Format:** [Markdown instructions with tool-reference tables and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PEAR_API_KEY and network access to pearmcp.com.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
