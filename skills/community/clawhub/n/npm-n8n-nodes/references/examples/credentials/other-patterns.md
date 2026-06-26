# Credential Patterns: Basic Auth, JWT, Multi-Auth

## Table of Contents
1. [Basic Auth (username + password)](#1-basic-auth)
2. [JWT — generate token in execute()](#2-jwt-token)
3. [Multi-auth — let user choose API key or OAuth2](#3-multi-auth-field)
4. [Credentials with environment selector](#4-environment-selector)

---

## 1. Basic Auth

Username + password sent as `Authorization: Basic <base64>`.

```typescript
import type {
  IAuthenticateGeneric,
  ICredentialTestRequest,
  ICredentialType,
  INodeProperties,
} from 'n8n-workflow';

export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';
  displayName = 'My Service API';

  properties: INodeProperties[] = [
    {
      displayName: 'Username',
      name: 'username',
      type: 'string',
      default: '',
      required: true,
    },
    {
      displayName: 'Password',
      name: 'password',
      type: 'string',
      typeOptions: { password: true },
      default: '',
      required: true,
    },
    {
      displayName: 'Base URL',
      name: 'baseUrl',
      type: 'string',
      default: 'https://api.myservice.com',
      required: true,
    },
  ];

  // n8n handles the base64 encoding automatically with the `auth` block
  authenticate: IAuthenticateGeneric = {
    type: 'generic',
    properties: {
      auth: {
        username: '={{$credentials.username}}',
        password: '={{$credentials.password}}',
      },
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

Alternatively, build the header manually in `execute()`:

```typescript
const creds   = await this.getCredentials('myServiceApi');
const encoded = Buffer.from(`${creds.username}:${creds.password}`).toString('base64');
headers: { Authorization: `Basic ${encoded}` }
```

---

## 2. JWT Token

For APIs that require you to generate and sign a JWT yourself (not OAuth2).

The credential stores the key material; the node generates the JWT per-request.

```typescript
export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';
  displayName = 'My Service API (JWT)';

  properties: INodeProperties[] = [
    {
      displayName: 'Issuer ID',
      name: 'issuerId',
      type: 'string',
      default: '',
      required: true,
      description: 'Your API issuer ID (found in developer console)',
    },
    {
      displayName: 'Key ID',
      name: 'keyId',
      type: 'string',
      default: '',
      required: true,
    },
    {
      displayName: 'Private Key',
      name: 'privateKey',
      type: 'string',
      typeOptions: {
        password: true,
        rows: 4,
      },
      default: '',
      required: true,
      placeholder: '-----BEGIN EC PRIVATE KEY-----\n...',
    },
  ];
  // No authenticate block — token is generated in execute()
}
```

In `execute()` (requires `jsonwebtoken` as a dependency):

```typescript
import * as jwt from 'jsonwebtoken';

const creds = await this.getCredentials('myServiceApi');

const now = Math.floor(Date.now() / 1000);
const token = jwt.sign(
  {
    iss: creds.issuerId,
    iat: now,
    exp: now + 1200,          // 20 minute expiry
    aud: 'https://api.myservice.com',
  },
  creds.privateKey as string,
  {
    algorithm: 'ES256',
    keyid: creds.keyId as string,
  },
);

headers: { Authorization: `Bearer ${token}` }
```

---

## 3. Multi-Auth Field

Let the user choose between auth methods (e.g. API key OR OAuth2) within one credential.

```typescript
export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';
  displayName = 'My Service API';

  properties: INodeProperties[] = [
    {
      displayName: 'Authentication Method',
      name: 'authMethod',
      type: 'options',
      options: [
        { name: 'API Key', value: 'apiKey' },
        { name: 'Username & Password', value: 'basicAuth' },
      ],
      default: 'apiKey',
    },
    {
      displayName: 'API Key',
      name: 'apiKey',
      type: 'string',
      typeOptions: { password: true },
      default: '',
      displayOptions: { show: { authMethod: ['apiKey'] } },
    },
    {
      displayName: 'Username',
      name: 'username',
      type: 'string',
      default: '',
      displayOptions: { show: { authMethod: ['basicAuth'] } },
    },
    {
      displayName: 'Password',
      name: 'password',
      type: 'string',
      typeOptions: { password: true },
      default: '',
      displayOptions: { show: { authMethod: ['basicAuth'] } },
    },
    {
      displayName: 'Base URL',
      name: 'baseUrl',
      type: 'string',
      default: 'https://api.myservice.com',
      required: true,
    },
  ];
  // No authenticate block — inject manually based on authMethod
}
```

In `execute()`:

```typescript
const creds      = await this.getCredentials('myServiceApi');
const authMethod = creds.authMethod as string;
const baseURL    = creds.baseUrl as string;

let authHeader: string;
if (authMethod === 'apiKey') {
  authHeader = `Bearer ${creds.apiKey}`;
} else {
  const encoded = Buffer.from(`${creds.username}:${creds.password}`).toString('base64');
  authHeader = `Basic ${encoded}`;
}

const response = await this.helpers.httpRequest({
  method: 'GET',
  url: `${baseURL}/endpoint`,
  headers: { Authorization: authHeader },
});
```

---

## 4. Environment Selector

Common pattern: production vs. sandbox URLs stored in the credential so the user doesn't set it per-node.

```typescript
export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';
  displayName = 'My Service API';

  properties: INodeProperties[] = [
    {
      displayName: 'API Token',
      name: 'apiToken',
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
        { name: 'Sandbox',    value: 'https://sandbox.api.myservice.com' },
        { name: 'Custom',     value: 'custom' },
      ],
      default: 'https://api.myservice.com',
    },
    {
      displayName: 'Custom URL',
      name: 'customUrl',
      type: 'string',
      default: '',
      placeholder: 'https://my-instance.myservice.com',
      displayOptions: { show: { environment: ['custom'] } },
    },
  ];
}
```

In `execute()`:

```typescript
const creds   = await this.getCredentials('myServiceApi');
const baseURL = creds.environment === 'custom'
  ? creds.customUrl as string
  : creds.environment as string;
```
