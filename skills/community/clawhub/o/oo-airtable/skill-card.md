## Description: <br>
This skill lets agents read, create, update, and delete Airtable data through the OOMOL oo CLI instead of calling Airtable APIs directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Airtable bases, tables, fields, and records through an OOMOL-connected account. It supports read, create, update, and delete workflows while requiring schema inspection before action payloads are built. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags a setup fallback that runs a remote OOMOL installer script on the user's machine. <br>
Mitigation: Review the installer first or install the oo CLI independently from a trusted official source before using setup fallback commands. <br>
Risk: The skill can create, update, and delete Airtable bases, tables, fields, and records through an authenticated account. <br>
Mitigation: Confirm the exact payload, target, and expected effect with the user before running write actions, and require explicit approval for destructive actions. <br>
Risk: The skill requires OAuth or other sensitive account credentials through the OOMOL connection. <br>
Mitigation: Use the existing OOMOL connection flow and avoid exposing raw tokens or credentials in prompts, command arguments, logs, or saved files. <br>


## Reference(s): <br>
- [ClawHub Airtable skill page](https://clawhub.ai/oomol/oo-airtable) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Airtable homepage](https://airtable.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo CLI connector schema and run commands; action responses are JSON with data and meta.executionId fields.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
