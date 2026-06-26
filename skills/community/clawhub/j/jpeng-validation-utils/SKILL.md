---
name: validation-utils
description: Provides data validation and type checking utilities for validating inputs and data structures. Use when you need to validate data types, check constraints, or verify data integrity.
---

# Validation Utils

Provides data validation and type checking utilities.

## Usage

```javascript
const v = require('./skills/validation-utils');

// Type checking
if (v.isString(value)) { ... }
if (v.isArray(value)) { ... }

// Validation
const result = v.validate(user, {
  name: v.required(v.isString),
  age: v.optional(v.isNumber),
  email: v.required(v.isEmail)
});

// Assert
v.assert(v.isPositive(5), 'Must be positive');
```

## Features

- Type checking utilities
- Required/optional validators
- Email, URL, UUID validation
- Number range validation
- String pattern validation
- Object schema validation
- Assertion helpers
