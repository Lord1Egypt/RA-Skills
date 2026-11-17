## Description:

Capture web screenshots, retrieve page titles, and scrape text or HTML content from web pages using a Playwright-backed service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dang-ngoc-duy](https://clawhub.ai/user/dang-ngoc-duy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture screenshots, inspect page titles, and extract page text or HTML from provided URLs. It is best suited for public or explicitly approved pages where screenshot handling and service operator trust are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots can be sent to a fixed Telegram group without clear confirmation.

Mitigation: Use only approved pages, confirm the recipient before forwarding screenshots, and keep screenshots local when handling internal, personal, or confidential content.

Risk: The browser service is unrestricted and depends on trust in the service operator.

Mitigation: Install only when the operator is trusted, restrict allowed URLs where possible, and avoid authenticated or confidential pages unless the workflow is changed to enforce scoping.

Risk: Scraped content can be incomplete for login-gated or dynamically loaded pages.

Mitigation: Treat empty or partial scrape results as operational limitations and verify important outputs before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dang-ngoc-duy/skills/playwright-service)
- [ClawHub publisher profile](https://clawhub.ai/user/dang-ngoc-duy)

## Skill Output:

**Output Type(s):** [text, HTML, files, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples; service responses may be JSON and screenshots may be image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots may be saved locally before optional forwarding to Telegram; scraped output depends on page access, authentication, and dynamic loading behavior.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
