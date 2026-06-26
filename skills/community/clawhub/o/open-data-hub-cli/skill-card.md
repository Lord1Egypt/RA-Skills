## Description: <br>
Query Open Data Hub/NOI Techpark data through `odh`: Tourism, Mobility, traffic, A22, parking, EV charging, STA GTFS, and transit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galjos](https://clawhub.ai/user/galjos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and agent operators use this skill to query Open Data Hub and NOI Techpark datasets through the `odh` CLI instead of scraping pages or guessing API shapes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the external odh CLI introduces trust in a third-party project. <br>
Mitigation: Confirm trust in the odh-cli project before installing and prefer the pinned Go install path when possible. <br>
Risk: The CLI and optional MCP server mode can make network requests to Open Data Hub services. <br>
Mitigation: Run MCP server mode only when an agent host should access the same CLI functions, and surface returned warnings, freshness, and source fields in answers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/galjos/open-data-hub-cli) <br>
- [odh-cli project homepage](https://github.com/galjos/odh-cli) <br>
- [Open Data Hub API](https://opendatahub.com/api/) <br>
- [Open Data Hub datasets documentation](https://docs.opendatahub.com/en/latest/datasets.html) <br>
- [Open Data Hub mobility getting started](https://docs.opendatahub.com/en/latest/howto/mobility/getstarted.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to prefer JSON output, respect CLI exit status, surface warnings, and verify data freshness and provenance fields returned by odh.] <br>

## Skill Version(s): <br>
0.3.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
