## Description: <br>
Run B2B lead research with lgf (Lead Gen Factory) to find leads, prospect companies, research ICPs, identify decision makers, and generate lead lists for B2B target profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Catafal](https://clawhub.ai/user/Catafal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, and business development users can ask an agent to run lgf for a stated ICP and return scored B2B leads, decision-maker details, and source links for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles generated leads and contact details that may be personal or sensitive business data. <br>
Mitigation: Review provider terms and ensure outreach, storage, and handling comply with applicable privacy laws, consent requirements, and platform rules. <br>
Risk: Running lgf requires local installation and API credentials for external services. <br>
Mitigation: Verify the Lead Gen Factory source before installing, use an isolated environment such as pipx, and use dedicated Tavily and OpenRouter API keys. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Catafal/lead-gen-factory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, CSV, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; lgf can return structured JSON and CSV lead outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.12+ and dedicated Tavily and OpenRouter API keys; generated leads may include personal or sensitive business contact data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
