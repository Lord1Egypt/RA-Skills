## Description:

PaleBlueDot CLI helps agents guide use of the PaleBlueDot AI Platform CLI for login, API token management, usage and balance queries, wallet balance checks, and browsing available models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derekdong-star](https://clawhub.ai/user/derekdong-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate the PaleBlueDot AI Platform CLI for authentication, token lifecycle management, usage inspection, wallet balance checks, and model discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact recommends a one-line remote installer that executes downloaded shell script content.

Mitigation: Inspect the installer before execution and prefer a pinned release or checksum-verified installation path.

Risk: Manual login and token commands involve sensitive session cookies and API token keys.

Mitigation: Treat cookies and token keys as passwords, avoid sharing them in chats or logs, and confirm token IDs before revealing or deleting keys.

## Reference(s):

- [PaleBlueDot CLI Skill Page](https://clawhub.ai/derekdong-star/skills/pbd-cli)
- [PaleBlueDot AI Platform](https://www.palebluedot.ai)
- [PaleBlueDot Open API Base URL](https://open.palebluedot.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw JSON output examples from pbd-cli commands.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
