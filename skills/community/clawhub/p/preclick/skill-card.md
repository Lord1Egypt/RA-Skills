## Description:

Companion skill for @cybrlab/preclick-openclaw. Requires PreClick plugin tools to assess URLs for threats and intent alignment before navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cplusdev](https://clawhub.ai/user/cplusdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to check URLs for threat signals and destination-intent alignment before opening links, following redirects, downloading files, or submitting credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party PreClick plugin that is not pinned to a reviewed version in the release evidence.

Mitigation: Install only trusted plugin versions, prefer a pinned and reviewed plugin release, and verify provenance when available.

Risk: URL scans may send target URLs and stated browsing intent to the plugin's scanning service.

Mitigation: Avoid scanning sensitive internal URLs or confidential intent text unless the user accepts that disclosure.

Risk: Scan results can be incomplete, delayed, or uncertain.

Mitigation: Follow the returned access directive, retry temporary failures once, and use confidence-aware language instead of guaranteeing safety.

## Reference(s):

- [PreClick ClawHub Skill Page](https://clawhub.ai/cplusdev/skills/preclick)
- [cplusdev Publisher Profile](https://clawhub.ai/user/cplusdev)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with shell command examples and structured scan-result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PreClick plugin scan results such as agent_access_directive, agent_access_reason, risk_score, confidence, analysis_complete, and intent_alignment.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
