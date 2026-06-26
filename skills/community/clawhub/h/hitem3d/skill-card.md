## Description: <br>
Generate downloadable 3D assets from images with the Hitem3D API, including single-image, portrait, multi-view, 3D printing, AR export, batch conversion, balance checks, and wait-and-download workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lihuihui-bj](https://clawhub.ai/user/lihuihui-bj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, 3D production teams, e-commerce visual teams, AR teams, and 3D printing users use this skill to route image-to-3D requests, run Hitem3D API workflows, download generated assets, and report saved paths, formats, model choices, resolution, and estimated credit cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An auth helper can print a bearer access token in command output. <br>
Mitigation: Avoid running auth commands in logged or shared contexts, never echo bearer tokens, and treat command output containing credentials as secret material. <br>
Risk: Selected images are sent to Hitem3D with API credentials from environment variables. <br>
Mitigation: Use the skill only for images that are appropriate to send to Hitem3D, keep HITEM3D_AK and HITEM3D_SK in environment variables, and avoid exposing credentials in prompts, logs, or saved files. <br>
Risk: Batch, high-resolution, portrait, or repeated generation jobs can consume paid Hitem3D credits. <br>
Mitigation: Review estimated per-task and total credit cost before large or expensive jobs and require explicit confirmation for large batches or jobs likely to exceed 100 credits. <br>
Risk: Downloaded 3D models may be untrusted output from an external service. <br>
Mitigation: Inspect downloaded 3D files before opening them in downstream tools, sharing them, or using them in production pipelines. <br>
Risk: Live end-to-end validation was blocked because usable Hitem3D API credentials were unavailable during review. <br>
Mitigation: Complete the live-validation checklist with real credentials before claiming production-proven reliability. <br>


## Reference(s): <br>
- [Hitem3D homepage](https://hitem3d.ai) <br>
- [ClawHub skill page](https://clawhub.ai/lihuihui-bj/hitem3d) <br>
- [Hitem3D API Reference](references/api.md) <br>
- [Hitem3D Product Guide](references/product-guide.md) <br>
- [Hitem3D Live Validation Plan](references/live-validation.md) <br>
- [Hitem3D Release Checklist](references/release-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Files, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands, API workflow summaries, and downloaded 3D asset files such as GLB, OBJ, STL, FBX, or USDZ] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HITEM3D_AK and HITEM3D_SK credentials, curl, python3, and base64; sends selected images to Hitem3D and can consume Hitem3D credits.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
