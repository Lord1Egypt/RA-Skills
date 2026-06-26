## Description: <br>
Scores photos for aesthetic and technical quality, then provides bilingual feedback, improvement suggestions, and optional comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kooui](https://clawhub.ai/user/kooui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Photographers, content creators, and external users can use this skill to evaluate one or more local images, compare aesthetic quality, and receive practical composition, color, lighting, technical quality, shooting, and post-processing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes user-supplied images with local Python ML dependencies and third-party model weights. <br>
Mitigation: Install and run it only in environments where local ML code and the configured model weights are approved. <br>
Risk: Photo inputs may contain sensitive personal or location information, and the skill workflow asks the agent to prepare a detailed evaluation for later retrieval. <br>
Mitigation: Use local processing for sensitive photos and request no retention of detailed evaluations when retention is not appropriate. <br>
Risk: Model-based aesthetic scoring can be subjective and may not reflect a user's audience, culture, brand, or accessibility goals. <br>
Mitigation: Treat scores and suggestions as decision support and review recommendations before using them for publication or commercial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kooui/photo-scorer) <br>
- [Publisher profile](https://clawhub.ai/user/kooui) <br>
- [Improved Aesthetic Predictor](https://github.com/christophschuhmann/improved-aesthetic-predictor) <br>
- [Neural Image Assessment](https://github.com/titu1994/neural-image-assessment) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports with optional JSON scoring output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports concise, medium, and detailed report lengths; scores are on a 0-10 scale with rating labels.] <br>

## Skill Version(s): <br>
1.4.10 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
