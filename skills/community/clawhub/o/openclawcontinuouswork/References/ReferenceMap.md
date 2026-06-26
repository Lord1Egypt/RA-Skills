# Reference Map

Auto-generated module index. New `References/*.md` files are included after running `python Scripts/BuildReferenceMap.py`.
Ordering can be configured by `References/ModuleOrder.json`.

## Canonical Flow
1. Read `GeneralRules.md` for baseline continuous execution behavior.
2. Apply `ContinuousExecutionDirective.md` when user enforces strong continuous-work constraints.
3. For optimization tasks, apply `OptimizationRules.md` + `OptimizationDirective.md`.
4. Use `OptimizationChecklist.md` during execution.
5. Use `ReportingTemplate.md` for updates.
6. Use `AcceptanceTemplate.md` + `QualityRubric.md` for closure.

## Available Modules
- `GeneralRules.md`
- `ContinuousExecutionDirective.md`
- `OptimizationRules.md`
- `OptimizationDirective.md`
- `OptimizationChecklist.md`
- `ReportingTemplate.md`
- `AcceptanceTemplate.md`
- `QualityRubric.md`
- `ModuleSystem.md`
- `ModuleOrderReport.md`
- `ModuleTemplate.md`

## Extending
- Add a new `.md` file into `References/`.
- (Optional) edit `References/ModuleOrder.json` for load priority.
- Run `python Scripts/BuildReferenceMap.py`.
- Commit and push.
