## Description: <br>
Use Peekaboo for macOS desktop GUI automation, screen understanding, and MCP-backed local app control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zimuoo](https://clawhub.ai/user/zimuoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and control native macOS applications with Peekaboo when browser automation is not appropriate. It helps agents focus apps, inspect UI state, perform semantic actions, and verify results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install a third-party desktop-control tool with Homebrew. <br>
Mitigation: Require explicit approval before installation and verify the Peekaboo tap and package source before running install commands. <br>
Risk: Screen Recording and Accessibility permissions can expose and control sensitive desktop content. <br>
Mitigation: Grant permissions only when native macOS automation is intended, pause when permissions are missing, and avoid risky or irreversible actions without user confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zimuoo/peekaboo-macos-automation) <br>
- [Publisher profile](https://clawhub.ai/user/zimuoo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSON from Peekaboo inspection commands when the agent runs local desktop automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
