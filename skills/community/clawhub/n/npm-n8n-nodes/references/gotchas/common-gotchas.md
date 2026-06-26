# Common Gotchas and Silent Failures

These are the issues that don't throw obvious errors — they just make your node broken, invisible, or wrong in subtle ways.

## Table of Contents
1. [Registration and discovery failures](#1-registration-and-discovery-failures)
2. [Credential name mismatches (silent!)](#2-credential-name-mismatches)
3. [pairedItem missing — expressions break silently](#3-paireditem-missing)
4. [json must be an object, never an array or primitive](#4-json-must-be-an-object)
5. [dist/ not committed or not built in CI](#5-dist-not-committed-or-built)
6. [Icons not copied to dist/](#6-icons-not-copied)
7. [Linting failures block n8n Cloud installation](#7-linting-failures)
8. [noDataExpression missing — expressions appear on wrong fields](#8-nodataexpression)
9. [OAuth2 token caching bug](#9-oauth2-token-caching)
10. [continueOnFail not handled — error swallowed silently](#10-continuenonfail-not-handled)
11. [TypeScript strict mode catches these — enable it](#11-typescript-strict-mode)
12. [Version mismatch — wrong node version on old workflows](#12-version-mismatch)

---

## 1. Registration and Discovery Failures

**Symptom:** Node doesn't appear in n8n's node picker.

**Causes and fixes:**

```json
// ❌ Wrong — missing the required keyword
"keywords": ["n8n", "automation"]

// ✅ Correct
"keywords": ["n8n-community-node-package"]
```

```json
// ❌ Wrong — pointing at source TypeScript files
"n8n": {
  "nodes": ["nodes/MyNode/MyNode.node.ts"]
}

// ✅ Correct — must point at compiled JavaScript in dist/
"n8n": {
  "nodes": ["dist/nodes/MyNode/MyNode.node.js"]
}
```

```json
// ❌ Wrong — path doesn't match actual folder/file name (case-sensitive!)
"nodes": ["dist/nodes/mynode/MyNode.node.js"]

// ✅ Correct — path must exactly match the filesystem
"nodes": ["dist/nodes/MyNode/MyNode.node.js"]
```

---

## 2. Credential Name Mismatches (Silent!)

This is the most common silent failure. The credential loads but never applies.

```typescript
// In credentials file:
export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';    // ← THIS string must match exactly
}

// In node file:
// ❌ Wrong — different casing
const creds = await this.getCredentials('MyServiceApi');
const creds = await this.getCredentials('myserviceapi');
const creds = await this.getCredentials('my-service-api');

// ✅ Correct — exact match, case-sensitive
const creds = await this.getCredentials('myServiceApi');
```

Also check the `credentials` array in the node description:
```typescript
credentials: [
  {
    name: 'myServiceApi',   // ← must match credential's `name` property
    required: true,
  },
],
```

And the `n8n.credentials` entry in `package.json`:
```json
"credentials": ["dist/credentials/MyServiceApi.credentials.js"]
//                                 ^ filename must match the TypeScript class file
```

---

## 3. pairedItem Missing — Expressions Break Silently

**Symptom:** `{{ $('Previous Node').item.json.field }}` returns wrong data or undefined. Users won't know why.

```typescript
// ❌ Wrong — pairedItem missing
returnData.push({ json: response });

// ✅ Correct — always include pairedItem
returnData.push({ json: response, pairedItem: { item: i } });
```

If you push multiple items for one input item:
```typescript
for (const subItem of responseArray) {
  returnData.push({
    json: subItem,
    pairedItem: { item: i },   // ← all sub-items link back to the same input item
  });
}
```

---

## 4. json Must Be an Object, Never an Array or Primitive

**Symptom:** n8n throws a confusing internal error or the node output looks wrong.

```typescript
// ❌ Wrong — json is an array
returnData.push({ json: [1, 2, 3], pairedItem: { item: i } });

// ❌ Wrong — json is a string or number
returnData.push({ json: 'hello' as any, pairedItem: { item: i } });

// ✅ Correct — wrap arrays
returnData.push({ json: { items: [1, 2, 3] }, pairedItem: { item: i } });

// ✅ Correct — or push each element separately
for (const element of responseArray) {
  returnData.push({ json: element as IDataObject, pairedItem: { item: i } });
}

// ✅ Correct — wrap primitives
returnData.push({ json: { value: 'hello' }, pairedItem: { item: i } });
```

---

## 5. dist/ Not Committed or Built in CI

**Symptom:** Works locally, broken when installed from npm.

npm only ships files listed in `"files"`. If `"files": ["dist"]` and `dist/` is gitignored and not built in CI, your published package will be empty.

**Fix for GitHub Actions:**
```yaml
# In publish.yml — always build before publishing
- name: Build
  run: npm run build      # ← must be here
- name: Publish
  run: npm publish --access public
```

The `prepublishOnly` script in package.json also helps: `"prepublishOnly": "npm run build && npm run lint"` — it runs automatically before `npm publish`.

---

## 6. Icons Not Copied to dist/

**Symptom:** Node appears with a broken/missing icon.

TypeScript compiler (`tsc`) copies `.ts` files only. SVG/PNG icons need to be copied separately by gulpfile:

```bash
# Check: does dist/ have your SVG?
ls dist/nodes/MyNode/
# Should show: MyNode.node.js  MyNode.node.d.ts  mynode.svg

# If SVG is missing, run:
npx gulp build:icons
# OR:
npm run build   # (if build script includes gulp)
```

And verify the icon path in your node matches exactly:
```typescript
icon: 'file:mynode.svg',   // file must exist at dist/nodes/MyNode/mynode.svg
```

---

## 7. Linting Failures Block n8n Cloud Installation

n8n Cloud validates `eslint-plugin-n8n-nodes-base` rules before installing community nodes. Linting errors = installation failure.

```bash
# Always check before publishing
npm run lint

# Auto-fix what's fixable
npm run lintfix

# Common errors:
# - "node-class-description-missing-subtitle" — add subtitle field
# - "node-param-description-missing-final-period" — end descriptions with "."
# - "node-param-display-name-miscased" — use Title Case for displayName
# - "cred-class-field-name-unsuffixed" — credential name must end with "Api"
```

---

## 8. noDataExpression Missing on Selectors

**Symptom:** User accidentally types an expression into the Resource or Operation dropdown, breaking the node UI.

```typescript
// ❌ Wrong — user can put expressions into resource/operation fields
{
  displayName: 'Resource',
  name: 'resource',
  type: 'options',
  options: [...],
  default: 'user',
}

// ✅ Correct — prevent expression mode on structural selectors
{
  displayName: 'Resource',
  name: 'resource',
  type: 'options',
  noDataExpression: true,   // ← always add this to resource/operation fields
  options: [...],
  default: 'user',
}
```

---

## 9. OAuth2 Token Caching Bug

**Symptom:** OAuth2 node works on first run, fails after token expiry.

```typescript
// ❌ Wrong — storing token outside getCredentials causes stale token issues
let cachedToken: string;

async execute() {
  if (!cachedToken) {
    const creds = await this.getCredentials('myOAuth2Api');
    cachedToken = (creds.oauthTokenData as any).access_token;
  }
  // cachedToken may be expired!
}

// ✅ Correct — always call getCredentials() fresh inside execute()
// n8n handles refresh automatically and returns the current valid token
async execute() {
  const creds = await this.getCredentials('myOAuth2Api');
  const token = (creds.oauthTokenData as { access_token: string }).access_token;
  // token is always fresh — n8n refreshed it before returning
}
```

---

## 10. continueOnFail Not Handled

**Symptom:** When user enables "Continue On Error", the node throws anyway and halts the workflow.

```typescript
// ❌ Wrong — error always stops workflow
} catch (error) {
  throw new NodeOperationError(this.getNode(), error.message);
}

// ✅ Correct — respect user's setting
} catch (error) {
  if (this.continueOnFail()) {
    returnData.push({ json: { error: error.message }, pairedItem: { item: i } });
    continue;
  }
  throw new NodeOperationError(this.getNode(), error, { itemIndex: i });
}
```

---

## 11. TypeScript Strict Mode Catches These — Enable It

```json
// tsconfig.json — always use strict: true
{
  "compilerOptions": {
    "strict": true    // ← catches null issues, implicit any, and more
  }
}
```

Common strict-mode patterns:
```typescript
// Instead of: const name = response.name
const name = response.name as string;        // explicit cast
const name = (response as IDataObject).name as string;

// Instead of: credentials.apiToken
const token = credentials.apiToken as string;  // TypeScript won't infer the type
```

---

## 12. Version Mismatch on Old Workflows

**Symptom:** Existing workflows use old node behavior; updating the package breaks them.

When you bump the npm package version but don't increment the node's `version` field, all instances in existing workflows silently use the new behavior — even if you changed output structure.

```typescript
// After a breaking change, ALWAYS increment version in the node description:
description: INodeTypeDescription = {
  version: [1, 2],          // ← add the new version
  defaultVersion: 2,         // ← new nodes get v2
}
// And add @version displayOptions to fields that changed
```

See `references/concepts/node-versioning.md` for the full pattern.
