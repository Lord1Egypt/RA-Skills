## Description: <br>
Ask the user for their Google saved places list, look up each place with goplaces, and recommend the single best one to visit today based on their preferences and visit history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsq704252212](https://clawhub.ai/user/wsq704252212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users with saved Google Places lists use this skill to choose one place to visit based on live place details, personal notes, cuisine or area preferences, and prior visit history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores saved places, personal notes, preferences, and visit history in a local JSON file. <br>
Mitigation: Install only if local retention is acceptable, and manually delete or edit skills/goplaces-togo/goplaces-visits.json to remove retained history. <br>
Risk: Place resolution and details lookups are sent through the configured goplaces and Google Places setup. <br>
Mitigation: Use a restricted Google Places API key and verify the goplaces binary on PATH before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wsq704252212/goplaces-togo) <br>
- [Publisher profile](https://clawhub.ai/user/wsq704252212) <br>
- [Google Takeout](https://takeout.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON file updates, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and local JSON state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist saved places, notes, preferences, and visit history in skills/goplaces-togo/goplaces-visits.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
