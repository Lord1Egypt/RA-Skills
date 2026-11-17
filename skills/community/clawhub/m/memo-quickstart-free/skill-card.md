## Description: <br>
Memo Quickstart Free guides agents through setting up and using a local memory workflow with session state, JSON memory files, human-readable archives, TF-IDF search, and save-before-response persistence steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to initialize a local memory store, persist preferences, decisions, facts, lessons, and context, and retrieve them with command-line memory tools during project work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist local memory derived from conversations, including user details that may be sensitive. <br>
Mitigation: Avoid storing passwords, financial details, secrets, or regulated data; review memory files and apply local file access controls before use. <br>
Risk: The skill instructs users to install and run a global npm package for memory commands. <br>
Mitigation: Verify the npm package source and run the commands in a controlled workspace before relying on the generated memory files. <br>
Risk: Server security evidence flags inconsistent network and API claims. <br>
Mitigation: Confirm the package behavior and command output before treating the workflow as offline or dependency-free. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memo-quickstart-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead the agent to create or update local memory files such as SESSION-STATE.json, MEMORY.md, and memories/*.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
