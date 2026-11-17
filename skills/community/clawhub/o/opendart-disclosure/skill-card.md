## Description:

Read Korea OpenDART disclosures using the OpenDART API. Use when the user asks for DART 공시 조회, recent filings by company, filtering by filing type/date, or quick summaries with source links. Supports company name/corp_code lookup and structured result extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kim-dongchul](https://clawhub.ai/user/kim-dongchul)

### License/Terms of Use:


## Use Case:

Developers, analysts, and Korean disclosure researchers use this skill to retrieve recent OpenDART filings by company identifier or company name, filter by date or filing type, and return concise summaries with source filing links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires network access to OpenDART and use of an OpenDART API key.

Mitigation: Grant network access only when OpenDART lookups are expected, and provide OPENDART_API_KEY through the normal secret-handling mechanism.

Risk: Passing the API key with --api-key may expose it in shell history or process listings.

Mitigation: Prefer the OPENDART_API_KEY environment variable instead of command-line API key arguments.

Risk: The helper caches OpenDART company-code data under ~/.cache/opendart/.

Mitigation: Review local cache handling requirements for the deployment environment and clear or refresh the cache when needed.

Risk: Company-name matching can be fuzzy and may select the wrong company.

Mitigation: Prefer corp_code when available, and review candidate matches before summarizing disclosures for ambiguous names.

## Reference(s):

- [OpenDART endpoints quick reference](references/opendart-endpoints.md)
- [OpenDART company code archive](https://opendart.fss.or.kr/api/corpCode.xml)
- [OpenDART disclosure list API](https://opendart.fss.or.kr/api/list.json)
- [DART filing document URL pattern](https://dart.fss.or.kr/dsaf001/main.do?rcpNo=<rcept_no>)
- [OpenDART Disclosure on ClawHub](https://clawhub.ai/kim-dongchul/skills/opendart-disclosure)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Text, Markdown, Guidance]

**Output Format:** [Markdown with optional JSON command output and direct source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include filing date, report name, receipt number, OpenDART filing URL, company match data, and concise Korean summaries when requested.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
