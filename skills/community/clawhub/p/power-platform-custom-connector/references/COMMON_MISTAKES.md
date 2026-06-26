# Common Mistakes Reference

Error catalog for Power Platform custom connector development. Each entry includes the mistake, symptoms, and fix.

---

## Swagger / OpenAPI Definition Errors

### 1. Using OpenAPI 3.0 Instead of Swagger 2.0

**Mistake:** Creating the definition with `"openapi": "3.0.0"` instead of `"swagger": "2.0"`.

**Symptoms:** Import fails with "OpenAPI definitions that are in OpenAPI 3.0 format are not supported."

**Fix:** Use Swagger 2.0 format. The repo provides an OpenAPI 3.0 → Swagger converter in `tools/paconn-cli/`.

```json
// ✗ Wrong
{ "openapi": "3.0.0" }

// ✓ Correct
{ "swagger": "2.0" }
```

### 2. Missing x-ms-connector-metadata

**Mistake:** Omitting the `x-ms-connector-metadata` array from the swagger root.

**Symptoms:** PR validation fails. Connector may not display metadata in the connector listing.

**Fix:** Always include Website, Privacy policy, and Categories:

```json
"x-ms-connector-metadata": [
  { "propertyName": "Website", "propertyValue": "https://myservice.com" },
  { "propertyName": "Privacy policy", "propertyValue": "https://myservice.com/privacy" },
  { "propertyName": "Categories", "propertyValue": "AI;Data" }
]
```

### 3. Missing x-ms-summary on Parameters

**Mistake:** Not adding `x-ms-summary` to parameters and schema properties.

**Symptoms:** Parameters show as generic names like "body" or technical names like "param_1" in the designer.

**Fix:** Add `x-ms-summary` with Title Case display names:

```json
// ✗ Hard to use in designer
{ "name": "q", "in": "query", "type": "string" }

// ✓ Clear label in designer
{ "name": "q", "in": "query", "type": "string", "x-ms-summary": "Search Query" }
```

### 4. Missing Response Schemas

**Mistake:** Defining responses with empty or no schema.

**Symptoms:** No dynamic content available in Power Automate when using the connector's output. Users can't select fields from the response.

**Fix:** Always define complete response schemas with `x-ms-summary` on each property:

```json
// ✗ No dynamic content
"responses": {
  "200": { "description": "Success" }
}

// ✓ Full dynamic content
"responses": {
  "200": {
    "description": "Success",
    "schema": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "x-ms-summary": "Item ID" },
        "name": { "type": "string", "x-ms-summary": "Item Name" }
      }
    }
  }
}
```

### 5. Internal Parameters Without Default Values

**Mistake:** Marking a parameter as `x-ms-visibility: "internal"` and `required: true` but not providing a default value.

**Symptoms:** The operation fails because the hidden required parameter has no value.

**Fix:** Always set a `default` value for internal required parameters:

```json
{
  "name": "api-version",
  "in": "query",
  "type": "string",
  "required": true,
  "default": "2024-01-01",
  "x-ms-visibility": "internal"
}
```

### 6. Definition File Exceeds 1 MB

**Mistake:** Creating an extremely large swagger file (e.g., including base64 examples in descriptions).

**Symptoms:** Import fails with size limit error.

**Fix:** Keep the swagger definition under 1 MB. Move large examples to the readme. Use `$ref` definitions to reduce duplication.

---

## apiProperties.json Errors

### 7. Wrong Brand Color for Independent Publisher

**Mistake:** Using a custom brand color for an Independent Publisher connector.

**Symptoms:** PR review rejection. Independent Publisher connectors must use the standard orange color.

**Fix:** Set `iconBrandColor` to `"#da3b01"`:

```json
// ✗ Wrong for Independent Publisher
"iconBrandColor": "#007ee5"

// ✓ Required for Independent Publisher
"iconBrandColor": "#da3b01"
```

Verified Publishers can use any brand color.

### 8. Real Secrets in Connector Files

**Mistake:** Including actual API keys, client secrets, or tokens in `apiProperties.json` or `apiDefinition.swagger.json`.

**Symptoms:** Security violation. PR immediately rejected.

**Fix:** Use placeholder values:

```json
// ✗ Never commit real secrets
"clientId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

// ✓ Use dummy placeholders
"clientId": "<<Enter your client ID>>"
```

---

## Webhook Trigger Errors

### 9. Missing Webhook Deletion Endpoint

**Mistake:** Defining a webhook registration endpoint (POST) but no deletion endpoint (DELETE).

**Symptoms:** Webhooks are never cleaned up when flows are deleted or modified, leading to orphaned webhooks on the external service.

**Fix:** Define a DELETE operation for the webhook path:

```json
"/webhooks/{webhookId}": {
  "delete": {
    "operationId": "DeleteWebhook",
    "x-ms-visibility": "internal",
    "parameters": [
      { "name": "webhookId", "in": "path", "required": true, "type": "string" }
    ],
    "responses": { "200": { "description": "Deleted" } }
  }
}
```

### 10. API Missing Location Header on Webhook Creation

**Mistake:** The API returns a 201 for webhook creation but doesn't include a `Location` header.

**Symptoms:** Platform cannot delete the webhook — no URL to send the DELETE request to.

**Fix:** Ensure your API returns a `Location` header pointing to the webhook resource:

```http
HTTP/1.1 201 Created
Location: https://api.myservice.com/webhooks/hook_abc123
```

---

## Submission / PR Errors

### 11. PR Submitted to Wrong Branch

**Mistake:** Submitting the pull request to `master` instead of `dev`.

**Symptoms:** PR is closed or redirected.

**Fix:** Always target the `dev` branch:

```bash
git checkout dev
git checkout -b feature/my-connector
# ... make changes ...
git push origin feature/my-connector
# Create PR targeting dev branch
```

### 12. Connector in Wrong Directory

**Mistake:** Placing an Independent Publisher connector in `certified-connectors/` or `custom-connectors/`.

**Symptoms:** PR review rejection.

**Fix:**
- Community contributors → `independent-publisher-connectors/YourConnector/`
- Service owners → `certified-connectors/YourConnector/`
- Samples only → `custom-connectors/YourConnector/`

### 13. Missing or Incomplete README

**Mistake:** No readme, or readme missing required sections.

**Symptoms:** PR review feedback requesting additions.

**Fix:** Follow the standard template:

```markdown
# Service Name
Description (2-3 sentences).

## Publisher: Your Name
## Prerequisites
## Supported Operations
## Obtaining Credentials
## Known Issues and Limitations
## Deployment Instructions
```

---

## Custom Code Errors

### 14. Custom Code Exceeds Time/Size Limits

**Mistake:** Script takes too long (>2 min) or is too large (>1 MB).

**Symptoms:** Connector fails with timeout or deployment error.

**Fix:** Optimize code. Avoid large data processing. Move complex logic to the backend API.

### 15. Using HttpClient Instead of Context.SendAsync

**Mistake:** Creating a new `HttpClient` instance instead of using the provided context method.

**Symptoms:** May work now but will break in the future (Microsoft plans to block this).

**Fix:** Use the context's `SendAsync`:

```csharp
// ✗ Will be blocked in future
var client = new HttpClient();
var response = await client.SendAsync(request);

// ✓ Correct approach
var response = await this.Context.SendAsync(
    this.Context.Request, this.CancellationToken
).ConfigureAwait(false);
```

---

## Operation & Definition Formatting Errors

### 16. OperationId Not Properly PascalCased

**Mistake:** Using hyphens, underscores, or lowercase in `operationId` (e.g., `get_user-info`, `listItems`).

**Symptoms:** Inconsistent naming, may cause issues with code generation and Copilot Studio action matching.

**Fix:** Capitalize every word and remove all non-alpha characters:

```json
// ✗ Wrong
"operationId": "get_user-info"
"operationId": "listAllItems"

// ✓ Correct
"operationId": "GetUserInfo"
"operationId": "ListAllItems"
```

### 17. Summary Too Long or Has Trailing Punctuation

**Mistake:** Writing verbose summaries exceeding 80 characters, or ending with a period.

**Symptoms:** Truncation in the Power Automate designer. Inconsistent appearance.

**Fix:** Keep summaries concise (≤80 chars), sentence case, no trailing punctuation:

```json
// ✗ Too long / has punctuation
"summary": "Get all of the currently available weather forecast data for the specified location."

// ✓ Concise
"summary": "Get weather forecast for a location"
```

### 18. Description Contains URLs or Is Not a Full Sentence

**Mistake:** Putting URLs in descriptions or using fragments instead of full sentences.

**Symptoms:** PR review feedback. URLs clutter the designer UI.

**Fix:** Use full sentences ending in punctuation. Move URLs to the readme:

```json
// ✗ URL in description / not a sentence
"description": "See https://api.example.com/docs for details"
"description": "Weather data"

// ✓ Full sentence, no URL
"description": "Retrieves current weather data for the specified city."
```

### 19. Multiple Responses With Schemas

**Mistake:** Providing schema definitions on both success and error responses.

**Symptoms:** Confusion in the designer about which schema represents the output. Potential dynamic content issues.

**Fix:** Only the success response (2XX or default) should have a schema. Error responses should have descriptions only:

```json
// ✗ Schema on error response
"responses": {
  "200": { "description": "Success", "schema": { "$ref": "#/definitions/Item" } },
  "404": { "description": "Not found", "schema": { "$ref": "#/definitions/Error" } }
}

// ✓ Schema only on success
"responses": {
  "200": { "description": "Success", "schema": { "$ref": "#/definitions/Item" } },
  "404": { "description": "The requested item was not found." }
}
```

### 20. Missing x-ms-url-encoding on Path Parameters

**Mistake:** Omitting `x-ms-url-encoding` on path parameters.

**Symptoms:** Path parameter values may be double-encoded, causing 404 errors or incorrect API calls.

**Fix:** Add `"x-ms-url-encoding": "single"` to all path parameters:

```json
// ✗ Missing url encoding
{ "name": "formId", "in": "path", "type": "string", "required": true }

// ✓ Correct
{ "name": "formId", "in": "path", "type": "string", "required": true, "x-ms-url-encoding": "single" }
```

### 21. Definition Properties Missing title and description

**Mistake:** Omitting `title` and/or `description` on properties inside schema definitions.

**Symptoms:** Properties display with raw technical names in the designer. PR review feedback.

**Fix:** Add `title` (Title Case) and `description` (full sentence with punctuation) to every property, unless it uses `$ref`:

```json
// ✗ Missing title and description
"properties": {
  "user_id": { "type": "string" },
  "score": { "type": "number" }
}

// ✓ Complete
"properties": {
  "user_id": {
    "type": "string",
    "title": "User ID",
    "description": "The unique identifier for the user."
  },
  "score": {
    "type": "number",
    "title": "Score",
    "description": "The calculated score value from 0 to 100.",
    "minimum": 0,
    "maximum": 100
  }
}
```

### 22. Default Values Inside Definition Properties

**Mistake:** Including `default` values on properties within schema definitions.

**Symptoms:** Unexpected pre-filled values in the designer that may confuse users or cause incorrect data submission.

**Fix:** Remove `default` from definition properties. Defaults belong on operation parameters, not schema definitions:

```json
// ✗ Default in definition property
"properties": {
  "status": { "type": "string", "default": "active" }
}

// ✓ Default removed
"properties": {
  "status": {
    "type": "string",
    "title": "Status",
    "description": "The current status of the item."
  }
}
```

### 23. Number/Integer Missing min/max When Described in Text

**Mistake:** Description says "value between 1 and 10" but the schema lacks `minimum`/`maximum` properties.

**Symptoms:** No input validation in the designer. Users can enter out-of-range values.

**Fix:** When the description mentions a range, add explicit `minimum` and `maximum`:

```json
// ✗ Range in description but no schema constraints
{
  "type": "integer",
  "description": "Priority level from 1 to 5."
}

// ✓ Constraints added
{
  "type": "integer",
  "description": "The priority level of the task.",
  "minimum": 1,
  "maximum": 5
}
```

### 24. Default Response Has a Schema Definition

**Mistake:** Putting a response schema on the `default` response instead of (or in addition to) a specific success code.

**Symptoms:** Swagger validator error `DefaultResponseHasSchema`. Designer may not surface dynamic content correctly.

**Fix:** Put schema definitions on explicit success responses (200, 201) only. The `default` response should have a description but no schema:

```json
// ✗ Schema on default response
"responses": {
  "default": {
    "description": "Operation Failed.",
    "schema": { "$ref": "#/definitions/ErrorResponse" }
  }
}

// ✓ Schema on success response only
"responses": {
  "200": {
    "description": "Success",
    "schema": { "$ref": "#/definitions/Result" }
  },
  "default": {
    "description": "Operation Failed."
  }
}
```

### 25. Summary Contains Slash or Ends With Non-Alphanumeric

**Mistake:** Including `/` in operation summaries, or ending with punctuation, space, or special characters.

**Symptoms:** Swagger validator errors `RestrictedCharactersInSummary` or `ValueMustEndWithAlphanumeric`. PR review feedback.

**Fix:** Summaries should contain only alphanumeric characters and parentheses. Must end with an alphanumeric character:

```json
// ✗ Contains slash, ends with period
"summary": "Get user/account info."

// ✓ Clean summary
"summary": "Get user account info"
```

### 26. Summary and Description Are Identical

**Mistake:** Copying the same text into both `summary` and `description` fields.

**Symptoms:** PR review feedback. Provides no additional value to the user since both fields display in different contexts.

**Fix:** Summary should be a concise phrase; description should provide additional context:

```json
// ✗ Identical text
"summary": "Get user details",
"description": "Get user details"

// ✓ Description adds value
"summary": "Get user details",
"description": "Retrieves the full profile and contact information for the specified user."
```

### 27. Path Parameter Not Marked Required

**Mistake:** Omitting `required: true` on a path parameter.

**Symptoms:** Swagger validator error `PathParameterMustBeRequired`. The operation may fail at runtime.

**Fix:** All path parameters must be marked as required:

```json
// ✗ Missing required
{ "name": "itemId", "in": "path", "type": "string" }

// ✓ Required and encoded
{ "name": "itemId", "in": "path", "type": "string", "required": true, "x-ms-url-encoding": "single" }
```

### 28. Parameter Named connectionId

**Mistake:** Using `connectionId` as a parameter name.

**Symptoms:** Swagger validator error `ConnectionIdParameterNotAllowed`. The name is reserved by the platform.

**Fix:** Rename the parameter to something else:

```json
// ✗ Reserved name
{ "name": "connectionId", "in": "query", "type": "string" }

// ✓ Renamed
{ "name": "connId", "in": "query", "type": "string" }
```

### 29. GET Operation With Body or Form Data Parameter

**Mistake:** Adding a `body` or `formData` parameter to a GET operation.

**Symptoms:** Swagger validator error `BodyOrFormDataParameterInFetchOperationNotAllowed`.

**Fix:** GET operations cannot have request bodies. Move data to query parameters or change the HTTP method:

```json
// ✗ GET with body
"/items": {
  "get": {
    "parameters": [{ "name": "body", "in": "body", "schema": { "type": "object" } }]
  }
}

// ✓ Use query parameters instead
"/items": {
  "get": {
    "parameters": [{ "name": "filter", "in": "query", "type": "string" }]
  }
}
```

### 30. Using redirectMode "Global" Instead of "GlobalPerConnector"

**Mistake:** Setting `"redirectMode": "Global"` in OAuth configuration.

**Symptoms:** Connector may work initially but violates the mandatory per-connector redirect URI requirement (since Feb 2024). Certification rejection.

**Fix:** Always use `"GlobalPerConnector"`:

```json
// ✗ Deprecated
"redirectMode": "Global",
"redirectUrl": "https://global.consent.azure-apim.net/redirect"

// ✓ Current standard
"redirectMode": "GlobalPerConnector"
```

### 31. Connector Title Exceeds 30 Characters

**Mistake:** Creating a connector title longer than 30 characters or including restricted words like "API" or "Connector".

**Symptoms:** Certification rejection. Swagger validator error `FieldLengthExceeded` or `ValueContainsRestrictedWords`.

**Fix:** Keep title ≤30 characters. Avoid restricted words:

```json
// ✗ Too long and contains restricted word
"title": "My Amazing Weather Data API Connector Service"

// ✓ Concise and clean
"title": "Weather Service"
```

### 32. Non-Production Host URL

**Mistake:** Using a staging, dev, or test URL as the connector host.

**Symptoms:** Certification rejection. Connector won't work for end users.

**Fix:** Always use the production host URL:

```json
// ✗ Non-production URLs
"host": "api-staging.myservice.com"
"host": "dev.myservice.com"
"host": "sandbox.api.myservice.com"

// ✓ Production URL
"host": "api.myservice.com"
```

### 33. Using collectionFormat "multi" on Array Parameters

**Mistake:** Defining an array query parameter with `"collectionFormat": "multi"` in the OpenAPI definition.

**Symptoms:** Import fails with: `The 'collectionFormat' keyword value 'Multi' is not supported.`

**Fix:** Convert the array parameter to a string type and accept comma-separated values. Then use custom code (`script.csx`) to split the comma-separated string back into repeated query parameters (`?param=a&param=b`) before forwarding the request.

```json
// ✗ Not supported by Custom Connector wizard
{
  "name": "services[]",
  "in": "query",
  "type": "array",
  "collectionFormat": "multi",
  "items": { "type": "string" },
  "description": "List of services to filter by."
}

// ✓ Use string with comma-separated values + custom code
{
  "name": "services[]",
  "in": "query",
  "type": "string",
  "description": "A comma-separated list of services to filter by.",
  "x-ms-summary": "Services"
}
```

See [CUSTOM_CODE.md](CUSTOM_CODE.md) Pattern 5 for the complete `script.csx` implementation.

### 34. Missing `type` on Non-Body Swagger 2.0 Parameters

**Mistake:** Defining query/header/path/formData parameters without a `type` field in Swagger 2.0.

**Symptoms:** APIM import/deployment fails with validation errors like:
- `JSON is valid against no schemas from 'oneOf'`
- `The input OpenAPI file is not valid for the OpenAPI 2.0 specification`

**Fix:** Ensure every non-body parameter includes `type` (for example, `string`, `integer`, `boolean`, `number`):

```json
// ✗ Missing type (invalid in Swagger 2.0)
{
  "name": "location_code",
  "in": "query",
  "required": false,
  "description": "Filter by location code."
}

// ✓ Valid non-body parameter
{
  "name": "location_code",
  "in": "query",
  "type": "string",
  "required": false,
  "description": "Filter by location code.",
  "x-ms-summary": "Location Code"
}
```

### 35. Treating `CustomScriptProvisioningFailed` as a Permanent Failure

**Mistake:** Changing connector files immediately after a failed `pac connector update` with a custom script provisioning error.

**Symptoms:** Update fails with `CustomScriptProvisioningFailed`, often with an upstream HTML 502 gateway/proxy error.

**Fix:** Retry the same command after a short delay before changing files:

```bash
# Retry after a short delay (often succeeds on second attempt)
pac connector update \
  --connector-id <connector-id> \
  --api-definition-file apiDefinition.swagger.json \
  --api-properties-file apiProperties.json \
  --script-file script.csx
```

If repeated retries fail, capture and report the correlation ID from the CLI output.

### 36. Assuming `pac connector download` Files Must Match Byte-for-Byte

**Mistake:** Treating every difference between local and downloaded connector files as a functional regression.

**Symptoms:** False positives in verification, unnecessary rollback/change churn after successful deployment.

**Fix:** Use semantic comparison and focus on functional sections. Some differences are platform-managed and may be expected:
- `policyTemplateInstances` may be added automatically
- `publisher` / `stackOwner` in downloaded `apiProperties.json` may differ or be blank

Verify functional parity for:
- Paths, parameters, and response schemas
- `x-ms-dynamic-values` mappings
- `connectionParameters` and custom script wiring

### 37. Breaking Power Apps WADL Conversion with Ambiguous Definition Properties

**Mistake:** Leaving `definitions.*.properties.*` entries without explicit schema metadata (for example, only `description`, `title`, and `x-ms-summary`) or introducing malformed JSON while bulk-editing swagger.

**Symptoms:** Power Automate/Power Apps update may partially succeed, but Power Apps conversion fails with messages like:
- `An error occured while converting OpenAPI file to WADL file`
- `Required property '<property_name>' cannot have an ambiguous schema`
- `Make sure the 'type' property is specified at JSON path definitions.<Schema>.properties.<Property>`

**Fix:**
1. Ensure every `definitions.*.properties.*` entry has a schema discriminator (`type`, `$ref`, `enum`, `anyOf`, `oneOf`, `allOf`).
2. Remove accidental empty objects (`{}`) in parameters/responses/schemas.
3. Parse-check JSON before deployment to catch trailing/extra data.
4. If source is OpenAPI 3.x, re-map nullable fields carefully so converted Swagger 2.0 properties retain explicit typing.

```bash
# JSON parse check
python -c "import json; json.load(open('apiDefinition.swagger.json', encoding='utf-8'))"

# Ambiguous definition-property check
python -c "import json; s=json.load(open('apiDefinition.swagger.json',encoding='utf-8')); bad=[]; [bad.append(f'{dn}.{pn}') for dn,dv in s.get('definitions',{}).items() for pn,pv in (dv.get('properties') or {}).items() if isinstance(pv,dict) and not any(k in pv for k in ('type','$ref','enum','anyOf','oneOf','allOf'))]; print('ambiguous_count',len(bad)); [print(x) for x in bad[:200]]"
```

### 38. Leaving Array `items` Schemas Untyped (`"items": {}`)

**Mistake:** Keeping array properties with empty item schemas after OpenAPI conversion or manual edits.

**Symptoms:** Power Apps WADL conversion fails with messages such as:
- `Required property '<property_name>' cannot have an ambiguous schema`
- Errors pointing to paths like `definitions.<Schema>.properties.<ArrayProperty>`

**Fix:** Ensure every array has typed or referenced `items` schema.

```json
// ✗ Ambiguous array item schema
"error_sample_list": {
  "type": "array",
  "items": {}
}

// ✓ Explicit item schema
"error_sample_list": {
  "type": "array",
  "items": { "type": "string" }
}
```

### 39. Marking `readOnly` Properties as `required`

**Mistake:** Including `readOnly: true` properties in a definition's `required` array.

**Symptoms:** Semantic validation errors like:
- `Read only properties cannot be marked as required by a schema`

**Fix:** Remove read-only properties from `required` arrays.

```bash
python -c "import json; s=json.load(open('apiDefinition.swagger.json',encoding='utf-8')); bad=[]; [bad.append((dn,p)) for dn,dv in s.get('definitions',{}).items() for p in (dv.get('required') or []) if isinstance((dv.get('properties') or {}).get(p),dict) and (dv.get('properties') or {}).get(p,{}).get('readOnly') is True]; print('readOnly_required_conflicts',len(bad)); [print(f'{dn}.{p}') for dn,p in bad]"
```

### 40. Updating Connector Without `--script-file`

**Mistake:** Running `pac connector update` with only swagger/properties when connector behavior depends on `script.csx`.

**Symptoms:** Update succeeds, but runtime behavior appears unchanged because script changes were not included in that deployment command.

**Fix:** Include script on every update when custom code is used.

```bash
pac connector update \
  --connector-id <connector-id> \
  --api-definition-file apiDefinition.swagger.json \
  --api-properties-file apiProperties.json \
  --script-file script.csx
```

### 41. Assuming `connectionParameters` Always Reach Custom Code Without Explicit Policy Mapping

**Mistake:** Relying on implicit runtime behavior for connection parameter propagation into request headers consumed by `script.csx`.

**Symptoms:** Intermittent or environment-dependent missing values in custom code (for example, missing `app_name`/`email` headers).

**Fix:** Add explicit `setheader` policy mappings from `@connectionParameters('...')` in `apiProperties.json`.

```json
"policyTemplateInstances": [
  {
    "templateId": "setheader",
    "title": "app_name",
    "parameters": {
      "x-ms-apimTemplateParameter.name": "app_name",
      "x-ms-apimTemplateParameter.value": "@connectionParameters('app_name')",
      "x-ms-apimTemplateParameter.existsAction": "override",
      "x-ms-apimTemplate-policySection": "Request"
    }
  }
]
```

### 33. Using collectionFormat "multi" on Array Parameters

**Mistake:** Defining an array query parameter with `"collectionFormat": "multi"` in the OpenAPI definition.

**Symptoms:** Import fails with: `The 'collectionFormat' keyword value 'Multi' is not supported.`

**Fix:** Convert the array parameter to a string type and accept comma-separated values. Then use custom code (`script.csx`) to split the comma-separated string back into repeated query parameters (`?param=a&param=b`) before forwarding the request.

```json
// ✗ Not supported by Custom Connector wizard
{
  "name": "services[]",
  "in": "query",
  "type": "array",
  "collectionFormat": "multi",
  "items": { "type": "string" },
  "description": "List of services to filter by."
}

// ✓ Use string with comma-separated values + custom code
{
  "name": "services[]",
  "in": "query",
  "type": "string",
  "description": "A comma-separated list of services to filter by.",
  "x-ms-summary": "Services"
}
```

See [CUSTOM_CODE.md](CUSTOM_CODE.md) Pattern 5 for the complete `script.csx` implementation.

---

## Validation Tips

1. **Use VS Code with the repo's schema mappings** — Clone the PowerPlatformConnectors repo and open it in VS Code. The `.vscode/settings.json` maps JSON schemas to `apiDefinition.swagger.json` and `apiProperties.json` for real-time validation.

2. **Test in the custom connector wizard** — Before submitting a PR, create the connector in Power Automate/Power Apps and test all operations. Run **at least 10 successful calls per operation**.

3. **Check the PR validation bot** — The repo runs automated swagger validation and breaking change detection on PRs. Fix all issues before requesting review.

4. **Run the Solution Checker** — Add your connector to a solution and run the [Solution Checker](https://learn.microsoft.com/en-us/connectors/custom-connectors/validate-custom-connector) to validate against Microsoft certification standards before submitting.

5. **Run the Package Validator** — Use the [ConnectorPackageValidator.ps1](https://github.com/microsoft/PowerPlatformConnectors/blob/dev/scripts/ConnectorPackageValidator.ps1) PowerShell script to validate the package structure before uploading.
