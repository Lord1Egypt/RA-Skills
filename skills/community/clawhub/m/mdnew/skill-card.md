## Description: <br>
Fetch clean, agent-optimized Markdown from any URL using the markdown.new service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThendCN](https://clawhub.ai/user/ThendCN) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to convert public web pages into clean Markdown for analysis when ordinary web fetch or browser output is too noisy or token-heavy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user-provided URL to an external conversion service, which may expose private, authenticated, internal, secret-bearing, or session-specific links. <br>
Mitigation: Use it for public pages or URLs that are acceptable to share with markdown.new, and avoid sensitive links unless external conversion has been approved. <br>


## Reference(s): <br>
- [Mdnew ClawHub release](https://clawhub.ai/ThendCN/mdnew) <br>
- [markdown.new service](https://markdown.new) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text] <br>
**Output Format:** [Markdown text printed to standard output, optionally preceded by an estimated token count line.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends the provided URL to markdown.new and may include x-markdown-tokens metadata when returned by the service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
