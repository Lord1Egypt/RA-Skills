## Description: <br>
Design UI screens in Paper, a professional design tool running locally on macOS, by creating artboards, writing HTML into designs, taking screenshots, and iterating visually. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CandooLabs](https://clawhub.ai/user/CandooLabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to control a local Paper design file from an agent workflow, create or modify UI artboards, inspect design structure, and capture screenshots for visual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent control of the currently open Paper design file, including operations that can edit, replace, duplicate, or delete design content. <br>
Mitigation: Review targets before replace or delete operations and keep backups or version history for important designs. <br>
Risk: Screenshot and session artifacts may be written under temporary local paths on the machine. <br>
Mitigation: Clean up /tmp/paper-screenshots and /tmp/paper-mcp-session on shared machines. <br>
Risk: Changing the Paper MCP URL could direct design operations to an unintended or untrusted endpoint. <br>
Mitigation: Keep PAPER_MCP_URL on the default localhost endpoint unless another server is intentionally trusted. <br>


## Reference(s): <br>
- [Paper Design website](https://paper.design) <br>
- [ClawHub Paper Design skill page](https://clawhub.ai/CandooLabs/paper-design) <br>
- [Publisher profile](https://clawhub.ai/user/CandooLabs) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON arguments; screenshot operations save JPEG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Paper on macOS, curl, python3, and access to the local Paper MCP endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
