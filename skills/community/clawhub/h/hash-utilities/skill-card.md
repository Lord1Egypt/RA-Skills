## Description:

Generate and verify hashes for strings and files using MD5, SHA variants, CRC32, HMAC, and BLAKE2 with a zero-dependency Python utility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compute hashes, verify file integrity, batch-hash local files, and generate HMAC signatures for selected input data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HMAC keys supplied on the command line may be exposed through shell history or process listings.

Mitigation: Use non-sensitive keys for routine use, or adapt the workflow to read HMAC keys from a prompt, stdin, or another secret-safe channel.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated hash values depend on the selected algorithm and input data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
