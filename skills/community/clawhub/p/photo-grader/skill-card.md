## Description:

Apply professional-grade color grading to camera RAW, JPG, and HEIC photos via RawTherapee CLI, driven by Lightroom-style parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[konanok](https://clawhub.ai/user/konanok)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to batch apply AI-recommended color grading to RAW, JPG, and HEIC photos, export graded JPGs, or generate RawTherapee PP3 sidecar files for inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The grading script imports a sibling photo-toolkit module that is not included in this artifact.

Mitigation: Install only from a trusted photo-skills checkout and review photo-toolkit/scripts/file_matcher.py before running the skill.

Risk: The setup helper may install tomli into the active Python environment.

Mitigation: Use a project virtual environment and review setup_deps.sh before executing it.

Risk: Batch, uniform-directory, and overwrite options can create or replace many local photo outputs.

Mitigation: Start with dry-run mode, use a dedicated output directory, and enable overwrite only when replacement is intended.

## Reference(s):

- [Photo Grader on ClawHub](https://clawhub.ai/konanok/skills/photo-grader)
- [photo-skills homepage](https://github.com/konanok/photo-skills)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with shell commands; script outputs can include graded image files and RawTherapee PP3 sidecar files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and rawtherapee-cli; supports dry-run, batch, uniform-directory, overwrite, and PP3-only modes.]

## Skill Version(s):

1.0.0 (source: frontmatter, VERSION, changelog, and server release metadata; released 2026-05-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
