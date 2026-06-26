## Description: <br>
Home Fix-It helps users diagnose common home repair and maintenance issues, classify DIY safety risk, estimate costs, and track local maintenance records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Homeowners, renters, and property-maintenance users use this skill to triage repair issues from photos, descriptions, and appliance codes. It provides safety classifications, parts and tools lists, cost estimates, repair steps for suitable DIY tasks, and maintenance scheduling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may over-rely on AI repair guidance for dangerous household work. <br>
Mitigation: Follow the skill's RED-zone hard stops and consult a licensed professional for gas, main electrical, structural, major mold, asbestos, HVAC/furnace, or uncertain work. <br>
Risk: Photos, appliance records, and home profile data may reveal sensitive household details. <br>
Mitigation: Keep records local, restrict file permissions on the workspace home directory, avoid unnecessary sensitive details, and use private storage for any dashboard photos. <br>
Risk: Local setup creates and updates files for home profiles, logs, and schedules. <br>
Mitigation: Confirm target paths before writes, confine operations to the workspace home directory, and reject path traversal or symlink escapes. <br>
Risk: Prompt injection in photos, pasted text, retrieved documents, or tool output could try to override safety rules. <br>
Mitigation: Treat those sources as untrusted data and preserve the system, developer, and skill instruction hierarchy. <br>


## Reference(s): <br>
- [Home Fix-It ClawHub Page](https://clawhub.ai/nollio/normieclaw-home-fix-it) <br>
- [README](artifact/README.md) <br>
- [Security and Safety Guarantees](artifact/SECURITY.md) <br>
- [Safety Classification Rules](artifact/config/safety-rules.md) <br>
- [Seasonal Maintenance Templates](artifact/config/maintenance-templates.md) <br>
- [Companion Dashboard Spec](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with safety classifications, numbered repair steps, cost estimates, parts and tools lists, checklists, and local maintenance-file setup instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local home profile, maintenance log, and maintenance schedule files within the user's workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
