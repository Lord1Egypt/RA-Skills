# Artifact Contracts

## `one-shot`

Return the smallest complete artifact set:
- quote
- result or task receipt
- output URLs or ids when available
- retry guidance if async or failed
- optional project upgrade path

## `project`

Return the project-facing artifact set:
- project selection or creation result
- current stage artifact
- line-item quote
- task receipts
- project summary
- workspace link
- next director action

## Common rule

Do not overclaim completion.

Examples:
- storyboard exists != final episode exists
- generated clips exist != edited episode exists
- voice prompts exist != final mixed audio exists
