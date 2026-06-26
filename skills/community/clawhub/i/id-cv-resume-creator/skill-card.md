## Description: <br>
Create a free digital identity, professional resume and CV, from classic PDF and HTML layouts to 3D worlds and playable games, with a permanent public URL and optional agent Access-ID support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rotorstar](https://clawhub.ai/user/rotorstar) <br>

### License/Terms of Use: <br>
Free-to-use <br>


## Use Case: <br>
External users and agents use this skill to collect requestor-approved resume details, route human review when appropriate, and publish a Talent.de CV, digital identity page, or downloadable PDF. Developers can also use the documented API and HITL flow to integrate CV creation into agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume details are sent to Talent.de and may result in a persistent online CV URL. <br>
Mitigation: Use only requestor-provided or requestor-approved data, keep human review enabled for normal use, and confirm before publishing. <br>
Risk: Claim tokens and TALENT_ACCESS_ID values provide control or privileged API access. <br>
Mitigation: Treat claim tokens and Access-ID values as secrets, share claim links only with the requestor, and store Access-ID values in environment variables. <br>
Risk: Sensitive personal, financial, government, or confidential business data could be included in a public profile by mistake. <br>
Mitigation: Do not include government IDs, passwords, private keys, financial details, or confidential business information in CV data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rotorstar/id-cv-resume-creator) <br>
- [Talent.de](https://www.talent.de) <br>
- [Talent API Base](https://www.talent.de/api) <br>
- [HITL Discovery](https://www.talent.de/.well-known/hitl.json) <br>
- [Template Previews](https://www.talent.de/de/cv-template-ideas) <br>
- [CV Data Reference](reference/cv-data.md) <br>
- [HITL Protocol](reference/hitl.md) <br>
- [Templates](reference/templates.md) <br>
- [Access System](shared/access.md) <br>
- [Privacy & Data Handling](shared/privacy.md) <br>
- [Error Codes](shared/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, markdown, configuration] <br>
**Output Format:** [Markdown guidance with HTTP examples, JSON request and response shapes, review links, and optional PDF output from the Talent.de API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces public CV URLs and claim tokens; optional Access-ID enables higher rate limits and callbacks.] <br>

## Skill Version(s): <br>
5.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
