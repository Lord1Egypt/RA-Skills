## Description: <br>
Text-to-speech via OpenAI Audio Speech API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pors](https://clawhub.ai/user/pors) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to convert text into speech audio through OpenAI's Audio Speech API, with options for voice, model, audio format, speed, and output file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation is sent to OpenAI under the user's account. <br>
Mitigation: Use an appropriate API key and avoid sending secrets or regulated content unless approved for the account and use case. <br>
Risk: API usage may incur OpenAI account charges and depends on local command-line tools. <br>
Mitigation: Confirm usage limits or budget before running the skill, and ensure curl and jq are installed. <br>


## Reference(s): <br>
- [OpenAI text-to-speech documentation](https://platform.openai.com/docs/guides/text-to-speech) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Shell script invocation that returns audio bytes to stdout or writes an audio file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY, curl, and jq; supports voice, model, format, speed, and output path options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
