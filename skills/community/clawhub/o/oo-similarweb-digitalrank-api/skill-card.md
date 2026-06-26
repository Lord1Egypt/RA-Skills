## Description: <br>
Use this skill for Similarweb requests that search and read data through the OOMOL Similarweb connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Similarweb through an OOMOL-connected account, including rank-tracker campaign metadata, top-site rankings, and subscription usage allowance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Similarweb API key and uses account credentials injected by OOMOL. <br>
Mitigation: Connect only the intended Similarweb account and avoid exposing raw credentials in prompts, files, or command output. <br>
Risk: The skill includes fallback commands for installing and authenticating the oo CLI. <br>
Mitigation: Run setup commands only after an auth, connection, or missing-CLI failure and review install steps before execution. <br>
Risk: Future connector actions could change Similarweb state if write or destructive actions are added. <br>
Mitigation: Confirm the exact payload and effect with the user before running any action tagged write or destructive. <br>


## Reference(s): <br>
- [Similarweb homepage](https://www.similarweb.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-similarweb-digitalrank-api) <br>
- [OOMOL Similarweb connection](https://console.oomol.com/app-connections?provider=similarweb_digitalrank_api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing payloads; connector responses include data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
