## Description: <br>
Read Korea OpenDART disclosures using the OpenDART API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kim-Dongchul](https://clawhub.ai/user/Kim-Dongchul) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to find Korean corporate disclosure filings by company name or corp_code, filter recent OpenDART results by date or filing type, and return concise summaries with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenDART API keys can be exposed if passed directly on the command line. <br>
Mitigation: Prefer setting OPENDART_API_KEY instead of using the --api-key argument. <br>
Risk: Cached public company-code data under ~/.cache/opendart can become stale. <br>
Mitigation: Refresh or delete the cache when up-to-date company-code resolution is required. <br>


## Reference(s): <br>
- [OpenDART endpoint reference](references/opendart-endpoints.md) <br>
- [ClawHub skill page](https://clawhub.ai/Kim-Dongchul/opendart-disclosure) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with OpenDART filing links and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an OpenDART API key and may cite direct DART filing URLs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
