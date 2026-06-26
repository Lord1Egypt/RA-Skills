## Description: <br>
Official integration patterns for Mapbox Maps SDK on iOS. Covers installation, adding markers, user location, custom data, styles, camera control, and featureset interactions. Based on official Mapbox documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Mapbox Maps SDK v11 into iOS apps with Swift, SwiftUI, and UIKit. It provides patterns for setup, map initialization, annotations, user location, custom GeoJSON data, camera control, map styles, and feature interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location examples can expose precise user coordinates if copied into production diagnostics or logging. <br>
Mitigation: Use a specific location-use explanation, request location only when needed, provide a clear way to stop location following, and avoid logging precise coordinates in production. <br>


## Reference(s): <br>
- [iOS Maps Guides](https://docs.mapbox.com/ios/maps/guides/) <br>
- [Mapbox Maps SDK for iOS API Reference](https://docs.mapbox.com/ios/maps/api/11.18.1/documentation/mapboxmaps/) <br>
- [Mapbox iOS Example Apps](https://github.com/mapbox/mapbox-maps-ios/tree/main/Sources/Examples) <br>
- [Mapbox Maps SDK Install Guide](https://docs.mapbox.com/ios/maps/guides/install/) <br>
- [Mapbox Interactions Guide](https://docs.mapbox.com/ios/maps/guides/user-interaction/Interactions/) <br>
- [SwiftUI User Guide](https://docs.mapbox.com/ios/maps/api/11.18.1/documentation/mapboxmaps/swiftui-user-guide) <br>
- [Migration Guide v10 to v11](https://docs.mapbox.com/ios/maps/guides/migrate-to-v11/) <br>
- [Annotations: Circle, Polyline, Polygon](references/annotations.md) <br>
- [Camera Control + Map Styles](references/camera-styles.md) <br>
- [Custom Data (GeoJSON): Lines, Polygons, Points, Update/Remove](references/custom-data.md) <br>
- [Interactions: Featureset, Custom Layer Taps, Long Press, Gestures](references/interactions.md) <br>
- [Location Tracking: Camera Follow User + Get Current Location](references/location-tracking.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with Swift and XML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides reference patterns and troubleshooting guidance; does not execute tools or write app files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
