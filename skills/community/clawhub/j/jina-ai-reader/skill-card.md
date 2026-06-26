## Description: <br>
Fetch clean, AI-friendly Markdown content from any URL using Jina.ai Reader, including paywalled sites, Twitter/X posts, and JavaScript-heavy pages that need rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangtianjiao](https://clawhub.ai/user/jiangtianjiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch readable Markdown from public web pages after search or when standard fetch tools struggle with Twitter/X, paywalls, or JavaScript-rendered pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs and fetched page content are sent through Jina.ai. <br>
Mitigation: Use the skill only for public pages and avoid internal sites, private documents, authenticated pages, signed URLs, or links containing tokens or credentials. <br>
Risk: Using the reader on paywalled content may conflict with a site's terms. <br>
Mitigation: Check applicable site terms and access rights before fetching or using paywalled content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangtianjiao/jina-ai-reader) <br>
- [Jina.ai Reader endpoint](https://r.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown text printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional flags can wait for JavaScript rendering and include image captions or links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
