## Description: <br>
Automate PostHog dashboard creation, sync, update, and export via API. Covers dashboard CRUD, insight creation, cohort management, and API-driven analytics workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analytics teams use this skill to manage PostHog dashboards and insights from version-controlled JSON configuration, including create, sync, update, and export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a write-capable PostHog personal API key to create and update dashboards. <br>
Mitigation: Use a dedicated least-privilege key, test in a non-production project first, and confirm the key has only the access needed for the intended dashboard work. <br>
Risk: Running create or update can change PostHog dashboard state and local dashboard JSON configuration. <br>
Mitigation: Keep dashboard configuration under version control or back it up before running write operations, and confirm POSTHOG_HOST points to the intended PostHog region. <br>


## Reference(s): <br>
- [PostHog API Docs](https://posthog.com/docs/api) <br>
- [PostHog Personal API Keys](https://posthog.com/docs/api/overview#personal-api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PostHog API requests through a bash script and may update dashboard JSON configuration with created dashboard IDs.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
