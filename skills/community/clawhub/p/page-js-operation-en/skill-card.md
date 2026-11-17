## Description:

Operate web page elements via CDP and Page JS Extension to reduce token use for UI automation testing, not general web browsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangjing](https://clawhub.ai/user/tangjing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to drive browser page elements through CDP for UI test development, regression testing, and public-page automation. It is intended for non-sensitive testing environments rather than personal browsing, credential handling, or production data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an unpinned browser extension dependency and CDP-based page mutation powers.

Mitigation: Review and pin the exact extension source before installation, use a dedicated Chrome profile, and restrict extension access to test domains.

Risk: Element keys may include page text that an agent could send to LLM services.

Mitigation: Use the skill only on public or non-sensitive test pages and avoid financial, medical, government, login, payment, and production-data pages.

Risk: Form submissions, deletions, and sensitive-field writes can change page state.

Mitigation: Require explicit user confirmation for form submission, deletion, and any credential-field write operation.

## Reference(s):

- [Chrome Extension Documentation](https://developer.chrome.com/docs/extensions/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Page JS Extension Source Repository](https://github.com/TangJing/openclaw_access_web_page_js)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CDP Runtime.evaluate snippets and browser-extension setup guidance for page element indexing, clicking, input filling, and dropdown selection.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
