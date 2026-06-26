## Description: <br>
Provides Microsoft Clarity analytics access through the OOMOL oo CLI connector for reading and exporting live insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and site operators use this skill to export recent Microsoft Clarity live insights from an OOMOL-connected account without handling raw API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup may ask the user to install the oo CLI through shell or PowerShell installer commands. <br>
Mitigation: Inspect or verify the installer before running it, and install only if the user trusts OOMOL. <br>
Risk: The skill requires a connected Microsoft Clarity account through OOMOL. <br>
Mitigation: Use an OOMOL account and Microsoft Clarity connection that the user trusts, and avoid exposing raw credentials in prompts or local files. <br>
Risk: Future connector actions could include write or destructive operations even though the current action is read-only. <br>
Mitigation: Confirm the exact payload and effect with the user before executing any action tagged write or destructive. <br>


## Reference(s): <br>
- [Microsoft Clarity homepage](https://clarity.microsoft.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-microsoft-clarity) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution and returns connector responses as JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
