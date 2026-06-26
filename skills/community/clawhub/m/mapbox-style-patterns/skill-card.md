## Description: <br>
Common style patterns, layer configurations, and recipes for typical mapping scenarios including restaurant finders, real estate, data visualization, navigation, delivery/logistics, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and adapt Mapbox style recipes, layer configurations, and data-driven styling patterns for POI, real estate, analytics, navigation, dark-mode, and logistics maps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delivery and logistics patterns can expose driver or customer live locations when adapted into a production app. <br>
Mitigation: Use informed consent, authenticated role-limited access, minimized precision and update frequency, short retention, and clear disclosure of who can view location data. <br>
Risk: Style recipes may be copied without testing against the app's real data density, zoom levels, device sizes, or accessibility requirements. <br>
Mitigation: Run visual regression checks across representative zoom levels, mobile and desktop widths, dense and sparse data, label collision cases, color contrast, and loading performance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mapbox/mapbox-style-patterns) <br>
- [Real Estate Map Pattern](references/real-estate.md) <br>
- [Data Visualization Base Map Pattern](references/data-viz-base.md) <br>
- [Navigation/Routing Map Pattern](references/navigation.md) <br>
- [Dark Mode / Night Theme Pattern](references/dark-mode.md) <br>
- [Delivery/Logistics Map Pattern](references/delivery-logistics.md) <br>
- [Expressions and Clustering Patterns](references/expressions-clustering.md) <br>
- [Common Map Style Modifications](references/common-modifications.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with JSON and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces style recommendations and layer configuration examples; users must adapt examples to their map data, access controls, and Mapbox implementation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
