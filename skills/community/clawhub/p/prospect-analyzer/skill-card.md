## Description:

Analyze any company's website to find content marketing gaps and qualify them as a potential client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinoneliraz](https://clawhub.ai/user/yinoneliraz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sales or marketing teams use this skill to research company websites, audit content gaps, compare visible competitor content, score lead quality, and generate a concise outreach angle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to browse third-party company websites supplied by the user.

Mitigation: Use public HTTPS-only targets and avoid analyzing untrusted or private URLs unless the browsing behavior is acceptable for the workspace.

Risk: The skill can create or update prospect tracking files in the workspace.

Mitigation: Run it in a workspace where changes under the prospects directory are expected, and review generated reports or queue updates before using them operationally.

Risk: The artifact includes a curl fallback for sites that do not load in the browser.

Mitigation: Require URL validation and safe invocation without shell interpolation before allowing curl on user-provided targets.

## Reference(s):

- [DriftMango SDR Kit](https://driftmango.com/sdr-kit)
- [Prospect Analyzer on ClawHub](https://clawhub.ai/yinoneliraz/skills/prospect-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prospect report file plus a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a prospects directory, write prospect analysis Markdown files, and update a prospect queue when queue integration is used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
