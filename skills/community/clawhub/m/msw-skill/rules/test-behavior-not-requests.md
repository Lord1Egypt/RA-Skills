---
title: Test Application Behavior, Not Request Mechanics
impact: HIGH
description: Assert on UI changes, state transitions, or return values — not on whether fetch was called with specific arguments.
tags: testing, behavior, assertion, fetch, ui
---

# Test Application Behavior, Not Request Mechanics

## Problem

Asserting that `fetch` was called with specific arguments tests implementation details, not behavior. If the app switches from `fetch` to `axios`, the test breaks even though behavior is identical.

## Incorrect

```typescript
// BUG: testing implementation, not behavior
test('logs in the user', async () => {
  render(<LoginForm />)
  await userEvent.type(screen.getByLabelText('Email'), 'john@test.com')
  await userEvent.type(screen.getByLabelText('Password'), 'password')
  await userEvent.click(screen.getByRole('button', { name: 'Sign In' }))

  // Fragile: tests HOW the app fetches, not WHAT happens
  expect(fetch).toHaveBeenCalledWith('/api/login', {
    method: 'POST',
    body: JSON.stringify({ email: 'john@test.com', password: 'password' }),
  })
})
```

## Correct

```typescript
test('logs in the user', async () => {
  render(<LoginForm />)
  await userEvent.type(screen.getByLabelText('Email'), 'john@test.com')
  await userEvent.type(screen.getByLabelText('Password'), 'password')
  await userEvent.click(screen.getByRole('button', { name: 'Sign In' }))

  // Tests WHAT the user sees after login
  await waitFor(() => {
    expect(screen.getByText('Welcome, John!')).toBeInTheDocument()
  })
})
```

## Why

MSW intercepts requests at the network level, so your tests should focus on observable outcomes: what the user sees, what state changes, what the function returns. This makes tests resilient to HTTP client refactors and more readable.
