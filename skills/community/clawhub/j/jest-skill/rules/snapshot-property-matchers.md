---
title: Use property matchers for dynamic fields
impact: MEDIUM
description: Snapshots with dynamic values (IDs, dates, random strings) break on every run. Use property matchers to assert the type without pinning the value.
tags: snapshot, property-matcher, dynamic, date, uuid, any
---

# Use property matchers for dynamic fields

## Problem

If an object contains dynamic values like timestamps, UUIDs, or auto-incrementing IDs, the snapshot changes on every test run. Tests fail, developers run `--updateSnapshot` reflexively, and the snapshot stops testing anything meaningful.

## Incorrect

```javascript
// BUG: createdAt and id change every run — snapshot always fails
test('creates user', () => {
  const user = createUser({ name: 'Alice' });
  expect(user).toMatchSnapshot();
  // Snapshot contains:
  // { id: "a1b2c3d4", name: "Alice", createdAt: "2024-01-15T10:30:00.000Z" }
  // Next run: id and createdAt are different — fails
});
```

## Correct

```javascript
// Property matchers: assert the type/shape of dynamic fields
test('creates user', () => {
  const user = createUser({ name: 'Alice' });
  expect(user).toMatchSnapshot({
    id: expect.any(String),
    createdAt: expect.any(Date),
  });
  // Snapshot pins `name: "Alice"` but allows any String id and any Date createdAt
});
```

```javascript
// Inline snapshot with property matchers
test('creates user', () => {
  const user = createUser({ name: 'Alice' });
  expect(user).toMatchInlineSnapshot(
    {
      id: expect.any(String),
      createdAt: expect.any(Date),
    },
    `
    {
      "id": Any<String>,
      "name": "Alice",
      "createdAt": Any<Date>,
    }
    `
  );
});
```

## Common Property Matchers

```javascript
expect(result).toMatchSnapshot({
  id: expect.any(String),                          // any string
  count: expect.any(Number),                        // any number
  createdAt: expect.any(Date),                      // any Date instance
  updatedAt: expect.stringMatching(/^\d{4}-\d{2}/), // ISO date string prefix
  items: expect.arrayContaining([                   // array with specific shape
    expect.objectContaining({ type: 'item' }),
  ]),
});
```

## Why

Property matchers let you get the benefits of snapshot testing (detecting unexpected changes to the overall shape) while tolerating expected variation in specific fields. This eliminates the "update snapshot, hope for the best" anti-pattern.

The first argument to `toMatchSnapshot()` is the property matcher object. Matched properties are replaced with the matcher's display representation (e.g., `Any<String>`) in the stored snapshot, while all other properties are pinned to their exact values.
