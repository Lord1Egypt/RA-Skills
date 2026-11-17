## Description:

Suite of shell scripts for developers to generate Chrome extensions, GitHub READMEs, SaaS landing pages, tech blogs, tweet threads, and code review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to draft starter project files, documentation, marketing pages, article outlines, social posts, and review-style reports from shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe file-writing behavior can overwrite README or generated project files.

Mitigation: Run the scripts in disposable or version-controlled directories and inspect target paths before execution.

Risk: Untrusted names or descriptions can trigger command-injection behavior.

Mitigation: Do not pass untrusted input to the scripts until the shell handling is reviewed and patched.

Risk: The code-review assistant can present canned output as if it analyzed code.

Mitigation: Do not rely on it for real security or merge-blocking code review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/my-awesome-tools)
- [Publisher profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, shell output, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some scripts write files or directories in the current or selected output path.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
