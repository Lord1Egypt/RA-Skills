## Description: <br>
Mistake-proofing technique manager. Use when json poka yoke tasks, csv poka yoke tasks, checking poka yoke status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage a local poka-yoke entry log, including adding, listing, searching, removing, exporting, and summarizing mistake-proofing records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled CLI writes local records and configuration files. <br>
Mitigation: Set POKA_YOKE_DIR to an intended workspace-specific directory before use when persistent local state should be isolated. <br>
Risk: Export commands can create JSON or CSV files in the current directory. <br>
Mitigation: Run export from the desired output directory and review generated files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/poka-yoke) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and local CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local data under POKA_YOKE_DIR, defaulting to ~/.poka-yoke, and may export JSON or CSV files in the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
