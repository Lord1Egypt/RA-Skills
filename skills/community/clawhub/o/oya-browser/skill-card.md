## Description:

Drive real Chrome browsers through Oya Browser to automate web tasks using persistent browser personas, MCP tools, the SDK, or the CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oyaaiprod](https://clawhub.ai/user/oyaaiprod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Oya Browser to navigate websites, read page content, interact with forms, handle authenticated workflows, and automate tasks across browsers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account setup asks for an email, and setup may import browser cookies into a persistent persona.

Mitigation: Review the account and cookie import steps first; provide an email and approve cookie import only when you understand and consent to those actions.

Risk: Browser personas can retain cookies and authenticated sessions across runs.

Mitigation: Use a persona only for the sites and sessions you intend to automate, and stop browsers when the task is complete.

## Reference(s):

- [Oya Browser](https://oyabrowser.com)
- [Oya Browser documentation](https://oyabrowser.com/docs)
- [Oya Browser agent documentation](https://oyabrowser.com/llms.txt)
- [Oya Browser on ClawHub](https://clawhub.ai/oyaaiprod/skills/oya-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown page analysis and browser interaction results, with optional code or shell instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser personas can retain cookies and authenticated sessions across runs; API-based use requires Node and may use OYA_API_KEY.]

## Skill Version(s):

1.0.230 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
