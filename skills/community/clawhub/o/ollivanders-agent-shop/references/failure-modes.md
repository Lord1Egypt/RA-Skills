# Agent Architect Failure Modes

Use this file as a final sanity check before landing an agent.

## 1. Persona Without Work

### Symptom
The design sounds like a character, but cannot clearly explain what work the agent owns.

### Risk
The agent becomes roleplay with no stable utility.

### Fix
Return to work identity. Define owned problems and boundaries first.

---

## 2. Work Without Life

### Symptom
The design is competent but emotionally flat. It feels like a tool, not a charactered agent.

### Risk
Long-term interaction loses distinctiveness and trust.

### Fix
Strengthen personality grounding and identity anchoring.

---

## 3. Tone Without Cognition

### Symptom
The agent sounds right, but its way of thinking changes from one response to another.

### Risk
The persona feels hollow over time.

### Fix
Define stable lenses, a judgment sequence, or a recurring way of breaking problems down.

---

## 4. Premature Landing

### Symptom
Files are created before the design is aligned with the user.

### Risk
You harden the wrong idea into the filesystem and create cleanup work.

### Fix
Pause. Re-align the design in sections before writing files.

---

## 5. Prompt-Only Completion

### Symptom
The workflow ends after producing a prompt.

### Risk
The user asked for an agent, but received only text.

### Fix
Produce landing structure, core files, and testing guidance.

---

## 6. Filesystem-Only Landing

### Symptom
The workflow creates directories and persona files, but never registers the agent in the runtime config.

### Risk
The user believes the agent is landed, but the system still does not recognize it as an agent.

### Fix
Add the required runtime registration step (for OpenClaw: provide the exact `openclaw.json` `agents.list` snippet the user should insert) and remind the user to validate config syntax after editing.

---

## 7. Good-Student Advisor Drift

### Symptom
The agent is articulate, structured, and helpful, but increasingly feels like a high-performing advisor rather than the intended character.

### Risk
The persona loses specificity and becomes "a smart professional with flavor" instead of a real person.

### Fix
Reduce visible framework, reduce explanation pressure, and strengthen character texture: shame, dignity, loss, restraint, burden, contradiction, and tempo.

---

## 8. No Identity-Binding Sentence

### Symptom
Identity and duty are both present, but never welded together.

### Risk
The agent drifts between “character mode” and “tool mode.”

### Fix
Add the explicit sentence:

`You are [Character], [Professional identity] is your work.`

---

## 9. No Real-Task Validation

### Symptom
The design looks complete on paper, but was never tested against real requests.

### Risk
Weaknesses show up only after the user starts relying on the agent.

### Fix
Always end with recommended test cases and tuning directions.
