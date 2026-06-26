# Common Mistakes

Error catalog for n8n node development. See [SKILL.md](../SKILL.md) for main skill.

---

## File Structure Errors

### 1. Class name doesn't match filename

**Wrong:**
```
File: MyService.node.ts
Class: export class MyServiceNode implements INodeType  // ← "Node" suffix doesn't match
```

**Fix:** Class name must exactly match the filename (minus `.node.ts`):
```
File: MyService.node.ts
Class: export class MyService implements INodeType      // ✓
```

### 2. Wrong npm package prefix

**Wrong:** `"name": "myservice-n8n-nodes"` or `"name": "n8n-myservice"`

**Fix:** Package name must start with `n8n-nodes-`:
```json
"name": "n8n-nodes-myservice"
```

### 3. Missing codex file

Every node needs a `.node.json` codex file alongside the `.node.ts` file. Without it, the node won't appear in search or have proper categorization.

### 4. Wrong paths in package.json n8n config

**Wrong:** Pointing to source files:
```json
"nodes": ["nodes/MyService/MyService.node.ts"]
```

**Fix:** Point to compiled output:
```json
"nodes": ["dist/nodes/MyService/MyService.node.js"]
```

---

## Description Errors

### 5. Missing noDataExpression on selectors

**Wrong:**
```typescript
{ displayName: 'Resource', name: 'resource', type: 'options', /* ... */ }
```

**Fix:** Always set `noDataExpression: true` on resource and operation selectors:
```typescript
{ displayName: 'Resource', name: 'resource', type: 'options', noDataExpression: true, /* ... */ }
```

### 6. Missing action field on operations

**Wrong:**
```typescript
options: [
  { name: 'Create', value: 'create' },
]
```

**Fix:** Every operation option needs an `action` field for the node action list:
```typescript
options: [
  { name: 'Create', value: 'create', action: 'Create a contact' },
]
```

### 7. Using string 'main' instead of NodeConnectionType

**Wrong:**
```typescript
inputs: ['main'],
outputs: ['main'],
```

**Fix:**
```typescript
inputs: [NodeConnectionType.Main],
outputs: [NodeConnectionType.Main],
```

### 8. Trigger node with non-empty inputs

**Wrong:**
```typescript
// Trigger node:
inputs: [NodeConnectionType.Main],  // ← Triggers don't have inputs
```

**Fix:**
```typescript
inputs: [],  // Trigger nodes have NO inputs
```

---

## Execute Method Errors

### 9. Missing continueOnFail handling

**Wrong:**
```typescript
for (let i = 0; i < items.length; i++) {
  const data = await apiRequest.call(this, 'GET', '/items');
  returnData.push(...data);  // ← No error handling, no item linking
}
```

**Fix:** Wrap each item in try/catch with `continueOnFail()`:
```typescript
for (let i = 0; i < items.length; i++) {
  try {
    const data = await apiRequest.call(this, 'GET', '/items');
    const executionData = this.helpers.constructExecutionMetaData(
      this.helpers.returnJsonArray(data),
      { itemData: { item: i } },
    );
    returnData.push(...executionData);
  } catch (error) {
    if (this.continueOnFail()) {
      returnData.push(...this.helpers.constructExecutionMetaData(
        this.helpers.returnJsonArray({ error: (error as Error).message }),
        { itemData: { item: i } },
      ));
      continue;
    }
    throw error;
  }
}
```

### 10. Missing constructExecutionMetaData

**Wrong:**
```typescript
returnData.push(...this.helpers.returnJsonArray(responseData));  // ← No item linking
```

**Fix:** Always wrap with `constructExecutionMetaData` for proper item tracking:
```typescript
const executionData = this.helpers.constructExecutionMetaData(
  this.helpers.returnJsonArray(responseData),
  { itemData: { item: i } },
);
returnData.push(...executionData);
```

### 11. Not returning nested array

**Wrong:**
```typescript
return returnData;  // ← Must be INodeExecutionData[][]
```

**Fix:**
```typescript
return [returnData];  // ← Wrap in outer array
```

---

## Credential Errors

### 12. Wrong credential expression syntax

**Wrong:**
```typescript
headers: { Authorization: '={{$credential.apiKey}}' }   // ← singular
```

**Fix:**
```typescript
headers: { Authorization: '={{$credentials.apiKey}}' }   // ← plural: $credentials
```

### 13. Missing password typeOptions on secrets

**Wrong:**
```typescript
{ displayName: 'API Key', name: 'apiKey', type: 'string', default: '' }
```

**Fix:**
```typescript
{ displayName: 'API Key', name: 'apiKey', type: 'string',
  typeOptions: { password: true }, default: '' }
```

### 14. Credential not registered in package.json

Even if the credential file exists, it won't load unless listed:
```json
"n8n": {
  "credentials": ["dist/credentials/MyServiceApi.credentials.js"]
}
```

---

## Declarative Node Errors

### 15. Including execute() in a declarative node

If `requestDefaults` is present, n8n uses the routing engine. An `execute()` method will be ignored. Either use routing OR execute, not both.

### 16. Missing routing on operation options

**Wrong (declarative):**
```typescript
options: [{ name: 'Create', value: 'create', action: 'Create item' }]  // ← No routing
```

**Fix:**
```typescript
options: [{
  name: 'Create', value: 'create', action: 'Create item',
  routing: { request: { method: 'POST', url: '/items' } },
}]
```

---

## Quick Fix Reference

| Error | Fix |
|-------|-----|
| Node not appearing in editor | Check `package.json` n8n.nodes paths, rebuild, restart |
| "Cannot find credential" | Check credential `name` matches between node and credential file |
| Empty response data | Check `postReceive` rootProperty extracts correct JSON path |
| Item linking broken | Add `constructExecutionMetaData` with `{ itemData: { item: i } }` |
| displayOptions not working | Verify resource/operation values match exactly (case-sensitive) |
| Expression not resolving | Use `=` prefix: `'=/path/{{$parameter.id}}'` not `'/path/{{$parameter.id}}'` |
