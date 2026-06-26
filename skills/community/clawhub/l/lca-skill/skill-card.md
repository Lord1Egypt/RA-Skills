## Description: <br>
AI-guided Life Cycle Assessment using openLCA. Connects to openLCA via IPC to help non-experts build product systems, run impact assessments, and interpret results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manmeet3591](https://clawhub.ai/user/manmeet3591) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and sustainability practitioners use this skill to run guided Life Cycle Assessment workflows in openLCA, including process selection, product system creation, LCIA calculation, result interpretation, and comparison of alternatives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: openLCA commands can create product systems or run calculations against the currently open database, so incorrect database, process, or impact method choices can produce misleading results. <br>
Mitigation: Confirm the intended openLCA database is open and review the selected process and impact method before creation or calculation commands. <br>
Risk: The skill installs and uses the olca-ipc Python package to communicate with a local IPC server. <br>
Mitigation: In controlled environments, pin or review the exact olca-ipc package version before installation. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/manmeet3591/claw_lca) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON bridge outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable openLCA IPC server and the OPENLCA_IPC_PORT environment variable when running bridge commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
