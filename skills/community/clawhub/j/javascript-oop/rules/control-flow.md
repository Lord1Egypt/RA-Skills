# Control Flow

- Prefer guard clauses and early return.
- Use braces for multiline branches.
- Break long conditions at the logical operator.
- Prefer `if` or `switch` over nested ternaries.
- Parenthesize mixed logical operators.

## Example

```js
function resolveStatus(user) {
    if (!user) {
        return "missing";
    }

    if (user.isActive && user.hasAcceptedTerms) {
        return "ready";
    }

    return "pending";
}
```

## End Check

- Verify early returns remove needless nesting.
- Verify branch logic reads top-to-bottom without ternary puzzles.
