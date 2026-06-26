## Description: <br>
Guides developers using the Baidu Maps JavaScript API ui-kit components for place autocomplete, place search, place details, and driving route planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahddbing](https://clawhub.ai/user/wahddbing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to integrate Baidu Maps UI components into JavaScript map applications, including search autocomplete, POI search and details, and driving route planning. It provides implementation guidance, API options, event callbacks, and example code for @baidumap/jsapi-ui-kit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baidu Maps API keys can be exposed or misused when copied into client-side examples. <br>
Mitigation: Use a restricted Baidu Maps API key and do not place server-side secrets in client code. <br>
Risk: Search terms, POI identifiers, and route coordinates may be handled by Baidu Maps services. <br>
Mitigation: Disclose location-service data handling to users and review the integration against applicable privacy requirements. <br>
Risk: Unpinned npm or CDN imports can change behavior over time. <br>
Mitigation: Pin package and CDN versions where possible before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wahddbing/jsapi-ui-kit) <br>
- [Publisher profile](https://clawhub.ai/user/wahddbing) <br>
- [Quick start](references/getting-started.md) <br>
- [PlaceAutocomplete reference](references/place-autocomplete.md) <br>
- [PlaceSearch reference](references/place-search.md) <br>
- [PlaceDetail reference](references/place-detail.md) <br>
- [RoutePlan reference](references/route-plan.md) <br>
- [Baidu Maps JavaScript API loader](https://api.map.baidu.com/api?v=1.0&type=webgl&ak=YOUR_AK) <br>
- [jsapi-ui-kit CDN stylesheet](https://unpkg.com/@baidumap/jsapi-ui-kit/dist/css/jsapi-ui-kit.css) <br>
- [jsapi-ui-kit CDN script](https://unpkg.com/@baidumap/jsapi-ui-kit/dist/jsapi-ui-kit.iife.js) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript, TypeScript, HTML, and shell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for package installation examples and BMAP_JSAPI_KEY for Baidu Maps API usage.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
