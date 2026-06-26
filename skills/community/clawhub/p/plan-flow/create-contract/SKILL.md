---
name: create-contract
description: Create an integration contract from API documentation
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---

# Create Contract

Create an integration contract document from API documentation.

## What It Does

1. Fetches or reads API documentation
2. Extracts endpoints, schemas, and authentication details
3. Creates TypeScript interfaces for all data types
4. Documents error handling and rate limits
5. Provides usage examples

## Usage

```
/create-contract <url>
```

**Arguments:**
- `url` (required): URL to the API documentation

## Output

Creates: `flow/contracts/<service>_contract.md`

## Contract Structure

```markdown
# Contract: [Service Name]

Source: [URL]

## Overview
Brief description of the API

## Authentication
```typescript
// Authentication example
const headers = {
  'Authorization': `Bearer ${token}`,
};
```

## Base Configuration
| Setting | Value |
|---------|-------|
| Base URL | https://api.example.com |
| Rate Limit | 100 req/min |
| Timeout | 30s |

## Endpoints

### GET /users
Get list of users

**Request:**
```typescript
interface GetUsersRequest {
  page?: number;
  limit?: number;
}
```

**Response:**
```typescript
interface GetUsersResponse {
  data: User[];
  meta: { total: number };
}
```

## TypeScript Interfaces
```typescript
interface User {
  id: string;
  email: string;
  name: string;
}
```

## Error Handling
| Code | Meaning | Action |
|------|---------|--------|
| 401 | Unauthorized | Refresh token |
| 429 | Rate Limited | Retry with backoff |

## Usage Examples
```typescript
// Fetch users
const users = await api.getUsers({ page: 1 });
```
```

## Example

```
/create-contract https://api.stripe.com/docs
```

**Output:**
```
Creating contract for: https://api.stripe.com/docs

Fetching documentation...
Extracting endpoints...
Generating TypeScript interfaces...

Contract created: flow/contracts/stripe_contract.md

Summary:
- 45 endpoints documented
- 28 TypeScript interfaces
- Authentication: Bearer token
- Rate limit: 100 req/sec
```

## What's Included

- **Overview**: Service description and version
- **Authentication**: How to authenticate requests
- **Endpoints**: All available endpoints with schemas
- **TypeScript Interfaces**: Types for all request/response data
- **Error Handling**: Error codes and recommended actions
- **Rate Limits**: Throttling information
- **Usage Examples**: Code snippets for common operations

## Use Cases

- Integrating with third-party APIs
- Documenting internal APIs
- Creating type-safe API clients
- Onboarding new developers
