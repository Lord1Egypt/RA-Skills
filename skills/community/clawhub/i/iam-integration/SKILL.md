---
name: iam-integration
description: Use when integrating a new service with the IAM (Identity and Access Management) system - covers gRPC client setup, JWT token validation, permission checks, and REST API usage for the changyuanfeilun platform.
---

# IAM Integration Guide

## Overview

IAM is the central identity service. Services integrate via **gRPC** (primary) or **REST**. All resources are scoped by `appCode` + `tenantCode`.

## Quick Reference

| Need | Method | Endpoint/Service |
|------|--------|-----------------|
| Validate JWT token | gRPC | `JwtTokenService.validateAccessToken` |
| Check permission | gRPC | `AuthorizationService.hasPermission` |
| Get user by UID | gRPC | `AccountService.GetByUid` |
| Login | REST | `POST /api/v1.0/login/generateTicket` |
| Exchange ticket for token | REST | `POST /api/v1.0/account/exchangeAuthTicket` |
| Get current user | REST | `GET /api/v1.0/account/current` |

## 1. gRPC Integration (Recommended)

### Dependency

```xml
<dependency>
    <groupId>com.feilun</groupId>
    <artifactId>iam-rich-client</artifactId>
</dependency>
<dependency>
    <groupId>com.feilun</groupId>
    <artifactId>iam-boot-starter</artifactId>
</dependency>
```

### Configuration

```yaml
grpc:
  client:
    iam-service:
      address: dns:///iam.${namespace}.svc.cluster.local:9090
      negotiation-type: plaintext
```

### Token Validation

```java
@Autowired JwtTokenRichClient jwtTokenClient;

// Validate token (with optional permission check)
ValidateAccessTokenRequest req = ValidateAccessTokenRequest.newBuilder()
    .setAccessToken(token)
    .setAppCode(appCode)
    .setTenantCode(tenantCode)
    // optional: add permission check
    .setPermissionCheck(PermissionCheck.newBuilder()
        .setObject("resource-name")
        .setAct("read")
        .build())
    .build();

ValidateAccessTokenResponse resp = jwtTokenClient.validateAccessToken(req);
// resp.getUid(), resp.getRoleCodesList(), resp.getValid()
```

### Permission Check

```java
@Autowired AuthorizationRichClient authClient;

HasPermissionRequest req = HasPermissionRequest.newBuilder()
    .setAppCode(appCode)
    .setTenantCode(tenantCode)
    .setSubject(uid)
    .setObject("resource-name")
    .setAct("write")
    .setSiteCode(siteCode)
    .build();

boolean allowed = authClient.hasPermission(req).getHasPermission();
```

### Get Account Info

```java
@Autowired AccountRichClient accountClient;

GetByUidRequest req = GetByUidRequest.newBuilder()
    .setUid(uid).setAppCode(appCode).setTenantCode(tenantCode)
    .build();

AccountProto account = accountClient.getByUid(req).getAccount();
```

## 2. REST API Integration

### Required Headers

| Header | Description |
|--------|-------------|
| `X-ACCESS-TOKEN` | JWT token |
| `X-App` | App code |
| `X-Tenant` | Tenant code |
| `X-Uid` | User UID (set by gateway) |
| `X-IS-MOBILE` | `true` / `false` |

### Auth Filter

Add `IamAuthInfoFilter` to your service to auto-extract auth context from headers into thread-local.

```java
// Access current user context anywhere in request thread
IamAuthContext ctx = IamAuthContextHolder.get();
String uid = ctx.getUid();
String tenantCode = ctx.getTenantCode();
```

## 3. Key Data Models

```
Account: uid, appCode, tenantCode, loginName, email, mobile,
         acctStatus(0=inactive,1=active,2=disabled,9=cancelled),
         acctType(0=sub,1=main), roleCodes[], siteScope[]

Authorization: subject(uid/role), object(resource), act(read/write/delete),
               permitAll(bool), permitTargetId[], permitObjectId[]
```

## 4. Multi-tenancy Rules

- Every call **must** include `appCode` + `tenantCode`
- JWT secrets are per-app/tenant (`iam_jwt_secret` table)
- Permissions are site-scoped — always pass `siteCode` when checking

## 5. Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `appCode`/`tenantCode` | Always required in every gRPC request |
| Checking permission without `siteCode` | Pass `siteCode` for site-scoped resources |
| Calling REST without `X-App`/`X-Tenant` headers | Required for all REST calls |
| Using system `mvn` to build | Use `./mvnw` — project requires Maven 3.8.x via wrapper |

## 6. Account Status Reference

| Code | Status |
|------|--------|
| 0 | Inactive (pending activation) |
| 1 | Active |
| 2 | Disabled |
| 3 | Locked |
| 8 | Cancellation in progress |
| 9 | Cancelled |
