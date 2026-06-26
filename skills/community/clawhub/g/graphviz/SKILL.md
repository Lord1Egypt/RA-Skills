---
name: graphviz
description: Generate SVG images from Graphviz DOT graphs using WebAssembly. Uses the graphviz_component.wasm running in the openclaw-wasm-sandbox plugin. No graphviz system binary or execution permission required.
---

# Graphviz SVG Generator

Generate SVG images from Graphviz DOT graph descriptions using WebAssembly.

## When to Use

Trigger when:
-  Keywords: graphviz, DOT, SVG, flowchart
- user asks to generate/convert/visualize a graph from DOT language
- user wants to render a Graphviz diagram as SVG
- user provides DOT notation and wants SVG output
- 用户要求生成/转换/可视化 DOT 语言图
- 用户想要将 Graphviz 图渲染为 SVG
- 用户提供 DOT 记号并想要 SVG 输出
- 关键词：流程图生成, 制图

## Prerequisites

- **Required plugin:** `openclaw-wasm-sandbox`
- **WASM file:** `~/.openclaw/skills/graphviz/files/graphviz_component.wasm` (Use the `wasm-sandbox-download` tool to download，URL: `https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/graphviz/files/graphviz_component.wasm`)

## How It Works

The WASM component:
- Accepts DOT graph string as **argument**
- Outputs SVG to **stdout**

## Tool

Use `wasm-sandbox-run` tool:

| Parameter | Value |
|-----------|-------|
| `wasmFile` | `~/.openclaw/skills/graphviz/files/graphviz_component.wasm` |
| `args` | DOT graph string, e.g. `["digraph { a -> b }"]` |

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/graphviz/files/graphviz_component.wasm",
  args: ["digraph { a -> b }"]
})
```

## Usage

1. User provides DOT graph description
2. Call `wasm-sandbox-run` with DOT string in `args`
3. Return the SVG output to the user

## DOT Language Reference

```
digraph name {           # Directed graph
  a -> b                 # Edge from a to b
  b -> c
  a [label="Node A"]     # Node with label
  b [shape=box]          # Node shape
}

graph name {             # Undirected graph
  a -- b
  b -- c
}
```

Common node attributes: `label`, `shape` (box, circle, diamond, triangle), `color`, `style` (filled, dashed)

Common edge attributes: `label`, `color`, `style`, `dir` (forward, back, both, none)

## Notes

- No system graphviz binary needed — pure WASM execution
- No execution permission required — runs in sandbox
- Runs in sandbox with no implicit file/network access
- Output is pure SVG ready to display or save
