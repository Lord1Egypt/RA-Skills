## Description:

Drive Owl Browser as an agent. Read pages as compact, handle-addressable OwlMark and click/type by handle, not by screenshot or pixel coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibnbd](https://clawhub.ai/user/ibnbd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Owl Browser to navigate and inspect webpages through compact OwlMark text and stable action handles. It supports browser workflows that need observe-act loops, form entry, navigation, and visual screenshots only when text rendering is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-control workflows can expose visited URLs, user actions, and observed page content to the configured Owl Browser service.

Mitigation: Use only a trusted localhost or internal HTTPS Owl Browser endpoint, and avoid sensitive pages unless that processing is acceptable.

Risk: The bearer token grants access to the Owl Browser API.

Mitigation: Protect OWL_API_TOKEN like a password and avoid exposing it in logs, shared shells, or untrusted environments.

Risk: Agent-driven click and type actions can affect live webpages.

Mitigation: Observe before acting, use exact handle tokens from the current page, and re-observe after each action before continuing.

## Reference(s):

- [Owl Browser homepage](https://www.owlbrowser.net)
- [ClawHub Owl Browser skill page](https://clawhub.ai/ibnbd/skills/owl-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OWL_API_ENDPOINT, OWL_API_TOKEN, and curl; browser actions are performed through a trusted Owl Browser API endpoint.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
