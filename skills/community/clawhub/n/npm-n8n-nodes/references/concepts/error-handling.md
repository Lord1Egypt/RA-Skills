# Error Handling

## Table of Contents
1. [NodeOperationError vs NodeApiError](#1-nodeoperationerror-vs-nodeapierror)
2. [continueOnFail pattern](#2-continuenonfail-pattern)
3. [Throwing with context](#3-throwing-with-context)
4. [Validating parameters before the loop](#4-validating-parameters)
5. [API error response handling](#5-api-error-response-handling)

---

## 1. NodeOperationError vs NodeApiError

| Error class | When to use | Has statusCode? |
|---|---|---|
| `NodeOperationError` | Logic errors, missing params, invalid input, config problems | No |
| `NodeApiError` | HTTP errors from external API calls (non-2xx responses) | Yes |

```typescript
import { NodeOperationError, NodeApiError } from 'n8n-workflow';

// Logic / config error — something wrong in the node setup or user input
throw new NodeOperationError(
  this.getNode(),
  'The "Template" field must contain at least one variable.',
  { itemIndex: i },
);

// API-level HTTP error — the external service returned 4xx/5xx
// Use when you have the raw error object from httpRequest catch
throw new NodeApiError(this.getNode(), error, { itemIndex: i });
```

---

## 2. continueOnFail Pattern

Always wrap the per-item logic in try/catch and respect `continueOnFail()`:

```typescript
for (let i = 0; i < items.length; i++) {
  try {
    const response = await this.helpers.httpRequest({ ... });
    returnData.push({ json: response, pairedItem: { item: i } });

  } catch (error) {
    if (this.continueOnFail()) {
      // Package the error as data and continue to the next item
      returnData.push({
        json: {
          error: error.message,
          statusCode: error.statusCode ?? undefined,
          // Include original input to help with debugging downstream
          input: items[i].json,
        },
        pairedItem: { item: i },
      });
      continue;
    }

    // Stop the workflow — throw with the item index for UI highlighting
    if (error.statusCode) {
      throw new NodeApiError(this.getNode(), error, { itemIndex: i });
    }
    throw new NodeOperationError(this.getNode(), error.message, { itemIndex: i });
  }
}
```

> `continueOnFail()` respects the user's "On Error" setting in the node's Settings tab. Always handle it — workflows that swallow errors silently are hard to debug.

---

## 3. Throwing with Context

The `itemIndex` option highlights the failing item in the n8n UI, making it much easier for users to debug:

```typescript
// Without context — user doesn't know which item failed
throw new NodeOperationError(this.getNode(), 'User ID is required');

// With context — UI highlights item 3 in red
throw new NodeOperationError(
  this.getNode(),
  'User ID is required',
  { itemIndex: i },
);

// With description (shown as detail in the error panel)
throw new NodeOperationError(
  this.getNode(),
  'Invalid date format',
  {
    itemIndex: i,
    description: 'Expected ISO 8601 format (e.g. 2024-01-15T10:30:00Z)',
  },
);
```

---

## 4. Validating Parameters

Validate before the loop to catch config errors early (cheaper than discovering them mid-loop):

```typescript
async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
  // Validate required credentials
  const credentials = await this.getCredentials('myServiceApi');
  if (!credentials.apiToken) {
    throw new NodeOperationError(this.getNode(), 'API Token is missing from credentials');
  }

  // Validate node-level parameters (use index 0 for params that don't vary per item)
  const resource  = this.getNodeParameter('resource', 0) as string;
  const operation = this.getNodeParameter('operation', 0) as string;

  const items = this.getInputData();
  const returnData: INodeExecutionData[] = [];

  for (let i = 0; i < items.length; i++) {
    try {
      // Validate per-item parameters
      const url = this.getNodeParameter('url', i) as string;
      if (!url.startsWith('https://')) {
        throw new NodeOperationError(
          this.getNode(),
          'URL must start with https://',
          { itemIndex: i },
        );
      }

      // ... rest of execute logic
    } catch (error) {
      if (this.continueOnFail()) {
        returnData.push({ json: { error: error.message }, pairedItem: { item: i } });
        continue;
      }
      throw error;
    }
  }

  return [returnData];
}
```

---

## 5. API Error Response Handling

Extract useful information from HTTP error responses:

```typescript
} catch (error) {
  // n8n's httpRequest throws errors with these properties:
  // error.statusCode  → HTTP status (400, 401, 403, 404, 429, 500...)
  // error.message     → Error message string
  // error.response    → Raw response object (may have .body)

  if (this.continueOnFail()) {
    returnData.push({
      json: {
        error: error.message,
        statusCode: error.statusCode,
        // Try to extract the API's error message if available
        apiError: error.response?.body
          ? (typeof error.response.body === 'string'
              ? error.response.body
              : JSON.stringify(error.response.body))
          : undefined,
      },
      pairedItem: { item: i },
    });
    continue;
  }

  // Map common status codes to helpful messages
  if (error.statusCode === 401) {
    throw new NodeOperationError(
      this.getNode(),
      'Authentication failed — check your credentials',
      { itemIndex: i },
    );
  }
  if (error.statusCode === 429) {
    throw new NodeOperationError(
      this.getNode(),
      'Rate limit exceeded — reduce request frequency or add a wait between items',
      { itemIndex: i },
    );
  }

  throw new NodeApiError(this.getNode(), error, { itemIndex: i });
}
```
