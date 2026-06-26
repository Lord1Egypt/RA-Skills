## Description: <br>
Gist (gist.github.com). Use this skill for ANY Gist request, including reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to manage GitHub Gists through an OOMOL-connected account, including reading gist data and performing create, update, star, fork, comment, and delete workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, star, fork, comment on, and delete GitHub Gists through the user's connected account. <br>
Mitigation: Review payloads and confirm the intended effect before approving write actions; require explicit approval for destructive actions. <br>
Risk: Delete actions may remove gists or comments in a way that is difficult to reverse. <br>
Mitigation: Confirm the exact target identifier and user intent before running delete_gist or delete_gist_comment. <br>
Risk: The skill requires a connected OOMOL account with access to GitHub Gist. <br>
Mitigation: Install it only when agents should manage GitHub Gists through that connected account. <br>


## Reference(s): <br>
- [Gist homepage](https://gist.github.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-gist) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector action responses are returned as JSON by the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
