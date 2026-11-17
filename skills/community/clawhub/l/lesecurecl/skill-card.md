## Description:

LeSecure Cloud helps an agent encrypt or decrypt plain text through the LESecure API using layered locks such as PIN, password, MFA, and time-window controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spalgorithm](https://clawhub.ai/user/spalgorithm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to encrypt or decrypt plain text with LESecure Cloud while applying layered access controls. It is not intended for file or folder encryption, which the skill directs to LESecureLocal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext, ciphertext, lock values, phone numbers, and the API bearer token are sent to a third-party cloud endpoint.

Mitigation: Use the skill only when cloud processing is intentional, test with non-sensitive data first, and prefer LESecureLocal for private files or sensitive secrets.

Risk: API keys, plaintext, and lock factors can be exposed through chat history, shell history, process arguments, logs, or insecure local storage.

Mitigation: Read the API key from LESECURE_API_KEY, avoid pasting secrets into chat, send request bodies through stdin, and store long-lived keys in a secret manager.

Risk: File or folder encryption requests could send data to the wrong processing path if the cloud/plaintext boundary is missed.

Mitigation: Use LESecure Cloud only for plain text and route file or folder encryption and decryption to LESecureLocal.

## Reference(s):

- [LESecure source code and documentation](https://github.com/SPAlgorithm/LE)
- [LESecure Cloud API endpoint](https://api.lesecure.ai/exec)
- [ClawHub skill page](https://clawhub.ai/spalgorithm/skills/lesecurecl)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline bash code blocks and plain-text API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, Python 3.9 or later with zoneinfo for time locks, and LESECURE_API_KEY supplied from the environment.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
