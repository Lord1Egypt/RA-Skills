## Description: <br>
Complete workflow for implementing Mapbox search in applications - from discovery questions to production-ready integration with best practices <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and implement the right Mapbox search workflow for applications that need address, place, POI, autocomplete, or geocoding-style location search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied client-side examples could expose overly broad Mapbox tokens or secret tokens. <br>
Mitigation: Use restricted public Mapbox tokens for client applications, apply URL restrictions, and keep secret tokens out of client code. <br>
Risk: Search and location flows may collect or transmit user location queries and selected places. <br>
Mitigation: Disclose the relevant search and location data flows before production use. <br>
Risk: Copied rendering examples using innerHTML or setHTML can introduce unsafe HTML handling. <br>
Mitigation: Use safe DOM construction or sanitize content before rendering user-controlled values. <br>


## Reference(s): <br>
- [Web: Mapbox Search JS Integration](references/web-search-js.md) <br>
- [React Integration Patterns](references/react-search.md) <br>
- [iOS: Search SDK for iOS](references/ios-search.md) <br>
- [Android: Search SDK for Android](references/android-search.md) <br>
- [Node.js: Mapbox Search JS Core](references/nodejs-search.md) <br>
- [Best Practices: The Good Parts](references/best-practices.md) <br>
- [Common Pitfalls and How to Avoid Them](references/pitfalls.md) <br>
- [Framework-Specific Hooks and Composables](references/framework-hooks.md) <br>
- [Testing and Monitoring](references/testing-monitoring.md) <br>
- [Mapbox Search Box API Documentation](https://docs.mapbox.com/api/search/search-box/) <br>
- [Mapbox Geocoding API Documentation](https://docs.mapbox.com/api/search/geocoding/) <br>
- [Mapbox Search JS Guides](https://docs.mapbox.com/mapbox-search-js/guides/) <br>
- [Search SDK for iOS Guides](https://docs.mapbox.com/ios/search/guides/) <br>
- [Search SDK for Android Guides](https://docs.mapbox.com/android/search/guides/) <br>
- [Location Helper Tool](https://labs.mapbox.com/location-helper/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform-specific implementation guidance for web, React, iOS, Android, and Node.js.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
