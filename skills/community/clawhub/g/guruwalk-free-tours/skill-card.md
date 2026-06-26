## Description: <br>
Search GuruWalk free tours through the GuruWalk MCP server and return bookable options by city, dates, and language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdanielwalk](https://clawhub.ai/user/gdanielwalk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travel planners and agents use this skill to find GuruWalk free walking tours for a city, date range, and preferred language, then return concise booking options with next available sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends city, date range, and language details to the disclosed GuruWalk API. <br>
Mitigation: Use it only for GuruWalk or free walking tour searches and provide only the search details needed. <br>
Risk: Malformed city slugs or date ranges can produce empty results instead of clear validation errors. <br>
Mitigation: Normalize city names to lower-case slugs, convert relative dates to ISO yyyy-mm-dd, and check that start_date is not after end_date before calling search. <br>
Risk: Returned tour records may include missing titles or no available sessions. <br>
Mitigation: Filter for events with available_spots greater than zero, handle missing fields gracefully, and suggest adjusting city, dates, or language one variable at a time. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gdanielwalk/guruwalk-free-tours) <br>
- [GuruWalk MCP server](https://guruwalk-api-44909317956.europe-southwest1.run.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown recommendations with booking URLs and parsed tour details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns concise tour options or a no-availability response after filtering available events.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
