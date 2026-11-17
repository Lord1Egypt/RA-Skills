## Description:

Submit changed public URLs through IndexNow, or set up the site's IndexNow verification file. Use when the user explicitly requests an IndexNow submission or verification setup for a site they manage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[domainrankhq](https://clawhub.ai/user/domainrankhq)

### License/Terms of Use:

MIT-0

## Use Case:

Website developers and operators use this skill to notify participating search engines about changed public pages or to set up an IndexNow verification key and file for a site they manage. Submissions and key setup are performed only when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting sends the public URL list and the site's IndexNow verification key to the IndexNow endpoint; participating search engines may share submitted URLs.

Mitigation: Submit only public URLs for a site the user manages. Exclude drafts, staging and private URLs, and links containing credentials, personal data, or access tokens; review the sitemap scope before submission.

Risk: Key setup writes `.indexnow-key` and a verification file in the project directory.

Mitigation: Run key setup or rotation only when requested, and check the target project directory before creating or replacing key files.

Risk: The security assessment reports medium confidence and incomplete reference checks because two local path references were unresolved.

Mitigation: Review the skill source and its local references before installation or use if those paths are available.

## Reference(s):

- [IndexNow documentation](https://www.indexnow.org/documentation)
- [IndexNow on ClawHub](https://clawhub.ai/domainrankhq/skills/indexnow-bing)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Files, Guidance]

**Output Format:** [Shell command invocations, IndexNow API submissions, status text, and optional key verification files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submissions are limited to public URLs on a site the user manages and require a configured IndexNow key.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
