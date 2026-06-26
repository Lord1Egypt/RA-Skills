## Description: <br>
Fetches and analyzes content from one or more URLs using Gemini 2.5 Flash so agents can answer questions about retrieved web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch up to 20 specific web pages with nansen-cli and get AI-generated answers to questions about their contents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs and questions are processed through Nansen and Gemini, which may expose private or access-controlled information if used with sensitive inputs. <br>
Mitigation: Use only with URLs and questions that are acceptable under the user's data policy, and avoid private or confidential content unless external processing is approved. <br>
Risk: The workflow requires a Nansen API key and broad access to the nansen CLI. <br>
Mitigation: Install only if the nansen-cli package is trusted, scope the API key to the intended use, and review generated nansen commands before execution. <br>
Risk: Paywalled, blocked, or unreachable pages can fail or return incomplete coverage. <br>
Mitigation: Check failed_urls and retrieved_urls before relying on the generated analysis. <br>


## Reference(s): <br>
- [Nansen Web Fetcher on ClawHub](https://clawhub.ai/nansen-devops/nansen-web-fetcher) <br>
- [Nansen](https://nansen.ai) <br>
- [nansen-cli package](https://www.npmjs.com/package/nansen-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON containing analysis, retrieved_urls, and failed_urls; optionally human-readable JSON with --pretty] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NANSEN_API_KEY and the nansen CLI; accepts up to 20 URLs and a required question; CLI timeout is 30 seconds.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
