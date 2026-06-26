## Description: <br>
Execute command-line tools through Nix when they are missing locally or when a newer tool version is needed, including multi-package shells and package search through nixpkgs-unstable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MSDimos](https://clawhub.ai/user/MSDimos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to run CLI tools through a Nix wrapper, recover from command-not-found failures, search for packages, and create temporary multi-tool environments without manually installing packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes broad command-line work through a package-fetching wrapper, which can cause agents to fetch and execute tools during normal workflows. <br>
Mitigation: Review commands before execution, avoid use with secrets, account changes, destructive file operations, financial workflows, or commands that should require explicit confirmation, and narrow activation rules before deployment. <br>
Risk: The artifact uses nixpkgs-unstable for package resolution, so tool behavior and versions may change over time. <br>
Mitigation: Use explicit package choices where practical, review the selected package before execution, and document exclusions for workflows that require pinned or audited tooling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MSDimos/nix-run) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that fetch and execute packages from nixpkgs-unstable through the bundled wrapper.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
