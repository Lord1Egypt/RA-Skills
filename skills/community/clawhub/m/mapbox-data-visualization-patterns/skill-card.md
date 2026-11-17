## Description:

Patterns for visualizing data on maps including choropleth maps, heat maps, 3D visualizations, data-driven styling, and animated data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and implement Mapbox GL JS data visualization patterns for choropleth maps, heat maps, clustering, 3D extrusions, circle and line layers, animations, legends, and performance optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable popup examples use Popup#setHTML with dataset values, which can introduce browser-side injection risk in downstream applications.

Mitigation: Build popup content with DOM APIs, textContent, setDOMContent, or a vetted sanitizer before using untrusted dataset values.

Risk: Projects that adopt optional JavaScript dependencies from the guidance may inherit dependency-chain risk if package versions are left floating.

Mitigation: Pin package versions and review dependency updates before production deployment.

## Reference(s):

- [Clustering (Point Density)](references/clustering.md)
- [3D Extrusions](references/3d-extrusions.md)
- [Circle/Bubble Maps and Line Data Visualization](references/circles-lines.md)
- [Animated Data Visualizations](references/animation.md)
- [Performance Optimization](references/performance.md)
- [Legends, UI Controls, and Common Use Cases](references/legends-use-cases.md)
- [Mapbox Expression Reference](https://docs.mapbox.com/style-spec/reference/expressions/)
- [Mapbox Data Visualization Tutorials](https://docs.mapbox.com/help/tutorials/#data-visualization)
- [ColorBrewer](https://colorbrewer2.org/)
- [Turf.js](https://turfjs.org/)
- [Simple Statistics](https://simple-statistics.github.io/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with JavaScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance and example Mapbox GL JS patterns; it does not execute code or call tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
