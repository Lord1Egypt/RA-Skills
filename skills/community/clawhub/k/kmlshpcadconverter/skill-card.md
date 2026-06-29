## Description: <br>
A GIS and CAD conversion skill for bidirectional conversion among DWG, DXF, SHP, KML, KMZ, GeoJSON, GeoPackage, GeoParquet, OVKML, OVJSN, DJI WPMZ, and Huace KML formats, with CRS handling for common China surveying workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo-gissss](https://clawhub.ai/user/leo-gissss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, GIS analysts, CAD technicians, survey teams, and drone-mapping operators use this skill to convert spatial files across GIS, CAD, mobile mapping, and drone mission formats while applying CRS detection, GCJ-02 correction, and format-specific export options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The DWG workflow can download and silently install ODA File Converter on Windows. <br>
Mitigation: Install ODA manually from a trusted source where possible, verify the installer, and use DWG conversion only in an environment where that third-party installation behavior is acceptable. <br>
Risk: DWG conversions and third-party spatial files may come from untrusted sources. <br>
Mitigation: Run conversions in a constrained environment when handling untrusted files and review generated outputs before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leo-gissss/kmlshpcadconverter) <br>
- [GIS format reference](references/formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces conversion guidance and commands for generating GIS/CAD output files such as KML, SHP, DXF, GeoJSON, GeoPackage, GeoParquet, OVKML, OVJSN, WPMZ, and Huace KML.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
