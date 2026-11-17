## Description:

KTO TourAPI CLI helps agents query Korea Tourism Organization TourAPI 4.0 for Korean tourism areas, categories, places, nearby points of interest, festivals, lodging, keyword search, and detailed content records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to ground Korea travel planning, festival calendars, map-based discovery, and tourism content workflows in Korea Tourism Organization TourAPI data. It is suited for JSONL-producing command-line workflows that feed jq, pandas, publishing tools, or downstream agent skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary reports that one command can be tricked into running shell code.

Mitigation: Review command arguments before execution and do not expose nearby.sh through automation or user-facing tools until radius input is validated as a plain integer.

Risk: The authoritative security summary reports that TOURAPI_BASE can redirect the TourAPI key.

Mitigation: Pin TOURAPI_BASE to the official HTTPS TourAPI endpoint or use a low-value test key for nonproduction endpoints.

Risk: The skill uses external API credentials and has a suspicious security verdict.

Mitigation: Install only in trusted environments, use trusted prompts and command arguments, and review the skill before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chloepark85/skills/kto-tourapi-cli)
- [Korean OpenData portal](https://www.data.go.kr/)
- [Korea Tourism Organization TourAPI 4.0 KorService2 endpoint](https://apis.data.go.kr/B551011/KorService2)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSONL command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, jq, and a TOURAPI_SERVICE_KEY environment variable; command outputs are generally JSONL, with detail lookups returning one compact JSON object.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
