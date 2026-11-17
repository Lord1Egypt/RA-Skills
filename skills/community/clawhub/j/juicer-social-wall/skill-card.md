## Description:

Run a live event social wall with Juicer, collecting hashtag posts across social networks for moderation and display on a screen or website.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juicer](https://clawhub.ai/user/juicer)

### License/Terms of Use:

MIT-0

## Use Case:

Event organizers use this skill to set up a hashtag wall for conferences, weddings, campaigns, and other events, then review, approve, hide, or pin posts before sharing the wall on a public screen or website.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posts shown on a public event wall may be unwanted or unrelated.

Mitigation: Enable the approval queue for public screens and review posts before approving them, especially before bulk approval.

Risk: Connected sources may involve account access, plan limits, or source costs.

Mitigation: Review connected accounts, source costs, and source sync status before handing over the wall.

Risk: Periodic checks may continue after the event if they are enabled.

Mitigation: If periodic checks are accepted, arrange to stop them after the event.

Risk: The separate Juicer integration was outside the scope of this skill's security review.

Mitigation: Review that integration separately before connecting it.

## Reference(s):

- [Juicer](https://www.juicer.io)
- [Juicer Developer Resources](https://www.juicer.io/developer)
- [ClawHub skill page](https://clawhub.ai/juicer/skills/juicer-social-wall)

## Skill Output:

**Output Type(s):** [Configuration, Guidance, Text]

**Output Format:** [Juicer feed setup and moderation actions, plus a wall link or embed and optional event recap in chat.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the event's hashtags, selected social networks, connected accounts, and moderation preferences.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
