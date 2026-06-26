## Description: <br>
Runs Jogg lip sync using video and audio inputs, reuses tasks when available, and monitors status until completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joggai-tech](https://clawhub.ai/user/joggai-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run or check Jogg lip-sync tasks for supplied video and audio inputs, returning the task status and final generated video URL when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected video and audio files or URLs to Jogg for processing. <br>
Mitigation: Use the skill only with media that is appropriate to send to Jogg and avoid sensitive media unless approved for that service. <br>
Risk: The runner requires a Jogg API key and can use a non-default base URL. <br>
Mitigation: Use a revocable API key and leave JOGG_BASE_URL at the default unless the alternate endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [Jogg API pricing](https://www.jogg.ai/api-pricing/) <br>
- [Jogg API key setup](https://docs.jogg.ai/api-reference/v2/QuickStart/GettingStarted) <br>
- [ClawHub skill page](https://clawhub.ai/joggai-tech/jogg-lip-sync) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Machine-readable JSON result on stdout with progress logs on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task action, reuse state, task_id, status, result_url when successful, and error_message when failed.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
