# Data Flow and pairedItem Tracking

## Why pairedItem Matters

n8n uses `pairedItem` to track which output item came from which input item. Without it:
- Expressions like `{{ $('Previous Node').item.json.id }}` silently return wrong data
- The "item linking" arrows in the UI don't draw
- Debugging becomes much harder

**Always include `pairedItem: { item: i }` on every `returnData.push()`.**

## Table of Contents
1. [Basic pairedItem usage](#1-basic-paireditem)
2. [One-to-many — multiple outputs per input item](#2-one-to-many)
3. [Many-to-one — aggregating items](#3-many-to-one)
4. [Accessing input item data in execute()](#4-accessing-input-data)
5. [Passing input data through to output](#5-passing-data-through)
6. [n8n data structure](#6-n8n-data-structure)

---

## 1. Basic pairedItem

```typescript
for (let i = 0; i < items.length; i++) {
  const response = await this.helpers.httpRequest({ ... });

  returnData.push({
    json: response,
    pairedItem: { item: i },   // ← always include, i = index in input items array
  });
}
```

---

## 2. One-to-Many (multiple outputs per input)

When one input item produces multiple output items (e.g., getting all posts for a user):

```typescript
for (let i = 0; i < items.length; i++) {
  const userId = items[i].json.id as string;

  const posts = await this.helpers.httpRequest({
    method: 'GET',
    url: `https://api.example.com/users/${userId}/posts`,
    headers: authHeader,
  }) as IDataObject[];

  for (const post of posts) {
    returnData.push({
      json: post,
      pairedItem: { item: i },   // all posts link back to the same input item
    });
  }
}
```

---

## 3. Many-to-One (aggregating)

When combining all input items into a single output (e.g., batch create):

```typescript
// Collect all input items
const allIds = items.map((item) => item.json.id as string);

// Make one API call
const response = await this.helpers.httpRequest({
  method: 'POST',
  url: 'https://api.example.com/batch',
  body: { ids: allIds },
  headers: authHeader,
});

// Single output — pair with all input items
returnData.push({
  json: response,
  pairedItem: items.map((_, index) => ({ item: index })),  // array of pairings
});
```

---

## 4. Accessing Input Data in execute()

```typescript
const items = this.getInputData();

for (let i = 0; i < items.length; i++) {
  // Access a field from the input JSON
  const name  = items[i].json.name as string;
  const email = items[i].json.email as string;
  const id    = items[i].json.id as number;

  // Access nested fields
  const city    = (items[i].json.address as IDataObject)?.city as string;
  const tagList = items[i].json.tags as string[];

  // Check if a field exists
  if (items[i].json.userId === undefined) {
    throw new NodeOperationError(
      this.getNode(),
      'Input item is missing required field "userId"',
      { itemIndex: i },
    );
  }

  // Access binary data from input
  if (items[i].binary?.attachment) {
    const buffer = await this.helpers.getBinaryDataBuffer(i, 'attachment');
    // use buffer...
  }
}
```

---

## 5. Passing Data Through

Common patterns for combining API response with original input data:

```typescript
// Merge response with original input fields
returnData.push({
  json: {
    ...items[i].json,        // original input fields
    ...response,             // API response fields (overwrites same-named keys)
    _nodeProcessed: true,    // add a marker field
  },
  pairedItem: { item: i },
});

// Keep only specific fields from response
const { id, status, updatedAt } = response as { id: string; status: string; updatedAt: string };
returnData.push({
  json: { id, status, updatedAt, originalInput: items[i].json },
  pairedItem: { item: i },
});

// Forward binary data from input to output unchanged
returnData.push({
  json: { ...response },
  binary: items[i].binary,   // pass through any binary attachments
  pairedItem: { item: i },
});
```

---

## 6. n8n Data Structure

Every item flowing through n8n has this shape:

```typescript
interface INodeExecutionData {
  json: IDataObject;              // the data (always required, can be {})
  binary?: {                      // optional file attachments
    [key: string]: IBinaryData;   // key is e.g. 'data', 'attachment', 'image'
  };
  pairedItem?: {
    item: number;                 // index in the input items array
  } | Array<{ item: number }>;   // or array for many-to-one
  error?: NodeOperationError;    // only set when continueOnFail pushes an error item
}
```

> `json` must always be a plain object `{}` — not an array, not a primitive. If your API returns an array, wrap it: `json: { items: responseArray }`, or push each element as a separate item.

```typescript
// API returns an array → push each element separately
const list = response as IDataObject[];
for (const item of list) {
  returnData.push({ json: item, pairedItem: { item: i } });
}

// OR wrap the array
returnData.push({
  json: { results: list, count: list.length },
  pairedItem: { item: i },
});
```
