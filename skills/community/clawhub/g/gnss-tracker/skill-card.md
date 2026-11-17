## Description:

Identifies smart-device QR codes, extracts an IMEI, and queries the device's latest known GNSS location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scow](https://clawhub.ai/user/scow)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to decode a device QR code or supplied IMEI and return the device's most recent recorded address and timestamp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query sensitive device location by arbitrary IMEI through a third-party service without clear consent or ownership checks.

Mitigation: Use only where there is clear authority to locate the device and its user; require confirmation of ownership or authorization before querying.

Risk: IMEIs are sent to search.iwown.com and location output may expose address and timestamp data.

Mitigation: Disclose the external service before use and return only the minimum location fields needed for the task.

## Reference(s):

- [IWOWN GNSS latest-location API endpoint](https://search.iwown.com/hpmservice/ai/vendor/gnss/latest?deviceid={imei})
- [ClawHub skill page](https://clawhub.ai/scow/skills/gnss-tracker)
- [Publisher profile](https://clawhub.ai/user/scow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance and JSON-formatted location query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful lookups include status, record_time, address, and raw provider data; unsuccessful lookups return an error status and message.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
