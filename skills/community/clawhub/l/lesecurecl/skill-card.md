## Description: <br>
LESecure Cloud encrypts or decrypts plain text through the LESecure API using layered locks such as PIN, password, MFA, and time windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spalgorithm](https://clawhub.ai/user/spalgorithm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to encrypt or decrypt plain text with the LESecure cloud service while applying one or more access locks. It is intended for text workflows where users are comfortable sending the content, lock values, and API token to the LESecure API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext, ciphertext, lock values, phone numbers, and the API bearer token are sent to a third-party cloud API. <br>
Mitigation: Use the skill only after acknowledging the remote transmission, avoid highly sensitive data unless the provider's privacy practices have been independently verified, and choose the local LESecure option when data should stay on-device. <br>
Risk: API keys and lock values can be exposed if pasted into chat, shell history, logs, or process arguments. <br>
Mitigation: Provide the API key through the LESECURE_API_KEY environment variable, send JSON request bodies through stdin, never print secrets, and rotate the key if it is ever pasted into chat. <br>
Risk: The cloud skill is limited to plain-text encryption and decryption, not files or folders. <br>
Mitigation: Redirect file or folder workflows to LESecureLocal instead of sending file content to the cloud API. <br>


## Reference(s): <br>
- [LeSecure Cloud listing](https://clawhub.ai/spalgorithm/lesecurecl) <br>
- [Source code and documentation](https://github.com/SPAlgorithm/LE) <br>
- [LESecure API endpoint](https://api.lesecure.ai/exec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and plain-text API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses stdin-fed JSON request bodies and the LESECURE_API_KEY environment variable for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
