## Description: <br>
Deploy OpenClaw securely on AWS with a single command. Creates VPC, EC2 (ARM64), Telegram channel, and configurable AI model (Bedrock, Gemini, or any provider) - SSM-only access, no SSH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godwinbabu](https://clawhub.ai/user/godwinbabu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to deploy, test, operate, and tear down an OpenClaw agent on AWS with EC2, SSM, Telegram, and configurable model providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment helper can grant broad AWS authority. <br>
Mitigation: Review before installing, prefer AWS SSO or an assume-role flow, run setup_deployer_role.sh --dry-run, and narrow the deployer policy to the specific SSM parameter paths, tagged instances, and IAM role/profile names. <br>
Risk: The deployed agent is persistent and includes proactive personal-assistant behaviors. <br>
Mitigation: Disable or edit the default heartbeat, memory, and agent-to-agent settings if the intended deployment should only run on demand. <br>
Risk: The skill handles AWS credentials, Telegram tokens, Gemini keys, and generated AWS keys. <br>
Mitigation: Treat .env.aws, Telegram tokens, Gemini keys, and generated AWS keys as secrets and avoid IAM-user access keys when SSO or assume-role access is available. <br>
Risk: Teardown can remove cloud resources if pointed at the wrong deployment or account. <br>
Mitigation: Use teardown only after verifying the target output file, deployment ID, and AWS account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godwinbabu/openclaw-aws-deploy) <br>
- [Troubleshooting guide](references/TROUBLESHOOTING.md) <br>
- [Gemini Flash configuration template](references/config-templates/gemini-flash.json) <br>
- [Gemini auth profiles template](references/config-templates/auth-profiles-gemini.json) <br>
- [OpenClaw systemd service template](references/config-templates/openclaw.service.txt) <br>
- [OpenClaw startup script template](references/config-templates/startup.sh) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Code, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands, configuration snippets, and generated deployment files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces AWS deployment output files, IAM setup guidance, preflight checks, smoke tests, and teardown commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, CHANGELOG released 2026-02-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
