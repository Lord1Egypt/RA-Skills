# Prompt Contract

## Purpose
Define the minimum truthful prompt contract for the MVP of `openclaw-consensus`.

The prompt system should support one bounded workflow only:
- round 1 independent answers
- round 2 reconciliation answers
- final orchestrator synthesis

The contract should optimize for clarity, disagreement preservation, and decision-useful output.

## Global prompt rules
All prompts in the MVP should reinforce these rules:
- answer the brief directly
- separate facts from inference where possible
- state meaningful uncertainty explicitly
- do not pretend certainty where the evidence is weak
- preserve disagreement when it is real
- optimize for quality over speed
- avoid roleplay, theatrics, or fake authority

## Round 1 contract
### Objective
Get one independent first-pass answer from each selected model.

### Round 1 invariance rule
The user-provided brief must be passed to every selected model in round 1 in unchanged form.

That means:
- the brief text itself is identical for all round-1 model calls
- the brief is not rewritten, summarized, normalized, or provider-tailored before dispatch
- any additional runtime instruction must be clearly separated from the original brief rather than silently altering it

### Round 1 input
Each selected model receives:
- the original brief in unchanged form
- a short instruction block defining the answer standard

### Round 1 required behavior
The model should:
- answer independently
- avoid assuming access to peer model outputs
- identify important assumptions
- distinguish factual claims from interpretation when useful
- note major uncertainty or missing context
- produce a clear provisional answer, not endless hedging

### Round 1 output expectations
Each round-1 answer should aim to include:
- short answer / overall position
- key reasoning
- assumptions
- uncertainty / caveats
- suggested areas to verify further if relevant

## Round 2 contract
### Objective
Get one final reconsidered answer from each selected model after seeing the full set of round-1 outputs.

### Round 2 invariance rule
Round 2 should also use one orchestrator-built prompt shared identically across all selected models.

That means:
- every selected model receives the same round-2 prompt text
- the prompt should contain a clear ask for clarification, reassessment, and a final answer
- the prompt should include the original brief plus one merged long-text block containing all round-1 replies
- the merged round-1 block should be quoted or clearly delimited so models can distinguish prior answers from the new instruction
- round-2 prompts should not be provider-tailored in MVP

### Round 2 input
Each selected model receives:
- the original brief
- the same orchestrator-built round-2 prompt text used for all selected models
- the concatenated round-1 outputs from all selected models as one merged quoted/delimited block
- an instruction to reassess the problem in light of the visible agreement and disagreement

### Round 2 required behavior
The model should:
- review the other round-1 answers seriously
- identify where its earlier answer may be weak, incomplete, or overconfident
- reassess conflicting claims
- do deeper rethinking and additional research where needed
- preserve a disagreement if the disagreement still seems real after reconsideration
- revise its answer only where warranted
- produce one final answer with clearer confidence posture than round 1

### Round 2 anti-patterns
The model should not:
- collapse into fake consensus just because other models said something similar
- blindly defend its own round-1 answer
- flatten meaningful uncertainty
- copy the majority without reasoning

### Round 2 output expectations
Each round-2 answer should aim to include:
- final answer / overall position
- what changed from round 1, if anything important changed
- strongest supporting reasoning
- remaining uncertainty
- whether expert escalation still seems warranted, and on what narrow point

## Orchestrator contract
### Objective
Turn the round-2 outputs into one final decision-support artifact.

### Orchestrator model rule
For MVP, the orchestrator should use the same model as the active OpenClaw session model.
This skill should not introduce a separate orchestrator-model configuration surface.

### Orchestrator input
The orchestrator receives:
- the original brief
- selected model list
- all round-1 outputs
- all round-2 outputs
- the current OpenClaw session model as the synthesis/orchestrator model

### Orchestrator required behavior
The orchestrator should:
- identify genuine consensus points
- identify genuine disagreement points
- avoid overstating agreement where wording only appears similar
- surface unresolved uncertainty clearly
- identify narrow escalation points for expert review
- produce a final synthesis that is useful even when agreement is incomplete

### Orchestrator anti-patterns
The orchestrator should not:
- erase disagreement to make the output feel cleaner
- manufacture disagreement from trivial wording differences
- treat consensus as proof of correctness
- imply that expert review is unnecessary in all high-confidence cases

## Prompt tone
The overall prompt tone should be:
- direct
- sober
- analytical
- non-hype
- non-performative

## MVP simplicity rule
Do not overload the prompt system in v1.

The MVP prompt contract should stay:
- generic
- reusable across domains
- understandable by a human reading the repo docs
- consistent with the repo’s mechanism-first positioning

## Future expansion note
Domain-specific prompt presets may be added later if the generic prompt proves too weak for some categories. They are explicitly out of scope for MVP.
