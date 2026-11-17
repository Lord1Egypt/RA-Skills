## Description:

Outreach Manager helps agents draft personalized creator, media, analyst, launch-partner, and social-selling outreach, follow-up cadences, negotiation scripts, and pipeline trackers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, founder-led sales teams, and agent operators use this skill to create creator, media, analyst, hunter, launch-partner, and advocate outreach. It turns campaign inputs, target details, budget, deliverables, and prior relationship context into ready-to-review messages, follow-ups, negotiation guidance, and pipeline tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store or propose updates containing contact paths, rates, response history, and pipeline status while the manifest declares only read access.

Mitigation: Review persistence requests before saving, avoid unnecessary sensitive relationship data, and prefer releases whose manifest declares narrow write permissions for any persisted outreach records.

Risk: Outreach drafts could include unverified creator claims, rates, past partnerships, content references, or performance data.

Mitigation: Verify specific claims before sending; when details cannot be verified, generalize them and follow the cold-copy rules.

Risk: Shared hot-cache updates could expose relationship details beyond the active outreach cycle.

Mitigation: Keep shared hot-cache entries minimal and limited to durable, non-sensitive facts needed for future work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/outreach-manager)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Cold Outreach Copy Rules](artifact/references/cold-copy-rules.md)
- [Outreach Manager Templates](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown outreach artifacts with message variants, follow-up cadence tables, negotiation scripts, and pipeline trackers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed memory updates for contact paths, rates, response history, and pipeline status when the agent host permits persistence.]

## Skill Version(s):

19.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
