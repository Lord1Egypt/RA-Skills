## Description: <br>
Find carbon emission factors for any material or process. 1M+ LCA datasets (HiQLCD, Ecoinvent, CarbonMinds). AI-powered BOM carbon footprint calculation and material comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KirbyInGitHub](https://clawhub.ai/user/KirbyInGitHub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, sustainability analysts, and OpenClaw agents use this skill to search LCA datasets, answer carbon-footprint questions, compare materials, and estimate BOM emissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends LCA questions, material lists, BOM details, and the HIQ_API_KEY to HiQ service endpoints. <br>
Mitigation: Use it only under an approved data-sharing policy, avoid confidential product or supplier data unless authorized, and store the API key in environment or OpenClaw configuration rather than prompts. <br>
Risk: Some dataset results may be restricted or require separate authorization. <br>
Mitigation: Confirm access rights for restricted LCA datasets before relying on or redistributing returned values. <br>
Risk: Carbon-footprint calculations and material comparisons depend on dataset choice, region, system boundary, and LCA methodology. <br>
Mitigation: Review generated results against the intended ISO/LCA methodology and document assumptions before using them in reports or decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KirbyInGitHub/hiq-cortex) <br>
- [HiQLCD platform](https://www.hiqlcd.com) <br>
- [HiQ Cortex web app](https://carbonx.hiqlcd.com/cortex) <br>
- [HiQ Cortex MCP endpoint](https://x.hiqlcd.com/api/deck/mcp) <br>
- [HiQ Cortex search API](https://x.hiqlcd.com/api/deck/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text and Markdown with command examples and optional JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and HIQ_API_KEY; search results may include dataset names, sources, regions, units, GWP100 values, quality fit, and links.] <br>

## Skill Version(s): <br>
1.3.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
