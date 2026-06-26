## Description: <br>
TextRazor (textrazor.com). Use this skill for ANY TextRazor request - searching and reading data. Whenever a task involves TextRazor, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate TextRazor through an OOMOL-connected account for account lookup, text analysis, classification, entity extraction, and managed TextRazor custom resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access through an OOMOL-connected TextRazor account. <br>
Mitigation: Install only when that account access is acceptable, and keep credentials managed through the connected account flow. <br>
Risk: Some TextRazor classifier and dictionary manager actions can modify, overwrite, or delete resources. <br>
Mitigation: Require explicit confirmation of the exact operation, payload, and target before running state-changing or destructive actions. <br>
Risk: First-time setup examples include installing the oo CLI from a remote installer. <br>
Mitigation: Prefer a verified package or reviewed installer path before running installation commands. <br>


## Reference(s): <br>
- [ClawHub TextRazor skill page](https://clawhub.ai/oomol/oo-textrazor) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [TextRazor homepage](https://www.textrazor.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call the OOMOL TextRazor connector and can return JSON data from TextRazor actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
