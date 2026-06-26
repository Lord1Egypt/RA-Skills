## Description: <br>
Patterns for visualizing data on maps including choropleth maps, heat maps, 3D visualizations, data-driven styling, and animated data. Covers layer types, color scales, and performance optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and map application teams use this skill to choose and implement Mapbox visualization patterns for statistical, density, 3D, animated, and large-dataset map displays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Popup examples that insert feature properties into HTML can expose users to unsafe content when map data is untrusted. <br>
Mitigation: Treat feature properties and external map data as untrusted; prefer DOM or textContent-based popups, or apply robust sanitization before using setHTML. <br>
Risk: Examples use external data endpoints and Mapbox services that may require scoped credentials. <br>
Mitigation: Use properly scoped Mapbox tokens and data endpoints when adapting the examples. <br>


## Reference(s): <br>
- [Mapbox Data Visualization Patterns](https://clawhub.ai/mapbox/mapbox-data-visualization-patterns) <br>
- [Clustering (Point Density)](references/clustering.md) <br>
- [3D Extrusions](references/3d-extrusions.md) <br>
- [Circle/Bubble Maps and Line Data Visualization](references/circles-lines.md) <br>
- [Animated Data Visualizations](references/animation.md) <br>
- [Performance Optimization](references/performance.md) <br>
- [Legends, UI Controls, and Common Use Cases](references/legends-use-cases.md) <br>
- [Mapbox Expression Reference](https://docs.mapbox.com/style-spec/reference/expressions/) <br>
- [Mapbox Data Visualization Tutorials](https://docs.mapbox.com/help/tutorials/#data-visualization) <br>
- [ColorBrewer](https://colorbrewer2.org/) <br>
- [Turf.js](https://turfjs.org/) <br>
- [Simple Statistics](https://simple-statistics.github.io/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript and Mapbox style-expression code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for adapting Mapbox visualization patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
