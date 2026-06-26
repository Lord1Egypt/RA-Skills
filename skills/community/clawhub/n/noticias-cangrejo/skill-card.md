## Description: <br>
Fetch and summarize recent news articles from GNews on any topic, generating a concise Markdown digest with date, greeting, and top links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidk2yoyo](https://clawhub.ai/user/davidk2yoyo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to request a topic-based news digest that queries GNews and returns a concise Markdown list of recent, relevant articles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search topics and the configured GNews API key are used in requests to GNews. <br>
Mitigation: Install only when sharing searched topics with GNews is acceptable, and provide the API key through the intended environment variable or dashboard secret configuration. <br>
Risk: The optional --output argument writes Markdown to the specified file path and can overwrite an existing file. <br>
Mitigation: Use --output only with an intended path, preferably a new file in the working directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidk2yoyo/noticias-cangrejo) <br>
- [GNews](https://gnews.io/) <br>
- [GNews Search API](https://gnews.io/api/v4/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown news digest with date, Spanish greeting, topic line, and numbered article links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GNEWS_API_KEY; supports optional language, article count, and output file arguments.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
