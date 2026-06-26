## Description: <br>
Interactive Infographic helps agents turn complex text, system architecture, workflows, knowledge bases, and long-form content into structured ContextWeave visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qhyw99](https://clawhub.ai/user/qhyw99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, analysts, and documentation authors use this skill to convert dense requirements, architecture descriptions, business processes, mind maps, and knowledge structures into visual diagrams. The agent prepares a structured request file, invokes the ContextWeave Node client, and returns the generated session and artifact details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the text, diagrams, or architecture details supplied for visualization to the ContextWeave backend at https://pptx.chenxitech.site. <br>
Mitigation: Avoid sending secrets, regulated data, or proprietary content unless the backend is trusted for that data. <br>
Risk: The local Node client uses CONTEXTWEAVE_MCP_API_KEY when present and otherwise falls back to an anonymous credential. <br>
Mitigation: Use a scoped ContextWeave API key and avoid exposing unrelated credentials in the execution environment. <br>
Risk: Generated visualizations may omit or misrepresent relationships if the input lacks clear definitions, hierarchy, or dependency direction. <br>
Mitigation: Review generated diagrams against the source material before using them in documentation, planning, or decision workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qhyw99/interactive-infographic) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/qhyw99) <br>
- [ContextWeave default backend](https://pptx.chenxitech.site) <br>
- [ContextWeave API example endpoint](https://api.contextweave.site) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Files, Configuration] <br>
**Output Format:** [Single JSON object with status, session_id, result, and error fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful generation returns a reusable ContextWeave session_id and result fields such as run_id or svg_url; export helpers can write diagram code or retrieve svg/pptx assets.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
