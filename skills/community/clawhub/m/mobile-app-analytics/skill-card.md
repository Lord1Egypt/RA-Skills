## Description: <br>
Track mobile app metrics with Firebase, App Store Connect, Play Console, retention, funnels, and cohort analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, product teams, and app operators use this skill to analyze mobile app performance across Firebase, App Store Connect, and Google Play Console. It helps compare cohorts, inspect funnels, monitor retention and revenue metrics, and document app-specific analytics context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics credentials or app identifiers could expose sensitive business data if broad account access is used. <br>
Mitigation: Use read-only or reporting-scoped credentials where available, rely on standard platform credential methods, and avoid storing secrets in local notes. <br>
Risk: Local notes may contain proprietary KPIs, funnels, goals, or product strategy. <br>
Mitigation: Review files saved under ~/mobile-app-analytics/ and avoid retaining sensitive details beyond what is needed for the analysis task. <br>
Risk: Custom analytics events can accidentally include personal data or conflict with consent requirements. <br>
Mitigation: Keep PII out of custom events and user properties, and apply ATT, GDPR, and platform consent requirements before querying or storing analytics context. <br>


## Reference(s): <br>
- [Mobile App Analytics on ClawHub](https://clawhub.ai/ivangdavila/mobile-app-analytics) <br>
- [Skill Homepage](https://clawic.com/skills/mobile-app-analytics) <br>
- [Firebase Analytics guide](firebase.md) <br>
- [App Store Connect Analytics guide](app-store.md) <br>
- [Google Play Console Analytics guide](play-console.md) <br>
- [Core Metrics guide](metrics.md) <br>
- [Memory Template](memory-template.md) <br>
- [App Store Connect API endpoint](https://api.appstoreconnect.apple.com/v1/apps/{app_id}/analyticsReportRequests) <br>
- [Google Android Publisher API endpoint](https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{package}/reviews) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with metric tables, SQL snippets, API examples, shell commands, and local configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local notes under ~/mobile-app-analytics/ when the user opts into analytics memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
