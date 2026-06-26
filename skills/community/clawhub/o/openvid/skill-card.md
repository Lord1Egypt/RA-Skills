## Description: <br>
Generate branded 15-180 second HD motion graphics explainer videos by providing a prompt with brand information and a public URL via OpenVid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aklo360](https://clawhub.ai/user/aklo360) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents, developers, and teams use this skill to request paid, branded explainer video generation from OpenVid using prompt text and an optional public URL for brand extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment details may vary between the documentation and the live 402 payment response. <br>
Mitigation: Verify the exact chain, amount, and recipient in the live 402 response before signing or submitting payment. <br>
Risk: Submitted URLs are fetched by the external service for brand extraction. <br>
Mitigation: Provide only public URLs and avoid internal, private, or access-controlled resources. <br>
Risk: Prompt text and generated videos are handled by an external service, with videos stored for 7 days. <br>
Mitigation: Do not submit sensitive prompt text, credentials, private business data, or confidential media requirements. <br>


## Reference(s): <br>
- [OpenVid ClawHub Page](https://clawhub.ai/aklo360/openvid) <br>
- [OpenVid Website](https://openvid.app) <br>
- [OpenVid Create Video](https://openvid.app/create) <br>
- [OpenVid API Gateway](https://gateway.openvid.app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with HTTP examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for requesting and polling paid OpenVid video-generation jobs; completed jobs return video URLs from the external service.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
