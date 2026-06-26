## Description: <br>
Generates short URLs from long URLs using shorturl.bot, with optional supported domains and custom suffixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minecraftxdd](https://clawhub.ai/user/minecraftxdd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to shorten long URLs, choose from supported short-link domains, and optionally request a custom URL suffix for sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs are sent to the external shorturl.bot service. <br>
Mitigation: Do not shorten password reset links, signed URLs, private internal links, API-key URLs, session-token URLs, or URLs with sensitive query parameters. <br>
Risk: Full API responses may expose metadata such as owner ID, submitter IP, timestamps, and the original URL. <br>
Mitigation: Use the default short-URL-only output when sharing results and avoid logging full responses unless that metadata is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minecraftxdd/openclaw-skill-shorturl) <br>
- [shorturl.bot API endpoint](https://www.shorturl.bot/api/urls/shorturl) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text URL by default, with optional JSON API response details described by the skill.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls an external URL-shortening service and may include original URL, short URL, ID, timestamp, owner ID, and submitter IP in full responses.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
