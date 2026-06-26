## Description: <br>
Search web content such as webpages, images, and videos using the /web-search API with an Access Token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fchange](https://clawhub.ai/user/fchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run authenticated web, image, and video searches through Gitee AI, then parse the returned JSON to answer information lookup and recent-content discovery requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Gitee AI under the user's API key. <br>
Mitigation: Confirm users are comfortable sending the query to Gitee AI before use, and avoid submitting sensitive queries unless approved for that service. <br>
Risk: API keys can be exposed when passed directly on a command line. <br>
Mitigation: Prefer the GITEEAI_API_KEY environment variable over the --api-key argument. <br>
Risk: The script depends on the Python requests package. <br>
Mitigation: Install dependencies from a trusted Python environment before running the skill. <br>


## Reference(s): <br>
- [Moark Web Search on ClawHub](https://clawhub.ai/fchange/moark-web-search) <br>
- [Gitee AI web-search API endpoint](https://ai.gitee.com/v1/web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result JSON is emitted after SEARCH_RESULTS_JSON; result count is limited to 1-50.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
