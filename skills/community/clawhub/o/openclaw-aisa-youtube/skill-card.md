## Description: <br>
YouTube Search API via AIsa unified endpoint for searching YouTube videos, channels, and playlists with a single AIsa API key and no Google API key or OAuth setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to search YouTube content through AIsa, including localized searches, pagination, and video, channel, or playlist filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube search queries and API-key-backed usage are sent to AIsa. <br>
Mitigation: Use a revocable or quota-limited AISA_API_KEY when available and avoid sensitive information in search queries or prompts. <br>
Risk: The artifact includes examples for AIsa chat-completions and smart-search services beyond the main YouTube search purpose. <br>
Mitigation: Review those examples separately and use only the AIsa services needed for the intended workflow. <br>
Risk: The API is pay-per-use and may return rate limit or authorization errors. <br>
Mitigation: Monitor AIsa usage, keep keys scoped where possible, and handle 401 and 429 responses in calling code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xjordansg-yolo/openclaw-aisa-youtube) <br>
- [AIsa API Documentation](https://docs.aisa.one) <br>
- [AIsa Dashboard / Marketplace](https://marketplace.aisa.one) <br>
- [YouTube Search API Reference](https://docs.aisa.one/reference/get_youtube-search) <br>
- [AIsa Smart Search API](https://docs.aisa.one/reference/get_search-smart) <br>
- [AIsa Chat Completions API](https://docs.aisa.one/reference/createchatcompletion) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with curl, Python, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and an AISA_API_KEY; executed examples return structured YouTube search result JSON from AIsa.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
