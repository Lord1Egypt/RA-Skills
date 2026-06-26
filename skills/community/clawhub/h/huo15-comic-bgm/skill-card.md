## Description: <br>
Generates one mood-matched background music track for a comic-video script, favoring Chinese-style instrumental music with guzheng, pipa, and flute. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and automation agents use this skill to add a single soundtrack to a comic-video project from script mood data and a target duration. It is suited for workflows that can provide a script JSON, choose an output MP3 path, and manage the required paid API credential. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote music generation can send mood-based prompts to a paid Suno-compatible API. <br>
Mitigation: Use the skill only with scripts you intend to process remotely, set SUNO_API_KEY deliberately, and monitor paid API usage. <br>
Risk: The package bundles unused Ark media helper code beyond the BGM workflow. <br>
Mitigation: Review the bundled helper code before deployment and avoid configuring unrelated API credentials unless those helpers are separately trusted and needed. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/zhaobod1/huo15-comic-bgm) <br>
- [Publisher profile](https://clawhub.ai/user/zhaobod1) <br>
- [Suno-compatible API endpoint](https://api.sunoapi.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and generated MP3 file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a script JSON input, target duration, output path, and SUNO_API_KEY for remote generation; may use local fallback audio when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
