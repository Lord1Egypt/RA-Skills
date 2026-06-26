## Description: <br>
Geolocates the current Windows machine with the native WinRT Location API through PowerShell 5.1, producing latitude, longitude, accuracy, and timestamp JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cute-omega](https://clawhub.ai/user/cute-omega) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Windows users and support or developer agents use this skill when a user explicitly asks for device-based geolocation on Windows. It helps return local coordinates and accuracy without an external API key or browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Device latitude and longitude are sensitive personal data. <br>
Mitigation: Run the skill only after the user clearly asks for device geolocation, avoid sharing exact coordinates unnecessarily, and reduce precision before pasting results into chats, logs, tickets, or third-party services. <br>
Risk: The PowerShell script accesses Windows location services and may fail or return coarse results when permission, hardware, WiFi, or policy support is unavailable. <br>
Mitigation: Use it on Windows 10 or later with Windows PowerShell 5.1, confirm Location is enabled, and treat low-accuracy or error JSON as a signal to troubleshoot rather than as a precise location. <br>


## Reference(s): <br>
- [BigDataCloud reverse geocode client](https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=35.6762&longitude=139.6503) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with PowerShell, bash, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns latitude, longitude, accuracy in meters, timestamp, and structured error fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
