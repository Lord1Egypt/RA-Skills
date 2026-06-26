## Description: <br>
Preflyt scans deployed web apps for security misconfigurations such as exposed environment files, databases, source code, open ports, missing security headers, .git exposure, and directory listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doureios39](https://clawhub.ai/user/doureios39) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and deployment agents use Preflyt after deploying a public web app, API, or backend to check for exposed secrets, unsafe defaults, open services, and missing security headers before treating the deployment as ready. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external npm-based scanner against public URLs, which creates expected outbound requests to the target site and Preflyt service. <br>
Mitigation: Use it only for public URLs you control or are authorized to test, and avoid scanning private, localhost, or customer-sensitive environments. <br>
Risk: Using --share uploads scan results to preflyt.dev and creates a public report link. <br>
Mitigation: Avoid --share for sensitive staging or customer deployments unless public report hosting is acceptable. <br>
Risk: A Pro license key may be supplied with --key. <br>
Mitigation: Treat license keys as secrets and avoid exposing them in logs, shared command transcripts, or committed configuration. <br>


## Reference(s): <br>
- [Preflyt homepage](https://preflyt.dev) <br>
- [preflyt-check source repository](https://github.com/doureios39/preflyt-check) <br>
- [preflyt-check npm package](https://www.npmjs.com/package/preflyt-check) <br>
- [ClawHub skill page](https://clawhub.ai/doureios39/preflyt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and scan-result guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a public URL; scan results remain terminal-only unless the --share option is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
