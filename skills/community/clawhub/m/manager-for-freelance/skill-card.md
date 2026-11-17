## Description:

Evaluates freelance job listings against Caleb Lopez's AI automation profile, skips poor fits, and drafts concise proposals for suitable opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caleb-lopz](https://clawhub.ai/user/caleb-lopz)

### License/Terms of Use:

MIT-0

## Use Case:

External freelancers and their agents use this skill to triage job-match notifications, compare each opportunity with a packaged freelancer profile, and generate either a one-line skip decision or a fit verdict with a ready-to-send proposal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: In a mixed-purpose chat, the skill may treat unrelated messages as job listings.

Mitigation: Use it in a dedicated job-posting context or invoke it explicitly when evaluating a job post.

Risk: Generated proposals or fit verdicts may be misleading if the job post is vague or the profile evidence is incomplete.

Mitigation: Review the verdict and proposal before sending, and confirm that every claimed qualification is supported by the packaged profile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caleb-lopz/skills/manager-for-freelance)
- [Publisher profile](https://clawhub.ai/user/caleb-lopz)
- [Caleb Lopez profile evidence](artifact/profile.md)
- [Proposal template evidence](artifact/proposal_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown containing a skip decision, or a verdict, proposal, and tactics section.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposal body targets 80-120 words and uses only the packaged profile as qualification evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
