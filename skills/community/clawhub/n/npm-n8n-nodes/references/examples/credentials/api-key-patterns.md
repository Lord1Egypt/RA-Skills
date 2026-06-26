# Credential Patterns: API Key / Token Auth

All credential files implement `ICredentialType` and live in `credentials/`.

The credential `name` field **must exactly match** the string you pass to `getCredentials('...')` in your node.

## Table of Contents
1. [Bearer Token (Authorization header)](#1-bearer-token)
2. [Custom Header (X-API-Key etc.)](#2-custom-header)
3. [Query String Key](#3-query-string-key)
4. [Multi-field / manual inject](#4-multi-field--manual-inject)
5. [Credential test reference](#5-credential-test-reference)

---

## 1. Bearer Token

Standard `Authorization: Bearer <token>` — used by most modern APIs.

```typescript
import type {
  IAuthenticateGeneric,
  ICredentialTestRequest,
  ICredentialType,
  INodeProperties,
} from 'n8n-workflow';

export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';                         // matches getCredentials('myServiceApi')
  displayName = 'My Service API';
  documentationUrl = 'https://docs.myservice.com/auth';

  properties: INodeProperties[] = [
    {
      displayName: 'API Token',
      name: 'apiToken',
      type: 'string',
      typeOptions: { password: true },            // ← always mask secrets
      default: '',
      required: true,
      placeholder: 'sk-xxxxxxxxxxxxxxxx',
    },
  ];

  // Auto-injected into every request when credential has an authenticate block.
  // Works automatically for declarative nodes. For programmatic nodes, read manually.
  authenticate: IAuthenticateGeneric = {
    type: 'generic',
    properties: {
      headers: { Authorization: '=Bearer {{$credentials.apiToken}}' },
    },
  };

  // Validates credentials when user clicks "Test" in the credentials UI
  test: ICredentialTestRequest = {
    request: {
      baseURL: 'https://api.myservice.com',
      url: '/me',
    },
  };
}
```

In `execute()`:
```typescript
const creds = await this.getCredentials('myServiceApi');
headers: { Authorization: `Bearer ${creds.apiToken}` }
```

---

## 2. Custom Header

APIs that use `X-API-Key`, `X-Auth-Token`, or similar.

```typescript
export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';
  displayName = 'My Service API';

  properties: INodeProperties[] = [
    {
      displayName: 'API Key',
      name: 'apiKey',
      type: 'string',
      typeOptions: { password: true },
      default: '',
      required: true,
    },
    {
      // Optional — lets users point at self-hosted instances
      displayName: 'Base URL',
      name: 'baseUrl',
      type: 'string',
      default: 'https://api.myservice.com',
      required: true,
    },
  ];

  authenticate: IAuthenticateGeneric = {
    type: 'generic',
    properties: {
      headers: { 'X-API-Key': '={{$credentials.apiKey}}' },
    },
  };

  test: ICredentialTestRequest = {
    request: {
      baseURL: '={{$credentials.baseUrl}}',
      url: '/health',
    },
  };
}
```

---

## 3. Query String Key

APIs that pass the key as a URL parameter (`?api_key=...`).

```typescript
export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';
  displayName = 'My Service API';

  properties: INodeProperties[] = [
    {
      displayName: 'API Key',
      name: 'apiKey',
      type: 'string',
      typeOptions: { password: true },
      default: '',
      required: true,
    },
  ];

  authenticate: IAuthenticateGeneric = {
    type: 'generic',
    properties: {
      qs: { api_key: '={{$credentials.apiKey}}' },  // appended to every request URL
    },
  };
}
```

---

## 4. Multi-Field / Manual Inject

When you need to combine multiple values (e.g. Client ID + Secret → Basic Auth header), or need an environment selector.

```typescript
export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';
  displayName = 'My Service API';

  properties: INodeProperties[] = [
    {
      displayName: 'Client ID',
      name: 'clientId',
      type: 'string',
      default: '',
      required: true,
    },
    {
      displayName: 'Client Secret',
      name: 'clientSecret',
      type: 'string',
      typeOptions: { password: true },
      default: '',
      required: true,
    },
    {
      displayName: 'Environment',
      name: 'environment',
      type: 'options',
      options: [
        { name: 'Production', value: 'https://api.myservice.com' },
        { name: 'Sandbox',    value: 'https://sandbox.myservice.com' },
      ],
      default: 'https://api.myservice.com',
    },
  ];
  // No authenticate block — read all values manually in execute()
}
```

In `execute()`:
```typescript
const creds   = await this.getCredentials('myServiceApi');
const baseURL  = creds.environment as string;
const encoded  = Buffer.from(`${creds.clientId}:${creds.clientSecret}`).toString('base64');
const headers  = { Authorization: `Basic ${encoded}` };
```

---

## 5. Credential Test Reference

The `test` block powers the "Test" button in the credentials UI.

```typescript
// Simple: just hit an endpoint and expect 200
test: ICredentialTestRequest = {
  request: {
    baseURL: 'https://api.myservice.com',
    url: '/me',
  },
};

// With custom error detection (looks for error field in 200 response body)
test: ICredentialTestRequest = {
  request: {
    baseURL: 'https://api.myservice.com',
    url: '/validate',
  },
  rules: [
    {
      type: 'responseSuccessBody',
      properties: {
        key: 'error',
        value: 'unauthorized',
        message: 'Invalid API token. Check your credentials.',
      },
    },
  ],
};

// Dynamic baseURL from credentials
test: ICredentialTestRequest = {
  request: {
    baseURL: '={{$credentials.baseUrl}}',
    url: '/health',
  },
};
```

### Rule types
| Type | What it checks |
|---|---|
| `responseCode` | Response HTTP status code equals expected value |
| `responseSuccessBody` | A key in the response body matches a bad value (marks as failed) |

### Custom test via node method

For complex validation (e.g., connecting to a database), define a `credentialTest` method in the node class instead:

```typescript
// In the credentials file:
// (no test block — the method name links them)

// In the node file:
methods = {
  credentialTest: {
    async testMyServiceApi(
      this: ICredentialTestFunctions,
      credential: ICredentialsDecrypted,
    ): Promise<INodeCredentialTestResult> {
      const creds = credential.data as { apiToken: string };
      try {
        await this.helpers.request({
          method: 'GET',
          url: 'https://api.myservice.com/me',
          headers: { Authorization: `Bearer ${creds.apiToken}` },
        });
        return { status: 'OK', message: 'Connection successful!' };
      } catch (error) {
        return { status: 'Error', message: `Connection failed: ${error.message}` };
      }
    },
  },
};
```
