## Description: <br>
Browse and extract text content, titles, and partial HTML from webpages using a local browser service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PingAGI](https://clawhub.ai/user/PingAGI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to retrieve webpage titles, text, partial HTML, and optional screenshots through a local browser service when web content needs to be inspected or summarized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browsing sensitive, private, or internal URLs may expose fetched text, HTML, or screenshots to the agent workflow. <br>
Mitigation: Use the skill only for pages the agent is intentionally allowed to browse, and avoid secrets or private/internal URLs unless necessary. <br>
Risk: Fetched webpage text, HTML, and screenshots are untrusted content and may contain misleading instructions or prompt-injection attempts. <br>
Mitigation: Treat browser output as data rather than instructions, and review or corroborate important information before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PingAGI/pingagi-web) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON browser response plus Markdown usage guidance with an example curl command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns page title, text, partial HTML, and an optional base64 screenshot; requires a trusted local browser service.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
