# Web App Configuration Import Contract

This reference defines field names and execution semantics. For generation defaults, example selection, validation, and delivery instructions, see [SKILL.md](../SKILL.md). For a complete configuration, see the [two-plan example](../assets/comparison.example.json).

## Template wrapper

| Path | Generation rules |
| --- | --- |
| `type` | Fixed string `"token-lab-template"` |
| `version` | Fixed number `1`; template format version |
| `name` | String of 1–100 characters after trimming whitespace; shown on the template card and in details |
| `description` | String of at most 1,000 characters describing the comparison, use case, or assumptions. Supply a nonempty description for new templates. The importer also accepts empty or omitted values; the app then displays a "No template description" placeholder |
| `config` | Complete multi-plan configuration described below |

Do not put `version` inside the inner `config` object. Plain configurations can be imported through the same UI: the template name is inferred from the filename, and the introduction uses the top-level `description` if present (otherwise empty). Determine which format an existing file uses before editing it; do not insert template metadata into a plain configuration.

## Top-level config and plans

All paths below are relative to the template's `config` object, or to the file root for plain configurations.

| Path | Generation rules |
| --- | --- |
| `unit` | Fixed string `"K"`; all token lengths are in thousands of tokens |
| `plans` | At most 8 entries; comparisons typically contain at least 2 |
| `baselineId` | The `id` of an existing plan; use `null` only when the plans array is empty |
| `baselineMode` | `"manual"` locks the baseline to the specified plan. `"auto"` selects the plan with the highest total cost after simulation, breaking ties by taking the first; a valid `baselineId` is still required in auto mode |
| `globalSimulation` | Shared numeric parameters with the same field names as `simulation`. `initialContext` is nested and `variables` contains custom variables. Also supports `estimateDuration` and `removedFields`; do not put `flow` or `model` here |
| `globalSimulation.estimateDuration` | Optional boolean; defaults to `true`. `false` hides the entire duration column and disables duration calculations for every plan |
| `globalSimulation.removedFields` | Optional array of deleted built-in numeric parameter paths. Must be unique and contain only built-in numeric fields; the simulator uses system defaults for deleted values. Preserve this field when editing an existing configuration; do not delete parameters arbitrarily in new experiments |
| `globalModelId` | Prefer `"custom"` and a complete `globalModel` to avoid dependencies on built-in model IDs that may change |
| `globalModel` | `{ "model": { ... }, "pricing": { ... } }`; inherited by plans with `useGlobal.model` set to `true` |
| `plans[i].id` | Unique, nonempty string; stable IDs such as `"plan-lazy"` are suitable |
| `plans[i].name` | 1–60 characters after trimming whitespace; names must be unique |
| `plans[i].description` | Optional string of at most 1,000 characters before interpolation; may be empty. Explain the strategy, purpose, use case, or key assumptions. Supports `{{variableName}}` references described below |
| `plans[i].estimateDuration` | Optional boolean; defaults to `true`. `false` disables duration calculation for this plan only and displays "—" in its cell, without hiding the global column or affecting other plans |
| `plans[i].color` | Must be selected from the palette below |
| `plans[i].simulation` | Full parameters from the next table plus `flow`; retain complete local values even when inheriting globals |
| `plans[i].model` / `.pricing` | Full model and pricing source metadata, even when the global model is inherited |
| `plans[i].useGlobal` | Optional boolean map with built-in parameter paths, `"model"`, or keys such as `"variables.variableName"` |

Only these plan fields are supported: `id`, `name`, `description`, `color`, `simulation`, `model`, `pricing`, `useGlobal`, and `estimateDuration`. Put plan explanations in `description`, not invented fields. Never include simulation results in an import configuration.

Choose colors in sequence from this palette:

```json
["#5869d9", "#d99b61", "#449b87", "#9a76c3", "#5c9ebd", "#c77891", "#9b9b4d", "#768397"]
```

## Simulation parameters

Explicitly include every field below, even the compression threshold for the mode not currently in use. Example values illustrate the format only. Follow the generation defaults in SKILL.md unless the user or an existing configuration specifies otherwise.

| Field | Example | Units and constraints |
| --- | --- | --- |
| `initialContext.agentPromptToken` | 4 | K tokens; nested field |
| `turnTotalCount` | 100 | User-message turns; integer from 1 to 1,000 |
| `skillsTotalCount` | 30 | Nonnegative safe integer |
| `toolsTotalCount` | 100 | Nonnegative safe integer |
| `turnAvgSkillsCount` | 0.33 | Nonnegative number, fractions allowed; no greater than the total number of Skills |
| `turnAvgToolsCount` | 1.5 | Nonnegative number, fractions allowed; no greater than the total number of Tools |
| `expectedPrefixCacheHitRate` | 0.9 | Between 0 and 1; applies only to identical prefixes recognized by the engine |
| `skillIndexToken` | 0.1 | Per-Skill index size in K tokens |
| `toolsIndexToken` | 0.013 | Per-Tool index size in K tokens |
| `toolSchemaToken` | 0.51 | Per-Tool schema size in K tokens |
| `userMessageToken` | 0.1 | Per-turn user message in K tokens |
| `skillDetailToken` | 3 | Per-Skill content in K tokens |
| `toolResultToken` | 3 | Per-tool result in K tokens |
| `readSkillPlanToken` | 0.1 | Model output for planning Skill reads, in K tokens |
| `schemaPlanToken` | 0.1 | Model output for planning schema discovery, in K tokens |
| `callToolsPlanToken` | 0.3 | Model output for planning tool calls, in K tokens |
| `agentResult` | 1 | Final agent response model output, in K tokens; field name does not end in `Token` |
| `compressionThresholdType` | `"TOKEN"` | Default is TOKEN; use TURN if explicitly requested |
| `compressionThresholdTurnCount` | 10 | Positive safe integer; TURN threshold must exceed the number of retained turns |
| `compressionThresholdToken` | 100 | K tokens; default is 100K; must be greater than zero in TOKEN mode |
| `compressionKeepTurns` | 2 | Nonnegative safe integer |
| `compressionTargetToken` | 4 | Compression summary output size in nonnegative K tokens; not the total post-compression context |
| `variables` | `{}` | Custom-variable map; may be empty |
| `flow` | See below | Explicit `initial` and `turn` arrays |

Every numeric value must be finite, and every token length must be nonnegative. JSON does not allow NaN or Infinity.

Built-in parameters inherit from globals **only** when `useGlobal[field] === true`; a missing or false flag uses the local plan value. Use flattened keys for nested paths such as `"initialContext.agentPromptToken"`. Flows always belong to their plans; `useGlobal.flow` is unsupported.

Duration settings are not part of `simulation` or `useGlobal`. Use the two-level switches defined above.

By default, custom variables inherit global values, even when a local variable has the same name. Set `useGlobal["variables.retrievalToken"]: false` to retain the local value. After merging global and local variables, each effective plan may contain at most 100 custom variables.

## Variables in plan descriptions

`plans[i].description` supports `{{variableName}}` interpolation. Names match configuration parameter names used by step formulas, but descriptions **only substitute numeric values**; they do not evaluate expressions. For example:

```json
{
  "description": "Compare {{toolsTotalCount}} tools, averaging {{turnAvgToolsCount}} per turn; the agent prompt is {{initialContext.agentPromptToken}}K tokens."
}
```

This snippet belongs at the plan top level. With the values from the full example above, it displays: "Compare 100 tools, averaging 1.5 per turn; the agent prompt is 4K tokens." For custom variables, reference the name directly (for example, `{{retrievalToken}}`), having first defined it under `globalSimulation.variables` or `plans[i].simulation.variables`. Do **not** use `{{variables.retrievalToken}}`.

- You may reference numeric fields from the simulation table, including dotted paths such as `initialContext.agentPromptToken`, and custom variables. Whitespace is permitted in `{{ toolsTotalCount }}`; names are case-sensitive.
- Substitution uses the plan's effective values, respecting built-in `useGlobal` flags and the default global-inheritance behavior of custom variables. Updates to global parameters, local overrides, or inherited values propagate to the plan list, detail cards, and template preview.
- Numeric values render without formatting; zero is valid. Token lengths remain in K, so write units explicitly. `{{expectedPrefixCacheHitRate}}` displays `0.9` for a value of 0.9; do not append `%` and imply 90%. Instead write "cache hit rate {{expectedPrefixCacheHitRate}} (0–1)". Percentage formatting directives are unsupported.
- Expressions such as `{{toolsTotalCount * toolSchemaToken}}`, Math functions, and format filters are unsupported. Descriptions cannot reference `turnIndex`, `llmIndex`, model prices, `compressionThresholdType`, duration switches, step fields, or simulation results. To display a computed constant, store it explicitly in a custom variable; it will not automatically update when other variables change.
- Unknown variables, variables without valid numeric values, and built-in fields deleted via `removedFields` remain as uninterpolated placeholders. The editor warns about unknown references, but import itself does not fail. Unsupported expressions likewise remain verbatim. New descriptions must not rely on that behavior; use resolvable references.
- Raw description length, including braces and variable names, must not exceed 1,000 characters. Import, export, and copy preserve the raw text rather than writing preview values into JSON. Interpolation applies only to plan descriptions, not to the template-level `description` or plan names.
- The web editor offers "Insert variable" for currently available parameters and "Description preview". A custom variable cannot be deleted while it remains referenced by a plan description. Change the reference first; plan-specific overrides are not affected by deletion of the global variable.

## Models and pricing sources

```json
{
  "model": {
    "name": "Demo Model (Illustrative Pricing)",
    "currency": "$",
    "inputCachedPrice": 0.2,
    "inputNotCachedPrice": 2,
    "outputPrice": 8
  },
  "pricing": {
    "id": "custom",
    "label": "Illustrative assumptions, not verified prices",
    "source": "",
    "date": "",
    "note": "Example format only; replace with the target model's USD prices per million tokens."
  }
}
```

This example shows the format, **not verified pricing**. All three rates are nonnegative USD per million tokens; automatic currency conversion is unsupported. The `source` may contain a link to official pricing and `date` the actual verification date; leave them blank when unknown. When changing rates, set `pricing.id` to `"custom"` so the configuration is not mistaken for an unmodified preset.

`pricing.contextWindow` is optional and expressed in **raw tokens**, not K tokens. `pricing.tier` is optional, with a shape like `{ "input_tokens_gt": 0, "input_tokens_lte": 128000 }`, also using raw tokens. These are provenance metadata; they do not automatically select a pricing tier or enforce the context window. For experiments crossing pricing tiers, choose suitable rates and document assumptions.

## Execution flow and formulas

```json
{
  "initial": [
    { "type": "action", "text": "agent prompt", "token": "initialContext.agentPromptToken" }
  ],
  "turn": [
    { "type": "action", "text": "user_message", "token": "userMessageToken", "durationSeconds": 0 },
    { "type": "llm", "text": "retrieval_plan", "token": 0.2, "durationSeconds": 1.8 },
    { "type": "action", "text": "retrieval_result", "token": "retrievalToken", "durationSeconds": 0.3 },
    { "type": "llm", "text": "agent_result", "token": "agentResult", "durationSeconds": 1.8 }
  ]
}
```

When using `retrievalToken` in this snippet, also define that variable as described below. The `initial` array permits `action` nodes only; `turn` allows `action` or `llm`. Explicitly include both arrays, even when empty (an empty array performs no steps for that phase). Each step supports only:

| Field | Rules |
| --- | --- |
| `type` | `"action"` or `"llm"` |
| `text` | Nonempty step name, also used for cost attribution; same-name steps are aggregated |
| `token` | Nonnegative finite number in K tokens or a formula string. Numeric strings such as `"0.5"` are also parsed as formulas |
| `enabled` | Optional boolean; enabled by default |
| `trigger` | Optional and permitted only in `turn`; omitted means run on every turn |
| `durationSeconds` | Optional nonnegative finite number in seconds. Defaults are 0.3 for `action` and 1.8 for `llm`; explicit 0 is valid. Strings, `null`, and formulas are invalid. The field may also be stored in `initial` |

Use the English `text` attribution keys from the complete templates when possible; the web app knows how to display them. Custom names also work.

- `action` nodes append context only. `llm` nodes send the current context to the model; their `token` value describes **output**, which is automatically appended to the history. Do not put input size in `llm.token` or append the model output again.
- The execution flow determines what is actually loaded. Changing `toolsTotalCount` or `skillDetailToken` alone does not automatically append any content. The obsolete `toolsMode` field is unsupported. See the scenarios in SKILL.md for strategy examples.
- The engine handles caching and compression. Check compression at the end of each turn, including the last; do not add a manual compression-call node. `expectedPrefixCacheHitRate: 0.9` denotes 90%, whereas `trigger.value: 30` denotes 30%; these parameters use different scales.

### Duration switches and estimation semantics

Explicitly include both boolean duration switches for new files and preserve existing values when editing. Missing switches default to enabled. Do not substitute `"false"`, `0`, `1`, or `null` for a boolean.

| Global `estimateDuration` | Plan `estimateDuration` | Calculation and UI behavior |
| --- | --- | --- |
| `true` / omitted | `true` / omitted | Estimate this plan's duration and show "Average TTFT per turn" |
| `true` / omitted | `false` | Show "—" for this plan's duration, keep the column, and leave other plans unchanged |
| `false` | Any valid value / omitted | Disable duration estimation for every plan and hide the entire column; preserve plan-level switches and step durations |

Even if every plan has `estimateDuration: false`, the duration column remains visible when the global switch is enabled. These switches do not change token or cost calculations. Invalid step durations still fail import validation even when duration calculations are disabled.

Although the web app labels the metric "Average TTFT per turn", its actual calculation is a **serial sum of estimated durations**:

```text
Turn duration = sum(durationSeconds of executed turn steps) + (compression calls during this turn × 1.8 seconds)
Average duration per turn = sum(turn durations) ÷ total user turns
```

- Count only enabled and triggered `turn` steps. One-time loading of initial context is excluded, even when a duration is supplied.
- Count each LLM step once; automatically appended model outputs do not add another duration.
- Count each tool or context step once per execution, regardless of token count or `turnAvgToolsCount`. If its duration already represents an entire batch of tool execution, supply the total batch duration directly.
- A compression request has a fixed 1.8-second duration and is charged to the triggering user turn, including the last. Do not insert manual compression steps.
- This metric is **not a measured time-to-first-token latency**. The simulator does not derive elapsed time from model speed, token lengths, or parallel execution. Label default or estimated durations as assumptions.
- Simulation reports contain `averageTurnDurationSeconds` and `rounds[i].durationSeconds`. When estimation is disabled, both are `null`, not zero. An empty flow without compression yields zero; when there are no user turns the average is `null` (although web configurations require at least one). These are simulation outputs and must not be saved in import JSON.

### Values available to formulas

Formulas may reference any numeric parameter in the simulation table, custom variables, and `turnIndex` (zero-based user-turn index) or `llmIndex` (number of model calls already executed earlier in the current turn, starting at zero). Both indices are zero during initialization. Compression does not count as a user turn; disabled or untriggered LLM steps do not increment `llmIndex`.

Formulas cannot access other step-output objects, accumulated context, model pricing, other plans, `compressionThresholdType`, `description`, `estimateDuration`, or `durationSeconds`. Put any required constants in custom variables. Parameter expressions are not recursively resolved through other formulas.

Operators include `+ - * / % **`, parentheses, comparisons, `! && || ??`, and ternaries. Supported Math functions: `min`, `max`, `ceil`, `floor`, `round`, `trunc`, `abs`, `sqrt`, `pow`, `log`, `log2`, `log10`, and `exp`. Supported constants: `Math.PI` and `Math.E`. Call functions as `Math.min(...)`, not `min(...)`.

```text
toolResultToken * turnAvgToolsCount
Math.min(toolResultToken * turnAvgToolsCount, 10)
turnIndex === 0 ? toolSchemaToken * turnAvgToolsCount : 0
llmIndex === 0 ? callToolsPlanToken : agentResult
```

A formula is limited to 2,000 characters, 256 evaluation nodes, and 32 nesting levels. Assignments, function definitions, randomness, arbitrary object access, and code execution are unsupported. Its result must be nonnegative and finite on **every executed turn**: for example, `1 / turnIndex` fails on the first turn. Do not assume later turns are safe based on a first-turn preview.

### Custom variables

Define them under `globalSimulation.variables` or `plans[i].simulation.variables`:

```json
{ "retrievalToken": { "label": "Retrieved result size (K)", "value": 2.5 } }
```

Names must match `^[A-Za-z_][A-Za-z0-9_]{0,63}$` and must not conflict with built-in fields, runtime variables, `Math`, `model`, `flow`, `variables`, JavaScript keywords, `__proto__`, `constructor`, or other reserved names. Each `label` is 1–60 characters, and each `value` must be finite and nonnegative. Variable objects only allow `label` and `value`. Indicate units in the label or in assumptions outside the configuration.

### Triggers

- `{ "type": "interval", "value": 3 }` executes on turns 1, 4, 7, and so on, starting with the first turn. `value` must be a positive safe integer. If the interval exceeds the session length, the first turn still runs once. Compression does not reset this counter.
- `{ "type": "probability", "value": 30 }` triggers with a 30% probability per turn. `value` must be finite and between 0 and 100. Each step's sample is determined separately by turn and step position; observed frequency can differ from the configured rate.
- A `trigger` contains only `type` and `value`; `initial` steps cannot have triggers.
- A planning LLM step that does not trigger does **not** automatically suppress a following tool-result step. For correlated behavior, give related steps the same interval trigger or use a deterministic `turnIndex` expression when appropriate. Two separate probability triggers with the same percentage are **not** correlated events.
- An LLM step with `token: 0` still sends a model request and incurs input charges. To skip the request, use `enabled` or `trigger`.

Only the current configuration schema is supported. The importer does not automatically supply missing global fields; include `globalSimulation` and `globalModelId`. Token specifications support only numbers or formula strings, not arrays of parameter names.
