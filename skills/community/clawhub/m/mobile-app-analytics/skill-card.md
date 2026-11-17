## Description:

Track mobile app metrics with Firebase, App Store Connect, Play Console, retention, funnels, and cohort analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, product teams, and external app operators use this skill to analyze mobile app acquisition, retention, engagement, revenue, and quality metrics across Firebase, App Store Connect, and Play Console.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local analytics context under ~/mobile-app-analytics/ could contain sensitive app strategy, user-level exports, or credentials if the user adds them.

Mitigation: Store only scoped app context and goals; do not put API keys, JWT private keys, access tokens, PII, or sensitive user-level exports in those files.

Risk: Platform API use can expose app IDs, date ranges, and credentials to Firebase, Apple, or Google services.

Mitigation: Use standard platform credential methods, least-privilege scopes, and restrict BigQuery or analytics API access appropriately.

Risk: Mobile analytics conclusions can be misleading when based on stale platform reports or unsegmented aggregate metrics.

Mitigation: Account for known platform data delays and segment analysis by install cohort, acquisition source, user tier, and platform.

## Reference(s):

- [Mobile App Analytics ClawHub Page](https://clawhub.ai/ivangdavila/skills/mobile-app-analytics)
- [Mobile App Analytics Homepage](https://clawic.com/skills/mobile-app-analytics)
- [Firebase Analytics Guide](artifact/firebase.md)
- [App Store Connect Analytics Guide](artifact/app-store.md)
- [Google Play Console Analytics Guide](artifact/play-console.md)
- [Core Metrics Reference](artifact/metrics.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Analysis, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline SQL, bash, Kotlin, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local app analytics notes and platform API queries when credentials are provided.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
