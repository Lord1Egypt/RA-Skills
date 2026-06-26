## Description: <br>
Naver Search lets an agent retrieve Naver web, news, shopping, image, video, booking, and local search results through SerpAPI-backed command-line scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[downwind7clawd-ctrl](https://clawhub.ai/user/downwind7clawd-ctrl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to gather Naver search evidence across web, news, shopping, images, video, and local or booking categories. It supports compact human-facing summaries and JSON output for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to SerpAPI and Naver, which can expose sensitive or confidential query content. <br>
Mitigation: Avoid secrets, personal data, and confidential internal terms in queries; use accounts and API keys approved for the data being searched. <br>
Risk: The skill requires a SERPAPI_API_KEY that may be stored in the environment or a local .env file. <br>
Mitigation: Keep the key private, restrict access to any .env file, and rotate the key if exposure is suspected. <br>
Risk: The serpapi dependency is not pinned in requirements.txt, which can reduce reproducibility. <br>
Mitigation: Pin and review the dependency version before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/downwind7clawd-ctrl/naver-search) <br>
- [Publisher profile](https://clawhub.ai/user/downwind7clawd-ctrl) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Compact text summaries or raw JSON from command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports compact, full, and json output modes; requires SERPAPI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
