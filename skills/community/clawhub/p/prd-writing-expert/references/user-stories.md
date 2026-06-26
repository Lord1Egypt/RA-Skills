# User Story Writing Guide

## User Story Format

Standard format:
```
As a [role]
I want to [action]
So that [value]
```

## Writing Principles

1. **INVEST Principle**
   - Independent
   - Negotiable
   - Valuable
   - Estimable
   - Small
   - Testable

2. **Focus on User Value**
   - Adopt user perspective
   - Emphasize "why" rather than "how"
   - Avoid technical jargon

## Acceptance Criteria

### Format
```
Given [precondition]
When [triggering action]
Then [expected result]
```

### Example
```
User Story: As a user, I want to register an account using my email so that I can access platform features

Acceptance Criteria:
Given the user is on the registration page
When the user enters a valid email and password and clicks register
Then the system sends a verification email
And the user account status is "Pending Verification"

Given the user receives the verification email
When the user clicks the verification link
Then the user account status changes to "Verified"
And the user can log into the system
```

## User Story Map

Structure for organizing user stories:

1. **User Activities** (High-level)
   - User Tasks
     - User Stories

2. **Release Slices**
   - MVP Slice
   - Enhancement Slice
   - Future Slice

## Common Mistakes

❌ Incorrect: "As a system, I want to save data"
✅ Correct: "As a user, I want my data to be saved so that I can continue next time"

❌ Incorrect: "As a user, I want the system to use a microservices architecture"
✅ Correct: "As a user, I want the system to respond quickly so that I can use it smoothly"

❌ Too large: "As a user, I want to complete a purchase"
✅ Split into:
   - "As a user, I want to browse products so that I can find what I want"
   - "As a user, I want to add items to my cart so that I can purchase multiple items together"
   - "As a user, I want to complete payment so that I can receive the product"