## Description: <br>
Reads route results from Amap or Baidu Maps and returns usable public transit, taxi, walking, or route-comparison guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyunting555](https://clawhub.ai/user/wuyunting555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to answer point-to-point travel questions with route details from Amap or Baidu Maps, including transfers, stops, walking segments, taxi comparisons, and alternate-route comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route queries and shared map tabs can reveal location information. <br>
Mitigation: Share only the specific map route tab needed for the task and avoid exposing saved places, account pages, or unrelated browser content. <br>
Risk: Route details can be time-sensitive or safety-critical. <br>
Mitigation: Verify time-sensitive travel details, service changes, and safety-critical decisions in the map application before acting. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown route summary or side-by-side comparison] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include route segments, station names, transfer counts, walking distances, timings, uncertainty notes, and Browser Relay handoff instructions when map extraction fails.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
