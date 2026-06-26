## Description: <br>
Markdown Browser post-processes OpenClaw web_fetch results with Content-Signal policy decisions, URL privacy redaction, optional markdown normalization, and a stable output schema. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnortegahyc](https://clawhub.ai/user/johnortegahyc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to process existing OpenClaw web_fetch payloads before downstream agent logic. It helps normalize markdown or HTML content, interpret Content-Signal headers, estimate tokens, and redact source URL details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can read a user-specified input file path. <br>
Mitigation: Review the input path before execution and provide only the intended web_fetch JSON payload. <br>
Risk: Content-Signal headers may be absent or incomplete. <br>
Mitigation: Treat unknown policy values as needing review before using fetched content in downstream agent logic. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/johnortegahyc/markdown-browser-skills-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON object from the wrapper tool, with Markdown or text content and status metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes content, format, token_estimate, content_signal, policy_action, source_url, status_code, and fallback_used fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
