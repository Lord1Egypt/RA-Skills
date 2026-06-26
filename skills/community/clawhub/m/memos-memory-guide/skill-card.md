## Description: <br>
Use the MemOS Local memory system to search past conversations, retrieve exact memory context, write shared public memory, and discover or install related skills when prior context or preferences are needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binyuli](https://clawhub.ai/user/binyuli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when to search, retrieve, summarize, or share long-term conversation memory while answering user requests that depend on prior context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to rely on broad prior conversation context. <br>
Mitigation: Install it only when persistent memory recall is desired, and verify retrieved memory details before using them in user-facing answers. <br>
Risk: The skill describes writing shared public memory that may be visible across agents. <br>
Mitigation: Avoid storing sensitive personal, financial, credential, or confidential business details, and review public-memory writes before sharing user-derived information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binyuli/memos-memory-guide) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides memory search, retrieval, public-memory writes, task summaries, skill discovery, and skill installation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
