# Node Properties: UI Fields Reference

`properties` defines everything the user sees in the node panel.

## Table of Contents
1. [All field types](#1-all-field-types)
2. [displayOptions — conditional visibility](#2-displayoptions)
3. [collection — optional grouped extras](#3-collection)
4. [fixedCollection — repeatable groups](#4-fixedcollection)
5. [noDataExpression, required, placeholder](#5-modifiers)
6. [subtitle — dynamic node header text](#6-subtitle)

---

## 1. All Field Types

```typescript
// ── String ────────────────────────────────────────────────────────
{ displayName: 'Name', name: 'name', type: 'string', default: '' }

// ── Password (masked) ────────────────────────────────────────────
{
  displayName: 'API Key', name: 'apiKey', type: 'string',
  typeOptions: { password: true }, default: ''
}

// ── Multi-line text ──────────────────────────────────────────────
{
  displayName: 'Body', name: 'body', type: 'string',
  typeOptions: { rows: 4 }, default: ''
}

// ── Number ───────────────────────────────────────────────────────
{
  displayName: 'Limit', name: 'limit', type: 'number',
  default: 50, typeOptions: { minValue: 1, maxValue: 1000 }
}

// ── Boolean toggle ───────────────────────────────────────────────
{ displayName: 'Active', name: 'active', type: 'boolean', default: false }

// ── Dropdown (single select) ─────────────────────────────────────
{
  displayName: 'Method', name: 'method', type: 'options',
  options: [
    { name: 'GET',  value: 'GET' },
    { name: 'POST', value: 'POST' },
  ],
  default: 'GET',
}

// ── Multi-select (returns array of values) ───────────────────────
{
  displayName: 'Events', name: 'events', type: 'multiOptions',
  options: [
    { name: 'Created', value: 'created' },
    { name: 'Updated', value: 'updated' },
    { name: 'Deleted', value: 'deleted' },
  ],
  default: ['created'],
}

// ── JSON editor ──────────────────────────────────────────────────
{ displayName: 'Body', name: 'body', type: 'json', default: '{}' }

// ── Color picker ─────────────────────────────────────────────────
{ displayName: 'Color', name: 'color', type: 'color', default: '#ff0000' }

// ── DateTime ─────────────────────────────────────────────────────
{ displayName: 'Start Date', name: 'startDate', type: 'dateTime', default: '' }

// ── Hidden (not shown in UI, used for internal values) ───────────
{ displayName: 'Internal', name: 'internal', type: 'hidden', default: 'fixedValue' }
```

Getting values in `execute()`:
```typescript
const name     = this.getNodeParameter('name', i) as string;
const limit    = this.getNodeParameter('limit', i, 50) as number;   // 50 = fallback
const active   = this.getNodeParameter('active', i) as boolean;
const method   = this.getNodeParameter('method', i) as string;
const events   = this.getNodeParameter('events', i) as string[];
const body     = this.getNodeParameter('body', i, '{}') as string;
const parsed   = JSON.parse(body);
```

---

## 2. displayOptions

Controls when a field is visible. The most important pattern in multi-operation nodes.

```typescript
// Show only when resource = 'user' AND operation = 'create'
{
  displayName: 'Email',
  name: 'email',
  type: 'string',
  default: '',
  displayOptions: {
    show: {
      resource: ['user'],
      operation: ['create', 'update'],   // visible for multiple operations
    },
  },
}

// Hide when returnAll = true
{
  displayName: 'Limit',
  name: 'limit',
  type: 'number',
  default: 50,
  displayOptions: {
    show: { returnAll: [false] },
  },
}

// Hide for specific values (inverse)
{
  displayName: 'Format',
  name: 'format',
  type: 'options',
  default: 'json',
  displayOptions: {
    hide: {
      operation: ['delete'],
    },
  },
}
```

> ⚠️ `displayOptions` only controls UI visibility — the field still exists in the schema. The value is just not shown to the user. Fields not shown use their `default` value.

---

## 3. collection

A collapsible group of optional fields. Good for "Additional Options" or "Filters".

```typescript
{
  displayName: 'Additional Options',
  name: 'options',
  type: 'collection',
  placeholder: 'Add Option',
  default: {},
  options: [
    {
      displayName: 'Timeout (ms)',
      name: 'timeout',
      type: 'number',
      default: 30000,
      description: 'Request timeout in milliseconds',
    },
    {
      displayName: 'Follow Redirects',
      name: 'followRedirects',
      type: 'boolean',
      default: true,
    },
    {
      displayName: 'Response Format',
      name: 'responseFormat',
      type: 'options',
      options: [
        { name: 'Automatic', value: 'auto' },
        { name: 'JSON',      value: 'json' },
        { name: 'Text',      value: 'text' },
      ],
      default: 'auto',
    },
  ],
}
```

In `execute()`:
```typescript
const options = this.getNodeParameter('options', i, {}) as {
  timeout?: number;
  followRedirects?: boolean;
  responseFormat?: string;
};
const timeout = options.timeout ?? 30000;
```

---

## 4. fixedCollection

Repeatable rows of grouped fields. The key pattern for things like custom headers, key-value pairs, or address entries.

```typescript
{
  displayName: 'Custom Headers',
  name: 'customHeaders',
  type: 'fixedCollection',
  placeholder: 'Add Header',
  typeOptions: { multipleValues: true },   // ← allows adding multiple rows
  default: {},
  options: [
    {
      displayName: 'Header',
      name: 'header',                        // ← key used to access values
      values: [
        {
          displayName: 'Name',
          name: 'name',
          type: 'string',
          default: '',
          placeholder: 'X-Custom-Header',
        },
        {
          displayName: 'Value',
          name: 'value',
          type: 'string',
          default: '',
        },
      ],
    },
  ],
}
```

In `execute()`:
```typescript
const customHeaders = this.getNodeParameter('customHeaders', i, {}) as {
  header?: Array<{ name: string; value: string }>;
};

const extraHeaders: Record<string, string> = {};
for (const h of (customHeaders.header ?? [])) {
  extraHeaders[h.name] = h.value;
}

// Merge with base headers
const headers = { Authorization: `Bearer ${token}`, ...extraHeaders };
```

### fixedCollection without multipleValues (exactly one set)

```typescript
{
  displayName: 'Coordinates',
  name: 'coordinates',
  type: 'fixedCollection',
  // NO typeOptions.multipleValues
  default: {},
  options: [
    {
      displayName: 'Location',
      name: 'location',
      values: [
        { displayName: 'Latitude',  name: 'lat', type: 'number', default: 0 },
        { displayName: 'Longitude', name: 'lng', type: 'number', default: 0 },
      ],
    },
  ],
}
```

In `execute()`:
```typescript
const coords = this.getNodeParameter('coordinates.location', i, {}) as {
  lat: number;
  lng: number;
};
```

---

## 5. Modifiers

```typescript
{
  displayName: 'Resource',
  name: 'resource',
  type: 'options',
  noDataExpression: true,    // ← prevents the "expression" toggle on this field
                              //   always use this on resource/operation selectors
  options: [...],
  default: 'user',
  required: true,             // ← shows red asterisk, blocks execution if empty
  placeholder: 'Enter name', // ← grey placeholder text
  description: 'The resource to work with',   // ← shown as tooltip
  hint: 'Use the resource ID from the URL',   // ← shown below field
}
```

---

## 6. Subtitle

Shows dynamic text below the node name in the canvas (helps users see what the node is doing at a glance):

```typescript
description: INodeTypeDescription = {
  // ...
  subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
  // Shows e.g. "create: user" under the node name
}
```

Other useful subtitle patterns:
```typescript
subtitle: '={{$parameter["resource"]}}'
subtitle: '={{$parameter["url"]}}'
subtitle: '={{$parameter["event"]}}'
```
