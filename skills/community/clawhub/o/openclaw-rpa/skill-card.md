## Description:

Record browser and local-file actions once, then replay them without the LLM for faster, deterministic automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laziobird](https://clawhub.ai/user/laziobird)

### License/Terms of Use:

Apache License 2.0

## Use Case:

External users and developers use this skill to record browser, API, Excel, and Word workflows and compile them into replayable Python automation scripts. It is suited to repeated local RPA tasks where the user wants to verify a flow once and rerun it without model-driven browser control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce and run generated Python automation with broad local browser and file authority.

Mitigation: Run it in a dedicated workspace or VM and review generated scripts before replay.

Risk: Recorded workflows may store login cookies and API keys on disk.

Mitigation: Avoid production credentials when possible, rotate any keys placed into scripts, and delete saved cookie or key files when no longer needed.

Risk: Screenshots can be sent to configured vision providers and recorded scripts can make arbitrary API calls.

Mitigation: Use trusted providers, avoid sensitive pages during recording, and review API endpoints and payloads before replay.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laziobird/skills/openclaw-rpa)
- [ClawHub publisher profile](https://clawhub.ai/user/laziobird)
- [OpenClaw RPA project page linked in skill documentation](https://github.com/laziobird/openclaw-rpa)
- [Qwen3-VL vision model reference linked in skill documentation](https://github.com/QwenLM/Qwen3-VL)
- [Alpha Vantage API documentation linked in examples](https://www.alphavantage.co/documentation/#daily)
- [Advanced setup guide](articles/advanced-setup.md)
- [API call guide](articles/api-call-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated Python/Playwright automation scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replay scripts can create local files, make configured API calls, and use stored browser session data depending on the recorded workflow.]

## Skill Version(s):

1.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
