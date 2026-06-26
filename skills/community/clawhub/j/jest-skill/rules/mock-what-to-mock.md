---
title: What to mock and what not to mock
impact: CRITICAL
description: Over-mocking makes tests pass without testing real behavior. Under-mocking makes tests slow and flaky. Mock at the right boundaries.
tags: mock, strategy, boundaries, integration, over-mocking, anti-pattern
---

# What to mock and what not to mock

## Problem

Agents default to mocking everything — database clients, utility functions, internal modules — producing tests that assert mock behavior, not real behavior. These tests pass even when the real code is broken. Conversely, mocking nothing makes tests slow, flaky, and dependent on external services.

## What to Mock

Mock things that are **external, slow, non-deterministic, or have side effects**:

```javascript
// MOCK: External HTTP calls
jest.mock('./api-client');

// MOCK: Database connections
jest.mock('./db');

// MOCK: File system writes (not reads of test fixtures)
jest.spyOn(fs, 'writeFileSync').mockImplementation(() => {});

// MOCK: Date/time for determinism
jest.useFakeTimers({ now: new Date('2024-01-01') });

// MOCK: Random values for determinism
jest.spyOn(Math, 'random').mockReturnValue(0.5);

// MOCK: Environment variables
jest.replaceProperty(process.env, 'API_KEY', 'test-key');

// MOCK: Third-party services (email, payments, analytics)
jest.mock('./email-service');
jest.mock('./payment-gateway');

// MOCK: Console output (when testing that logs happen, not output)
jest.spyOn(console, 'error').mockImplementation(() => {});
```

## What NOT to Mock

Do not mock things that are **internal, fast, deterministic, and pure**:

```javascript
// DON'T MOCK: The code under test itself
// BAD — mocking the function you're testing
jest.spyOn(userService, 'validateAge');
userService.validateAge(25);
expect(userService.validateAge).toHaveBeenCalled(); // tests nothing

// DON'T MOCK: Pure utility functions
// BAD — mocking a formatter you own
jest.mock('./utils/formatCurrency');
// Now you're testing that your code calls formatCurrency, not that it formats correctly

// DON'T MOCK: Data transformations
// BAD
jest.mock('./mappers/userMapper');
// You should test that the mapping logic is correct

// DON'T MOCK: Simple constructors and value objects
// BAD
jest.mock('./models/User');

// DON'T MOCK: Standard library functions (unless for determinism)
// BAD — mocking Array.prototype.filter
jest.spyOn(Array.prototype, 'filter');
```

## Decision Framework

| Question | If Yes → | If No → |
|---|---|---|
| Is it an external service (HTTP, DB, queue)? | Mock it | Don't mock |
| Is it non-deterministic (time, random, UUID)? | Mock it | Don't mock |
| Does it have side effects (write files, send email)? | Mock it | Don't mock |
| Is it slow (> 100ms)? | Mock it | Don't mock |
| Is it code you own and are testing? | Don't mock | — |
| Is it a pure function? | Don't mock | — |
| Is it a data structure or value object? | Don't mock | — |

## The Mock Boundary Rule

Draw a line around your **unit under test**. Mock everything that crosses that line outward. Don't mock anything inside it.

```
┌─────────────────────────────────┐
│         Unit Under Test         │
│                                 │
│  Controller → Service → Mapper  │  ← don't mock these
│                                 │
└──────────┬──────────────────────┘
           │ (mock boundary)
           ▼
    ┌──────────────┐
    │  Database     │  ← mock this
    │  HTTP Client  │  ← mock this
    │  File System  │  ← mock this
    │  Clock/Random │  ← mock this
    └──────────────┘
```

## Common Over-Mocking Anti-Pattern

```javascript
// BAD: Every dependency is mocked — test proves nothing
jest.mock('./userRepository');
jest.mock('./emailService');
jest.mock('./validator');
jest.mock('./mapper');

test('creates user', async () => {
  validator.validate.mockReturnValue(true);
  mapper.toEntity.mockReturnValue({ name: 'Alice' });
  userRepository.save.mockResolvedValue({ id: 1 });

  await userService.createUser({ name: 'Alice' });

  expect(userRepository.save).toHaveBeenCalled(); // only tests wiring
});
```

```javascript
// GOOD: Only mock the external boundary (database)
jest.mock('./userRepository');

test('creates user with validation', async () => {
  userRepository.save.mockResolvedValue({ id: 1, name: 'Alice' });

  const result = await userService.createUser({ name: 'Alice' });

  // Tests real validation, real mapping, real business logic
  expect(result).toEqual({ id: 1, name: 'Alice' });
  expect(userRepository.save).toHaveBeenCalledWith(
    expect.objectContaining({ name: 'Alice' })
  );
});
```

## Why

- **Over-mocked tests** are tautological — they test that mocks return what you told them to return. They pass when the real code is broken.
- **Under-mocked tests** are slow, flaky, and require external services to be running. They fail due to network issues, not code bugs.
- **Right-boundary mocking** tests real logic while isolating external dependencies. It catches real bugs and runs fast.

The goal is to test **behavior**, not **implementation**. If you can change the internal implementation without breaking the test, your mock boundaries are correct.
