## Description: <br>
Generate videos through the NanoPhoto.AI Veo 3.1 API for text-to-video, reference-image, first-and-last-frame, multi-shot, and status-check workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanophotohq](https://clawhub.ai/user/nanophotohq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to submit and monitor NanoPhoto.AI Veo 3.1 video generation jobs, including text-only, reference-image, first-and-last-frame, and multi-shot video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, referenced public image URLs, task IDs, and the NanoPhoto API key are sent to NanoPhoto.AI for processing. <br>
Mitigation: Use the skill only when that third-party data sharing is approved, and avoid confidential, regulated, private, or unauthorized media unless the organization permits it. <br>
Risk: The required NanoPhoto API key could be exposed if pasted into chat or committed to files. <br>
Mitigation: Store NANOPHOTO_API_KEY in the platform's secure skill environment setting or another approved secret store. <br>
Risk: Image-based generation requires public image URLs, which may disclose private or sensitive media. <br>
Mitigation: Provide only public image URLs that the user is authorized and comfortable sending to NanoPhoto.AI. <br>


## Reference(s): <br>
- [Veo 3.1 API Reference](references/api.md) <br>
- [NanoPhoto.AI homepage](https://nanophoto.ai) <br>
- [ClawHub skill page](https://clawhub.ai/nanophotohq/nanophoto-veo-3-1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return task IDs, status responses, shot-level video URLs, and timing information when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
