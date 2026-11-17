## Description:

科研技能鉴赏 routes users to a curated set of 13 Chinese academic workflow skills for literature search, citation checking, research integrity review, paper meetings, defense practice, methodology support, and skill improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and agent users use this skill as a lightweight router for choosing the right Chinese academic workflow skill before starting a research task. It helps select specialized skills for literature retrieval, knowledge-base management, citation validation, integrity checks, meeting preparation, defense rehearsal, methodology guidance, and skill authoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect this router skill to perform retrieval, checking, conversion, or knowledge-base work directly.

Mitigation: State that the skill is an entry point only and hand off concrete tasks to the matching specialized skill.

Risk: A routing mistake could send a research task to a neighboring skill with a different scope.

Mitigation: Compare the request against the quick routing table and the listed boundaries before recommending a skill.

Risk: Recommended SmartLib-dependent skills may share the same wallet quota.

Mitigation: Tell users that SmartLib search, download, and verification skills share quota under the same email.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j-levee/skills/keji-skill-showcase)
- [SkillHub installation guide](https://skillhub.cn/install/skillhub.md)
- [SkillHub skill listing](https://skillhub.cloud.tencent.com/skills/keji-skill-showcase)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown text with routing recommendations and installation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not execute retrieval, checking, conversion, or code-running tasks itself.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
