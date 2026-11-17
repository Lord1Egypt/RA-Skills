## Description:

Set up IndexNow for a website so an agent can generate a key file, add a URL submission script, and integrate sitemap-based URL submission into deploy or content-update workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuyangtusenpo](https://clawhub.ai/user/tuyangtusenpo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to add IndexNow to websites, publish a verification key, read sitemap URLs, and submit changed URLs after deploys or content updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic submission can send the site's sitemap URLs to the IndexNow endpoint after deploys or content updates.

Mitigation: Enable the npm script only for sites where public URL submission is intended, and confirm the sitemap belongs to the target site before running it.

Risk: An unrelated secret could be passed through INDEXNOW_KEY by mistake.

Mitigation: Use an IndexNow key generated specifically for the public site and avoid reusing unrelated project credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuyangtusenpo/skills/indexnow-setup)
- [IndexNow API endpoint](https://api.indexnow.org/IndexNow)
- [Bing Webmaster Tools](https://www.bing.com/webmasters)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify a Node.js URL submission script and project npm configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
