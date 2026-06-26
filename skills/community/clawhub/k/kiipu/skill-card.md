## Description: <br>
Use when the user wants to create, delete, restore, or purge Kiipu posts, manage authentication, or check local setup through the Kiipu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mycreat](https://clawhub.ai/user/mycreat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to manage Kiipu posts and local Kiipu CLI setup from an agent workflow. It supports post creation, deletion, restoration, permanent purge, authentication checks, and setup diagnostics through the local Kiipu CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger real Kiipu post changes, including deletion and permanent purge. <br>
Mitigation: Verify the exact post ID before delete or purge, and treat purge as permanent. <br>
Risk: The skill depends on the separately installed @kiipu/cli package and its local authentication state. <br>
Mitigation: Install it only on trusted machines, verify local setup with kiipu doctor, and avoid pasting API keys into shared or logged contexts. <br>


## Reference(s): <br>
- [Kiipu Skill Release](https://clawhub.ai/mycreat/kiipu) <br>
- [mycreat Publisher Profile](https://clawhub.ai/user/mycreat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report local CLI results and ask for explicit post IDs before destructive actions.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
