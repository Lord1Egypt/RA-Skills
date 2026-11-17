## Description:

Helps agents research Kaggle competitions and manage Kaggle datasets, models, notebooks, submissions, discussions, benchmarks, and badges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shepsci](https://clawhub.ai/user/shepsci)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kaggle participants use this skill to research competitions, inspect results, download resources, and manage submissions, notebooks, datasets, models, and badges through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad changes to a Kaggle account, including submissions, notebook runs, publishing, and badge automation; permission metadata may not fully reflect this authority.

Mitigation: Use the top-level command entry point, review dry runs, and obtain explicit approval before account changes; keep KAGGLE_SKILL_READ_ONLY=1 for read-only work.

Risk: Running badge phase scripts directly can change the account without the normal review flow.

Mitigation: Avoid running badge phase scripts directly unless those changes are intended and authorized.

## Reference(s):

- [Kaggle skill release on ClawHub](https://clawhub.ai/shepsci/skills/kaggle)
- [Project homepage listed in release metadata](https://github.com/shepsci/kaggle-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance, Files]

**Output Format:** [Short text or optional JSON; commands can download files and produce local records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public reads need no account credential; account operations require Kaggle authentication.]

## Skill Version(s):

3.0.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
