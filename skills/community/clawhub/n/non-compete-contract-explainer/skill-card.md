## Description:

Explain U.S. state-by-state and select international non-compete and restrictive-covenant law using bundled, source-cited jurisdiction snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0 for the server release; bundled content is CC BY 4.0

## Use Case:

External users and agents use this skill to explain how covered jurisdictions treat non-competes, non-solicits, blue-pencil rules, contractor reach, and related restrictive-covenant issues. It provides general legal information and directs fact-specific enforceability questions to licensed counsel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake jurisdiction summaries for legal advice about their own contract.

Mitigation: Present the skill as legal information only, avoid yes/no enforceability verdicts on user facts, and direct fact-specific questions to licensed counsel in the relevant jurisdiction.

Risk: Bundled legal snapshots may become stale as non-compete law changes.

Mitigation: Show the packaged, law-checked, human-review, and next-review dates, and recommend checking the canonical source before relying on an answer.

Risk: The skill mentions an optional unpinned npx install command for a related skill.

Mitigation: Do not run that command unless the installer deliberately wants the separate package and has reviewed or pinned the install source.

Risk: Optional canonical refreshes could expose user facts if performed carelessly.

Mitigation: Fetch only the fixed canonical URL for the jurisdiction and never send user facts or contract text upstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/skills/non-compete-contract-explainer)
- [OpenAgreements non-compete practice guides](https://openagreements.org/practice-guides/non-compete)
- [OpenAgreements editors](https://openagreements.org/editors)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown explanations with source citations, quality dates, and optional refresh guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline bundled jurisdiction snapshots; optional refresh should fetch only the fixed canonical URL after user approval.]

## Skill Version(s):

0.2.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
