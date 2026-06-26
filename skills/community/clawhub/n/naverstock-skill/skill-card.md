## Description: <br>
Fetch text-based real-time stock prices for KRX and overseas markets using Naver Finance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seungdols](https://clawhub.ai/user/seungdols) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to look up public stock, ticker, and currency quote data from Naver Finance and return structured price information for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The entered stock, ticker, or currency term may be sent to Naver Finance as part of the lookup. <br>
Mitigation: Use only public market lookup terms and avoid entering sensitive or private portfolio information. <br>
Risk: Market quote data can be delayed, unavailable, or different between regular KRX and Nextrade sessions. <br>
Mitigation: Treat returned prices as informational data and verify important financial decisions against an authoritative market source. <br>
Risk: The skill runs a bundled local Node.js script. <br>
Mitigation: Install and run it only in environments where local script execution and outbound public market-data lookups are acceptable. <br>


## Reference(s): <br>
- [Naver Stock ClawHub Release](https://clawhub.ai/seungdols/naverstock-skill) <br>
- [seungdols ClawHub Publisher Profile](https://clawhub.ai/user/seungdols) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON object printed by a local Node.js command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a stock name, ticker, code, or currency search term.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
