## Description:

Provides development guidance for using Baidu Map JavaScript API UI Kit components for place autocomplete, place search, place detail display, and driving route planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahddbing](https://clawhub.ai/user/wahddbing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to implement Baidu Maps UI Kit workflows in web map applications, including search input autocomplete, POI search, POI detail panels, and driving route planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map searches, selected places, coordinates, phone fields, and route endpoints can contain sensitive user data.

Mitigation: Provide notice and consent where appropriate, minimize logged location and POI data, and handle route and place data as user-sensitive application data.

Risk: An unrestricted Baidu Maps JavaScript API key can be abused if exposed in production applications.

Mitigation: Restrict BMAP_JSAPI_KEY by allowed origins and APIs, rotate keys when needed, and avoid shipping unrestricted keys.

Risk: CDN or package dependency drift can change runtime behavior after deployment.

Mitigation: Pin package versions, prefer lockfile-based installs or reviewed self-hosted assets, and use a restrictive Content Security Policy for production apps.

Risk: RoutePlan documentation states that only driving route planning is currently available.

Mitigation: Design application flows to expose driving route planning only, and validate unsupported transit, riding, or walking modes before promising them to users.

## Reference(s):

- [Quick Start](references/getting-started.md)
- [PlaceAutocomplete Reference](references/place-autocomplete.md)
- [PlaceSearch Reference](references/place-search.md)
- [PlaceDetail Reference](references/place-detail.md)
- [RoutePlan Reference](references/route-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/wahddbing/skills/jsapi-ui-kit)
- [Baidu Maps JavaScript API Loader](https://api.map.baidu.com/api?v=1.0&type=webgl&ak=YOUR_AK)
- [jsapi-ui-kit CDN Bundle](https://unpkg.com/@baidumap/jsapi-ui-kit/dist/jsapi-ui-kit.iife.js)
- [jsapi-ui-kit CDN Stylesheet](https://unpkg.com/@baidumap/jsapi-ui-kit/dist/css/jsapi-ui-kit.css)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, TypeScript, HTML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js for package installation examples and a Baidu Maps JavaScript API key in BMAP_JSAPI_KEY for implementations.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
