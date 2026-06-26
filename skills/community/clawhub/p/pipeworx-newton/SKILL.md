---
name: pipeworx-newton
description: Symbolic math solver — simplify, differentiate, integrate, and factor expressions via the Newton API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "∫"
    homepage: https://pipeworx.io/packs/newton
---

# Newton Math Solver

Symbolic mathematics over an API. Simplify algebraic expressions, compute derivatives and integrals, and factor polynomials. All operations return exact symbolic results, not numerical approximations.

## Tools

| Tool | Description |
|------|-------------|
| `simplify` | Simplify a mathematical expression (e.g., `"2^2+2(2)"` becomes `"8"`) |
| `derive` | Differentiate with respect to x (e.g., `"x^3+2x^2+x"` becomes `"3x^2+4x+1"`) |
| `integrate` | Indefinite integral with respect to x (e.g., `"x^2"` becomes `"1/3 x^3"`) |
| `factor` | Factor a polynomial (e.g., `"x^2-1"` becomes `"(x-1)(x+1)"`) |

## When to use

- Calculus homework help — derivatives and integrals
- Simplifying complex expressions during technical discussions
- Factoring polynomials for algebra problems
- Verifying hand-computed symbolic math

## Example: derivative of sin(x)*x^2

```bash
curl -s -X POST https://gateway.pipeworx.io/newton/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"derive","arguments":{"expression":"x^3+2x^2+x"}}}'
```

```json
{
  "operation": "derive",
  "expression": "x^3+2x^2+x",
  "result": "3 x^2 + 4 x + 1"
}
```

## Setup

```json
{
  "mcpServers": {
    "pipeworx-newton": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/newton/mcp"]
    }
  }
}
```
