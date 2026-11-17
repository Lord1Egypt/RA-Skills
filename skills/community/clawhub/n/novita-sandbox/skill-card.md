## Description:

Run browser operations and untrusted code in an isolated Novita cloud sandbox backed by Firecracker VMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piston4711](https://clawhub.ai/user/piston4711)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to isolate external browsing, web-derived commands, and untrusted project build or test work in Novita sandboxes while keeping the local workspace out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload arbitrary local files to Novita, which may expose private workspace data or credentials.

Mitigation: Use a dedicated environment, give the skill only the Novita API key it needs, and avoid uploading secrets or broad workspace files.

Risk: The helper can download sandbox output to local paths and overwrite files without enforced path limits or confirmation.

Mitigation: Download only into a disposable staging directory and review files before moving them into a workspace.

Risk: Paused sandboxes preserve state and can resume with prior browser, file, or process context.

Mitigation: Kill sandboxes when finished to clear preserved state and stop billing.

## Reference(s):

- [Novita Sandbox: Browser Use Integration](references/browser-use.md)
- [ClawHub Skill Page](https://clawhub.ai/piston4711/skills/novita-sandbox)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, JSON, Guidance]

**Output Format:** [Markdown guidance with bash, Python, and JavaScript examples; the helper CLI returns JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sandbox command output is truncated to 8000 characters by the helper script.]

## Skill Version(s):

0.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
