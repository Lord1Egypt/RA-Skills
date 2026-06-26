## Memory Contract

This skill follows `memory-governor`.

Typical outputs:

- [memory type] -> [target class]
- [memory type] -> [target class]

Current adapter examples:

- [target class] -> [current path or downstream system]

### Capability Declaration

```toml
[capabilities]
families = ["writer"]
```

Constraints:

- This skill does not define its own global memory rules.
- This skill should not bypass `memory-governor` promotion or exclusion rules.
- One-off corrections should land in `learning_candidates` before becoming reusable lessons or hard rules.
- Compiled wiki, digest, or report outputs are downstream views unless the host explicitly authorizes promotion.
- If an optional adapter is missing, use the current fallback behavior instead of inventing a new global rule.
