## Description: <br>
Fetch raw JSON listing payloads from Paragon MLS for parser debugging, source payload inspection, and custom downstream analysis of unprocessed listing data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch raw Paragon MLS listing JSON when parsed MLS fields look wrong, parser behavior needs debugging, or custom analysis requires unnormalized source payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on and builds local MCP code outside the reviewed package. <br>
Mitigation: Install only when you control and trust the configured local paragon-mls-mcp project and have reviewed its dependencies and build scripts. <br>
Risk: Raw MLS listing payloads may contain sensitive or access-controlled listing data. <br>
Mitigation: Use the raw listing tool only for authorized MLS records, and redact raw payloads before logging, sharing, or sending them to downstream tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earlvanze/paragon-mls-raw-listings) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [Raw JSON payloads with concise Markdown guidance and an example shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Raw payload structure may vary across MLS regions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
