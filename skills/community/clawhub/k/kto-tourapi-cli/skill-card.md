## Description: <br>
Korean tourism content via KTO TourAPI 4.0, with Bash subcommands for area codes, categories, area browsing, nearby search, keyword search, festivals, stays, and full content details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, travel-planning agents, and content builders use this skill to retrieve authoritative Korean tourism records from KTO TourAPI for itineraries, festival calendars, lodging discovery, nearby place lookup, and grounded tourism answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tourism queries, coordinates, dates, and the data.go.kr TourAPI key are sent to the configured TourAPI endpoint. <br>
Mitigation: Use the default TourAPI endpoint unless a replacement service is trusted, keep TOURAPI_SERVICE_KEY out of shared logs and transcripts, and avoid exposing query data beyond the intended API call. <br>
Risk: The CLI supports overriding TOURAPI_BASE, which can redirect requests and credentials to another service. <br>
Mitigation: Only set TOURAPI_BASE to a trusted endpoint and review environment configuration before running the scripts. <br>


## Reference(s): <br>
- [KTO TourAPI KorService2 endpoint](https://apis.data.go.kr/B551011/KorService2) <br>
- [Korean OpenData portal](https://www.data.go.kr/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Bash commands and JSONL output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Subcommands emit one JSON object per line for downstream tools such as jq, csvkit, pandas, or other agent skills.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
