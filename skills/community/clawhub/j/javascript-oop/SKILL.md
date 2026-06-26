---
name: JavaScript OOP
description: >
  Use this skill for JavaScript implementation, refactoring, debugging, or review when
  you need strong Java-style OOP conventions, ES2025+ standard features, targeted rule
  files, and explicit controller, service, repository, policy, use-case, and port
  boundaries.
---

# JavaScript Skill

## Scope

Use this skill for JavaScript or Node/browser code changes and reviews.

## Precedence

- Follow explicit user instructions first.
- Follow repository conventions, formatter, linter, and `AGENTS.md` before generic
  defaults in these rules.
- Use the rule files as focused guidance and review checklists, not as a reason to fight
  established local patterns.

## ES2025+ Baseline

- Assume a modern runtime such as Node 22+ or evergreen engines.
- Prefer standardized Stage 4 ECMAScript features only.
- Prefer newer standard helpers when they reduce boilerplate.
- Treat 2026-finished APIs as conditional on target runtime support.
- Do not default to Stage 3 syntax such as `using`, `await using`, or decorators.

## Java-Style OOP Baseline

- Treat classes as the default home for stateful business behavior.
- Limit free functions to small pure transforms, validators, calculators, and mappers.
- Treat controllers, services, repositories, policies, use cases, ports, and
  specifications as first-class architectural concepts.
- Treat stateful browser behavior as interface-layer controller code rather than loose
  script modules.
- Prefer parameter objects, `#private` fields, and explicit value objects over ad hoc
  argument lists and mutable shapes.
- Prefer intent methods, domain errors, and stable event payload DTOs over generic
  property mutation.
- Keep composition-root wiring explicit and centralized, with dependencies flowing
  inward.

## Operating Model

1. Start with this file.
2. Load the baseline rules for almost every task:
   - [References](rules/references.md)
   - [Variables](rules/variables.md)
   - [Functions](rules/functions.md)
   - [Modules](rules/modules.md)
   - [Naming Conventions](rules/naming-conventions.md)
   - [SOLID and Structure](rules/solid-and-structure.md)
3. Load only the rule groups that match the task.
4. Use each file's local `Example` and `End Check`, then finish with the global
   checklist at the bottom of this file.

## Rule Map

### Syntax and formatting

- [Strings](rules/strings.md)
- [Comments](rules/comments.md)
- [Formatting](rules/formatting.md)
- [Control Flow](rules/control-flow.md)
- [Hoisting](rules/hoisting.md)

### Objects, arrays, and data shape

- [Objects](rules/objects.md)
- [Destructuring](rules/destructuring.md)
- [Accessors](rules/accessors.md)
- [Collections](rules/collections.md)

### Functions, classes, and modules

- [Arrow Functions](rules/arrow-functions.md)
- [Classes and Constructors](rules/classes-and-constructors.md)
- [Events](rules/events.md)
- [Standard Library](rules/standard-library.md)
- [UI Controllers](rules/ui-controllers.md)

### Equality, conversion, and modern syntax

- [Value Semantics](rules/value-semantics.md)

### Async and failure handling

- [Async](rules/async.md)
- [Error Handling](rules/error-handling.md)

## Task-Based Loading

Load these additional files when the task has these traits:

- Data reshaping or DTO work: `objects`, `destructuring`, `collections`,
  `value-semantics`.
- Domain and service design or refactors: `classes-and-constructors`, `functions`,
  `accessors`, `modules`, `error-handling`, `naming-conventions`,
  `solid-and-structure`.
- Browser widgets, DOM bindings, and event-driven UI controllers: `ui-controllers`,
  `classes-and-constructors`, `modules`, `naming-conventions`, `comments`.
- Async flows, I/O, retries, timers, concurrency, or background work: `async`,
  `error-handling`, `standard-library`.
- Nullability, defaults, parsing, regex, or binary conversion: `value-semantics`,
  `standard-library`.
- Formatting, documentation, or readability cleanup: `formatting`, `strings`,
  `comments`, `control-flow`.
- Code review: start from the changed lines, then load only the rules implicated by the
  diff plus the end-check categories below.

## Important Distinctions

- `value-semantics.md` owns equality, conversions, defaults, truthiness, and optional
  chaining.
- `async.md` owns `Promise.try()`, `Array.fromAsync()`, and async flow rules.
- `collections.md` owns iterator helpers, Set algebra, copy depth, and change-by-copy
  collections inside service and repository workflows.
- `classes-and-constructors.md` owns encapsulation, constructor discipline, and factory
  guidance.
- `ui-controllers.md` owns DOM lifecycle, event binding, teardown, and interface-layer
  controller guidance.
- `functions.md` owns parameter-object APIs and the boundary between tiny pure helpers
  and named service or use-case methods.
- `objects.md` owns value-object and DTO boundary guidance.
- `error-handling.md` owns domain-error policy.
- `standard-library.md` owns concrete ES2025+ helper APIs such as `RegExp.escape()`,
  `Error.isError()`, and binary conversion helpers inside object-oriented designs.
- `solid-and-structure.md` is the only file that names SRP, OCP, LSP, ISP, DIP, and the
  composition-root and application layering model.

## End Check

- Verify repository conventions override generic defaults when they differ.
- Verify chosen ES2025+ features are standardized and fit target runtime support.
- Verify behavior lives on objects, services, use cases, or controllers rather than
  scattered utilities.
- Verify naming, encapsulation, module boundaries, value objects, and DTO boundaries stay
  explicit.
- Verify ports, adapters, and layer placement are clear.
- Verify browser controllers keep lifecycle, DOM boundaries, and cleanup explicit.
- Verify async work, error handling, and collection mutation choices are intentional.
- Verify comments and formatting remain consistent and low-noise.
