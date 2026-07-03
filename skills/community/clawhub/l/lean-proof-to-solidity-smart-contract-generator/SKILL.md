---
name: lean-proof-to-solidity-smart-contract-generator
description: "Lean Proof To Solidity Smart Contract Generator: The tool allows you to validate Lean, generate Solidity from it, compile the. Use when an agent needs lean proof to solidity smart contract generator, fetch allowable advanced lean templates and snippets, validate advanced lean solidity ir before generation, generate solidity from advanced lean solidity ir, compile generated solidity to abi and bytecode, catalog, compile abi bytecode, soliditytext through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/lean-proof-to-solidity-smart-contract-generator
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/lean-proof-to-solidity-smart-contract-generator"}}
---
# Lean Proof To Solidity Smart Contract Generator

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
PROOF OF CONCEPT - This tool does not include an exhaustive Lean to Solidity code mapping, but it shows the capabilities of our system and the value of going from proven Lean straight to Solidity. Build your logic in a proven language first, then generate your Solidity from that. We have included Lean templates and allowable Lean snippets to get you started. Try it live in the builder, or use the AI agent to help you build faster. The tool allows you to validate Lean, generate Solidity from it, compile the generated Solidity to ABI and bytecode, encode ABI calls, and then run offline EVM simulation before deployment. The full system is available for licensing - inquire directly if interested.

## Product Instructions
Use this tool to work directly in the advanced Lean Solidity IR lane.

Recommended flow:
1. `catalog`
2. `validate_lean`
3. `generate_solidity`
4. `get_task` until the generation task reaches `completed`
5. `compile_abi_bytecode`
6. `encode_call`
7. `evm_simulation`
8. `list_tasks` only when you need to review recent generation jobs in your current budget scope

Action breakdown

`catalog`
- Purpose: Fetch the allowable advanced Lean templates and reusable advanced Lean snippets.
- Output: immediate payload containing only `advancedTemplates` and `advancedSnippets`.

Example:
```json
{
  "action": "catalog"
}
```

`validate_lean`
- Purpose: Validate advanced Lean Solidity IR source before running a generation job.
- Use it for: checking that the Lean source parses, resolves the target expression, and is suitable for the advanced Solidity generator.
- Input: `leanSourceText` and `leanSourceExpr`.
- Output: immediate validation result. On failure it returns a human summary, stable `errorKind`, and parsed `diagnostics` with submitted line and column information.

Example:
```json
{
  "action": "validate_lean",
  "leanSourceText": "import HeytingLean.LeanSP.Emit.SolEmit\n\nnamespace Demo\nopen LeanSP.Emit\n\ndef counter : SolContract :=\n  { name := \"Counter\"\n  , stateVars := [ { name := \"storedValue\", ty := .uint 256, visibility := .pub } ]\n  , functions :=\n      [ { name := \"setValue\"\n        , params := [(\"newValue\", .uint 256)]\n        , visibility := .external\n        , body := [ .assign (.var \"storedValue\") (.var \"newValue\") ]\n        }\n      ]\n  }\n",
  "leanSourceExpr": "Demo.counter"
}
```

`generate_solidity`
- Purpose: Generate Solidity from advanced Lean Solidity IR source.
- Use it for: users who already understand the Lean authoring model and want Solidity out.
- Input: `leanSourceText` and `leanSourceExpr`.
- Output: a background task id. Poll with `get_task` until the task reaches `completed`. The completed result includes emitted Solidity text and related metadata.

Example:
```json
{
  "action": "generate_solidity",
  "leanSourceText": "import HeytingLean.LeanSP.Emit.SolEmit\n\nnamespace Demo\nopen LeanSP.Emit\n\ndef counter : SolContract :=\n  { name := \"Counter\"\n  , stateVars := [ { name := \"storedValue\", ty := .uint 256, visibility := .pub } ]\n  , functions :=\n      [ { name := \"setValue\"\n        , params := [(\"newValue\", .uint 256)]\n        , visibility := .external\n        , body := [ .assign (.var \"storedValue\") (.var \"newValue\") ]\n        }\n      ]\n  }\n",
  "leanSourceExpr": "Demo.counter"
}
```

`compile_abi_bytecode`
- Purpose: Compile Solidity and return ABI plus bytecode.
- Use it for: turning generated Solidity text into deployable artifacts.
- Input: `solidityText` and optionally `sourceName`, `contractName`, and `extraSources`.
- Output: immediate compile payload with ABI, bytecode, deployed bytecode, and selected contract metadata.

`encode_call`
- Purpose: Encode calldata for a function call using an ABI item.
- Use it for: preparing calls for EVM simulation.

`evm_simulation`
- Purpose: Run an offline EVM simulation against compiled contract output.
- Use it for: checking generated contract behavior before deployment.

`get_task`
- Purpose: Fetch the current status and result for a background task.
- Use it for: polling `generate_solidity`.

`list_tasks`
- Purpose: List your recent background tasks in the current budget scope.
- Use it for: finding recent advanced Lean generation jobs without storing every task id yourself.

Notes:
- `catalog` returns immediately with only the advanced templates and snippet catalog.
- `validate_lean` returns immediately with structured diagnostics.
- `generate_solidity` submits a background task.
- `compile_abi_bytecode`, `encode_call`, and `evm_simulation` return immediately.
- `get_task` and `list_tasks` are restricted to the caller's active budget scope.
- The restricted builder and component-composition paths still exist in the backend, but they are intentionally hidden from the current user-facing product surface.

## When To Use
- Use this skill for `Lean Proof To Solidity Smart Contract Generator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: lean proof to solidity smart contract generator, fetch allowable advanced lean templates and snippets, validate advanced lean solidity ir before generation, generate solidity from advanced lean solidity ir, compile generated solidity to abi and bytecode, catalog, compile abi bytecode, soliditytext.
- Supported action names: `catalog`, `compile_abi_bytecode`, `encode_call`, `evm_simulation`, `generate_solidity`, `get_task`, `list_tasks`, `validate_lean`.

## Use Cases
- Fetch allowable advanced Lean templates and snippets
- Validate advanced Lean Solidity IR before generation
- Generate Solidity from advanced Lean Solidity IR
- Compile generated Solidity to ABI and bytecode
- Encode ABI function calls for simulation
- Run offline EVM simulation before deployment
- Poll background Lean generation tasks within the active budget

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `8`.
x402 availability: not enabled for this product.

- `catalog` (action slug: `catalog`): Fetch the advanced Lean catalog. Returns only the allowable advanced templates and reusable advanced Lean snippets. Price: `0` credits. Parameters: none.
- `compile_abi_bytecode` (action slug: `compile-abi-bytecode`): Compile Solidity source and return ABI plus deployable bytecode immediately. Price: `0` credits. Parameters: `contractName`, `extraSources`, `solidityText`, `sourceName`.
- `encode_call` (action slug: `encode-call`): Encode a contract function call using one ABI item and return the calldata immediately for later simulation or execution. Price: `0` credits. Parameters: `abiItem`, `args`, `expectReturnAddress`, `expectReturnHex`, `expectReturnStartsWith`, `expectReturnU256`, `expectRevert`, `fromAlias`, plus 3 more.
- `evm_simulation` (action slug: `evm-simulation`): Run offline EVM simulation against compiled contract output and return the result immediately. Price: `0` credits. Parameters: `calls`, `compileOutput`.
- `generate_solidity` (action slug: `generate-solidity`): Generate Solidity from advanced Lean Solidity IR source and return a background task id for the generation job. Price: `0` credits. Parameters: `leanSourceExpr`, `leanSourceText`.
- `get_task` (action slug: `get-task`): Fetch the current status and result payload for a previously submitted background generate_solidity task within the caller's budget scope. Price: `0` credits. Parameters: `task_id`.
- `list_tasks` (action slug: `list-tasks`): List recent background generate_solidity tasks for the caller's active budget only. Price: `0` credits. Parameters: `limit`.
- `validate_lean` (action slug: `validate-lean`): Validate advanced Lean Solidity IR source immediately and return structured diagnostics that explain what is wrong before you submit a generation job. Price: `0` credits. Parameters: `leanSourceExpr`, `leanSourceText`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "lean-proof-to-solidity-smart-contract-generator"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "lean-proof-to-solidity-smart-contract-generator"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "lean-proof-to-solidity-smart-contract-generator"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "lean-proof-to-solidity-smart-contract-generator"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "lean-proof-to-solidity-smart-contract-generator"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "lean-proof-to-solidity-smart-contract-generator"
  }
}
```

## Call This Tool
Product slug: `lean-proof-to-solidity-smart-contract-generator`

Marketplace page: https://www.agentpmt.com/marketplace/lean-proof-to-solidity-smart-contract-generator

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
    "name": "Lean-Proof-To-Solidity-Smart-Contract-Generator",
    "arguments": {
      "action": "catalog"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "lean-proof-to-solidity-smart-contract-generator",
  "parameters": {
    "action": "catalog"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `catalog` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/lean-proof-to-solidity-smart-contract-generator
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
