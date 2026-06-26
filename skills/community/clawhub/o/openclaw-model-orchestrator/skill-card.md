## Description: <br>
Multi-LLM orchestration for OpenClaw with fan-out, pipeline, and consensus patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[homeofe](https://clawhub.ai/user/homeofe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw use this skill to route coding, research, security, review, and bulk tasks across planner, worker, and reviewer models through fan-out, pipeline, or consensus workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text, code snippets, and intermediate outputs may be sent to the configured model providers during orchestration. <br>
Mitigation: Use only with providers approved for the data being processed, and avoid secrets, regulated data, or private customer material unless those providers are approved for that use. <br>
Risk: Synthesized results may contain incorrect, incomplete, or conflicting model-generated guidance. <br>
Mitigation: Review final outputs and any reported disagreements before relying on the result for implementation, security, or operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/homeofe/openclaw-model-orchestrator) <br>
- [Artifact README](artifact/README.md) <br>
- [OpenClaw plugin manifest](artifact/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown chat responses with model recommendations, progress updates, and synthesized final results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include intermediate progress messages and final synthesized output from multiple configured models.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and package.json; plugin manifest reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
