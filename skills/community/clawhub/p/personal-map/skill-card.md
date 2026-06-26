## Description: <br>
Generates personal Gaode/AMap map QR codes from geocoding, POI search, route planning, nearby search, IP location, and itinerary data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbs-amap](https://clawhub.ai/user/lbs-amap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to turn location, route, POI, and itinerary requests into Gaode/AMap API calls and shareable personal map QR codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive locations, routes, or IP addresses may be sent to external map services. <br>
Mitigation: Use the skill only for explicit map, routing, POI, or itinerary tasks and avoid submitting sensitive home/work locations or third-party IP addresses unless the user clearly requests that lookup. <br>
Risk: Generated map details and QR payloads may be shared with separate external services. <br>
Mitigation: Tell users when map data is being sent to Gaode/AMap and when QR-code payloads are sent to the QR-code service; avoid including unnecessary personal details in map names, points, or route data. <br>
Risk: QR-code images may be saved locally and persist after the session. <br>
Mitigation: Save QR images only when needed, use clear file paths, and delete locally saved QR images when they are no longer required. <br>
Risk: The skill requires a sensitive AMAP_API_KEY credential. <br>
Mitigation: Provide the API key through the documented environment variable and avoid placing it in prompts, shared files, logs, or generated examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lbs-amap/personal-map) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lbs-amap) <br>
- [Gaode/AMap Open Platform](https://lbs.amap.com/) <br>
- [QR code generation service used by the artifact](https://api.qrserver.com/v1/create-qr-code/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python examples, JSON-like API results, URLs, and optional locally saved QR-code image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_API_KEY; may call external Gaode/AMap and QR-code services and may save QR images locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
