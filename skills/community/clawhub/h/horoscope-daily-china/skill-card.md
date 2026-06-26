## Description: <br>
Creates 12 constellation fortune images with TianAPI as a five-page, large-font output for social media publishing on Xiaohongshu, Douyin, and Toutiao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangj85](https://clawhub.ai/user/zhangj85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators and operators use this skill to generate daily Chinese horoscope image sets and publishing copy for social platforms. The workflow requires the user to supply a TianAPI key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TianAPI credentials are required for normal use. <br>
Mitigation: Create a local config.json with the user's own TianAPI key and keep that file out of version control. <br>
Risk: Generated horoscope scores are presentation-adjusted entertainment content. <br>
Mitigation: Present the output as entertainment only and preserve the disclaimer that it should not be treated as decision guidance. <br>
Risk: The required config.json structure may be missing after installation. <br>
Mitigation: Create the expected config.json before running the generator and verify the TianAPI endpoint and quota settings. <br>


## Reference(s): <br>
- [Daily Horoscope Creator ClawHub page](https://clawhub.ai/zhangj85/horoscope-daily-china) <br>
- [TianAPI](https://www.tianapi.com/) <br>
- [Horoscope Image Standard](references/horoscope-image-standard.md) <br>
- [Script Usage README](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Configuration, Shell commands] <br>
**Output Format:** [PNG image files plus a publishing-copy text file; usage instructions are Markdown with shell commands and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates five 1080x1400 PNG pages and one publishing-copy text file; requires a user-provided TianAPI key.] <br>

## Skill Version(s): <br>
1.2.1 (source: evidence release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
