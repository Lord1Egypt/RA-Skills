## Description: <br>
Text-to-speech via OpenAI Audio Speech API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicoataiza](https://clawhub.ai/user/nicoataiza) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to generate speech from text with OpenAI's Audio Speech API, selecting supported voices, models, formats, speed, and an optional output file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text supplied to the skill is sent to OpenAI's speech API using the configured API key. <br>
Mitigation: Install only when that data transfer is acceptable for the intended use, and avoid submitting sensitive text unless permitted by the user's policy. <br>
Risk: API usage may incur charges on the configured OpenAI account. <br>
Mitigation: Use an appropriate API key, monitor usage, and set account-level limits where available. <br>
Risk: The skill requires a local API key and may read it from environment or local configuration. <br>
Mitigation: Keep OPENAI_API_KEY and any local configuration files out of source control and restrict local file permissions. <br>
Risk: The script depends on jq even though the declared binary requirement only lists curl. <br>
Mitigation: Install jq before use or update the skill metadata to declare jq as a required binary. <br>


## Reference(s): <br>
- [OpenAI Text-to-Speech Documentation](https://platform.openai.com/docs/guides/text-to-speech) <br>
- [ClawHub Skill Page](https://clawhub.ai/nicoataiza/openai-tts-bak-2026-01-28t18-01-23-10-30) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, API Calls, Configuration instructions] <br>
**Output Format:** [Audio file or binary audio stream, with optional output path text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and OPENAI_API_KEY; supports voice, model, audio format, speed, and output-path options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
