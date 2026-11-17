## Description:

Automates jewellery product marketing using Google Vertex AI (Gemini and Imagen) and Google Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsmebasil](https://clawhub.ai/user/itsmebasil)

### License/Terms of Use:

MIT-0

## Use Case:

External jewellery marketers and developers use this skill to turn product photos and metadata into generated lifestyle images, product images, Instagram captions, hashtags, and organized Google Drive asset folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends product images and metadata to Anthropic, Google Vertex AI, Redis, and Google Drive.

Mitigation: Disclose these data flows before use and run the skill only with data approved for those services.

Risk: The bundled worker accepts image URLs for cloud-backed processing.

Mitigation: Use URL allowlisting or direct uploads, and enforce download size and timeout limits in a controlled environment.

Risk: Generated assets are uploaded to Google Drive folders.

Mitigation: Restrict Drive destinations and sharing permissions before deployment.

Risk: Server security evidence marks the release suspicious and notes broad cloud-backed processing exposure.

Mitigation: Add authentication, rate limits, strict metadata schemas, and deployment controls before installation or execution.

## Reference(s):

- [Pattern Skill Page](https://clawhub.ai/itsmebasil/skills/pattern-skills)
- [Google Drive API scope used by the worker](https://www.googleapis.com/auth/drive.file)
- [Gemini Vertex AI endpoint declared in artifact](https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/publishers/google/models/gemini-1.5-pro:generateContent)
- [Imagen Vertex AI endpoint declared in artifact](https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/publishers/google/models/imagen-3.0-generate-002:predict)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JSON payloads, image links, Drive links, captions, hashtags, and supporting implementation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated image assets and text files stored in Google Drive, with cache reuse for matching image and metadata payloads.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact config declares 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
