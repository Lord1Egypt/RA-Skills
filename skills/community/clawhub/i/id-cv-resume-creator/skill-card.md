## Description:

Creates digital identity pages, professional resumes, CVs, public profile URLs, and optional PDF exports through the talent.de API with human-in-the-loop review support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rotorstar](https://clawhub.ai/user/rotorstar)

### License/Terms of Use:

Free-to-use

## Use Case:

External users and agents use this skill to create a hosted professional profile, resume, or CV from requestor-approved data. It is especially suited to workflows that need template selection, final human approval, a permanent public URL, and optional PDF output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CV data is sent to talent.de and can create a persistent public profile.

Mitigation: Use only data the requestor explicitly provides or approves, summarize key fields before submission, and clearly explain that the result is a hosted public profile URL.

Risk: Some documented direct or timeout flows can publish personal data without final human approval.

Mitigation: Prefer the HITL flow with explicit final approval, avoid skip_hitl for attended sessions, and avoid fail-open timeout behavior unless the requestor has accepted that workflow.

Risk: Permanent claim links behave like bearer secrets and can let anyone with the link claim ownership.

Mitigation: Share claim links only with the requestor, keep them out of logs and third-party channels when possible, and treat them like passwords.

Risk: Callback webhooks may carry personal data and depend on Access-ID based HMAC verification.

Mitigation: Use polling or SSE when callback risk is not acceptable; when callbacks are used, require HTTPS, verify X-HITL-Signature, and protect TALENT_ACCESS_ID as a secret.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rotorstar/skills/id-cv-resume-creator)
- [talent.de homepage](https://www.talent.de)
- [talent.de API base](https://www.talent.de/api)
- [HITL discovery document](https://www.talent.de/.well-known/hitl.json)
- [HITL review base](https://www.talent.de/en/hitl/review)
- [Template previews](https://www.talent.de/de/cv-template-ideas)
- [CV Data Reference](reference/cv-data.md)
- [Templates Reference](reference/templates.md)
- [HITL Protocol Reference](reference/hitl.md)
- [Access System](shared/access.md)
- [Error Codes](shared/errors.md)
- [Privacy and Data Handling](shared/privacy.md)

## Skill Output:

**Output Type(s):** [Guidance, API calls, JSON payloads, Markdown summaries, Configuration]

**Output Format:** [Markdown guidance with HTTP examples, JSON request and response shapes, review links, public CV URLs, claim links, and optional PDF output metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to talent.de; optional TALENT_ACCESS_ID increases rate limits and enables callback webhooks.]

## Skill Version(s):

5.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
