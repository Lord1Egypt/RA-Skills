## Description: <br>
Place outbound phone calls via Mobayilo with safe defaults (preview mode by default) and explicit live execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adusingi](https://clawhub.ai/user/adusingi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw workflow operators use this skill to check Mobayilo readiness and place outbound calls for booking, confirmation, or follow-up workflows with dry-run defaults and explicit live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live execution can place real outbound calls using the user's Mobayilo account. <br>
Mitigation: Keep dry-run mode for testing and enable MOBY_REQUIRE_APPROVAL=1 for workflows that may place real calls. <br>
Risk: The skill depends on the external moby CLI installer or binary. <br>
Mitigation: Verify the moby installer or use a pinned trusted binary before enabling workflows. <br>
Risk: Local status logs and verification-script output can expose operational account or call details on shared hosts. <br>
Mitigation: Protect local log files and delete or secure /tmp verification outputs on shared systems. <br>


## Reference(s): <br>
- [Mobayilo homepage](https://mobayilo.com) <br>
- [Mobayilo Voice ClawHub listing](https://clawhub.ai/adusingi/mobayilo-voice) <br>
- [Mobayilo Voice Adapter Runbook](docs/runbook.md) <br>
- [Mobayilo Voice README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Operator summary text, JSON payloads, and Markdown instructions with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; live calls require explicit execution.] <br>

## Skill Version(s): <br>
0.2.0-beta.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
