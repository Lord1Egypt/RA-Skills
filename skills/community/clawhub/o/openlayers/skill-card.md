## Description: <br>
Build, debug, and integrate OpenLayers web maps with map and view setup, tiled and vector layers, GeoJSON overlays, projection handling, feature styling, interactions, layer ordering, fit-to-extent flows, and frontend integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to produce OpenLayers implementation guidance, targeted debugging advice, and small working examples for browser-based GIS maps. It is suited for projection-aware web mapping work involving GeoJSON, OSM or XYZ tiles, WMS or WMTS layers, feature interaction, and SPA lifecycle handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled scaffold command writes files to a user-specified output path. <br>
Mitigation: Review the --out path before running scaffold commands and keep generated demos in a disposable project directory. <br>
Risk: Generated demo pages load OpenLayers modules and CSS from jsDelivr using an ol@latest URL. <br>
Mitigation: Pin the OpenLayers version before using generated pages in a production or repeatable build. <br>
Risk: The GeoJSON scaffold inlines the provided GeoJSON file into generated HTML. <br>
Mitigation: Use non-sensitive sample data for demos and review the generated HTML before sharing it. <br>
Risk: Security guidance classifies the release context as powerful and appropriate for maintainer or developer use. <br>
Mitigation: Confirm exact targets, keep tokens scoped, and review any command before allowing writes. <br>


## Reference(s): <br>
- [OpenLayers homepage](https://openlayers.org/) <br>
- [OpenLayers ClawHub release](https://clawhub.ai/jvy/openlayers) <br>
- [OpenLayers Patterns](references/patterns.md) <br>
- [Layer Recipes](references/layer-recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and optional generated HTML files from the bundled scaffold script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scaffold script writes local HTML files and reports the written path as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
