## Description:

Automate Chrome and Chromium with Puppeteer for scraping, testing, screenshots, and browser workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuxingling55-sketch](https://clawhub.ai/user/xuxingling55-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up Puppeteer-based browser automation for web scraping, end-to-end testing, screenshots, PDF generation, and repeatable Chrome or Chromium workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create Puppeteer files, automation scripts, browser output, workflow memory, and browser profile data on the local machine.

Mitigation: Review generated files before reuse and inspect or delete ~/puppeteer/memory.md when retained workflow details are not desired.

Risk: The security summary flags guidance to hide persistent workflow memory from the user.

Mitigation: Tell users when workflow details are being retained and avoid storing credentials or sensitive site details in memory files.

Risk: The security summary flags anti-detection scraping advice.

Mitigation: Use the skill only for sites and applications the user is authorized to automate, and respect site terms, rate limits, and access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuxingling55-sketch/skills/hilda-puppeteer)
- [Skill homepage](https://clawic.com/skills/puppeteer)
- [Setup guidance](artifact/setup.md)
- [Selector guidance](artifact/selectors.md)
- [Waiting patterns](artifact/waiting.md)
- [Memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local Puppeteer scripts, screenshots, PDFs, scraped data, and workflow memory under ~/puppeteer.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
