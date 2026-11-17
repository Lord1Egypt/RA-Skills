## Description:

Wrapper skill for OpenClaw web_fetch results. Use when you need MECE post-processing on fetched pages: policy decision from Content-Signal, privacy redaction, optional markdown normalization fallback, and stable output schema without re-implementing network fetch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnortegahyc](https://clawhub.ai/user/johnortegahyc)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to post-process OpenClaw web_fetch results into a stable object with normalized content, Content-Signal policy handling, URL redaction, token estimates, status, and fallback metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes fetched page content and runs a local Node.js script.

Mitigation: Review fetched content before downstream use and run the script only in an environment approved for local Node execution.

Risk: The npm dependency is declared as a version range, so installs may resolve to different package versions over time.

Mitigation: Install from a reviewed lockfile or pin the turndown dependency before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johnortegahyc/skills/markdown-browser-skills-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON object with normalized content, policy action, redacted source URL, status code, token estimate, and fallback flag.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes existing web_fetch payloads and does not perform direct network fetching during normal operation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
