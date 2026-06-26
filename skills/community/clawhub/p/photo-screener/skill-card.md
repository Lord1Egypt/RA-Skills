## Description: <br>
AI-powered photo pre-screening using MobileCLIP2-S0 for aesthetic scoring, near-duplicate removal, scene classification, and preparation of photo batches for multimodal LLM processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[konanok](https://clawhub.ai/user/konanok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to pre-screen large photo collections before sending selected images to a multimodal LLM. It scores image quality, removes near duplicates, classifies scenes, and writes a local screening report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download external ML model weights into the user's home cache. <br>
Mitigation: Pre-download and verify model files before agent use; avoid routine --auto-download use in automated workflows. <br>
Risk: The skill reads local photo paths and writes a local JSON report that can include filenames, full paths, scene labels, scores, and rejection details. <br>
Mitigation: Run it only on intended photo directories and review the report before sharing it with other tools or services. <br>
Risk: The aesthetic model source is a GitHub-hosted weight file that may need stricter supply-chain controls. <br>
Mitigation: Pin trusted model sources and use checksums or an internally approved cache when operating in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/konanok/photo-screener) <br>
- [Project homepage](https://github.com/konanok/photo-skills) <br>
- [Hugging Face mirror used for model downloads](https://hf-mirror.com) <br>
- [LAION aesthetic predictor weights](https://github.com/christophschuhmann/improved-aesthetic-predictor/raw/main/sac+logos+ava1-l14-linearMSE.pth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and a local JSON screening report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report includes selected photos, rejected photos, duplicate groups, scene labels, scores, and LLM batch groupings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
