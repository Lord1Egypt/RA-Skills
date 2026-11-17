## Description:

Monitor DX clusters for rare station spots, track active DX expeditions, and get daily band activity digests for amateur radio operators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capt-marbles](https://clawhub.ai/user/capt-marbles)

### License/Terms of Use:


## Use Case:

External amateur radio operators use this skill to query DX cluster spots, monitor rare station activity, and generate daily band activity digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages scheduled background monitoring that makes recurring network connections and writes ongoing logs.

Mitigation: Run manual one-shot commands first, avoid root execution, and add cron jobs only after reviewing the network and logging behavior.

Risk: The monitor stores state and example alert logs in shared temporary paths.

Mitigation: Move state and logs to a private user-owned directory and define a cleanup or removal process before scheduled use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/capt-marbles/skills/ham-radio-dx)
- [NG3K Amateur Radio DX Announcements](https://www.ng3k.com/misc/adxo.html)
- [DX World](https://www.dx-world.net/)
- [425 DX News](http://www.425dxn.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from the monitor script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-line DX spot listings, daily digest text, cron configuration guidance, and optional JSON spot data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
