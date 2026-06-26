## Description: <br>
Control Tesla vehicles from macOS via the Tesla Owner API using teslapy for authentication, vehicle listing, status, lock/unlock, climate, charging, location, and related remote commands with local-only auth caching and confirmation gates for disruptive actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[officialpm](https://clawhub.ai/user/officialpm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Tesla owners and developers use this skill to check vehicle state, generate chat-friendly reports, and run explicit remote vehicle commands from macOS while keeping authentication cache, defaults, and mileage history local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a Tesla account and issue real vehicle commands. <br>
Mitigation: Install only when that access is acceptable, review proposed commands before execution, and rely on documented confirmation gates for disruptive actions. <br>
Risk: Token caches, mileage databases, exports, raw JSON, and precise location outputs can contain sensitive vehicle or account data. <br>
Mitigation: Keep local cache and export files private, avoid committing logs or outputs, and prefer sanitized JSON or approximate location unless precise data is explicitly needed. <br>
Risk: Recurring mileage recording through launchd can repeatedly query vehicles and may wake them depending on configuration. <br>
Mitigation: Review the launchd configuration before enabling it and preserve the documented no-wake and auto-wake limits for routine recording. <br>


## Reference(s): <br>
- [My Tesla ClawHub release page](https://clawhub.ai/officialpm/my-tesla) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; command results may be plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands can issue real vehicle actions, use local credential caching, or expose sensitive vehicle data when raw JSON or precise location is requested.] <br>

## Skill Version(s): <br>
0.1.64 (source: server release metadata, VERSION.txt, and CHANGELOG.md, released 2026-01-29) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
