## Description:

Use when building, embedding, customizing, or troubleshooting AR/XR experiences with the Kivicube Web Plugin, including WebAR/Web3D H5 pages, landing pages, event pages, product showcases, sceneId or collectionId setup, Vue/React wrappers, SceneApi runtime control, camera, autoplay, permissions, CORS, and compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[listenlin](https://clawhub.ai/user/listenlin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external integrators use this skill to build and troubleshoot Kivicube WebAR, Web3D, and XR landing pages, including iframe embedding, scene or collection setup, custom host UI, runtime SceneApi workflows, and deployment issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad iframe permissions may expose camera, microphone, sensor, autoplay, fullscreen, gyroscope, and accelerometer capabilities beyond what a particular AR/XR page needs.

Mitigation: Reduce iframe permissions to the minimum required for the reviewed experience and remove microphone permission unless a separately reviewed audio feature requires it.

Risk: The integration uses a third-party Kivicube script loaded from a public URL.

Mitigation: Consider pinning or self-hosting a reviewed copy of the vendor script and enforce CSP controls that allow only the required Kivicube script and frame origins.

Risk: Camera and photo workflows can affect user privacy expectations.

Mitigation: Provide clear camera and photo notices, keep an explicit user gesture for media start flows, and test on target mobile browsers and WebViews before launch.

## Reference(s):

- [Skill listing](https://clawhub.ai/listenlin/skills/kivicube-web-plugin-ar-xr-builder)
- [Kivicube Web Plugin script](https://www.kivicube.com/lib/iframe-plugin.js)
- [Integration](references/integration.md)
- [Patterns](references/patterns.md)
- [Examples](references/examples.md)
- [Scene Objects Reference](references/scene_objects_reference.md)
- [Media And Animation Reference](references/media_animation_reference.md)
- [Rendering And Camera Reference](references/rendering_camera_reference.md)
- [Best Practices](references/best_practices.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with inline code examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTML, JavaScript, Vue, React, and troubleshooting steps for browser-based AR/XR integrations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
