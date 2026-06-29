## Description: <br>
Agility CMS (agilitycms.com). Use this skill for Agility CMS search and read requests through the OOMOL-connected oo CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Agility CMS connector schemas and run read-oriented content, page, sitemap, and content-model actions through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on OOMOL as the intermediary for Agility CMS access. <br>
Mitigation: Install it only when that intermediary is intended for the deployment. <br>
Risk: Remote oo CLI installer commands may change over time. <br>
Mitigation: Review the installer before running remote install commands. <br>
Risk: Future write or destructive Agility actions could modify or remove CMS data. <br>
Mitigation: Confirm the exact payload and effect with the user before allowing any write or destructive action to run. <br>


## Reference(s): <br>
- [Agility CMS homepage](https://agilitycms.com/) <br>
- [oo CLI repository](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-agility) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request or response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include Agility CMS data and an execution id under meta.executionId.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
