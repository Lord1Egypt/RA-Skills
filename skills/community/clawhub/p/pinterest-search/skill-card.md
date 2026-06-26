## Description: <br>
Searches Pinterest for images and pins from keyword queries and returns structured results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikehankk](https://clawhub.ai/user/mikehankk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to find Pinterest visual inspiration, pin metadata, and image links for a user-provided keyword query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Pinterest cookies, proxy settings, downloads, and local result or image caches. <br>
Mitigation: Review before installation, avoid untrusted proxies, provide a Pinterest cookie only when authenticated search is necessary, run from a constrained project directory, and clear caches when privacy matters. <br>
Risk: The server security summary flags explicit anti-analysis comments and broad downloader behavior. <br>
Mitigation: Treat the release as suspicious until those comments and downloader behavior are reviewed and fixed. <br>


## Reference(s): <br>
- [Pinterest Search on ClawHub](https://clawhub.ai/mikehankk/pinterest-search) <br>
- [Bun Runtime](https://bun.sh) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON arrays saved to local files, with optional shell commands for cookie, proxy, and cache configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include Pinterest pin IDs, titles, descriptions, image URLs, dimensions, links, domains, pinner metadata, local result caches, and optional downloaded images.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
