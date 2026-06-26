## Description: <br>
Retrieves Amazon seller policy, regulation, and news feed items by marketplace and time window, then fetches the full Markdown article for a selected record. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and agents use this skill to review official Amazon seller policy and compliance updates, filter recent items by marketplace and date, and open the full source article when more detail is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically submit user feedback or inferred intent to a separate LinkFox endpoint. <br>
Mitigation: Install only when this telemetry behavior is acceptable and disclose or control feedback submission according to the deployment environment. <br>
Risk: The skill requires a LinkFox API key and may persist large API responses to disk when using the helper workflow. <br>
Mitigation: Store credentials in the documented environment variable, use temporary output directories for persisted responses, and remove saved response files after use. <br>
Risk: Feed data may lag the live Amazon source. <br>
Mitigation: Treat linked Amazon originals as authoritative when making compliance or operational decisions. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-amazon-policy-feed) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Guidance] <br>
**Output Format:** [Structured JSON feed records and Markdown article detail] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [List responses include titles, Chinese AI summaries, original URLs, publish times, and record IDs; detail responses return Markdown article bodies.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
