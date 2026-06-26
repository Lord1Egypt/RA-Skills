## Description: <br>
Track parcels locally with parcelcli for Evri, Royal Mail, UPS, FedEx, and DHL. Use when the user asks to track a package, detect a carrier, check delivery status, watch a parcel, or summarize courier tracking without sending tracking data to third-party aggregators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cavit99](https://clawhub.ai/user/cavit99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track parcels with a local parcelcli installation, detect carriers, summarize normalized tracking status, and manage local delivery watches without sending tracking data to third-party aggregators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external local parcelcli Go module and browser-driven carrier pages. <br>
Mitigation: Install only if the external module is trusted, keep Chrome available or provide a Chrome path, and retry timeouts or WAF failures once later rather than looping. <br>
Risk: Tracking numbers, postcodes, and saved parcel watches can expose delivery information. <br>
Mitigation: Provide tracking numbers and postcodes only for parcels the user wants checked, do not infer postcodes from memory, keep watch state local, and remove saved watches when monitoring is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cavit99/parcelcli) <br>
- [parcelcli homepage](https://github.com/cavit99/parcelcli) <br>
- [Go install module](github.com/cavit99/parcelcli/cmd/parcelcli@v1.0.3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and summarized JSON fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should use normalized parcel status fields and avoid raw carrier page text.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
