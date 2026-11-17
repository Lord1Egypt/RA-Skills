## Description:

Analyze Instagram profiles and posts with engagement metrics, view counts, follower ratios, and Reels-focused analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tevfikgulep](https://clawhub.ai/user/tevfikgulep)

### License/Terms of Use:


## Use Case:

Developers, analysts, and social media teams use this skill to analyze trusted Instagram usernames and post or Reel URLs, calculate engagement and view metrics, and export results for reporting or follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled Instagram URLs and usernames can broaden network activity beyond the intended target set.

Mitigation: Use only trusted Instagram usernames and Instagram post or Reel URLs, and prefer host and username validation before operational use.

Risk: The skill writes analysis outputs to local data directories that may contain profile, engagement, or account-related information.

Mitigation: Keep outputs in a controlled directory and define privacy, retention, and access expectations before use.

Risk: Instagram credentials may be needed for some metrics and could be exposed if stored in shared folders or source control.

Mitigation: Store credentials outside shared folders and source control, and use environment-specific secret handling.

Risk: Unpinned dependencies can change behavior or introduce supply-chain risk over time.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tevfikgulep/skills/instagram-analyzer)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON and CSV file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes profile, post, batch, and Reels-link outputs under the configured data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
