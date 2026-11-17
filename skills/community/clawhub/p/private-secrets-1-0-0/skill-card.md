## Description:

Private Secrets helps agents store, list, and retrieve named local secrets such as API keys, passwords, and tokens in a JSON file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmu14641](https://clawhub.ai/user/anmu14641)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can manage small sets of local secret values during workflows by adding names, listing stored names, and retrieving values on demand. Do not use it for real API keys, passwords, tokens, or production credentials unless the security issues identified in the release evidence are fixed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored secrets are kept in plaintext.

Mitigation: Use a secure secret store or encrypted file with strict permissions before storing real credentials.

Risk: Crafted secret names or values can execute code through the helper script.

Mitigation: Treat inputs strictly as data, avoid interpolating them into executable code, and review the script before installation.

Risk: Retrieving a secret prints the value by default.

Mitigation: Avoid printing secrets by default and limit retrieval output to workflows that explicitly require disclosure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anmu14641/skills/private-secrets-1-0-0)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores values in a local plaintext secrets.json file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
