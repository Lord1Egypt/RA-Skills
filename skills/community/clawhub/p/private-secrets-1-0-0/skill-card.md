## Description: <br>
Stores, lists, and retrieves named secrets such as API keys, passwords, and tokens in a local plaintext JSON file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmu14641](https://clawhub.ai/user/anmu14641) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users can use this skill as a simple local helper for adding, listing, and retrieving named secrets during agent workflows. It is best suited to low-risk local notes because server security evidence reports plaintext storage and possible stdout disclosure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive credentials are stored in plaintext and may be disclosed through command output. <br>
Mitigation: Do not store production passwords, long-lived API keys, wallet seeds, or other high-value secrets unless plaintext workspace storage and stdout disclosure are acceptable. <br>
Risk: The helper implementation may run unintended local code from crafted inputs. <br>
Mitigation: Prefer an OS keychain or encrypted secret manager, or update the helper to pass inputs safely to Node and restrict the secrets file permissions before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anmu14641/private-secrets-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text command output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores data in a local plaintext JSON file at /workspace/skills/private-secrets-1.0.0/secrets.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
