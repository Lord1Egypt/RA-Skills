## Description: <br>
Automates jewellery product marketing using Google Vertex AI, Imagen, and Google Drive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsmebasil](https://clawhub.ai/user/itsmebasil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and ecommerce teams can use this skill to turn jewellery product photos and metadata into generated lifestyle images, studio product images, social captions, hashtags, and organized Google Drive assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product images and metadata may be sent to Anthropic and Google services. <br>
Mitigation: Use only product data approved for those services and disclose external processing to operators before running the skill. <br>
Risk: The runnable worker exposes a web endpoint that evidence.security says lacks authentication. <br>
Mitigation: Add authentication and URL allowlisting before exposing the FastAPI worker. <br>
Risk: Drive links and generated outputs may persist in a broad Redis or local cache. <br>
Mitigation: Restrict the Google service account to a dedicated Drive folder and disable or re-scope caching in shared environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/itsmebasil/pattern-skills) <br>
- [Google Drive file scope](https://www.googleapis.com/auth/drive.file) <br>
- [Vertex AI Gemini 1.5 Pro endpoint](https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/publishers/google/models/gemini-1.5-pro:generateContent) <br>
- [Vertex AI Imagen 3 endpoint](https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/publishers/google/models/imagen-3.0-generate-002:predict) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Images, URLs, Files, JSON] <br>
**Output Format:** [JSON payload with generated image links, caption text, hashtags, and a Google Drive folder link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Inputs include a product image and jewellery metadata; generated assets may be cached for up to 30 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
