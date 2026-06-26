## Description: <br>
Jimeng AI (volcengine.com) connector skill for reading, creating, and updating Jimeng AI tasks through the OOMOL `oo` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Jimeng AI image and video generation jobs, inspect action schemas, and retrieve asynchronous task results through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions may create Jimeng AI generation tasks or affect paid account usage. <br>
Mitigation: Require clear user intent and confirm the exact payload and expected effect before running actions tagged [write]. <br>
Risk: A missing or expired Jimeng AI connection can cause authentication, scope, or billing failures. <br>
Mitigation: Run setup, reconnection, or billing recovery steps only after a command returns the matching error. <br>


## Reference(s): <br>
- [Jimeng AI skill page](https://clawhub.ai/oomol/oo-jimeng-ai) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Jimeng AI homepage](https://www.volcengine.com/product/jimeng) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live connector schema before constructing action payloads; asynchronous submit actions return execution metadata for later result retrieval.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
