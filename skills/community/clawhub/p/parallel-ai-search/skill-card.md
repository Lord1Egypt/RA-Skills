## Description: <br>
Uses Parallel's parallel-cli for live web search, URL extraction, deep research reports, dataset enrichment, entity discovery, and web monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they need current web evidence, source extraction, structured enrichment, entity discovery, or ongoing monitoring through Parallel's CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and run Parallel's CLI, including an unverified remote installer and broad curl access. <br>
Mitigation: Install only after reviewing the installer or use the pipx path, use a dedicated Parallel API key, avoid pasting secrets into chat or shell history, and confirm monitor cadences and webhook destinations before creating ongoing monitors. <br>


## Reference(s): <br>
- [Parallel CLI documentation](https://docs.parallel.ai/integrations/cli) <br>
- [Command templates](references/command-templates.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, citations, and JSON or file output references when Parallel CLI commands are used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save long search, extraction, research, enrichment, or entity-discovery outputs to files in /tmp.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
