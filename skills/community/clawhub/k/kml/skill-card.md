## Description:

Inspect, validate, summarize, and extract KML/KMZ structure and placemark data, including geometry counts, bounding boxes, folder and overlay counts, and coordinate issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GIS-adjacent analysts use this skill to inspect local KML/KMZ files, validate coordinate and packaging issues, and produce lightweight placemark summaries before deeper GIS work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or very large KML/KMZ files can consume local CPU or memory during XML or archive parsing.

Mitigation: Run inspection with file size, CPU, memory, and timeout limits when inputs are untrusted or unusually large.

Risk: The skill provides lightweight inspection and validation, not deterministic GIS conversion, reprojection, clipping, or geometry repair.

Mitigation: Route conversion, reprojection, clipping, and batch GIS processing to a dedicated GIS tool such as qgis.

Risk: Automatic invocation on local files may process inputs before a user has confirmed trust and expected size.

Mitigation: Confirm the file source and expected scope before running the helper on local KML or KMZ files.

## Reference(s):

- [KML And KMZ Notes](references/patterns.md)
- [OGC KML 2.2 Namespace](http://www.opengis.net/kml/2.2)
- [Google KML Extensions Namespace](http://www.google.com/kml/ext/2.2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON command output when the local helper script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python helper inspects .kml and .kmz files and returns summaries, placemark extracts, or validation errors; no external API calls.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
