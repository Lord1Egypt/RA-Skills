## Description: <br>
Generate and save location-aware background images by choosing a real place cue, using local time and weather, and rendering through `nano-banana-pro`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chadnewbry](https://clawhub.ai/user/chadnewbry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate finished place-aware background images for apps, dashboards, wallpapers, and mockups. It helps choose grounded city cues, apply local time and weather context when provided or approved, shape UI-readable prompts, and save rendered image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using Gemini API access with Nano Banana Pro may incur provider quota use or billing. <br>
Mitigation: Confirm API key permissions, quota, and billing expectations before running the skill. <br>
Risk: Screenshots, private images, or precise location details may be used as rendering inputs if the user provides or approves them. <br>
Mitigation: Provide only location and visual context intended for image generation, and avoid sensitive inputs. <br>
Risk: Generated files are saved locally, defaulting to ./generated/ when no output path is specified. <br>
Mitigation: Specify an explicit output path when file location matters. <br>


## Reference(s): <br>
- [Location-Aware Background Prompt Patterns](references/prompt-patterns.md) <br>
- [ClawHub Listing](https://clawhub.ai/chadnewbry/location-aware-backgrounds) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Guidance] <br>
**Output Format:** [PNG image files plus Markdown rationale, exact prompt text, saved file paths, and an optional production recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; defaults to one image and saves under ./generated/ when no output path is specified.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
