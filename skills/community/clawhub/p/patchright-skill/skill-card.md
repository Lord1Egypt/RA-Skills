## Description:

Patchright-based browser automation with bot detection bypass for interacting with local web applications, testing localhost or private-network dev servers, taking screenshots, and performing UI interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallnest](https://clawhub.ai/user/smallnest)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to drive browser automation for QA, end-to-end testing, frontend debugging, visual verification, and pre-deployment checks in local or private development environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a persistent, unauthenticated browser-control service.

Mitigation: Run it only in a trusted local environment, stop the server when finished, and add authentication or URL allowlists before broader use.

Risk: Browser navigation and JavaScript execution can operate beyond the intended local-testing purpose.

Mitigation: Limit use to intended localhost, dev-server, or private-network targets and avoid sensitive logged-in sessions.

Risk: Screenshots and extracted page data may capture sensitive information.

Mitigation: Choose screenshot output paths carefully and review generated artifacts before sharing or retaining them.

Risk: The dependency is specified with a broad lower bound.

Mitigation: Pin and review the Patchright dependency before installation or release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smallnest/skills/patchright-skill)
- [Patchright Skill Reference](reference.md)
- [Patchright Scripts](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots or extracted page data through the local browser automation scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
