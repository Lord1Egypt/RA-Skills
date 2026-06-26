## Description: <br>
Inspect, validate, summarize, and extract data from KML and KMZ files, including Placemark geometry counts, Folder structure, coordinate ranges, bbox generation, altitude tuples, Google Earth packaging issues, and conversion guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and geospatial data reviewers use this skill to inspect KML or KMZ structure, summarize placemarks and geometry counts, validate coordinate tuples, and identify common packaging or XML problems before cleanup or conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: KML/KMZ files can contain private place names and precise location data. <br>
Mitigation: Use the skill only with files that are acceptable to summarize in the conversation, and avoid sharing sensitive location data. <br>
Risk: Coordinate summaries can be misleading when the source export workflow or intended CRS is misunderstood. <br>
Mitigation: Confirm the source workflow when precision matters, and route reprojection, clipping, deterministic conversion, or geometry repair to a dedicated GIS skill. <br>


## Reference(s): <br>
- [KML and KMZ patterns](references/patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/jvy/kml) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, json, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON output from helper commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries include source type, document name, placemark and geometry counts, folder and overlay counts, bounding boxes, validation errors, and suspicious coordinate patterns when present.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
