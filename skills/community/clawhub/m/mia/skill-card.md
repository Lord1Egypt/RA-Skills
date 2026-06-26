## Description: <br>
MIA helps OpenClaw reuse task experience through memory retrieval, planning, and feedback modules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingyangqiao](https://clawhub.ai/user/jingyangqiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to retrieve similar prior task trajectories, generate task plans from current and historical context, and collect answer-quality feedback for new questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task history, execution traces, questions, answers, and feedback can be stored persistently in local memory or feedback files. <br>
Mitigation: Keep memory and feedback files in private locations, avoid storing secrets or personal data, and periodically review or delete stored records. <br>
Risk: Planning prompts may be sent to a configured model API endpoint. <br>
Mitigation: Use local mode or a trusted HTTPS endpoint with a dedicated API key for sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jingyangqiao/mia) <br>
- [Main skill documentation](artifact/SKILL.md) <br>
- [MIA Memory documentation](artifact/mia-memory/SKILL.md) <br>
- [MIA Planner documentation](artifact/mia-planner/SKILL.md) <br>
- [MIA Feedback documentation](artifact/mia-feedback/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Memory and feedback commands read and write local JSONL files; planner output may use a configured OpenAI-compatible model endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
