## Description:

MapV Three helps agents provide guidance and examples for building 3D map and Web GIS applications with Z-up coordinates, map editing, measurement tools, feature drawing, data management, and geospatial visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-maps](https://clawhub.ai/user/baidu-maps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GIS engineers use this skill to ask an agent for MapV Three guidance and example code for 3D web maps, map editors, measurement tools, data-driven layers, 3D Tiles, and map provider integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may use external map, terrain, tile, route, or data providers and location data.

Mitigation: Confirm provider terms, data permissions, and network behavior before using generated code with production datasets.

Risk: Map provider tokens and bearer token examples could be copied into source code.

Mitigation: Store Baidu, Mapbox, Cesium, Tianditu, and bearer tokens in secure configuration and avoid pasting real credentials into generated examples.

Risk: HTML overlays and popups may render untrusted text.

Mitigation: Sanitize user-controlled content before rendering DOM overlays, labels, popups, or custom HTML markers.

Risk: Map editing and delete API examples could affect production geospatial data if adapted directly.

Mitigation: Require explicit authorization, confirmations, and review before connecting generated editing or deletion flows to production data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baidu-maps/skills/mapv-three)
- [MapV-Three Development Guide](SKILL.md)
- [Engine Usage Guide](references/engine.md)
- [Initialization Guide](references/initialization.md)
- [DataSource Guide](references/datasource.md)
- [Editor Guide](references/editor.md)
- [Measure Guide](references/measure.md)
- [3D Tiles Loading Guide](references/3dtiles-loading.md)
- [Imagery Tile Provider Guide](references/imagery-tile-provider.md)
- [Vector Tile Provider Guide](references/vector-tile-provider.md)
- [Terrain Tile Provider Guide](references/terrain-tile-provider.md)
- [LBS Services Reference](references/services.md)
- [DOM Overlay Guide](references/dom-overlay.md)
- [Popup Guide](references/popup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MapV Three and Baidu Maps context; Baidu Maps examples require BMAP_JSAPI_KEY, and provider-specific examples may require separate Mapbox, Cesium, or Tianditu tokens.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
