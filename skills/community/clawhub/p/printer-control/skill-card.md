## Description: <br>
Control local and network printers on Windows to list printers, print files or text, check status, and set the default printer with name matching support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpl666ya](https://clawhub.ai/user/zhangpl666ya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT operators, and local workstation users use this skill to automate Windows printer discovery, status checks, print jobs, and default-printer changes through agent-proposed Python or PowerShell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Print operations consume physical resources and can be disruptive when sent to the wrong printer or with the wrong content. <br>
Mitigation: Require explicit user authorization before each print operation and confirm the printer, content, and copy count before running commands. <br>
Risk: The PowerShell fallback builds commands from user-controlled printer names, file paths, and text. <br>
Mitigation: Prefer the pywin32 execution path and avoid untrusted printer names, file paths, or text until the PowerShell calls use safe parameter binding or strict validation. <br>
Risk: Changing the default printer affects subsequent printing behavior on the workstation. <br>
Mitigation: Confirm the exact target printer before default-printer changes and check the current default printer before and after the operation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhangpl666ya/printer-control) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include printer names, printer status details, print-job command proposals, and default-printer configuration commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
