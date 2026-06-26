## Description: <br>
Manage and monitor a local Pi-hole instance by querying the FTL database for statistics and helping run Pi-hole CLI management commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect Pi-hole query statistics, identify high-volume clients or domains, update gravity, and manage blocking on a local Pi-hole deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pi-hole blocking toggles, gravity updates, and other CLI operations can make live network changes. <br>
Mitigation: Require explicit user confirmation before running state-changing or sudo commands. <br>
Risk: The skill needs local read access to /etc/pihole/pihole-FTL.db, which can expose DNS query history. <br>
Mitigation: Grant the minimum required local permissions and avoid sharing query output beyond the intended operator context. <br>


## Reference(s): <br>
- [Pi-hole Database Schema](references/db-schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/1999AZZAR/pihole-ctl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command output and inline shell commands when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only Pi-hole FTL database query results and proposed Pi-hole CLI commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
