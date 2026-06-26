## Description: <br>
Interzoid (interzoid.com) supports requests that search, read, validate, enrich, or compare company, organization, name, email, IP, and license credit data through the OOMOL connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Interzoid lookup and matching actions through an OOMOL-connected account. It supports schema-first requests for email enrichment, IP profile and reputation checks, company and full-name similarity keys, full-name match scoring, organization name standardization, and remaining credit checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send names, emails, IP addresses, organization names, and account-related lookup requests to Interzoid through an OOMOL-connected account. <br>
Mitigation: Use it only with an intended OOMOL-connected Interzoid account and avoid submitting data that should not be processed by that service. <br>
Risk: First-time setup may require installing the oo CLI, including documented pipe-to-shell installation commands. <br>
Mitigation: Review the installation method first, or use manual vendor installation steps before running setup commands. <br>
Risk: Connected account credentials and scopes can expire or be missing, causing failed actions or requiring reconnection. <br>
Mitigation: Run connection or authentication setup only after an auth or connection error and confirm the intended Interzoid connection before retrying. <br>


## Reference(s): <br>
- [ClawHub Interzoid skill page](https://clawhub.ai/oomol/oo-interzoid) <br>
- [Interzoid homepage](https://www.interzoid.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to inspect live action schemas before constructing JSON payloads and to read response data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
