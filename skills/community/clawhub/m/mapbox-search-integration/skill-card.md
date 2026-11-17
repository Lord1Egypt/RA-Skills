## Description:

Complete workflow for implementing Mapbox search in applications - from discovery questions to production-ready integration with best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and implement the right Mapbox search approach for applications that need address, place, point-of-interest, or geocoding search. It guides discovery, product selection, platform-specific integration, testing, monitoring, and production-readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production-style web examples may include unsafe rendering patterns such as innerHTML or setHTML.

Mitigation: Use safe DOM rendering, escaping, or sanitization before adapting examples into a real application.

Risk: Backend proxy examples may be copied without adequate abuse controls.

Mitigation: Add authentication or rate limits, validate inputs, and avoid exposing secret Mapbox tokens.

Risk: Direct API integrations can mix sessions or omit token restrictions.

Mitigation: Prefer SDK-based patterns when possible, isolate search sessions per user, and restrict public tokens to the minimum required scope and allowed URLs.

Risk: Search and location queries may send user data to Mapbox.

Mitigation: Provide clear user notice and review privacy requirements before collecting or sending search and location data.

## Reference(s):

- [Web: Mapbox Search JS Integration](artifact/references/web-search-js.md)
- [React Integration Patterns](artifact/references/react-search.md)
- [iOS: Search SDK for iOS](artifact/references/ios-search.md)
- [Android: Search SDK for Android](artifact/references/android-search.md)
- [Node.js: Mapbox Search JS Core](artifact/references/nodejs-search.md)
- [Best Practices: The Good Parts](artifact/references/best-practices.md)
- [Common Pitfalls and How to Avoid Them](artifact/references/pitfalls.md)
- [Framework-Specific Hooks and Composables](artifact/references/framework-hooks.md)
- [Testing and Monitoring](artifact/references/testing-monitoring.md)
- [Search Box API Documentation](https://docs.mapbox.com/api/search/search-box/)
- [Geocoding API Documentation](https://docs.mapbox.com/api/search/geocoding/)
- [Mapbox Search JS](https://docs.mapbox.com/mapbox-search-js/guides/)
- [Search JS React API](https://docs.mapbox.com/mapbox-search-js/api/react/)
- [Search JS Web API](https://docs.mapbox.com/mapbox-search-js/api/web/)
- [Search JS Core API](https://docs.mapbox.com/mapbox-search-js/api/core/)
- [Search SDK for iOS](https://docs.mapbox.com/ios/search/guides/)
- [Search SDK for Android](https://docs.mapbox.com/android/search/guides/)
- [Location Helper Tool](https://labs.mapbox.com/location-helper/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with platform-specific code examples and configuration checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API and SDK selection advice, session-token guidance, testing steps, and production-readiness checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
