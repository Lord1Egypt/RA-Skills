## Description:

Official integration patterns for Mapbox Maps SDK on iOS. Covers installation, adding markers, user location, custom data, styles, camera control, and featureset interactions. Based on official Mapbox documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Mapbox Maps SDK v11 into iOS applications with Swift, SwiftUI, and UIKit. It helps with setup, annotations, user location, custom GeoJSON data, styles, camera behavior, and map interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access tokens can be mishandled when copying setup examples into an application.

Mitigation: Use only public Mapbox tokens in iOS client configuration and avoid committing real tokens beyond intended public-token usage.

Risk: Location examples may collect or display precise user location.

Mitigation: Add a clear iOS purpose string, request user consent, and provide an appropriate privacy disclosure before enabling location features.

Risk: Generated implementation guidance can be copied without validating it against the target app and SDK version.

Mitigation: Review generated Swift and configuration snippets against the app's Mapbox Maps SDK version and test map, annotation, and location behavior before release.

## Reference(s):

- [iOS Maps Guides](https://docs.mapbox.com/ios/maps/guides/)
- [Mapbox Maps iOS API Reference](https://docs.mapbox.com/ios/maps/api/11.18.1/documentation/mapboxmaps/)
- [Mapbox Maps iOS Example Apps](https://github.com/mapbox/mapbox-maps-ios/tree/main/Sources/Examples)
- [Install Mapbox Maps SDK for iOS](https://docs.mapbox.com/ios/maps/guides/install/)
- [Interactions Guide](https://docs.mapbox.com/ios/maps/guides/user-interaction/Interactions/)
- [SwiftUI User Guide](https://docs.mapbox.com/ios/maps/api/11.18.1/documentation/mapboxmaps/swiftui-user-guide)
- [Migration Guide v10 to v11](https://docs.mapbox.com/ios/maps/guides/migrate-to-v11/)
- [Annotations: Circle, Polyline, Polygon](references/annotations.md)
- [Camera Control + Map Styles](references/camera-styles.md)
- [Custom Data: GeoJSON](references/custom-data.md)
- [Interactions: Featureset, Custom Layer Taps, Long Press, Gestures](references/interactions.md)
- [Location Tracking: Camera Follow User + Get Current Location](references/location-tracking.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with Swift and XML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides implementation patterns and troubleshooting guidance for Mapbox Maps SDK v11 on iOS.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
