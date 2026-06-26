## Description: <br>
Searches Google Patents through SerpApi for patent research, infringement risk checks, competitive IP analysis, patent details, full text, and PDF retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiafar](https://clawhub.ai/user/jiafar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and IP researchers use this skill to search patents, inspect claims and full text, download reference PDFs, and assess patent or freedom-to-operate risk for products and competitors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent searches and patent IDs are sent to SerpApi. <br>
Mitigation: Avoid confidential product, legal, or IP research terms unless sharing them with SerpApi is approved. <br>
Risk: The skill includes a built-in SerpApi key. <br>
Mitigation: Configure a user-owned SERPAPI_API_KEY and remove or disable the bundled fallback key before deployment. <br>
Risk: PDF downloads can write to caller-chosen file paths. <br>
Mitigation: Use explicit trusted output directories and review PDF output paths before running download commands. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jiafar/google-patents) <br>
- [SerpApi Google Patents search endpoint](https://serpapi.com/search.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command responses, and optional downloaded PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SERPAPI_API_KEY when configured; search and patent IDs are sent to SerpApi; PDF downloads write to the caller-selected output path.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
