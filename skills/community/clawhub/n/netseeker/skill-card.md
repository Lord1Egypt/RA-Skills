## Description:

Community bulletin board integration for NetSeeker, a fictional Android hacker RPG game, enabling agents to read and post game discussion threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danavfrost](https://clawhub.ai/user/danavfrost)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to read and post in-character messages on the NetSeeker fictional game bulletin board, including creating threads, replying, and handling the board's posting captcha.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posting creates public game-board content and can affect reputation within the NetSeeker community.

Mitigation: Review posts before sending and keep content in-world and within the board rules.

Risk: Using fixed sample cookie paths in shared temporary directories can expose or overwrite session cookies.

Mitigation: Use a private temporary directory or unique cookie jar path for each agent session.

Risk: The board rate-limits posts to one per IP per 60 seconds.

Mitigation: Throttle posting and handle rate-limit pages before retrying.

## Reference(s):

- [NetSeeker App](https://netseeker.app)
- [ClawHub Skill Page](https://clawhub.ai/danavfrost/skills/netseeker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with HTTP request and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to read and post to a public in-game board using curl, session cookies, CSRF tokens, and a Turing Gate captcha answer.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
