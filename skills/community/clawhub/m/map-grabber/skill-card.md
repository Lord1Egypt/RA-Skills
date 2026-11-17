## Description:

Fetch OpenStreetMap vector data (streets, buildings) for an address and export to SVG, GeoPackage, or DXF for CAD/Rhino.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qrost](https://clawhub.ai/user/qrost)

### License/Terms of Use:

MIT

## Use Case:

Developers, designers, and architecture or CAD users use this skill to generate local base-map files for a requested address or place name. It can create street-network previews and vector exports, with optional building footprints, for CAD or Rhino workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested addresses or place names are sent to external OpenStreetMap/geocoding-related services.

Mitigation: Use the skill only when sharing the requested location with those services is acceptable.

Risk: Runtime behavior depends on Python packages such as osmnx and ezdxf.

Mitigation: Install in a virtual environment and pin dependency versions when reproducibility matters.

Risk: Generated map outputs are written to local file paths.

Mitigation: Choose output paths intentionally, especially when returning media from environments with allowed-directory restrictions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Shell commands, Text]

**Output Format:** [PNG, SVG, GeoPackage, or DXF files with brief text confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an address or place name and at least one requested output path; DXF export requires ezdxf.]

## Skill Version(s):

1.1.2 (source: frontmatter, clawhub.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
