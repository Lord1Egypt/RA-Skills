# markdown-it Architecture Principles

## Data Flow

Input is parsed through three nested rule chains: `core` → `block` → `inline`.

```
core
    core.rule1 (normalize)
    ...
    core.ruleX
    block
        block.rule1 (blockquote)
        ...
        block.ruleX
    core.ruleX1 (intermediate rules operating on block tokens)
    ...
    inline (applied to each block token of type="inline")
        inline.rule1 (text)
        ...
        inline.ruleX
    core.ruleYY (applied to all tokens)
    ... (abbreviation, footnote, typographer, linkify)
```

Each chain (`core` / `block` / `inline`) has its own `state` object, making parsing independent and rules can be disabled at any time.

## Token Stream

Does not use a traditional AST, but rather a **token array** (Token Stream). Tokens are simple sequences:
- Open/close tags are separated
- Special "inline containers" embed child tokens (bold, italic, text, etc.)

Summary:
- Top level: paired/singleton "block" tokens (headings, lists, blockquotes, paragraphs, code blocks, etc.)
- Each inline token's `children` property contains an inline token stream:
  - Open/close tags (bold, italic, link, inline code...)
  - Plain text, newlines

## Rules

A Rule is a function that operates on the parser `state`, managed by name via the `Ruler` instance, and can be `enabled`/`disabled`.

Some rules have a "validation mode" — they only look ahead without modifying the token stream. This is a core design principle: the token stream is "write-only" during the block/inline parsing phase.

Rules are independent of each other, so they can be safely enabled/disabled/added. To write a new rule, refer to existing plugins and rule files:
- `lib/parser_core.mjs`
- `lib/parser_block.mjs`
- `lib/parser_inline.mjs`

## Renderer

After the token stream is generated, it is passed to the `Renderer`, which traverses the tokens and calls the corresponding rendering function:

```js
function (tokens, idx, options, env, renderer) {
  return htmlResult;
}
```

Rendering rules are stored in `md.renderer.rules[name]`. Overriding them directly modifies the output without changing the parser.

## Parsing Order Summary

1. Parse blocks, populate the top level of the token stream
2. Parse inline container content, populate `children`
3. Render

Additional transformations can be inserted in between.