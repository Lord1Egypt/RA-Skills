# Credential Patterns: OAuth2

Extend the built-in `oAuth2Api` credential to inherit all OAuth2 fields and automatic token refresh. You only need to override the specific fields for your service.

## Table of Contents
1. [Authorization Code (user login)](#1-authorization-code-user-login)
2. [Client Credentials (machine-to-machine)](#2-client-credentials-machine-to-machine)
3. [PKCE flow](#3-pkce-flow)
4. [User-configurable scopes](#4-user-configurable-scopes)
5. [Reading OAuth2 tokens in execute()](#5-reading-oauth2-tokens-in-execute)
6. [OAuth2 with extra auth params](#6-oauth2-with-extra-auth-params)

---

## 1. Authorization Code (User Login)

User is redirected to the service's login page, grants permission, n8n handles token exchange and refresh automatically.

Use for: Google, GitHub, Slack, Dropbox, Microsoft, Salesforce, etc.

```typescript
import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class MyServiceOAuth2Api implements ICredentialType {
  name = 'myServiceOAuth2Api';
  extends = ['oAuth2Api'];           // ← inherit all standard OAuth2 fields + refresh logic
  displayName = 'My Service OAuth2';
  documentationUrl = 'https://docs.myservice.com/oauth2';

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
      default: 'https://auth.myservice.com/oauth/authorize',
      required: true,
    },
    {
      displayName: 'Access Token URL',
      name: 'accessTokenUrl',
      type: 'hidden',
      default: 'https://auth.myservice.com/oauth/token',
      required: true,
    },
    {
      displayName: 'Scope',
      name: 'scope',
      type: 'hidden',
      default: 'read:user read:data',
    },
    {
      // 'header' = credentials sent as Authorization: Basic header during token exchange
      // 'body'   = credentials sent in request body (some APIs require this)
      displayName: 'Authentication',
      name: 'authentication',
      type: 'hidden',
      default: 'header',
    },
  ];
}
```

---

## 2. Client Credentials (Machine-to-Machine)

No user login. App authenticates with its own Client ID + Secret.

Use for: service accounts, server-to-server integrations, background processes.

```typescript
export class MyServiceClientCredApi implements ICredentialType {
  name = 'myServiceClientCredApi';
  extends = ['oAuth2Api'];
  displayName = 'My Service API (App Auth)';

  properties: INodeProperties[] = [
    {
      displayName: 'Grant Type',
      name: 'grantType',
      type: 'hidden',
      default: 'clientCredentials',
    },
    {
      displayName: 'Access Token URL',
      name: 'accessTokenUrl',
      type: 'hidden',
      default: 'https://auth.myservice.com/oauth/token',
      required: true,
    },
    {
      displayName: 'Scope',
      name: 'scope',
      type: 'hidden',
      default: 'api.read api.write',
    },
    {
      displayName: 'Authentication',
      name: 'authentication',
      type: 'hidden',
      default: 'body',        // many client_credentials APIs expect creds in body
    },
  ];
}
```

---

## 3. PKCE Flow

Like Authorization Code but with a code verifier/challenge to prevent interception. Used by mobile apps and SPAs; some APIs mandate it.

```typescript
export class MyServicePkceApi implements ICredentialType {
  name = 'myServicePkceApi';
  extends = ['oAuth2Api'];
  displayName = 'My Service OAuth2 (PKCE)';

  properties: INodeProperties[] = [
    {
      displayName: 'Grant Type',
      name: 'grantType',
      type: 'hidden',
      default: 'pkce',
    },
    {
      displayName: 'Authorization URL',
      name: 'authUrl',
      type: 'hidden',
      default: 'https://auth.myservice.com/oauth/authorize',
    },
    {
      displayName: 'Access Token URL',
      name: 'accessTokenUrl',
      type: 'hidden',
      default: 'https://auth.myservice.com/oauth/token',
    },
    {
      displayName: 'Scope',
      name: 'scope',
      type: 'hidden',
      default: 'openid profile email',
    },
    {
      displayName: 'Authentication',
      name: 'authentication',
      type: 'hidden',
      default: 'header',
    },
  ];
}
```

---

## 4. User-Configurable Scopes

When users need to select which permissions to grant (e.g., read-only vs. read-write).

```typescript
export class MyServiceOAuth2Api implements ICredentialType {
  name = 'myServiceOAuth2Api';
  extends = ['oAuth2Api'];
  displayName = 'My Service OAuth2';

  properties: INodeProperties[] = [
    { displayName: 'Grant Type',       name: 'grantType',      type: 'hidden', default: 'authorizationCode' },
    { displayName: 'Authorization URL', name: 'authUrl',       type: 'hidden', default: 'https://auth.myservice.com/oauth/authorize' },
    { displayName: 'Access Token URL', name: 'accessTokenUrl', type: 'hidden', default: 'https://auth.myservice.com/oauth/token' },
    { displayName: 'Authentication',   name: 'authentication', type: 'hidden', default: 'header' },
    {
      // NOT hidden — user can edit
      displayName: 'Scope',
      name: 'scope',
      type: 'string',
      default: 'read',
      description: 'Space-separated list of scopes, e.g. "read write admin"',
    },
  ];
}
```

---

## 5. Reading OAuth2 Tokens in execute()

n8n handles token refresh automatically before calling `execute()`. The current token is available on the credentials object:

```typescript
const credentials = await this.getCredentials('myServiceOAuth2Api');

// Access token (after automatic refresh if needed)
const tokenData = credentials.oauthTokenData as {
  access_token: string;
  token_type: string;
  expires_in?: number;
  refresh_token?: string;
};

const accessToken = tokenData.access_token;

// Use it
const response = await this.helpers.httpRequest({
  method: 'GET',
  url: 'https://api.myservice.com/me',
  headers: { Authorization: `Bearer ${accessToken}` },
});
```

> ⚠️ Do not cache the access token across executions — always read from `getCredentials()` to ensure you get the refreshed token.

---

## 6. OAuth2 with Extra Auth Params

Some APIs need additional parameters in the authorization URL (e.g. `response_type=code&prompt=consent`):

```typescript
properties: INodeProperties[] = [
  { displayName: 'Grant Type',         name: 'grantType',           type: 'hidden', default: 'authorizationCode' },
  { displayName: 'Authorization URL',  name: 'authUrl',             type: 'hidden', default: 'https://auth.myservice.com/oauth/authorize' },
  { displayName: 'Access Token URL',   name: 'accessTokenUrl',      type: 'hidden', default: 'https://auth.myservice.com/oauth/token' },
  { displayName: 'Scope',              name: 'scope',               type: 'hidden', default: 'openid profile' },
  { displayName: 'Authentication',     name: 'authentication',      type: 'hidden', default: 'header' },
  {
    // Extra query params appended to the authorization URL
    displayName: 'Auth URI Query Parameters',
    name: 'authQueryParameters',
    type: 'hidden',
    default: 'access_type=offline&prompt=consent',
  },
],
```
