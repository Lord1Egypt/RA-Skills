## Description: <br>
Health check dashboard for agent platform APIs that tests availability, response time, authentication status, Cloudflare blocking, and SSL validity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minduploadedcrab](https://clawhub.ai/user/minduploadedcrab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and platform operators use this skill to run CLI health checks across agent platform APIs, inspect uptime and response behavior, and review authentication, Cloudflare, and SSL status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The health check can read API keys from existing ClawQuests, Colony, or Bankr config files and send them to the corresponding service auth endpoints. <br>
Mitigation: Review data/platforms.json before running; use --only to limit targets, --no-history to avoid saving results, or remove auth_config entries for unauthenticated checks. <br>
Risk: Health checks contact multiple third-party and local endpoints and save result history by default. <br>
Mitigation: Run only where outbound checks are expected, narrow scope with --only, and add --no-history when local result persistence is not desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/minduploadedcrab/platform-healthcheck) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Platform Configuration](artifact/data/platforms.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal table text or JSON health-check results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save local result history to data/history.json unless --no-history is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
