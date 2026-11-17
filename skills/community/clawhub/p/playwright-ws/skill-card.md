## Description:

Browser automation via remote Playwright WebSocket server for screenshots, PDFs and testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[first-it-consulting](https://clawhub.ai/user/first-it-consulting)

### License/Terms of Use:

MIT

## Use Case:

Developers and test engineers use the skill to automate browser checks through a trusted remote Playwright server, capture screenshots, export PDFs, and run Playwright tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured WebSocket server can observe requested URLs, page contents, screenshots, and test interactions.

Mitigation: Use a server you control or fully trust, restrict access to its browser-control endpoint, and avoid routing sensitive sites or content through it.

Risk: The security assessment is suspicious and partial; it raises concern about an access boundary in the Docker example and could not fully interpret several components.

Mitigation: Review and pin dependency versions, and restrict the browser-control endpoint to trusted access before installing or using the skill.

## Reference(s):

- [Playwright API Reference](references/api-reference.md)
- [Selector Strategies](references/selectors.md)
- [Playwright Documentation](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [Images, PDF documents, Test results]

**Output Format:** [PNG or JPEG screenshots, PDF files, and Playwright test output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots and PDFs are saved to requested paths; test output is reported by Playwright.]

## Skill Version(s):

1.0.5 (source: server release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
