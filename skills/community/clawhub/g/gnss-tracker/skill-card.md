## Description: <br>
Extracts an IMEI from a device QR code or user input and queries the latest GNSS location for that device. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scow](https://clawhub.ai/user/scow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support operators use this skill to identify smart device QR codes or IMEIs and return the most recent recorded location when they are authorized to locate the device. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IMEIs and returned device locations are sensitive personal data. <br>
Mitigation: Use the skill only for devices the user owns or is explicitly authorized to locate, and limit sharing of raw lookup results. <br>
Risk: The lookup sends the IMEI to an external iwown endpoint and may reveal a device location without clear ownership checks. <br>
Mitigation: Confirm authorization before querying, avoid testing with unrelated IMEIs, and treat the returned address and timestamp as confidential. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scow/gnss-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Plain text location summary or JSON status with record time, address, and raw lookup data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send an IMEI to an external iwown endpoint and may return raw location data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
