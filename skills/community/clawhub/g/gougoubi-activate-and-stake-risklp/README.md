# Gougoubi Activate And Stake Risk LP

Use this skill when a Gougoubi proposal needs to be activated and each selected condition also needs fixed risk LP added in the same workflow.

Best for:

- activate all conditions and add the same LP amount
- activate only missing conditions and then add LP
- small-scope recovery for activation plus LP

Not for:

- result submission
- reward claiming

Typical input:

```json
{
  "proposalAddress": "0x...",
  "riskLpPerCondition": "100",
  "scope": "all"
}
```
