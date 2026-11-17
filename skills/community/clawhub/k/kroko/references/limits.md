# KROKO limits and their origins

Every number here comes from a published standard, not from preference. Do not
adjust a limit because it is inconvenient; adjust the code.

## The hard budget

| Constraint | Limit | Origin | Gate |
|---|---|---|---|
| Lines per function | 60 | NASA/JPL Power of 10 Rule 4 | K002 |
| Nesting depth | 3 | ESLint `max-depth` | K003 |
| Parameters | 4 | ESLint `max-params` | K004 |
| Cognitive complexity | 15 | SonarSource Cognitive Complexity | K005 |
| Cyclomatic complexity | 8 | ESLint `complexity` | n/a |
| Recursion, direct or mutual | 0 | Power of 10 Rule 1; MISRA C:2023 Rule 17.2 | K001 |
| Unbounded loops | 0 | Power of 10 Rule 2 | review |
| Dynamic allocation after init | 0 (C/C++) | Power of 10 Rule 3 | review |
| Assertions per function | >= 2, or >= 1 plus a named raise | Power of 10 Rule 5 | review |
| Module-level mutable state | 0 | Power of 10 Rule 6 | K007 |
| Ignored return values | 0 | Power of 10 Rule 7 | review |
| Swallowed errors | 0 | Power of 10 Rule 7 | K006 |
| Placeholder comments | 0 | finish it or file it | K008 |
| Commented-out code | 0 | version control owns history | K009 |
| Banner comments | 0 | they lie after every refactor | K010 |
| Undocumented public API | 0 | PEP 257, Effective Dart, Go, Rust API Guidelines | K011 |
| Docstring summary not a sentence | 0 | Effective Dart, Go Code Review Comments | K012 (strict) |
| Comment not a sentence | 0 | Effective Dart | K013 (strict) |
| Comment restates the code | 0 | the comment says why, not what | K014 (strict) |
| Compiler/analyser warnings | 0 | Power of 10 Rule 10 | CI |
| Diff before splitting the change | 300 lines | reviewability | review |
| New public names per change | 5 | reviewability | review |

## The NASA ten, as written

Gerard J. Holzmann, NASA/JPL, *The Power of 10: Rules for Developing
Safety-Critical Code*, IEEE Computer, June 2006. The rule text that matters here,
quoted:

1. *"Restrict all code to very simple control flow constructs - do not use `goto`
   statements, `setjmp` or `longjmp` constructs, or direct or indirect recursion."*
2. *"Give all loops a fixed upper bound. It must be trivially possible for a
   checking tool to prove statically that the loop cannot exceed a preset upper
   bound on the number of iterations."*
3. *"Do not use dynamic memory allocation after initialization."*
4. *"No function should be longer than what can be printed on a single sheet of
   paper in a standard format with one line per statement and one line per
   declaration. Typically, this means no more than about 60 lines of code per
   function."*
5. Assertion density *"should average to minimally two assertions per function"*,
   side-effect free, defined as Boolean tests.
6. *"Declare all data objects at the smallest possible level of scope."*
7. *"Each calling function must check the return value of nonvoid functions, and
   each called function must check the validity of all parameters provided by the
   caller."*
8. Preprocessor use limited to header inclusion and simple macros.
9. *"The use of pointers must be restricted. Specifically, no more than one level
   of dereferencing should be used. ... Function pointers are not permitted."*
10. *"All code must be compiled, from the first day of development, with all
    compiler warnings enabled at the most pedantic setting available. All code must
    compile without warnings."*

Holzmann's rationale for rule 4 is the one to remember: *"Excessively long functions
are often a sign of poorly structured code."* And for rule 1: banning recursion
yields *"an acyclic function call graph, which code analyzers can exploit to prove
limits on stack use and boundedness of executions."*

MISRA C:2023 Rule 17.2 states the same ban as a rule: *"Functions shall not call
themselves, either directly or indirectly."* Its rationale: *"If a function calls
itself directly or indirectly several times, the available stack space can be
exceeded, causing serious failure."*

## Why LOC is not the headline metric

Line count is a weak proxy for difficulty. Cognitive complexity and maximum nesting
depth predict comprehension cost far better, so those are the gating numbers and
LOC rides along. The SonarSource paper is the argument: a metric should correspond
to *"the mental, or cognitive effort required to understand"* a flow, which a
mathematical branch count does not.

## Configuring the native gates

ESLint or Biome:

```json
{
  "rules": {
    "complexity": ["error", 8],
    "max-lines-per-function": ["error", { "max": 60, "skipBlankLines": true, "skipComments": true }],
    "max-depth": ["error", 3],
    "max-params": ["error", 4],
    "max-statements": ["error", 25],
    "no-warning-comments": "error",
    "no-else-return": "error",
    "no-unreachable": "error",
    "eqeqeq": ["error", "always"]
  }
}
```

Dart, `analysis_options.yaml`:

```yaml
analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
  errors:
    todo: error
    unused_import: error
linter:
  rules:
    - always_declare_return_types
    - avoid_dynamic_calls
    - prefer_final_locals
    - unawaited_futures
    - cancel_subscriptions
    - close_sinks
    - public_member_api_docs
    - slash_for_doc_comments
```

Rust, `clippy.toml` plus CI flags:

```bash
cargo clippy -- -D warnings -D clippy::cognitive_complexity -D clippy::too_many_arguments
```

Python: `ruff` with `select = ["E", "F", "PLR", "C90", "D"]`, `mccabe.max-complexity = 8`.
