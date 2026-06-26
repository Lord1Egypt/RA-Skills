## Description: <br>
Visual image search using Google Lens via SerpAPI to identify objects, landmarks, products, plants, animals, artwork, logos, and other visual entities from an image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TobiasLee](https://clawhub.ai/user/TobiasLee) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to run reverse image search, verify uncertain visual identifications, find similar images or exact matches, and retrieve product-oriented visual results from user-provided image URLs or local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local image files can be uploaded to third-party public image hosts before being submitted for visual search. <br>
Mitigation: Prefer already-public image URLs, or confirm that the image contains no private photos, documents, credentials, proprietary material, or sensitive screenshots before using a local file. <br>
Risk: Search requests and image URLs are sent to SerpAPI and may be subject to external service handling and retention. <br>
Mitigation: Use the skill only for images and search context that are acceptable to share with SerpAPI under the applicable account and data-handling terms. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TobiasLee/image-search) <br>
- [Publisher Profile](https://clawhub.ai/user/TobiasLee) <br>
- [SerpAPI](https://serpapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries by default, with optional raw JSON output from SerpAPI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SERPAPI_KEY. Local image files may be uploaded to external image hosting before search.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
