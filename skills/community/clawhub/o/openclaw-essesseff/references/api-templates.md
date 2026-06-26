# Templates API

Source: https://www.essesseff.com/docs/api/templates

List and retrieve essesseff app templates (global and account-specific).

---

## GET /global/templates

List global essesseff app templates

```
GET /api/v1/global/templates
```

### Description

Lists all available global essesseff app templates. Global templates are system-level templates provided by essesseff (not account-specific). No account_slug is required for global endpoints.

### Query Parameters

#### language (optional)

Filter templates by programming language: `go`, `python`, `node`, `java`, `rust`, `php`

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/global/templates" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

With language filter:

```
curl -X GET \
  "https://www.essesseff.com/api/v1/global/templates?language=go" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
[
  {
    "name": "essesseff-hello-world-go-template",
    "language": "go",
    "description": "essesseff Hello World Go template",
    "template_org_login": "essesseff-hello-world-go-template",
    "source_template_repo": "hello-world",
    "is_global_template": true,
    "replacement_string": "hello-world"
  },
  {
    "name": "essesseff-helloworld-springboot-templat",
    "language": "java",
    "description": "essesseff Hello World Java Spring Boot template",
    "template_org_login": "essesseff-helloworld-springboot-templat",
    "source_template_repo": "helloworld",
    "is_global_template": true,
    "replacement_string": "helloworld"
  }
]
```

**Note:** For global templates, `replacement_string` is typically `"hello-world"` (Go, Python, Node.js templates), except for Java (Spring Boot) which uses `"helloworld"` (no hyphen).

---

## GET /global/templates/{template_name}

Get global template details

```
GET /api/v1/global/templates/{template_name}
```

### Description

Gets complete details for a specific global template (all fields needed for app creation).

### Path Parameters

#### template_name (required)

The unique name of the global template (e.g., "essesseff-hello-world-go-template")

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/global/templates/essesseff-hello-world-go-template" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
{
  "name": "essesseff-hello-world-go-template",
  "language": "go",
  "description": "essesseff Hello World Go template",
  "template_org_login": "essesseff-hello-world-go-template",
  "source_template_repo": "hello-world",
  "is_global_template": true,
  "replacement_string": "hello-world"
}
```

---

## GET /accounts/{account_slug}/templates

List team-account-specific templates

```
GET /api/v1/accounts/{account_slug}/templates
```

### Description

Lists all team-account-specific templates for the specified account. The API key must belong to the specified account_slug.

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key. The API key must belong to this account.

### Query Parameters

#### language (optional)

Filter templates by programming language: `go`, `python`, `node`, `java`, `rust`, `php`

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/templates" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
[
  {
    "name": "my-custom-template",
    "language": "go",
    "description": "Custom Go template for my team",
    "template_org_login": "my-org",
    "source_template_repo": "my-custom-template-repo",
    "is_global_template": false,
    "replacement_string": "hello-world"
  }
]
```

---

## GET /accounts/{account_slug}/templates/{template_name}

Get team-account-specific template details

```
GET /api/v1/accounts/{account_slug}/templates/{template_name}
```

### Description

Gets complete details for a team-account-specific template (all fields needed for app creation).

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key. The API key must belong to this account.

#### template_name (required)

The unique name of the team-account-specific template

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/templates/my-custom-template" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
{
  "name": "my-custom-template",
  "language": "go",
  "description": "Custom Go template for my team",
  "template_org_login": "my-org",
  "source_template_repo": "my-custom-template-repo",
  "is_global_template": false,
  "replacement_string": "hello-world"
}
```
