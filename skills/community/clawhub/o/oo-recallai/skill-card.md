## Description: <br>
Recall.ai (recall.ai). Use this skill for ANY Recall.ai request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Recall.ai meeting bots through an OOMOL-connected account, including bot creation, retrieval, listing, removal from active calls, and deletion of completed bot media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a user's Recall.ai account through OOMOL and may create bots, remove bots from calls, or delete bot media. <br>
Mitigation: Install only when that account access is intended, review prompts carefully, and require explicit approval before write or destructive actions. <br>
Risk: First-time setup may require installing the oo CLI. <br>
Mitigation: Verify the oo CLI installer source before running setup commands. <br>


## Reference(s): <br>
- [Recall.ai homepage](https://www.recall.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
