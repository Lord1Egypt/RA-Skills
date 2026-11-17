# Understand the learning request

Read during new-course intake, especially for broad, vague, ambiguous or terse requests. The host agent performs the interpretation; bundled Python checks structure and preserves the agreed brief. No API key for a separate model, keyword classifier or lengthy questionnaire is required.

## Decide what actually needs clarification

Reuse the user's words, prior preferences, examples and supplied materials. A short request is not necessarily unclear: “SQL JOIN for an interview next week” is specific; “AI”, “quant”, or “learn some economics” may leave substantially different courses possible. Do not infer baseline, occupation, examination, preferences or intent from brevity alone.

Consider the subject's possible meanings, desired use, prerequisites and available time. Research unfamiliar terminology with the actual host tools when needed; do not send private work details to search. Present a concise interpretation and useful choices, not hidden chain-of-thought or a large preliminary essay.

- **Specific request:** go straight to a targeted course proposal. Ask only missing information that materially affects it or delivery. Do not pad a narrow course into a survey.
- **Broad topic:** propose a useful introductory direction and a small set of alternatives, with what the learner would be able to do in each. State a recommended direction as a proposal. One concrete choice is usually more helpful than “Please describe your learning objectives in detail.”
- **Ambiguous meaning:** clarify the meaning before researching or building a whole course around one interpretation. E.g. “Agent” might mean AI agents, a software role or another field; context may already settle it.
- **Unrealistic goal:** explain what the available time can establish; propose a bounded achievable outcome and optional later stages. Do not promise expertise, certification or employment.
- **User delegates direction:** choose and explain a reasonable scope, mark uncertain assumptions and offer an editable plan. Unanswered questions do not count as approval; required account/destination information still must be supplied.

For “我想学点 AI”, possible directions include understanding everyday AI tools and limits, building a small AI application, or learning the mathematical foundations. If context suggests practical work use, recommend that direction as a proposal and ask which direction fits. For “想学音乐”, distinguish listening/appreciation, an instrument and composition; do not silently default to Western harmony. For “SQL JOIN 面试，三天”, prioritize join semantics, NULL, row multiplicity, query explanation and short exercises instead of a full database syllabus. These are examples, not universal outlines.

Aim for one compact clarification round when it resolves the direction. Combine ordinary missing settings in a second short exchange when useful. The existing two/three connection-exchange target is separate; authorization and organization approvals have no promised dialogue limit. If a reply changes the interpretation, correct it instead of defending the original plan.

## Build a coherent learning brief

Before drafting the plan, organize the topic into:

1. **Interpretation and boundaries:** what the learner means, what they want it for, what the course includes and excludes. Keep the explicit user goal intact. Separate user statements from suggested defaults and uncertain assumptions.
2. **Observable outcomes:** what they can explain, compare, apply, create or evaluate at the end. “Understand everything about economics” is not an observable outcome. Base expectations on known experience; label unknowns.
3. **Prerequisites and concept relationships:** identify only necessary prior knowledge; distinguish foundations, core ideas and optional branches. Explain dependencies to the learner briefly. Do not assume every subject needs mathematics, coding or a linear historical survey.
4. **Ordered route:** connect foundation → core ideas → worked application → practice → synthesis/review, adapting to the subject. Each module/day should support an outcome and prepare something later. Add missing connective concepts rather than unrelated breadth.
5. **Quality within the budget:** select a few important concepts with explanation, example, comparison/counterexample and practice. Put enrichment beyond the core time budget. Richness means useful connections and depth, not more words or links. Sources must support the actual topic; apply `content.md` for evidence, image and expansion-link requirements.

A plan for a broad request should include a visible short “How I interpreted your goal” passage, scope, assumed starting point, ordered phases and concrete daily outputs. A precise request can use a shorter brief. The user can revise the interpretation before approval. Reuse the brief and prerequisite relationships when authoring later lessons; do not widen or retarget an approved course silently.

## Optional structured record

Keep the relevant original study wording (exclude passwords, tokens, unrelated conversation and private authorization data) in `config.json.learning_brief` when this deeper analysis was useful. All authored fields use the chosen course language; preserve original study wording in `request`. Empty prerequisites, exclusions, assumptions or open questions are valid when unnecessary. Do not fabricate items just to fill a schema.

```json
{
  "request": "学点经济学，想更好理解生活里的选择",
  "interpretation": "以日常决策为入口的经济学基础",
  "outcomes": ["用机会成本比较两个日常选择", "说明一个供需模型的适用条件"],
  "scope": {"included": ["选择与约束", "供需与激励"], "excluded": ["计量推导", "个人投资建议"]},
  "prerequisites": [],
  "sequence": [
    {"topic": "选择与机会成本", "outcome": "比较两种选择的放弃价值"},
    {"topic": "供需与激励", "outcome": "解释价格变化并指出模型限制"},
    {"topic": "综合应用", "outcome": "分析一个生活案例并核对假设"}
  ],
  "assumptions": [{"statement": "先采用不依赖微积分的入门解释", "status": "proposed"}],
  "open_questions": []
}
```

`OMNI brief-check --input /private/brief.json` checks the brief itself before copying it into config. It returns `needs_confirmation` when proposals/questions remain. This is not a consent detector or automatic assessment of semantic quality. Mark an assumption `confirmed` only if supported by the user's actual statements/approval, never merely because the validator accepts it. `init` also checks a supplied `learning_brief`; existing configs without it remain valid. Existing approval hashes protect the complete config, including this record.

For optional learner-started feedback use [assessment](assessment.md). Keep default responses light and preserve explicit practical-training requirements. Do not infer mastery percentages, add quiz reminders or automatically replan an approved curriculum.
