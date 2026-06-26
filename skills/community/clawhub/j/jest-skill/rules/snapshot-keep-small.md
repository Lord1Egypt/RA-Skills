---
title: Keep snapshots small and focused
impact: MEDIUM
description: Large snapshots are hard to review, frequently break on unrelated changes, and get rubber-stamp updated without inspection.
tags: snapshot, toMatchSnapshot, inline, focused, size
---

# Keep snapshots small and focused

## Problem

Snapshotting an entire component tree or large data structure produces hundreds of lines of snapshot text. Reviewers skip over large snapshot diffs, changes get auto-updated without inspection, and unrelated changes (e.g., a CSS class rename) break dozens of snapshots across the codebase.

## Incorrect

```javascript
// BUG: Snapshot of entire page component — 500+ lines, breaks on any child change
test('renders dashboard', () => {
  const tree = renderer.create(<Dashboard />).toJSON();
  expect(tree).toMatchSnapshot(); // massive snapshot
});
```

## Correct

```javascript
// Snapshot only the specific piece you care about
test('renders user greeting', () => {
  const { getByTestId } = render(<Dashboard />);
  expect(getByTestId('greeting')).toMatchSnapshot();
});
```

```javascript
// Better: Use inline snapshots for small outputs
test('formats greeting message', () => {
  expect(formatGreeting('Alice')).toMatchInlineSnapshot(`"Hello, Alice!"`);
});
```

```javascript
// Best: Use specific matchers instead of snapshots when possible
test('renders user greeting', () => {
  const { getByText } = render(<Dashboard user="Alice" />);
  expect(getByText('Hello, Alice!')).toBeInTheDocument();
});
```

## Guidelines

| Approach | When to use |
|---|---|
| **Specific matchers** | Always prefer when you know the exact expected output |
| **Inline snapshot** | Small outputs (< 10 lines) — keeps expectation in the test file |
| **External snapshot** | Medium outputs (10–50 lines) — use `.toMatchSnapshot()` |
| **Avoid** | Outputs > 50 lines — break into smaller units |

## Why

Snapshot tests are a *change-detection* tool, not a *correctness* tool. They tell you "something changed" but not "this is right." Their value is inversely proportional to their size:

- **Small snapshots**: Easy to review, clear what changed, meaningful diffs.
- **Large snapshots**: Impossible to review, get auto-updated with `--updateSnapshot`, eventually test nothing meaningful.

If a snapshot is over 50 lines, break the component or data into smaller units and snapshot each independently. Prefer specific assertions over snapshots whenever possible.
