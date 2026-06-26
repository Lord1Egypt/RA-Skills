## Description: <br>
Perform global web searches using Google Custom Search API with customizable result counts and formatted results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leohuang8688](https://clawhub.ai/user/leohuang8688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current web search results for news, research, product, and academic queries through Google Custom Search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Failed searches can expose the user's Google API key in returned error output. <br>
Mitigation: Use a restricted Google Custom Search API key with quota and billing limits, and prefer a patched version that redacts HTTP error URLs before returning failures. <br>
Risk: Search queries are sent to Google Custom Search and may contain sensitive user-provided text. <br>
Mitigation: Avoid searching for secrets, private personal data, or confidential business information. <br>
Risk: Unpinned dependencies can change behavior before production deployment. <br>
Mitigation: Pin and review dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leohuang8688/google-search-2) <br>
- [Google Custom Search JSON API overview](https://developers.google.com/custom-search/v1/overview) <br>
- [Google Cloud Custom Search documentation](https://cloud.google.com/custom-search/docs) <br>
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Formatted search results with titles, URLs, snippets, and source domains.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_API_KEY and GOOGLE_CX; returns up to 10 results per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
