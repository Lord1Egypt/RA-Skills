## Description: <br>
Infinite organized memory that complements your agent's built-in memory with unlimited categorized storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to set up and maintain a local, categorized long-term memory folder for projects, people, decisions, domain knowledge, collections, and other structured information that grows over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores user-approved notes in a plaintext ~/memory folder, so sensitive information may persist locally. <br>
Mitigation: Avoid saving passwords, tokens, regulated data, or sensitive personal details unless the user intentionally wants that information persisted locally. <br>
Risk: Optional sync can copy selected built-in memory content into the local memory folder. <br>
Mitigation: Review exactly what will be copied before enabling sync, and keep sync one-way from built-in memory into ~/memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/memory) <br>
- [Skill homepage](https://clawic.com/skills/memory) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory templates](artifact/memory-template.md) <br>
- [Organization patterns](artifact/patterns.md) <br>
- [Troubleshooting guide](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, configuration notes, and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent to create, search, and maintain local plaintext files under ~/memory when the user chooses to use it.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
