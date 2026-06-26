## Description: <br>
Guides developers in using MapV-Three to build 3D map and GIS applications with map editing, measurement tools, feature drawing, data management, and geospatial visualization patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-maps](https://clawhub.ai/user/baidu-maps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as reference guidance for building Web-GIS and 3D map applications with MapV-Three, including editors, measurement workflows, spatial data visualization, tracking animations, tiled imagery, 3D Tiles, and location services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map-service credentials may be exposed or over-permissioned when copied into projects. <br>
Mitigation: Use restricted and rotatable Baidu, Mapbox, Cesium, or Tianditu keys and do not commit production credentials. <br>
Risk: Popup or DOM overlay examples can become unsafe if raw HTML is populated from untrusted user or dataset content. <br>
Mitigation: Escape or sanitize untrusted content before using copied popup, DOM overlay, or innerHTML-style examples. <br>
Risk: External map providers may introduce privacy, billing, or terms-of-use obligations. <br>
Mitigation: Review provider privacy, billing, and service terms before deploying applications built from this guidance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baidu-maps/mapv-three) <br>
- [MapV-Three Development Guide](SKILL.md) <br>
- [Engine](references/engine.md) <br>
- [Initialization](references/initialization.md) <br>
- [DataSource](references/datasource.md) <br>
- [GeoJSON DataSource](references/datasource/geojson-datasource.md) <br>
- [Editor](references/editor.md) <br>
- [Measure](references/measure.md) <br>
- [3D Tiles Loading](references/3dtiles-loading.md) <br>
- [Services](references/services.md) <br>
- [Coordinate System](references/common/coordinate-system.md) <br>
- [Best Practices](references/common/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires map-service credentials such as BMAP_JSAPI_KEY for applicable examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
