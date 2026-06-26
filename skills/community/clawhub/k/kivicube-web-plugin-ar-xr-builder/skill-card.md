## Description: <br>
Use when building, embedding, customizing, or troubleshooting AR/XR experiences with the Kivicube Web Plugin, including WebAR/Web3D H5 pages, landing pages, event pages, product showcases, sceneId or collectionId setup, Vue/React wrappers, SceneApi runtime control, camera, autoplay, permissions, CORS, and compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[listenlin](https://clawhub.ai/user/listenlin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build, embed, customize, and troubleshoot Kivicube WebAR, Web3D, and XR landing page integrations. It helps with iframe/plugin setup, scene and collection opening, runtime SceneApi use, camera/photo flows, framework wrappers, and common permission, autoplay, CORS, and compatibility issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated integrations can depend on Kivicube's hosted iframe plugin script. <br>
Mitigation: Confirm the hosted script is trusted for the deployment and account for it in CSP and third-party dependency review. <br>
Risk: AR/XR flows may request camera, sensor, microphone, autoplay, fullscreen, gyroscope, or accelerometer permissions. <br>
Mitigation: Request only the browser permissions the page actually needs, preserve explicit user gestures where possible, and test permission behavior on target mobile browsers and WebViews. <br>
Risk: Camera and photo workflows can expose captured base64 images or private media assets. <br>
Mitigation: Disclose photo capture clearly to end users and treat captured images and private media URLs as sensitive data. <br>
Risk: Camera-dependent WebAR pages may fail or behave differently outside secure contexts. <br>
Mitigation: Run production pages on HTTPS and validate real-device behavior before launch. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/listenlin/kivicube-web-plugin-ar-xr-builder) <br>
- [Kivicube Web Plugin Script](https://www.kivicube.com/lib/iframe-plugin.js) <br>
- [Integration](references/integration.md) <br>
- [Examples](references/examples.md) <br>
- [Patterns](references/patterns.md) <br>
- [Scene Objects Reference](references/scene_objects_reference.md) <br>
- [Media And Animation Reference](references/media_animation_reference.md) <br>
- [Rendering And Camera Reference](references/rendering_camera_reference.md) <br>
- [Best Practices](references/best_practices.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with HTML, JavaScript, Vue, and React code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include integration checklists, troubleshooting steps, and implementation snippets for Kivicube Web Plugin workflows] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
