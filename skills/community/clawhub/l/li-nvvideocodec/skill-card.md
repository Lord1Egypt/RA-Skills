## Description: <br>
Compresses batches of local videos with FFmpeg and NVIDIA NVENC AV1 hardware encoding, with selectable compression profiles and validation before batch runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users with a supported NVIDIA GPU use this skill to check the local video compression environment, analyze input video directories, and run test or batch AV1 compression jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The compression script can automatically install an unpinned Python package at runtime. <br>
Mitigation: Install tqdm from a trusted source before use, or run the skill in an isolated environment to avoid runtime package installation. <br>
Risk: The agent wrapper can launch batch compression without an in-script confirmation step. <br>
Mitigation: Run test mode on a small sample first, confirm the input and output directories, and inspect output quality before allowing a full batch run. <br>
Risk: Compression settings may reduce quality or fail to save space for already-compressed videos. <br>
Mitigation: Use the built-in validation pass and review the generated output directory before replacing or deleting any original files outside the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/43622283/li-nvvideocodec) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>
- [PyPI Mirror Used by Runtime Installer](https://pypi.tuna.tsinghua.edu.cn/simple) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON and terminal text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent interface supports environment checks, video directory analysis, and compression runs that write output files to a separate directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, SKILL.md frontmatter, skill.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
