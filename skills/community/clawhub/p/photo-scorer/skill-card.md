## Description:

给你的照片打分、评价反馈、给出改进建议或美学分析 / Aesthetic photo scorer with detailed analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

Photographers, content creators, and visual reviewers use this skill to score photos, compare images, and receive composition, color, lighting, technical quality, and improvement guidance in Chinese or English.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation relies on mutable third-party code, unpinned machine-learning packages, and unchecked model files.

Mitigation: Review install steps before use, install in a dedicated virtual environment or container as a non-admin user, pin dependency versions, verify model checksums, and avoid dependency installs from mutable third-party repositories unless those sources are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kooui/skills/photo-scorer)
- [Publisher profile](https://clawhub.ai/user/kooui)
- [Improved Aesthetic Predictor](https://github.com/christophschuhmann/improved-aesthetic-predictor)
- [NIMA neural image assessment](https://github.com/titu1994/neural-image-assessment)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown photo scoring reports with numeric scores, rating labels, comparative tables, and improvement suggestions; scripts can also emit JSON score data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports concise, medium, and detailed report lengths; works with local image files and configurable local model paths.]

## Skill Version(s):

1.4.10 (source: server release metadata; artifact frontmatter and README list 1.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
