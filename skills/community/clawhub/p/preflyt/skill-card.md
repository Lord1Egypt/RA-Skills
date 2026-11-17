## Description:

Scan deployed web apps for security misconfigurations after every deploy, including exposed .env files, databases, source code, open ports, missing security headers, .git exposure, and directory listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doureios39](https://clawhub.ai/user/doureios39)

### License/Terms of Use:


## Use Case:

Developers and deployment agents use Preflyt after deploying public web apps, APIs, or backends to scan the live URL for exposed secrets, unsafe defaults, and common deployment security misconfigurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents and CI jobs to run an npm package after deployment, and the documented command uses an unpinned npx package.

Mitigation: Install and review a pinned preflyt-check version through the project lockfile before use, and run scans in a least-privileged CI job.

Risk: Scanning the wrong URL could test a site outside the user's deployment scope.

Mitigation: Confirm the target URL belongs to the intended deployment before running the scan.

Risk: Using --share uploads scan results to preflyt.dev and creates a public report link.

Mitigation: Use --share only when a public report is acceptable; otherwise keep results in the terminal.

Risk: Passing a license key on the command line can expose it through shell history, process listings, or CI logs.

Mitigation: Avoid command-line license keys; use a reviewed secret-management approach if authenticated scans are required.

## Reference(s):

- [Preflyt homepage](https://preflyt.dev)
- [preflyt-check source](https://github.com/doureios39/preflyt-check)
- [preflyt-check npm package](https://www.npmjs.com/package/preflyt-check)
- [Preflyt skill page](https://clawhub.ai/doureios39/skills/preflyt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise scan-result guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs require Node.js and a public target URL; --share uploads scan results to preflyt.dev and creates a public report link.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
