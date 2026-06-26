## Description: <br>
Preflight checks draft content with simulated audience personas before publishing and returns engagement predictions, share potential, and specific rewrites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kbo4sho](https://clawhub.ai/user/kbo4sho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, product teams, and developers use Preflight to test draft social posts, launch copy, pricing announcements, and blog posts against simulated audience personas before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft content submitted for review is sent to the configured model service. <br>
Mitigation: Keep the model endpoint pointed at localhost or another trusted service and avoid submitting sensitive unpublished material to untrusted endpoints. <br>
Risk: Project-specific persona files can change the audience model and influence the feedback. <br>
Mitigation: Review any preflight-personas.md file before relying on its results. <br>
Risk: Persona reactions are predictive guidance and may be incorrect or misleading for the real audience. <br>
Mitigation: Use the verdict and rewrites as pre-publication input, then review important claims and final copy before publishing. <br>


## Reference(s): <br>
- [Preflight Personas](references/personas.md) <br>
- [ClawHub Preflight release page](https://clawhub.ai/kbo4sho/preflight) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Brief Markdown verdict with engagement and share counts; optional JSON from the bundled script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quick checks use 4 personas; thorough checks use all 8 default personas or a project-specific persona file.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
