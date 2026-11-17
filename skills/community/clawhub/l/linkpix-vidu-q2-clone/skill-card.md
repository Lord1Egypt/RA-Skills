## Description:

Helps sellers turn a reference video into a product-specific script and generate a Vidu Q2 marketing video through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and marketing teams use a reference video to draft a product-specific script and, after approving the cost and creative details, generate a short promotional video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference videos and product images may be uploaded to Qinghu AI, and an API key is required.

Mitigation: Upload only approved media and use a scoped or revocable API key where possible.

Risk: Video generation consumes credits and submitted tasks cannot be cancelled.

Mitigation: Review the generated script, model, duration, assets, and credit estimate; obtain explicit approval before submission.

Risk: Recreating a reference video too closely could copy protected material or misrepresent originality.

Mitigation: Borrow structure and pacing while creating original product-specific visuals and dialogue.

Risk: Installing or upgrading qhkit runs third-party software locally.

Mitigation: Prefer a preinstalled or pinned version and review commands before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-vidu-q2-clone)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key settings](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with script comparisons, commands, and video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the task ID, completed video URL, and charged credits when available.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
