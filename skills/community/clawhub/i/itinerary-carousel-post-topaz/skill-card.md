## Description: <br>
Create and publish an Instagram carousel post from a tabiji.ai itinerary, with Topaz Labs AI image enhancement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and developers use this skill to turn a tabiji.ai itinerary into a six-slide Instagram carousel with sourced photos, Topaz image enhancement, text overlays, and Instagram publishing steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can use account credentials to publicly publish Instagram content and modify a GitHub repository. <br>
Mitigation: Run only for Instagram accounts and repositories you control, and require explicit human review before any git push or Instagram publish command. <br>
Risk: Images and captions may be sent to Topaz Labs, GitHub, and Instagram during execution. <br>
Mitigation: Confirm that the selected images, captions, itinerary details, and account credentials are appropriate for those services before running the workflow. <br>
Risk: Generated slides or captions could be inaccurate, low quality, or unsuitable for public posting. <br>
Mitigation: Review every generated slide, caption, source image, and final permalink before treating the post as complete. <br>


## Reference(s): <br>
- [Instagram Graph API Carousel Publishing Reference](references/instagram-graph-api.md) <br>
- [ClawHub skill page](https://clawhub.ai/psyduckler/itinerary-carousel-post-topaz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, JSON, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an operational carousel-publishing workflow and expected temporary file outputs; execution can publish public Instagram content and push repository changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
