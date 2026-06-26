## Description: <br>
Safety for AI agents. Real-time threat classification to detect malicious content before it causes agents harm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samidh](https://clawhub.ai/user/samidh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use Ironclaw to classify skill files, direct messages, outbound data, and shell commands before taking higher-risk actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Content submitted for classification is sent to Ironclaw's remote API. <br>
Mitigation: Redact secrets, private conversations, proprietary data, and account details before submitting content. <br>
Risk: Ironclaw API keys may grant higher request limits if exposed. <br>
Mitigation: Protect any Ironclaw API key and avoid sharing it in prompts, logs, or skill files. <br>
Risk: Classifier results may be uncertain or incomplete. <br>
Mitigation: Use Ironclaw as an additional safety layer and manually review low-confidence or high-impact decisions. <br>
Risk: Future skill updates could change behavior. <br>
Mitigation: Review changelogs and scan new versions before replacing local skill files. <br>


## Reference(s): <br>
- [Ironclaw homepage](https://ironclaw.io) <br>
- [Ironclaw API base](https://ironclaw.io/api/v1) <br>
- [Ironclaw label endpoint](https://ironclaw.io/api/v1/label) <br>
- [Ironclaw documentation](https://ironclaw.io/docs) <br>
- [ClawHub skill page](https://clawhub.ai/samidh/ironclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with HTTP request examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Classification API responses include a label and confidence score; anonymous and registered usage have different rate limits.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
