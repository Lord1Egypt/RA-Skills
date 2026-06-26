## Description: <br>
This skill lets an agent read, create, and update flomo memos, tags, daily reviews, memory context, and profile data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent work with their flomo account for memo creation, memo search and retrieval, daily reviews, memory context, user profile, formatting guidance, and tag management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private flomo account content, including memos, tags, daily reviews, and generated memory/profile data. <br>
Mitigation: Install only when the user trusts OOMOL and expects agent access to the connected flomo account. <br>
Risk: Write actions can create memos, update existing memos, or rename tags. <br>
Mitigation: Require explicit user confirmation of the exact payload and intended effect before running write actions. <br>
Risk: Broad trigger wording can cause the skill to be selected for many flomo-related requests. <br>
Mitigation: Use the skill for flomo tasks, but confirm before any state-changing action and rely on the live action schema before constructing payloads. <br>


## Reference(s): <br>
- [flomo homepage](https://flomoapp.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-flomo) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read private flomo account data and may propose or execute write actions after user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
