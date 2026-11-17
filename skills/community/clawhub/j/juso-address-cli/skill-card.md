## Description:

Search and resolve Korean road addresses via the official juso.go.kr OpenAPI, including keyword search with zip codes, English address lookup, and address-to-coordinate conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to normalize Korean road addresses, retrieve postal codes, look up English road-address forms, and optionally resolve a selected address to entrance coordinates for workflows such as checkout, shipping, invoicing, registration, or real-estate intake.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Address searches and juso.go.kr confirmation keys are sent to the official juso.go.kr API.

Mitigation: Store keys in environment variables, send only address data needed for the task, and run the included scripts only against the documented juso.go.kr endpoints.

Risk: The scripts do not retry on rate-limit responses, so high-volume use can fail or produce incomplete automation results.

Mitigation: Throttle callers within the documented juso.go.kr limits and add caller-side backoff before retrying requests.

Risk: The one-shot resolver selects the first search match before requesting coordinates, which can be wrong for ambiguous address strings.

Mitigation: Inspect search results for ambiguous inputs or constrain the query before using coordinates in downstream workflows.

## Reference(s):

- [Official juso.go.kr OpenAPI documentation](https://business.juso.go.kr/addrlink/openApi/apiExprn.do)
- [juso.go.kr error-code list](https://business.juso.go.kr/addrlink/devCenterEventBoard/devBoardList.do?cPath=99MD)
- [ClawHub skill page](https://clawhub.ai/chloepark85/skills/juso-address-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSONL command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included scripts print compact JSON objects, one per line, and report errors to stderr with non-zero exit codes.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
