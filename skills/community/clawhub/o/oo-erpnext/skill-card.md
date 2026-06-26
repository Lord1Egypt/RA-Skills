## Description: <br>
ERPNext helps agents read, create, update, and delete ERPNext documents through the OOMOL oo CLI connector instead of calling the ERPNext API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and business operators use this skill to manage ERPNext DocTypes and documents from an agent workflow through an OOMOL-connected account. It supports document lookup, listing, counts, field reads, creation, updates, field setting, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow includes optional remote installer commands that execute downloaded shell or PowerShell scripts. <br>
Mitigation: Prefer official verified installation steps, or inspect and verify the installer before running any remote script in a shell. <br>
Risk: The skill requires a connected ERPNext account and may use sensitive credentials handled through the OOMOL connection. <br>
Mitigation: Install only when the OOMOL publisher and connected ERPNext account are trusted, and avoid exposing raw tokens or credentials in prompts, logs, or payloads. <br>
Risk: Write and destructive ERPNext actions can change or delete business records. <br>
Mitigation: Confirm the exact DocType, document name, payload, and intended effect with the user before running write or destructive actions. <br>


## Reference(s): <br>
- [ERPNext homepage](https://erpnext.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-erpnext) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution; command responses include JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
