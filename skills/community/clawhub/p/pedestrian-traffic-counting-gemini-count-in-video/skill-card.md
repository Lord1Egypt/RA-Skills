## Description: <br>
Analyze and count objects in videos using Google Gemini API (object counting, pedestrian detection, vehicle tracking, and surveillance video analysis). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to prepare Gemini prompts and Python workflows for counting pedestrians, vehicles, cyclists, and other objects in video footage. It is intended for surveillance, traffic, and batch video analysis scenarios where structured count output is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos may be uploaded to Google Gemini for processing, which can expose surveillance footage or other sensitive content to a cloud service. <br>
Mitigation: Use only footage you are authorized to process, avoid regulated or confidential video unless approved, and keep batch jobs scoped to a dedicated folder. <br>
Risk: The skill relies on a Gemini API key and API usage can incur cost. <br>
Mitigation: Store GEMINI_API_KEY in an environment variable or secrets manager, restrict access to the key, and monitor API usage and billing. <br>
Risk: Object counts can be wrong in crowded, low-quality, occluded, or ambiguous video scenes. <br>
Mitigation: Validate prompts on representative samples, use explicit inclusion and exclusion rules, and review results before using them for operational decisions. <br>


## Reference(s): <br>
- [Gemini Video API Docs](https://ai.google.dev/gemini-api/docs/video-understanding) <br>
- [Gemini Python SDK Quickstart](https://ai.google.dev/gemini-api/docs/quickstart?lang=python) <br>
- [Google AI Studio API Key](https://aistudio.google.com/apikey) <br>
- [Gemini API Pricing](https://ai.google.dev/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python code examples and JSON output schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance uses GEMINI_API_KEY and may include File API upload, polling, parsing, and batch-processing patterns.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
