## Description:

Reviews Chinese theses with structure-aware checks, style learning from user-provided reference papers, and Word comment injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urnotlhh](https://clawhub.ai/user/urnotlhh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review Chinese undergraduate or master's theses, learn a style profile from their own reference papers, and return findings as structured reports and Word comments for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM endpoint configuration can expose credentials when used with sensitive thesis content.

Mitigation: Review endpoint settings before installation and use explicit per-endpoint API keys instead of relying on global OpenClaw credentials.

Risk: DOCX input and output handling can affect unrelated local files if paths are reused or supplied by an untrusted party.

Mitigation: Use a dedicated empty output directory, avoid untrusted DOCX files, and do not accept review configs from untrusted users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urnotlhh/skills/paper-style-review)
- [README](README.md)
- [Review config example](references/review-config.example.json)
- [Project defaults](references/project-defaults.json)
- [Style profile schema](references/style-profile.schema.json)
- [Style profile extractor](references/style-profile-extractor.md)
- [Format rule matrix](references/format-rule-matrix.md)
- [Format rules](references/format-rules.json)
- [Format public addendum](references/format-public-addendum.md)
- [AI diff report schema](references/ai-diff-report.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON, Markdown, and annotated DOCX files produced by a command-line review pipeline.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces style-profile.json, ref-style-basis.md, target-structure-map.json, target-style-units.json, review reports, annotations.json, final-advice.md, run-summary.json, and <target>-annotated.docx when configured inputs are available.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
