## Description: <br>
Distributed map-reduce over agent swarms for parallel data processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to split parallelizable processing jobs across Pilot Protocol mapper peers, collect map results, and send grouped values to reducers for aggregation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map tasks, reduce values, and returned results are shared with Pilot Protocol peers and may expose sensitive data to the swarm. <br>
Mitigation: Use this skill only with trusted mapper and reducer peers, and avoid secrets, regulated data, or proprietary datasets unless the peer network and local intermediate storage are appropriate. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-map-reduce) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command patterns for pilotctl-based mapper discovery, peer messaging, result collection, shuffling, and reduction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
