# Lean Proof To Solidity Smart Contract Generator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `lean-proof-to-solidity-smart-contract-generator`

x402 availability: not enabled for this product.

## `catalog`

Action slug: `catalog`

Price: `0` credits

Fetch the advanced Lean catalog. Returns only the allowable advanced templates and reusable advanced Lean snippets.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `compile_abi_bytecode`

Action slug: `compile-abi-bytecode`

Price: `0` credits

Compile Solidity source and return ABI plus deployable bytecode immediately.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `contractName` | `string` | no | Optional specific contract name to select from the compiled output. |
| `extraSources` | `array` | no | Additional Solidity source files required for compilation. |
| `solidityText` | `string` | yes | Primary Solidity source file contents. |
| `sourceName` | `string` | no | Filename to assign to the primary Solidity source. |

Sample parameters:

```json
{
  "contractName": "example contractName",
  "extraSources": [
    {}
  ],
  "solidityText": "example solidityText",
  "sourceName": "example sourceName"
}
```

Generated JSON parameter schema:

```json
{
  "contractName": {
    "description": "Optional specific contract name to select from the compiled output.",
    "required": false,
    "type": "string"
  },
  "extraSources": {
    "description": "Additional Solidity source files required for compilation.",
    "items": {
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "solidityText": {
    "description": "Primary Solidity source file contents.",
    "required": true,
    "type": "string"
  },
  "sourceName": {
    "description": "Filename to assign to the primary Solidity source.",
    "required": false,
    "type": "string"
  }
}
```

## `encode_call`

Action slug: `encode-call`

Price: `0` credits

Encode a contract function call using one ABI item and return the calldata immediately for later simulation or execution.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `abiItem` | `object` | yes | Single ABI item describing the function to encode. |
| `args` | `array` | no | Ordered function arguments. |
| `expectReturnAddress` | `string` | no | Expected address result. |
| `expectReturnHex` | `string` | no | Exact hex return value expected from the call. |
| `expectReturnStartsWith` | `string` | no | Hex prefix expected from the call result. |
| `expectReturnU256` | `string` | no | Expected uint256 result encoded as a decimal string. |
| `expectRevert` | `boolean` | no | Whether the later EVM simulation should expect a revert for this call. |
| `fromAlias` | `string` | no | Optional sender alias for the simulator. |
| `fromPrivateKeyHex` | `string` | no | Optional explicit private key for the sender. |
| `label` | `string` | no | Optional label for the encoded call. |
| `valueWei` | `string` | no | Optional call value in wei. |

Sample parameters:

```json
{
  "abiItem": {},
  "args": [
    "example arg"
  ],
  "expectReturnAddress": "example expectReturnAddress",
  "expectReturnHex": "example expectReturnHex",
  "expectReturnStartsWith": "example expectReturnStartsWith",
  "expectReturnU256": "example expectReturnU256",
  "expectRevert": true,
  "fromAlias": "example fromAlias"
}
```

Generated JSON parameter schema:

```json
{
  "abiItem": {
    "description": "Single ABI item describing the function to encode.",
    "required": true,
    "type": "object"
  },
  "args": {
    "description": "Ordered function arguments.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "expectReturnAddress": {
    "description": "Expected address result.",
    "required": false,
    "type": "string"
  },
  "expectReturnHex": {
    "description": "Exact hex return value expected from the call.",
    "required": false,
    "type": "string"
  },
  "expectReturnStartsWith": {
    "description": "Hex prefix expected from the call result.",
    "required": false,
    "type": "string"
  },
  "expectReturnU256": {
    "description": "Expected uint256 result encoded as a decimal string.",
    "required": false,
    "type": "string"
  },
  "expectRevert": {
    "description": "Whether the later EVM simulation should expect a revert for this call.",
    "required": false,
    "type": "boolean"
  },
  "fromAlias": {
    "description": "Optional sender alias for the simulator.",
    "required": false,
    "type": "string"
  },
  "fromPrivateKeyHex": {
    "description": "Optional explicit private key for the sender.",
    "required": false,
    "type": "string"
  },
  "label": {
    "description": "Optional label for the encoded call.",
    "required": false,
    "type": "string"
  },
  "valueWei": {
    "description": "Optional call value in wei.",
    "required": false,
    "type": "string"
  }
}
```

## `evm_simulation`

Action slug: `evm-simulation`

Price: `0` credits

Run offline EVM simulation against compiled contract output and return the result immediately.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `calls` | `array` | no | Sequence of encoded simulation calls to execute. |
| `compileOutput` | `object` | yes | Compiler output produced by the compile_abi_bytecode action. |

Sample parameters:

```json
{
  "calls": [
    {}
  ],
  "compileOutput": {}
}
```

Generated JSON parameter schema:

```json
{
  "calls": {
    "description": "Sequence of encoded simulation calls to execute.",
    "items": {
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "compileOutput": {
    "description": "Compiler output produced by the compile_abi_bytecode action.",
    "required": true,
    "type": "object"
  }
}
```

## `generate_solidity`

Action slug: `generate-solidity`

Price: `0` credits

Generate Solidity from advanced Lean Solidity IR source and return a background task id for the generation job.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `leanSourceExpr` | `string` | yes | Lean expression naming the contract value to emit, such as a `SolContract` declaration. |
| `leanSourceText` | `string` | yes | Lean source text that defines an advanced Solidity IR contract. |

Sample parameters:

```json
{
  "leanSourceExpr": "example leanSourceExpr",
  "leanSourceText": "example leanSourceText"
}
```

Generated JSON parameter schema:

```json
{
  "leanSourceExpr": {
    "description": "Lean expression naming the contract value to emit, such as a `SolContract` declaration.",
    "required": true,
    "type": "string"
  },
  "leanSourceText": {
    "description": "Lean source text that defines an advanced Solidity IR contract.",
    "required": true,
    "type": "string"
  }
}
```

## `get_task`

Action slug: `get-task`

Price: `0` credits

Fetch the current status and result payload for a previously submitted background generate_solidity task within the caller's budget scope.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `string` | yes | Task identifier returned by a prior background action. |

Sample parameters:

```json
{
  "task_id": "example task id"
}
```

Generated JSON parameter schema:

```json
{
  "task_id": {
    "description": "Task identifier returned by a prior background action.",
    "required": true,
    "type": "string"
  }
}
```

## `list_tasks`

Action slug: `list-tasks`

Price: `0` credits

List recent background generate_solidity tasks for the caller's active budget only.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Maximum number of tasks to return. |

Sample parameters:

```json
{
  "limit": 1
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "description": "Maximum number of tasks to return.",
    "required": false,
    "type": "integer"
  }
}
```

## `validate_lean`

Action slug: `validate-lean`

Price: `0` credits

Validate advanced Lean Solidity IR source immediately and return structured diagnostics that explain what is wrong before you submit a generation job.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `leanSourceExpr` | `string` | yes | Lean expression naming the contract value to validate, such as a `SolContract` declaration. |
| `leanSourceText` | `string` | yes | Lean source text that defines an advanced Solidity IR contract. |

Sample parameters:

```json
{
  "leanSourceExpr": "example leanSourceExpr",
  "leanSourceText": "example leanSourceText"
}
```

Generated JSON parameter schema:

```json
{
  "leanSourceExpr": {
    "description": "Lean expression naming the contract value to validate, such as a `SolContract` declaration.",
    "required": true,
    "type": "string"
  },
  "leanSourceText": {
    "description": "Lean source text that defines an advanced Solidity IR contract.",
    "required": true,
    "type": "string"
  }
}
```
