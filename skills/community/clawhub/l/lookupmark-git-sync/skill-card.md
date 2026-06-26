## Description: <br>
Manage whitelisted git repositories from chat with status, log, diff, fetch, pull, and push commands guarded by repository allowlists and confirmation for write actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lookupmark](https://clawhub.ai/user/lookupmark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and synchronize configured local git repositories from an agent chat. It supports read-only repository status workflows by default and allows pull or push only when explicitly confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run real git write and network actions against configured repositories. <br>
Mitigation: Review the configured repository allowlist before installing and require explicit confirmation before pull or push actions. <br>
Risk: Pull may temporarily stash local changes and can affect an active working tree. <br>
Mitigation: Run status first, review uncommitted changes, and use pull only when temporary stashing is acceptable. <br>


## Reference(s): <br>
- [Git Sync on ClawHub](https://clawhub.ai/lookupmark/lookupmark-git-sync) <br>
- [Git CLI](https://git-scm.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and git command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write actions use normal git credentials, require explicit confirmation, and are limited to configured repositories; pull may temporarily stash local changes.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
