## Description: <br>
Manage DNS zones across multiple providers using octoDNS ("DNS as code"). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markjr](https://clawhub.ai/user/markjr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, infrastructure engineers, and DNS operators use this skill to manage DNS zone files, preview octoDNS changes, sync providers, migrate zones, and automate record updates with safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles high-value DNS credentials and live DNS changes. <br>
Mitigation: Review or patch credential handling before installation, use a user-controlled or secret-manager location, set credential files to 600 permissions, and use least-privilege DNS API tokens. <br>
Risk: Running octoDNS with --doit can make production-impacting DNS changes, including unintended record deletion when zone YAML omits existing records. <br>
Mitigation: Always dump existing zones first, run a dry-run preview, review delete lines and record counts, and require explicit confirmation before applying changes. <br>
Risk: Webhook or CI automation examples can become unsafe if deployed without controls. <br>
Mitigation: Do not deploy webhook or CI examples without authentication, input validation, approval gates, and protected secrets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/markjr/octodns-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/markjr) <br>
- [Author GitHub Profile](https://github.com/markjr) <br>
- [octoDNS Documentation](https://octodns.readthedocs.io/) <br>
- [octoDNS GitHub Repository](https://github.com/octodns/octodns) <br>
- [octodns-easydns Provider](https://github.com/octodns/octodns-easydns) <br>
- [DNS Record Format Guide](references/records.md) <br>
- [Provider Migration Guide](references/migration.md) <br>
- [Dynamic DNS Guide](references/dynamic-dns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide agents to create or modify local DNS configuration files and run octoDNS helper scripts.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
