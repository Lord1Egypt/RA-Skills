## Description: <br>
Automates Jianying/Xiaoyunque Seedance 2.0 video generation for text-to-video, image-to-video, and reference video-to-video workflows using Playwright and a user-provided Jianying login session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Deemo-Soul](https://clawhub.ai/user/Deemo-Soul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video creators use this skill to drive Jianying's web interface for AI video generation, including prompt-only generation and transformations from reference images or videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes real-looking browser session cookies and automatically uses cookies.json. <br>
Mitigation: Delete the bundled cookies.json before use and provide only your own Jianying credentials after deciding to trust the publisher. <br>
Risk: Prompts and selected reference media are submitted to Jianying during generation. <br>
Mitigation: Avoid sensitive prompts or media unless sharing them with Jianying is acceptable for the intended use. <br>
Risk: Generation can consume Jianying credits and the output path behavior may be unexpected. <br>
Mitigation: Confirm credit costs before generation and set an explicit output_dir for all runs. <br>


## Reference(s): <br>
- [Seedance 2.0 Prompt Guide](references/prompt-guide.md) <br>
- [Jianying Xiaoyunque](https://xyq.jianying.com/home) <br>
- [ClawHub Skill Page](https://clawhub.ai/Deemo-Soul/jianying-video-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated local video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Jianying cookies.json file and may write MP4 outputs or dry-run screenshots to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
