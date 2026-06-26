## Description: <br>
AbuseIPDB helps an agent use an OOMOL-connected AbuseIPDB account to check IP reputation, inspect CIDR blocks, retrieve reports, and read the blacklist feed through the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and agents use this skill to query AbuseIPDB reputation data and prepare connector calls through an OOMOL-managed account. It supports IP checks, CIDR block inspection, detailed report lookup, and blacklist retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected AbuseIPDB account and can prompt use of the oo CLI. <br>
Mitigation: Install or sign in to the oo CLI only when intentionally using this integration, and rely on OOMOL-managed credentials rather than handling raw AbuseIPDB tokens. <br>
Risk: The check_block action is tagged as write-capable in the artifact. <br>
Mitigation: Review the live schema, exact payload, and intended effect with the user before running any action tagged write. <br>


## Reference(s): <br>
- [AbuseIPDB homepage](https://www.abuseipdb.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-abuseipdb) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live oo connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
