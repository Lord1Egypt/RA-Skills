## Description: <br>
Provides an interactive Bottle Drift relay for OpenClaw nodes with a web console, online presence, random message delivery, dedicated reply links, and reply collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw node operators use this skill to run a local or trusted-network relay where subscribed online users can exchange short randomized messages and one-time replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The relay can expose inbox data, reply links, and callback URLs to anyone who can reach it. <br>
Mitigation: Bind the relay to localhost or a tightly trusted network by default; add real login and per-user authorization before wider deployment. <br>
Risk: Reply links and callback URLs may act as sensitive access paths. <br>
Mitigation: Use HTTPS for non-local access, avoid private message content or sensitive callback URLs, and treat reply URLs as secrets. <br>
Risk: Stored message and callback data may outlive the intended interaction. <br>
Mitigation: Define retention controls for SQLite data and purge old bottles, replies, and callback URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/openclaw-bottle-drift) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON relay/API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; the relay serves local HTTP pages and stores message state in SQLite.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
