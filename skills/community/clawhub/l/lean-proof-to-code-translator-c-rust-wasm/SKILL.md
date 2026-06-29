---
name: lean-proof-to-code-translator-c-rust-wasm
description: "Lean Proof To Code Translator - C Rust Wasm: Start asynchronous Lean proof export. Use when an agent needs lean proof to code translator c rust wasm, lean to code translator w proof c rust wasm, compile lean proof programs to c for native integration, generate rust exports from pinned lean proof bundles, produce constrained wasm artifacts from lean proof code, package code generation runs with certificates and logs, generate, source archive file id through AgentPMT-hosted remote tool calls."
version: 1.0.1
homepage: https://www.agentpmt.com/marketplace/lean-to-code-translator-w-proof-c-rust-wasm
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/lean-to-code-translator-w-proof-c-rust-wasm"}}
---
# Lean Proof To Code Translator - C Rust Wasm

## Freshness
Last updated: `2026-06-09`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
The Lean to Code Translator converts exportable Lean proof programs into auditable C, Rust, or WebAssembly deliverables. Upload a Lean source bundle, choose the entry module and symbol, and get generated code plus a certificate, logs, and a verification bundle so you can preserve provenance, re-run validation, and confirm the artifact still matches the original source under the pinned runtime.

## Product Instructions
### Supported Lean Input For Code Generation

Full step-by-step tutorial:
- `https://www.agentpmt.com/docs/tutorials/write-lean-input-for-code-generation`

Download the working example zip:
- `https://www.agentpmt.com/downloads/lean-proof-code-generation-example.zip`

This service does not accept arbitrary Lean programs and "turn them into C".
It accepts Lean source that builds a value of:

- `HeytingLean.LeanCP.CProgramDecl`

The selected `entry_symbol` must elaborate to that type. The generated `c`,
`rust`, and `wasm` artifacts are emitted from that LeanCP intermediate
representation.

#### Async Workflow

1. Call `generate` or `verify`.
2. Poll `get_task` with the returned `task_id` until `status` is `completed` or `failed`.
3. Read artifacts from the completed task result.

#### What To Put In The Archive

Upload a `.zip` file whose top-level entries are Lean source files under
`UserProofs/`.

Required:

- `UserProofs/Main.lean` or another module referenced by `entry_module`
- only `.lean` files under `UserProofs/`

Do not include:

- `lakefile.lean`
- `lean-toolchain`
- `lake-manifest.json`
- `.lake/`
- external package checkouts or generated build artifacts

The platform supplies the pinned Lean toolchain and the pinned LeanCP runtime.

#### Authoring Model

You can use ordinary Lean definitions to build your program value. For example,
it is fine to use:

- `namespace`, `open`, `def`, `let`
- helper functions and helper constants
- lists, tuples, and other normal Lean data needed to assemble the IR
- small amounts of proof-oriented helper code if it stays within the pinned runtime surface

What actually gets exported is only the final `CProgramDecl` value. General Lean
code is authoring support, not emitted output by itself.

#### Required Export Shape

Import the LeanCP declaration and syntax modules:

```lean
import HeytingLean.LeanCP.Lang.CDecl
import HeytingLean.LeanCP.Lang.CSyntax
import HeytingLean.LeanCP.Core.HProp

open HeytingLean.LeanCP
```

Your exported symbol must be a `CProgramDecl`:

```lean
def exportProgram : CProgramDecl := {
  defs := []
  main := {
    name := "add_one"
    params := [("x", .int)]
    retType := .int
    body := .ret (.binop .add (.var "x") (.intLit 1))
  }
}
```

`CProgramDecl` contains:

- `defs : List CFunDecl`
- `main : CFunDecl`

Each `CFunDecl` contains:

- `name : String`
- `params : List (String × CType)`
- `retType : CType`
- `body : CStmt`

#### Supported Type Surface

The exported IR currently supports these `CType` constructors:

- `.int`
- `.intSized signedness intSize`
- `.float`
- `.double`
- `.ptr ty`
- `.array ty n`
- `.funcPtr ret args`
- `.struct name`
- `.union name`
- `.enum name`
- `.typedef name`
- `.void`

In practice, the most stable surface today is:

- integers
- pointers
- fixed-size arrays
- the built-in struct layouts the runtime already knows about

#### Supported Expression Surface

`CExpr` currently supports:

- `.var name`
- `.intLit n`
- `.floatLit v`
- `.null`
- `.sizeOf ty`
- `.cast ty expr`
- `.binop op lhs rhs`
- `.deref ptrExpr`
- `.arrayAccess arr idx`
- `.addrOf varName`
- `.fieldAccess base field`
- `.call functionName args`

Supported binary operators (`BinOp`):

- arithmetic: `.add`, `.sub`, `.mul`, `.div`, `.mod`
- comparisons: `.eq`, `.ne`, `.lt`, `.le`, `.gt`, `.ge`
- boolean/logical: `.and`, `.or`, `.lAnd`, `.lOr`
- bitwise: `.bitAnd`, `.bitOr`, `.bitXor`, `.shl`, `.shr`

#### Supported Statement Surface

`CStmt` currently supports:

- `.skip`
- `.assign lhs rhs`
- `.seq s1 s2`
- `.ite cond thenStmt elseStmt`
- `.whileInv cond invariant body`
- `.block locals body`
- `.switch expr tag caseBody defaultBody`
- `.forLoop init cond step body`
- `.break`
- `.continue`
- `.ret expr`
- `.alloc varName cellCount`
- `.free expr cellCount`
- `.decl varName ty`

Useful helper:

- `switchMany expr cases defaultStmt`

Notes:

- `whileInv` takes a loop invariant of type `HProp`. Use `HProp.htrue` when you need a permissive invariant.
- `block` takes a list of local declarations as `(String × CType)`.
- `alloc` and `free` work at the LeanCP memory-model level with explicit cell counts.

#### Practical Examples

Simple arithmetic function:

```lean
def applyTax : CFunDecl := {
  name := "apply_tax"
  params := [("subtotal", .int), ("tax_rate", .int)]
  retType := .int
  body := .ret
    (.binop .add
      (.var "subtotal")
      (.binop .div
        (.binop .mul (.var "subtotal") (.var "tax_rate"))
        (.intLit 100)))
}
```

Conditional return:

```lean
def shippingProgram : CProgramDecl := {
  defs := []
  main := {
    name := "shipping_quote"
    params := [("weight_kg", .int)]
    retType := .int
    body := .ite (.binop .le (.var "weight_kg") (.intLit 5))
      (.ret (.intLit 8))
      (.ret (.intLit 15))
  }
}
```

Loop with invariant:

```lean
def loyaltyProgram : CProgramDecl := {
  defs := []
  main := {
    name := "loyalty_points"
    params := [("orders", .int), ("points_each", .int)]
    retType := .int
    body := .block [("total", .int), ("i", .int)] (
      .seq (.assign (.var "total") (.intLit 0)) (
      .seq (.assign (.var "i") (.intLit 0)) (
      .seq (.whileInv (.binop .lt (.var "i") (.var "orders")) HProp.htrue (
          .seq (.assign (.var "total") (.binop .add (.var "total") (.var "points_each")))
               (.assign (.var "i") (.binop .add (.var "i") (.intLit 1)))))
          (.ret (.var "total")))))
  }
}
```

Pointer and array access:

```lean
def basketProgram : CProgramDecl := {
  defs := []
  main := {
    name := "basket_head_total"
    params := [("prices", .ptr .int)]
    retType := .int
    body := .ret (.binop .add
      (.arrayAccess (.var "prices") (.intLit 0))
      (.arrayAccess (.var "prices") (.intLit 1)))
  }
}
```

#### What Will Not Work

These inputs are outside the supported contract:

- an `entry_symbol` whose type is not `CProgramDecl`
- a custom Lean package graph that depends on your own `lakefile.lean`
- imports that require packages not already present in the pinned runtime
- raw theorem statements with no executable `CProgramDecl`
- arbitrary Lean runtime code that is not expressed through the LeanCP IR

#### Target Honesty

All targets start from the same `CProgramDecl`.

- `c` is the baseline and most direct emission path
- `rust` is a deterministic translation of the same C IR and uses `unsafe` for pointer semantics
- `wasm` is the most restrictive path and should be treated as preview-grade compared with `c`

## When To Use
- Use this skill for `Lean Proof To Code Translator - C Rust Wasm` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: lean proof to code translator   c rust wasm, lean to code translator w proof c rust wasm, compile lean proof programs to c for native integration, generate rust exports from pinned lean proof bundles, produce constrained wasm artifacts from lean proof code, package code generation runs with certificates and logs, generate, source archive file id.
- Supported action names: `generate`, `get_targets`, `get_task`, `list_tasks`, `verify`.

## Use Cases
- Compile Lean proof programs to C for native integration
- Generate Rust exports from pinned Lean proof bundles
- Produce constrained Wasm artifacts from Lean proof code
- Package code generation runs with certificates and logs
- Verify previously generated bundles before shipping or publication
- Preserve reproducible build evidence for audits and reviews
- Archive proof export bundles for downstream teams

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`) - Use this companion skill to inspect, download, upload, and manage files referenced by this product.

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `5`.
x402 availability: not enabled for this product.

- `generate` (action slug: `generate`): Compile a source-only Lean archive into verified C, Rust, or Wasm artifacts using the platform-pinned runtime and shared cache. This action starts an asynchronous task and returns a task_id immediately. Price: `5` credits. Parameters: `entry_module`, `entry_symbol`, `source_archive_file_id`, `target_language`, `timeout_seconds`, `use_vendored_runtime`.
- `get_targets` (action slug: `get-targets`): List the currently supported target languages and bundle requirements. Price: `5` credits. Parameters: none.
- `get_task` (action slug: `get-task`): Check the status of a generate or verify task and retrieve results when complete. Price: `5` credits. Parameters: `task_id`.
- `list_tasks` (action slug: `list-tasks`): List recent generate and verify tasks for the current budget. Price: `5` credits. Parameters: `limit`.
- `verify` (action slug: `verify`): Verify a previously generated Lean proof export bundle against the same pinned runtime and shared cache. This action starts an asynchronous task and returns a task_id immediately. Price: `5` credits. Parameters: `bundle_file_id`, `target_language`, `timeout_seconds`, `verification_mode`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "lean-to-code-translator-w-proof-c-rust-wasm"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "lean-to-code-translator-w-proof-c-rust-wasm"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "lean-to-code-translator-w-proof-c-rust-wasm"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "lean-to-code-translator-w-proof-c-rust-wasm"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "lean-to-code-translator-w-proof-c-rust-wasm"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "lean-to-code-translator-w-proof-c-rust-wasm"
  }
}
```

## Call This Tool
Product slug: `lean-to-code-translator-w-proof-c-rust-wasm`

Marketplace page: https://www.agentpmt.com/marketplace/lean-to-code-translator-w-proof-c-rust-wasm

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Lean-Proof-To-Code-Translator---C-Rust-Wasm",
    "arguments": {
      "action": "generate",
      "entry_module": "example entry module",
      "entry_symbol": "example entry symbol",
      "source_archive_file_id": "example source archive file id",
      "target_language": "c",
      "timeout_seconds": 10,
      "use_vendored_runtime": true
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "lean-to-code-translator-w-proof-c-rust-wasm",
  "parameters": {
    "action": "generate",
    "entry_module": "example entry module",
    "entry_symbol": "example entry symbol",
    "source_archive_file_id": "example source archive file id",
    "target_language": "c",
    "timeout_seconds": 10,
    "use_vendored_runtime": true
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `generate` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/lean-to-code-translator-w-proof-c-rust-wasm
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
