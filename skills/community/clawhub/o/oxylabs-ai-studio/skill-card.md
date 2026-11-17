## Description:

Web scraping, crawling, searching, and browser automation using Oxylabs AI Studio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drfirass](https://clawhub.ai/user/drfirass)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation engineers use this skill to scrape pages, search the web, crawl domains, map site URLs, and run browser-navigation tasks through Oxylabs AI Studio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can modify the system Python environment.

Mitigation: Review setup.sh before running it, install the Oxylabs SDK in a virtual environment with a pinned version, and do not run setup as root.

Risk: URLs, prompts, and extracted page content may be sent to Oxylabs AI Studio during scraping, crawling, search, mapping, and browser tasks.

Mitigation: Avoid internal URLs, private pages, secret query strings, and regulated data unless that data sharing is explicitly approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/drfirass/skills/oxylabs-ai-studio)
- [Oxylabs AI Studio](https://aistudio.oxylabs.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown text printed to stdout by wrapper scripts, with setup and environment configuration instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OXYLABS_API_KEY and sends requested URLs, prompts, and extracted web data to Oxylabs AI Studio.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
