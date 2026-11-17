## Description:

Geolocates the current Windows machine using the native WinRT Location API through PowerShell 5.1 and returns latitude, longitude, accuracy, and timestamp as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cute-omega](https://clawhub.ai/user/cute-omega)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill when they want an agent to provide a Windows-native way to find the current device location without external API keys or browser access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output can disclose a sensitive physical location through latitude, longitude, accuracy, and timestamp values.

Mitigation: Use the skill only when device location access is intended, keep coordinates private, and share them with reverse-geocoding services only when that disclosure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cute-omega/skills/locate-on-windows)
- [BigDataCloud reverse geocode client](https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=35.6762&longitude=139.6503)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with PowerShell, JSON, and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local device coordinates and accuracy values that should be treated as sensitive location data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
