## Description:

Official integration patterns for Mapbox Maps SDK on Android, covering installation, markers, user location, custom data, styles, camera control, and featureset interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Mapbox Maps SDK v11 into Android applications with Kotlin, Jetpack Compose, and the View system. It provides implementation patterns for setup, annotations, user location, GeoJSON data, styles, camera behavior, and map interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location examples can be adapted into apps that collect precise user location without sufficient user understanding or need.

Mitigation: Add clear in-app disclosure, request runtime permission only when location is needed, and avoid background or continuous tracking unless the app use case requires it.

Risk: Location listeners and camera-follow behavior can continue longer than intended if copied without lifecycle cleanup.

Mitigation: Remove location listeners when tracking is no longer active and keep MapView lifecycle methods wired to the Android lifecycle.

Risk: Mapbox token setup examples can be misused if developers substitute sensitive tokens or over-scoped credentials.

Mitigation: Use appropriately scoped Mapbox access tokens and follow the app team's credential management process before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mapbox/skills/mapbox-android-patterns)
- [Android Maps Guides](https://docs.mapbox.com/android/maps/guides/)
- [API Reference](https://docs.mapbox.com/android/maps/api/11.18.1/)
- [Interactions Guide](https://docs.mapbox.com/android/maps/guides/user-interaction/interactions/)
- [Jetpack Compose Guide](https://docs.mapbox.com/android/maps/guides/using-jetpack-compose/)
- [Migration Guide v10 to v11](https://docs.mapbox.com/android/maps/guides/migrate-to-v11/)
- [Example Apps](https://github.com/mapbox/mapbox-maps-android/tree/main/Examples)
- [Annotations](references/annotations.md)
- [Camera Control and Map Styles](references/camera-styles.md)
- [Custom Data](references/custom-data.md)
- [Interactions](references/interactions.md)
- [Location Tracking](references/location-tracking.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Kotlin, XML, and Gradle code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides implementation patterns and troubleshooting guidance; it does not execute code or call external services.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
