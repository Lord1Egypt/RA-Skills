## Description: <br>
Query logistics tracking information via the Track123 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Djttt](https://clawhub.ai/user/Djttt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query domestic and international parcel tracking status, list supported carriers, and format shipment updates from Track123. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes a live-looking Track123 credential in config.json. <br>
Mitigation: Replace or delete the bundled config.json before use and configure a user-controlled Track123 API key. <br>
Risk: Tracking numbers and shipment details are sent to Track123 for lookup. <br>
Mitigation: Only query tracking numbers whose disclosure to Track123 is acceptable for the user's privacy and compliance requirements. <br>
Risk: Shipment results are cached locally by default. <br>
Mitigation: Use --no-cache or remove .cache.json when shipment details should not remain on disk. <br>
Risk: The skill depends on axios for outbound API calls. <br>
Mitigation: Review and update dependencies before use in sensitive environments. <br>


## Reference(s): <br>
- [Kuaidi Query on ClawHub](https://clawhub.ai/Djttt/kuaidi-query) <br>
- [Track123](https://www.track123.com/) <br>
- [Track123 API reference](references/track123-api.md) <br>
- [Usage examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [CLI output in text, compact text, or JSON format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Track123 credentials in config.json and may cache shipment query results locally.] <br>

## Skill Version(s): <br>
1.0.3 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
