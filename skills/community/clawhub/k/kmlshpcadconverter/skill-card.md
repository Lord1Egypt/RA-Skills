## Description:

Generates guidance, commands, and Python usage patterns for converting common GIS and CAD geospatial formats, including DWG, DXF, SHP, KML/KMZ, GeoJSON, GeoPackage, GeoParquet, OVKML/OVJSN, DJI WPMZ, and Huace KML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-gissss](https://clawhub.ai/user/leo-gissss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, GIS analysts, surveying teams, and drone mapping operators use this skill to plan and run geospatial format conversions and coordinate-system handling across CAD, GIS, web map, and drone route files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DWG conversion may download and silently install ODA File Converter without integrity verification or explicit confirmation.

Mitigation: Install dependencies in a dedicated virtual environment, manually install ODA File Converter from the vendor when possible, and review or disable the auto-install path before running on sensitive systems.

Risk: Automatic coordinate-system detection can be wrong for custom, non-China, or low-confidence projected data.

Mitigation: Review conversion logs and manually specify the source CRS when data uses a custom projection or when automatic detection is uncertain.

## Reference(s):

- [GIS Format Reference](artifact/references/formats.md)
- [ClawHub Skill Page](https://clawhub.ai/leo-gissss/skills/kmlshpcadconverter)
- [ClawHub Publisher Profile](https://clawhub.ai/user/leo-gissss)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create converted GIS/CAD files and conversion logs when the generated commands are executed.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
