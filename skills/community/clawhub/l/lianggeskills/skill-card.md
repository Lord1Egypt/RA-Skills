## Description:

Lianggeskills is a Chinese personal workflow assistant for Web3/AI work that manages task priorities, task status, progress check-ins, and supportive responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[271498019](https://clawhub.ai/user/271498019)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill as a Chinese-language personal work assistant for Web3, crypto, on-chain trading, meme-coin, alpha-discovery, and AI-trend workflows. It helps sort work through an Eisenhower matrix, track tasks across four states, issue progress reminders, and provide emotional-support responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad high-priority trigger phrases can interrupt work or change task state too easily.

Mitigation: Review and narrow trigger phrases before deployment, and require explicit confirmation before actions that pause work or alter task state.

Risk: The skill can proactively message the user during configured work hours.

Mitigation: Confirm the desired timezone, work-hour window, and reminder intervals before enabling timer-driven actions.

Risk: Task records are kept in local task memory and may include sensitive work details.

Mitigation: Clarify where task memory is stored, restrict access to the storage location, and avoid sensitive tasks unless retention is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/271498019/skills/lianggeskills)
- [ClawHub Publisher Profile](https://clawhub.ai/user/271498019)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Plain text and Markdown-style task/status responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local task-state and quote-library JSON files when executed in a compatible OpenClaw environment.]

## Skill Version(s):

1.0.0 (source: skill frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
