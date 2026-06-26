## Description: <br>
Extracts clean markdown from web pages through the markdown.new API with auto, AI, and browser extraction methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviclaw](https://clawhub.ai/user/aviclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to convert public web pages into clean markdown for summarization, note capture, documentation workflows, or downstream text processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs, and potentially fetched page content, are sent to markdown.new. <br>
Mitigation: Use the skill for public webpages and avoid internal, authenticated, signed, or sensitive URLs unless the external service is trusted for that data. <br>
Risk: Extraction depends on an external service and can fail because of network issues, timeouts, API errors, or Cloudflare blocks. <br>
Mitigation: Handle failure responses, retry when appropriate, and choose the browser or AI method only when the default extraction method is insufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aviclaw/markdown-extract) <br>
- [markdown.new API endpoint](https://markdown.new/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Text] <br>
**Output Format:** [JSON response containing extracted markdown on success or an error message on failure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports auto, ai, and browser extraction methods; external API requests may time out or return service-specific errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
