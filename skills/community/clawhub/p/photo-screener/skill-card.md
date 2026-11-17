## Description:

AI-powered photo pre-screening that scores aesthetic quality, removes near duplicates, and classifies scenes with MobileCLIP2-S0 before multimodal LLM processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[konanok](https://clawhub.ai/user/konanok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to reduce large photo batches into ranked, deduplicated, scene-labeled selections before sending images to a multimodal LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and loads external ML model files without integrity verification.

Mitigation: Install and run it in a virtual environment, review the setup script first, avoid --auto-download unless the model sources are approved, and prefer manually downloaded verified model artifacts.

Risk: The skill processes local photo directories and writes report files containing image paths and screening metadata.

Mitigation: Run it only on photo directories approved for local processing and avoid elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/konanok/skills/photo-screener)
- [Project homepage](https://github.com/konanok/photo-skills)
- [Improved aesthetic predictor weights](https://github.com/christophschuhmann/improved-aesthetic-predictor/raw/main/sac+logos+ava1-l14-linearMSE.pth)
- [Hugging Face mirror used for model downloads](https://hf-mirror.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON report plus console status and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces filter_report.json with summary metrics, selected photo batches, rejected low-score photos, duplicate groups, and encode errors.]

## Skill Version(s):

1.0.0 (source: frontmatter, VERSION, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
