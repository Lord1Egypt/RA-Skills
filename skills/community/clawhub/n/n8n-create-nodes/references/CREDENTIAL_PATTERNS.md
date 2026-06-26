# Credential Patterns

Reference for creating n8n credential types. See [SKILL.md](../SKILL.md) for main skill.

---

## Credential Class Structure

```typescript
import {
  IAuthenticateGeneric,
  ICredentialTestRequest,
  ICredentialType,
  INodeProperties,
} from 'n8n-workflow';

export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';                 // camelCase, referenced in node's credentials[]
  displayName = 'My Service API';        // Shown in credential selector
  documentationUrl = 'myService';        // Links to n8n docs or custom URL
  properties: INodeProperties[] = [];    // Auth fields shown to user
  authenticate: IAuthenticateGeneric;    // How auth is injected into requests
  test: ICredentialTestRequest;          // Endpoint to verify credentials
}
```

---

## Pattern 1: API Key in Header

```typescript
export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';
  displayName = 'My Service API';
  properties: INodeProperties[] = [
    {
      displayName: 'API Key',
      name: 'apiKey',
      type: 'string',
      typeOptions: { password: true },   // ALWAYS mask secrets
      default: '',
    },
  ];
  authenticate: IAuthenticateGeneric = {
    type: 'generic',
    properties: {
      headers: {
        Authorization: '={{"Bearer " + $credentials.apiKey}}',
      },
    },
  };
  test: ICredentialTestRequest = {
    request: {
      baseURL: 'https://api.myservice.com',
      url: '/me',
    },
  };
}
```

## Pattern 2: API Key in Query String

```typescript
authenticate: IAuthenticateGeneric = {
  type: 'generic',
  properties: {
    qs: {
      api_key: '={{$credentials.apiKey}}',
    },
  },
};
```

## Pattern 3: API Key in Custom Header

```typescript
properties: INodeProperties[] = [
  {
    displayName: 'API Key',
    name: 'apiKey',
    type: 'string',
    typeOptions: { password: true },
    default: '',
  },
];
authenticate: IAuthenticateGeneric = {
  type: 'generic',
  properties: {
    headers: {
      'X-API-Key': '={{$credentials.apiKey}}',
    },
  },
};
```

## Pattern 4: Basic Auth

```typescript
properties: INodeProperties[] = [
  {
    displayName: 'Username',
    name: 'username',
    type: 'string',
    default: '',
  },
  {
    displayName: 'Password',
    name: 'password',
    type: 'string',
    typeOptions: { password: true },
    default: '',
  },
];
authenticate: IAuthenticateGeneric = {
  type: 'generic',
  properties: {
    auth: {
      username: '={{$credentials.username}}',
      password: '={{$credentials.password}}',
    },
  },
};
```

---

## Pattern 5: OAuth2

OAuth2 credentials extend the built-in `oAuth2Api` base:

```typescript
export class MyServiceOAuth2Api implements ICredentialType {
  name = 'myServiceOAuth2Api';
  displayName = 'My Service OAuth2 API';
  extends = ['oAuth2Api'];              // Inherit OAuth2 fields
  documentationUrl = 'myService';
  properties: INodeProperties[] = [
    {
      displayName: 'Grant Type',
      name: 'grantType',
      type: 'hidden',
      default: 'authorizationCode',
    },
    {
      displayName: 'Authorization URL',
      name: 'authUrl',
      type: 'hidden',
      default: 'https://myservice.com/oauth/authorize',
    },
    {
      displayName: 'Access Token URL',
      name: 'accessTokenUrl',
      type: 'hidden',
      default: 'https://myservice.com/oauth/token',
    },
    {
      displayName: 'Scope',
      name: 'scope',
      type: 'hidden',
      default: 'read write',
    },
  ];
}
```

**Key points:**
- Use `type: 'hidden'` for fields the user shouldn't edit (URLs, grant type)
- The base `oAuth2Api` provides Client ID and Client Secret fields automatically
- n8n handles the full OAuth2 flow (redirect, token exchange, refresh)

---

## Domain/URL Credentials

When the API base URL varies per customer (self-hosted services):

```typescript
properties: INodeProperties[] = [
  {
    displayName: 'Domain',
    name: 'domain',
    type: 'string',
    default: 'https://myinstance.myservice.com',
    placeholder: 'https://your-instance.myservice.com',
  },
  {
    displayName: 'API Key',
    name: 'apiKey',
    type: 'string',
    typeOptions: { password: true },
    default: '',
  },
];
test: ICredentialTestRequest = {
  request: {
    baseURL: '={{$credentials.domain}}',
    url: '/api/v1/me',
  },
};
```

---

## Custom Credential Test (testedBy)

For complex validation not suited to a simple HTTP request:

```typescript
// In credential file:
// (no test property — use testedBy instead)

// In node file, reference it:
credentials: [
  { name: 'myServiceApi', required: true, testedBy: 'myServiceApiTest' },
],

// Also in node file, add test method:
methods = {
  credentialTest: {
    async myServiceApiTest(
      this: ICredentialTestFunctions,
      credential: ICredentialsDecrypted,
    ): Promise<INodeCredentialTestResult> {
      try {
        // Custom validation logic
        return { status: 'OK', message: 'Connection successful' };
      } catch (error) {
        return { status: 'Error', message: error.message };
      }
    },
  },
};
```

---

## Injection Locations

The `authenticate.properties` object supports these locations:

| Location | Where it's injected | Example |
|----------|-------------------|---------|
| `headers` | HTTP headers | `Authorization: Bearer ...` |
| `qs` | URL query parameters | `?api_key=...` |
| `body` | Request body | `{ "token": "..." }` |
| `auth` | Basic auth (username/password) | `{ username, password }` |

**Expression syntax:** Always use `'={{$credentials.fieldName}}'` to reference credential values.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `typeOptions: { password: true }` on secrets | Always mask API keys, tokens, passwords |
| Wrong expression: `$credential.apiKey` | Use `$credentials.apiKey` (plural) |
| Forgot to list credential in `package.json` | Add to `n8n.credentials` array |
| Test endpoint requires auth but `authenticate` not set | `test.request` auto-uses the `authenticate` config |
| OAuth2 showing editable URL fields | Use `type: 'hidden'` for auth/token URLs |
