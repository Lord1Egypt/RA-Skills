# Module: Modify The Proposed Method

Use this module when writing `modify_method_guide.md` and `analysis_bundle.json.modify_guide`.

The guide is for a reader who wants to propose a new model or algorithm based on the paper's framework. It is not a parameter-tuning checklist and not a full implementation plan.

## Scope

Focus on method-level extension points:

- where to replace or add the paper's core module;
- where the new module's input comes from;
- where its output is consumed;
- which training loss, aggregation rule, sampler, controller, or inference step must be adjusted;
- which minimal files/functions/classes form the edit surface;
- what invariants must remain true so the original pipeline still runs.

Avoid over-detailing:

- do not list every CLI flag unless it gates the method branch;
- do not recommend only changing learning rate, seed, epoch count, batch size, threshold, or dataset path;
- do not frame ordinary backbone swaps as the main answer unless the paper's contribution is itself a backbone architecture;
- do not prescribe a large refactor when a few core functions define the method boundary.

## Output Shape

Use a compact table:

| Research change idea | Core edit surface | What to preserve | Minimal smoke check |
| --- | --- | --- | --- |

`Core edit surface` should list real files, classes, and functions, but stay at the level a researcher needs before writing code.

## Invariants

Always identify:

- data/interface shape expected by the existing pipeline;
- model output contract;
- loss or metric contract;
- communication/exchange contract if the paper is distributed, federated, multi-agent, graph-based, or systems-oriented;
- experiment entry points that should still run after the method change.
