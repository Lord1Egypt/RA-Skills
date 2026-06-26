## Description: <br>
Search and analyze TikTok KOLs using the KOLens API, including creator metrics and optional contact information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maweis1981](https://clawhub.ai/user/maweis1981) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search TikTok creators by keyword, inspect KOL metrics, and retrieve available outreach fields through a configured KOLens API endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API credentials could be exposed through logs, commits, shell history, or shared outputs. <br>
Mitigation: Keep KOLENS_API_KEY private, avoid logging or committing credentials, and rotate keys if exposure is suspected. <br>
Risk: The configured KOLens API URL and provider control the service that receives requests and returns creator data. <br>
Mitigation: Install only when the provider and API URL are trusted, and use HTTPS endpoints. <br>
Risk: Creator contact collection can raise privacy, platform-terms, and outreach-compliance concerns. <br>
Mitigation: Use contact collection only for legitimate outreach and follow TikTok terms plus applicable privacy laws such as GDPR and CCPA. <br>


## Reference(s): <br>
- [KOLens ClawHub listing](https://clawhub.ai/maweis1981/kolens) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KOLENS_API_KEY and KOLENS_API_URL environment variables; responses depend on the configured KOLens API service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
