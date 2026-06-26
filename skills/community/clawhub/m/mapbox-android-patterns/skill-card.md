## Description: <br>
Provides official integration patterns for Mapbox Maps SDK v11 on Android, covering installation, markers, user location, custom data, styles, camera control, and featureset interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement Mapbox Maps SDK v11 in Android apps with Kotlin, Jetpack Compose, or the Android View system. It helps with setup, map initialization, annotations, user-location display, GeoJSON data, camera and style controls, and map feature interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mapbox access tokens can be exposed if developers commit sensitive credentials or use overly broad token scopes. <br>
Mitigation: Use scoped app tokens, avoid committing sensitive tokens, and review token handling before shipping an app. <br>
Risk: Location display or tracking patterns can affect user privacy if enabled without clear user disclosure and consent. <br>
Mitigation: Request platform permissions appropriately and add clear in-app disclosure and consent before enabling user-location features. <br>


## Reference(s): <br>
- [Android Maps Guides](https://docs.mapbox.com/android/maps/guides/) <br>
- [Mapbox Maps SDK for Android API Reference](https://docs.mapbox.com/android/maps/api/11.18.1/) <br>
- [Mapbox Android Example Apps](https://github.com/mapbox/mapbox-maps-android/tree/main/Examples) <br>
- [Mapbox Android Interactions Guide](https://docs.mapbox.com/android/maps/guides/user-interaction/interactions/) <br>
- [Mapbox Jetpack Compose Guide](https://docs.mapbox.com/android/maps/guides/using-jetpack-compose/) <br>
- [Mapbox Android v11 Migration Guide](https://docs.mapbox.com/android/maps/guides/migrate-to-v11/) <br>
- [Annotations reference](references/annotations.md) <br>
- [Camera and styles reference](references/camera-styles.md) <br>
- [Custom data reference](references/custom-data.md) <br>
- [Interactions reference](references/interactions.md) <br>
- [Location tracking reference](references/location-tracking.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Kotlin, XML, and Gradle code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples may include Mapbox token configuration and user-location permission patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
