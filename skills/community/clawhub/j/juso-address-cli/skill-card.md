## Description: <br>
Searches and resolves Korean road addresses via the official juso.go.kr OpenAPI, including keyword search with zip codes, English address lookup, and address-to-coordinate conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to normalize Korean address strings into form-ready road-address records, postal codes, English addresses, or entrance coordinates for checkout, shipping, invoicing, registration, and intake workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence marks this release suspicious. <br>
Mitigation: Review the scripts before deployment and run them with only the filesystem and network access needed for the address lookup task. <br>
Risk: The scripts send address queries and confirmation keys to the external juso.go.kr API. <br>
Mitigation: Use environment variables for keys, avoid submitting addresses you are not permitted to process, and follow the service's terms and rate limits. <br>
Risk: The one-shot resolver chooses the first search result before requesting coordinates, which can select the wrong address for ambiguous input. <br>
Mitigation: Inspect the returned JSONL or run search first when precision matters, then pass the selected address fields to the coordinate command. <br>


## Reference(s): <br>
- [Official juso.go.kr OpenAPI documentation](https://business.juso.go.kr/addrlink/openApi/apiExprn.do) <br>
- [juso.go.kr error-code list](https://business.juso.go.kr/addrlink/devCenterEventBoard/devBoardList.do?cPath=99MD) <br>
- [ClawHub release page](https://clawhub.ai/chloepark85/juso-address-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSONL from shell scripts with concise command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, python3, and juso.go.kr confirmation keys for live API calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
