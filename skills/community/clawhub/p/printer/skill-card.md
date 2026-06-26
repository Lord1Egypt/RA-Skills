## Description: <br>
Manage printers via CUPS on macOS, including discovery, setup, printing, queues, status checks, and wake commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DhvanilPatel](https://clawhub.ai/user/DhvanilPatel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, IT staff, and macOS users can use this skill to get command-line guidance for managing local and network printers with CUPS. It helps discover printers, configure queues and defaults, print files, inspect status, and troubleshoot common printer issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Printer-management commands can change queues, defaults, printer settings, or jobs if run with incorrect names, IP addresses, file paths, or job IDs. <br>
Mitigation: Verify the exact printer name, IP address, file path, and job ID before running any command. <br>
Risk: Some commands can have broad or persistent effects, including sudo lpadmin changes, queue-wide cancellation, disabling or rejecting jobs, printer removal, Homebrew package installation, or launchd keep-alive setup. <br>
Mitigation: Require explicit user approval before executing sudo commands, queue-wide actions, removal commands, package installs, or persistent keep-alive configuration. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are macOS-focused CUPS command guidance and may reference required local binaries such as lp, lpstat, and lpadmin.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
