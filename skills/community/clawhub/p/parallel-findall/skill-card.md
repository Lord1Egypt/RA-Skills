## Description: <br>
Discover entities (companies, people, products) matching a natural-language description via the Parallel FindAll API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[normallygaussian](https://clawhub.ai/user/normallygaussian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to run Parallel FindAll entity-discovery jobs from an authenticated CLI and return structured lists of matching companies, people, products, papers, or similar enumerable entities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FindAll runs use an external Parallel API through an authenticated CLI and may expose objectives or saved result files to Parallel and helper agents. <br>
Mitigation: Confirm the authenticated account before use and avoid submitting sensitive objectives or result files unless that sharing is acceptable. <br>
Risk: Large match limits or pro-tier generator runs may consume quota. <br>
Mitigation: Choose the smallest match limit and generator tier that satisfies the user's request, and warn users before high-volume or pro-tier runs. <br>
Risk: Lower-quality runs can return noisy entities, empty URLs, duplicate sources, or category placeholders. <br>
Mitigation: Filter noisy matches, group large result sets by source domain, and preserve the FindAll run identifier so users can extend, inspect, or cancel the run. <br>


## Reference(s): <br>
- [Parallel Homepage](https://parallel.ai) <br>
- [Parallel API Docs](https://docs.parallel.ai) <br>
- [Parallel FindAll API Reference](https://docs.parallel.ai/api-reference/findall) <br>
- [Parallel CLI Integration Docs](https://docs.parallel.ai/integrations/cli) <br>
- [ClawHub Skill Page](https://clawhub.ai/normallygaussian/parallel-findall) <br>
- [Publisher Profile](https://clawhub.ai/user/normallygaussian) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON result handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [FindAll results may include a run identifier, status, generated schema, and matches array; large runs can be saved to a file for later summarization.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
