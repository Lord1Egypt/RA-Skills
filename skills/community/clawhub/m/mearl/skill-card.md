## Description:

Mearl lets agents use a unified CLI to operate a browser, reuse logged-in cookies for API calls, manage mocks and request rules, and inspect requests, logs, events, screenshots, API schemas, and page state across local, CDP, and cloud connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-loat](https://clawhub.ai/user/f-loat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use Mearl to automate browser interactions, debug web and API behavior, capture page and network evidence, and test mocked or modified request flows in controlled local or cloud-connected browser environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate against logged-in browser sessions and reuse cookies for browser-backed API requests.

Mitigation: Use it in controlled browser or test environments, avoid sensitive logged-in sessions unless necessary, and confirm the target domain and requested action before sending authenticated requests.

Risk: File-backed payloads and request actions can move local file contents into network requests when users provide @file payloads or send_request inputs.

Mitigation: Use explicit absolute file paths only for intended payloads, review file contents before use, and restrict destination domains to trusted systems.

Risk: Request rules, cookie copying, persistent profiles, and cloud connector tokens can affect browser traffic or extend access beyond a single action.

Mitigation: Review and remove request rules after testing, minimize cookie copying and persistent profiles, protect cloud connector tokens, and stop cloud connectors when work is complete.

## Reference(s):

- [Mearl Chrome Web Store listing](https://chromewebstore.google.com/detail/mearl/aoehhjnofngknnjefamjbplchbolghkm)
- [Usage examples](references/examples.md)
- [API parameter reference](references/api-reference.md)
- [Connection troubleshooting](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/f-loat/skills/mearl)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include browser action plans, CLI commands, page observations, API request details, screenshots saved to files, and troubleshooting steps.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
