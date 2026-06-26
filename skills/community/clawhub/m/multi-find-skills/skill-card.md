## Description: <br>
Multi Find Skills helps an agent search ClawHub, LobeHub, and skills.sh for relevant skills, compare candidate quality, provide install guidance, and maintain explicit user preference memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzairong](https://clawhub.ai/user/wangzairong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need to discover, compare, and install agent skills across multiple public skill marketplaces. It is intended for finding stronger workflows or safer alternatives while preserving explicit search and recommendation preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative security review marks the skill as suspicious because it includes risky install guidance and proactive behavior. <br>
Mitigation: Review each recommended skill before installation, keep proactive search disabled or passive when unwanted, and do not install flagged candidates without explicit approval. <br>
Risk: The skill searches external public skill marketplaces and may send search queries outside the local machine. <br>
Mitigation: Avoid entering sensitive information in search terms and restrict source preferences when external search is not acceptable. <br>
Risk: Install commands can affect the local agent environment, especially with force, auto-confirm, or global install options. <br>
Mitigation: Require explicit user confirmation before installs and avoid `--force`, `-y`, and `-g` unless the user intentionally accepts those effects. <br>
Risk: The skill can keep recommendation history and preferences in a local memory file. <br>
Mitigation: Set memory behavior to passive or remove the memory file if retained recommendation history is not desired. <br>


## Reference(s): <br>
- [ClawHub listing for Multi Find Skills](https://clawhub.ai/wangzairong/multi-find-skills) <br>
- [ClawHub](https://clawhub.ai) <br>
- [skills.sh](https://skills.sh) <br>
- [LobeHub skills](https://lobehub.com/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with comparison tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local memory file with user-stated preferences when the user explicitly provides feedback.] <br>

## Skill Version(s): <br>
2.8.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
