## Description: <br>
Lookup Pathé Netherlands movies, posters, descriptions, cinemas, and showtimes via the Pathé JSON APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[humboldtjs](https://clawhub.ai/user/humboldtjs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to look up Pathé Netherlands movie information, posters, cinema availability, and showtimes through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Pathé public APIs, so results depend on live third-party service availability and returned data. <br>
Mitigation: Use the skill for Pathé movie and showtime lookup requests, and present unavailable or incomplete API data clearly to the user. <br>
Risk: Poster delivery may temporarily save image files under /tmp when sending posters through WhatsApp. <br>
Mitigation: Limit temporary image downloads to user-requested posters and clean up temporary files when practical. <br>


## Reference(s): <br>
- [Pathé API](https://www.pathe.nl/api) <br>
- [Pathé API Reference](references/api.md) <br>
- [ClawHub Release Page](https://clawhub.ai/humboldtjs/pathe-movie) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional URLs, local media paths, and structured API-derived details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include downloaded temporary poster image paths for WhatsApp media delivery when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
