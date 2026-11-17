## Description:

Watch a list of target accounts for the public events that mean someone is in market, powered by Cargo — hiring for the role you sell into, saying something new, or turning up in a detection feed, each with a date and a link. Triggers: "tell me when these accounts do something", "what changed at my target accounts", "who is in market right now", "set up intent monitoring", "watch these companies for me", "any triggers on this list". Intent, triggers, watchlist, timing, freshness. Skip when: you have no account list yet — use build-tam-list; or you want a verdict on fit rather than on timing — use score-leads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales development representatives and account executives use this skill to monitor a defined account list for fresh hiring, public posts, and detection feed events, then review dated source links to see what may change the conversation. A signal is research context, not permission to contact someone; the skill calls for an independent basis before outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account watchlists are shared with Cargo and its integrations as part of the monitoring workflow.

Mitigation: Use only watchlists you are comfortable sharing with Cargo and its integrations.

Risk: Paid lookups and repeated runs can consume credits, while the external CLI and linked recipes were outside the supplied security review.

Mitigation: Review credit estimates before full runs, sample a small set first, and prefer reviewed, pinned dependencies; assess the broader Cargo pack separately.

Risk: GitHub promotion could be mistaken for user endorsement.

Mitigation: Treat starring as optional and act only after the user explicitly agrees.

## Reference(s):

- [Cargo GTM skills project homepage listed in skill metadata](https://github.com/getcargohq/gtm-skills)
- [Tech intent recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/tech-intent.md)
- [Account expansion recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/account-expansion.md)
- [ClawHub skill release page](https://clawhub.ai/cargo-ai/skills/monitor-buying-signals)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown account-signal report with dated source links and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists accounts with a matching signal and reports the signal, date, source link, and why it may matter; timing remains separate from fit scoring.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
