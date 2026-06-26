## Description: <br>
Hippius Storage helps agents use Hippius decentralized storage on Bittensor Subnet 75 to upload files, query storage, and manage buckets through an S3-compatible API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxquick](https://clawhub.ai/user/maxquick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and operators use this skill to configure Hippius storage credentials, generate S3 and CLI commands, and inspect buckets, objects, credits, and account storage status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles powerful Hippius S3 and wallet-related credentials. <br>
Mitigation: Use least-privilege S3 keys, keep credentials in environment variables or local config, and avoid entering a wallet seed phrase unless it is necessary for the requested operation. <br>
Risk: Upload, sync, delete, pin, and unencrypted IPFS operations can modify storage state or expose data. <br>
Mitigation: Require explicit confirmation before state-changing or unencrypted operations, and prefer the recommended S3 workflow when it satisfies the task. <br>
Risk: The RPC endpoint option can query account and blockchain information but does not control where storage data is sent. <br>
Mitigation: Treat RPC configuration as account or status lookup only, and use the documented HTTPS S3 endpoint for storage operations. <br>


## Reference(s): <br>
- [Hippius Storage Guide](references/storage_guide.md) <br>
- [Hippius CLI Commands Reference](references/cli_commands.md) <br>
- [Hippius Docs](https://docs.hippius.com) <br>
- [Hippius Console](https://console.hippius.com) <br>
- [Hippius Stats](https://hipstats.com) <br>
- [Hippius CLI GitHub](https://github.com/thenervelab/hippius-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that require Hippius S3 credentials, AWS CLI, boto3, MinIO, or a local IPFS node.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
