## Description:

Review open feed recommendation repositories with source-backed evidence, artifact-readiness checks, and cautious architecture summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical reviewers use this skill to evaluate public feed recommendation repositories or claims, distinguish source-backed findings from unproven claims, and report artifact readiness or execution gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may overstate public repository evidence as proof of live-platform behavior, reach prediction, or production equivalence.

Mitigation: Frame findings as source-backed review only, and require needed artifacts plus user-supplied run evidence before treating execution or live behavior as verified.

Risk: Phoenix execution may be reported as verified before required artifacts and local run results are available.

Mitigation: State that source inspection succeeded but execution is blocked until the expected Phoenix artifacts are present and a local run result is supplied.

## Reference(s):

- [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)
- [Open Feed Recsys Reviewer ClawHub Page](https://clawhub.ai/zack-dev-cm/skills/open-feed-recsys-lab)
- [zack-dev-cm Publisher Profile](https://clawhub.ai/user/zack-dev-cm)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise Markdown review with target, supported claims, blocked checks, architecture summary, risks, and next verification step.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public source or user-provided local files only; does not treat Phoenix execution as verified without required artifacts and user-supplied run evidence.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
