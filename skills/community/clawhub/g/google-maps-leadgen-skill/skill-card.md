## Description: <br>
Generate B2B leads from Google Maps using a self-hosted MCP server and export deduplicated, enriched results to CSV or XLSX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Realowg](https://clawhub.ai/user/Realowg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, business development, and operations users use this skill to run repeatable Google Maps lead-generation batches by geography and industry, enrich places with contact fields, and export lead files for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a configured Google Maps MCP server and can consume Google Maps API quota or billing. <br>
Mitigation: Install only with a trusted MCP server, verify the server configuration, and monitor quota and expected run cost before large batches. <br>
Risk: Generated CSV or XLSX lead files may contain business contact data and could be sent to the wrong location or recipient. <br>
Mitigation: Store exports in a deliberate folder and verify the destination channel or recipient before sending files through chat or Telegram. <br>
Risk: Google Maps API keys or generated lead files could be exposed if committed or shared unintentionally. <br>
Mitigation: Keep API keys in environment configuration, do not commit credentials or lead exports, and review files before sharing. <br>


## Reference(s): <br>
- [Google Maps Leadgen on ClawHub](https://clawhub.ai/Realowg/google-maps-leadgen-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files, text] <br>
**Output Format:** [Markdown guidance with shell command examples, CSV or XLSX lead exports, and JSON run summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports include name, address, phone, website, email, rating, place_id, and Google Maps URL; optional delivery can send generated files through chat or Telegram.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
