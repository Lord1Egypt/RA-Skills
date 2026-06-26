## Description: <br>
Standardize OpenClaw cron wrappers, prompt contracts, and delivery-mode expectations for jobs that rely on ClankerHive claims, result JSON artifacts, cron delivery status, wrapper scripts, or reply-vs-message delivery behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit or design OpenClaw cron jobs so wrapper behavior, prompt handling, result artifacts, and delivery.mode settings stay aligned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides operational guidance for cron-job contract cleanup but does not enforce safe wrapper or delivery.mode changes itself. <br>
Mitigation: Review actual cron wrapper code and delivery.mode changes separately, then validate edited jobs before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pfrederiksen/openclaw-cron-standard) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown guidance with checklists and contract recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 for OpenClaw workflows that follow the documented contract.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
