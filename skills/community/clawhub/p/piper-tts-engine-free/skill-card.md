## Description: <br>
A local Piper-based text-to-speech skill for generating single MP3 voice outputs without cloud API calls or API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content creators use this skill to generate local offline speech from a single text input, usually as an MP3 file for voice messages, narration, or accessibility support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to run relative setup and speech scripts that are not present in the artifact, which could execute unrelated workspace files. <br>
Mitigation: Review the exact script path and contents before execution; only run trusted setup-piper.sh or piper-speak.sh files for explicit text-to-speech tasks. <br>
Risk: Broad trigger language could cause the skill to be applied to unrelated file, document, or conversion requests. <br>
Mitigation: Use the skill only for explicit local text-to-speech requests and decline unrelated file processing tasks. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown with inline bash commands, configuration snippets, and generated MP3 file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local MP3 output paths and optional audio_as_voice delivery markup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
