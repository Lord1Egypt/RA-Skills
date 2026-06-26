## Description: <br>
Review open feed recommendation repositories with source-backed evidence, artifact-readiness checks, and cautious architecture summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, reviewers, and technical analysts use this skill to inspect public feed recommendation repositories or claims, record source-backed evidence, and distinguish reproducible findings from unverified production or reach claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A review could overstate whether public source matches a live feed ranking system or predicts reach. <br>
Mitigation: Label public algorithm claims as supported, partly supported, unsupported, or not present in the public repository, and avoid promising reach, ranking, virality, revenue, or live-platform equivalence. <br>
Risk: Repository code or local files could be inspected or run beyond the user's intended scope. <br>
Mitigation: Use only public source or user-provided local files, and require separate approval before running repository code, modifying files, deleting files, or inspecting non-public data. <br>
Risk: Phoenix execution could be described as verified when required artifacts or local run results are missing. <br>
Mitigation: Treat source inspection and runnable-model proof separately, and mark Phoenix execution as blocked unless official artifacts are present and the user supplies a local run result. <br>


## Reference(s): <br>
- [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) <br>
- [Open Feed Recsys Reviewer release page](https://clawhub.ai/zack-dev-cm/open-feed-recsys-lab) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review with source-backed findings, blocked items, architecture notes, risks, and next checks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public source or user-provided local files only; does not execute repository code unless separately requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
