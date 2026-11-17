## Description:

Kiln helps agents design, check, slice, print, and monitor 3D objects through an MCP server and CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeofaxel](https://clawhub.ai/user/codeofaxel)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Makers and 3D-printing users use Kiln through an AI agent to turn ideas or existing files into printable models, prepare them for compatible printers, and manage or monitor prints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design history or workspace files may be uploaded to the user's Kiln account without asking first.

Mitigation: Require explicit permission before each upload, including uploads triggered by branching. Keep confidential work local until cloud syncing is approved.

Risk: Executable-package behavior and hosted-service data handling are unverified in the supplied artifacts.

Mitigation: Use a vetted package version and keep sensitive designs local unless the user approves sharing them.

Risk: A print action can affect physical equipment and material.

Mitigation: Run the printability preflight and get the user's confirmation before each print unless they explicitly enabled auto-print.

## Reference(s):

- [Kiln for AI agents](https://kiln3d.com/agents)
- [Installation guide](https://kiln3d.com/install)
- [Supported printers](https://kiln3d.com/printers)
- [Design version history](https://kiln3d.com/version-control)

## Skill Output:

**Output Type(s):** [Files, Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [3D model and slicer files with text summaries, estimates, and printer status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected design, printer, slicer, and connected services.]

## Skill Version(s):

1.5.1 (source: server-resolved release evidence, server.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
