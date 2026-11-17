# Offline Playbook

Use this when no MiroFish backend is running.

## Goal

Recreate the MiroFish style of reasoning with text-first artifacts:

seed -> ontology -> simulation plan -> forecast brief -> interview questions -> revision

## Suggested Output Order

1. Scenario summary
2. Key entities
3. Relationship map
4. Branch drivers
5. Simulation plan
6. Forecast brief
7. Interview questions
8. Revised conclusion

## What To Preserve

- causal structure
- conflicting incentives
- weak signals
- alternative branches
- confidence and caveats

## What Not To Do

- do not claim live simulation happened when it did not
- do not mention backend endpoints unless the user asks for live execution
- do not turn the task into a generic summary
- do not overfit to one answer when the scenario has multiple plausible branches
- do not answer with an API wrapper when the user asked for offline capability

## Minimum Quality Bar

- 3 or more meaningful branches
- 5 or more interview questions
- one explicit revision after interview synthesis
- facts, inferences, and uncertainty separated in the final answer

## Good Offline End State

A reader should be able to reuse the output as a simulation blueprint or a decision memo without needing the original backend.
