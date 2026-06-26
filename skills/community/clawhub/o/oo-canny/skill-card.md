## Description: <br>
Canny (canny.io). Use this skill for ANY Canny request - reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who manage Canny workspaces use this skill to read boards, posts, comments, and users and to create or update Canny records through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Canny content through actions tagged as write actions. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running any write action. <br>
Risk: The skill requires access to an OOMOL-connected Canny account and may depend on sensitive credentials managed outside the prompt. <br>
Mitigation: Install only when Canny operation through OOMOL is intended, keep raw tokens out of prompts and files, and use the OOMOL connection flow for credential handling. <br>
Risk: Connector input schemas may change over time or differ by action. <br>
Mitigation: Fetch the live action schema with oo connector schema before constructing or running a payload. <br>


## Reference(s): <br>
- [ClawHub Canny skill](https://clawhub.ai/oomol/oo-canny) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Canny homepage](https://canny.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, an authenticated OOMOL account, and a connected Canny API key; write actions require confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
