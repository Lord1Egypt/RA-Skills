## Description: <br>
Search the web and X (Twitter) using SkillBoss API Hub with real-time access, citations, and image understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current web information and X/Twitter discussion through a SkillBoss-compatible search API, including optional domain, handle, date, image, and video filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SkillBoss API key and sends search queries to a remote API service. <br>
Mitigation: Use a limited or throwaway key for review, and avoid sending secrets, customer data, or confidential business content in queries. <br>
Risk: Security evidence reports that the implementation sends requests to a different API host than the documentation advertises. <br>
Mitigation: Review before installing and confirm the intended API host with the maintainer before using the skill in a trusted environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/martin-llm) <br>
- [Declared homepage](https://github.com/yourusername/xai-grok-search) <br>
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text search responses with citation metadata and setup examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; search requests may return raw API response data and can take 30-60+ seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
