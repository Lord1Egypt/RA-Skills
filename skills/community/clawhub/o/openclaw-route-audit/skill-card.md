## Description: <br>
Use static route analysis plus runtime cron delivery audit to validate OpenClaw cron notification wiring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit OpenClaw cron notification routing, compare static route checks with runtime delivery results, and identify mismatches or silent delivery failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit reads local OpenClaw cron configuration and a local runtime audit script. <br>
Mitigation: Inspect the referenced local files before use and confirm they do not contain secrets or content you are unwilling to process locally. <br>
Risk: The helper relies on openclaw-route-check from PATH or ROUTE_CHECK_BIN. <br>
Mitigation: Verify that the resolved executable is the trusted openclaw-route-check binary before running the audit. <br>
Risk: Some OpenClaw files may require elevated access depending on local installation permissions. <br>
Mitigation: Avoid elevated privileges unless the required /root/.openclaw files genuinely require them. <br>
Risk: The helper temporarily writes audit JSON files under /tmp. <br>
Mitigation: Run it in an environment where temporary local audit outputs are acceptable and clean up temporary files if needed. <br>


## Reference(s): <br>
- [OpenClaw Route Audit ClawHub release](https://clawhub.ai/pfrederiksen/openclaw-route-audit) <br>
- [openclaw-route-check repository](https://github.com/pfrederiksen/openclaw-route-check) <br>
- [GitHub Publish Notes](references/github-publish-notes.md) <br>
- [Publish Checklist](references/publish-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled helper emits combined JSON audit results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit posture; helper checks local prerequisites and temporarily writes audit JSON under /tmp.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
