## Description:

Search and fetch images from the internet for any purpose - paper figures, news photos, stock images, product photos, scientific illustrations, social media images, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newtontech](https://clawhub.ai/user/newtontech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, content creators, and agents use this skill to find, retrieve, evaluate, and compose images for papers, presentations, blog posts, product research, news workflows, and scientific figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image and research queries sent to external providers may disclose confidential project names, private URLs, unreleased research topics, or personal data.

Mitigation: Avoid sensitive query content unless the user explicitly approves sharing it with the selected provider.

Risk: Optional npx or uv MCP and image-generation commands may introduce supply-chain or environment exposure if run without review.

Mitigation: Pin and review package versions, isolate the execution environment, and expose only the specific API key required.

Risk: Fetched images can carry license, attribution, or terms-of-service obligations that are unsuitable for the intended publication or commercial use.

Mitigation: Check the source license and attribution requirements before reuse, and prefer public-domain or clearly licensed assets when possible.

## Reference(s):

- [Image Fetch Toolkit on ClawHub](https://clawhub.ai/newtontech/skills/image-fetch-toolkit)
- [Unsplash API Documentation](https://unsplash.com/developers)
- [Pexels API Documentation](https://www.pexels.com/api/)
- [Pixabay API Documentation](https://pixabay.com/api/docs/)
- [Flickr API App Documentation](https://www.flickr.com/services/apps/)
- [Google Custom Search Documentation](https://developers.google.com/custom-search)
- [Bing Image Search API](https://www.microsoft.com/en-us/bing/apis/bing-image-search-api)
- [Paper Search MCP](https://github.com/openags/paper-search-mcp)
- [NewsAPI](https://newsapi.org)
- [GNews API](https://gnews.io)
- [Wikimedia Commons API](https://commons.wikimedia.org/w/api.php)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands, API examples, and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require external API keys and provider-specific licensing or attribution review before use.]

## Skill Version(s):

1.0.0 (source: package.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
