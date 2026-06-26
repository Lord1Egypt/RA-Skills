# Custom Code Reference (script.csx)

C# custom code for request/response transformation in Power Platform custom connectors.

**Source:** [Microsoft Docs — Write code in a custom connector](https://learn.microsoft.com/en-us/connectors/custom-connectors/write-code)

---

## When to Use Custom Code

| Scenario | Approach |
|----------|----------|
| Inject headers / query params | Use [policy templates](POLICY_TEMPLATES.md) instead |
| Simple URL routing | Use `dynamichosturl` policy template |
| Transform response JSON structure | **Custom code** |
| Combine multiple API calls into one action | **Custom code** |
| Conditional logic per operation | **Custom code** |
| Regex matching / string processing | **Custom code** |
| External data fetching during request | **Custom code** |

**Rule:** Policy templates first, custom code only when needed.

---

## Constraints

| Constraint | Limit |
|------------|-------|
| Language | C# (.NET Standard 2.0) |
| Execution timeout | 2 minutes |
| File size | 1 MB max |
| Scripts per connector | 1 (one `script.csx` file) |
| File extension | `.cs` or `.csx` |
| HTTP client | Must use `this.Context.SendAsync()`, not `HttpClient` directly |
| Gateway support | Not supported with on-premises data gateway |

---

## ScriptBase Class & IScriptContext Interface

```csharp
public abstract class ScriptBase
{
    // Context object with request info and helper methods
    public IScriptContext Context { get; }

    // Cancellation token for the execution
    public CancellationToken CancellationToken { get; }

    // Helper: Creates StringContent from serialized JSON
    public static StringContent CreateJsonContent(string serializedJson);

    // Your code goes here
    public abstract Task<HttpResponseMessage> ExecuteAsync();
}

public interface IScriptContext
{
    // Correlation ID for tracing
    string CorrelationId { get; }

    // The operation ID from the swagger definition
    string OperationId { get; }

    // The incoming HTTP request
    HttpRequestMessage Request { get; }

    // Logger instance
    ILogger Logger { get; }

    // Send HTTP requests (use instead of HttpClient)
    Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request,
        CancellationToken cancellationToken);
}
```

---

## Patterns

### Pattern 1: Operation Router (Most Common)

Route to different handlers based on the `OperationId` from the swagger definition:

```csharp
public class Script : ScriptBase
{
    public override async Task<HttpResponseMessage> ExecuteAsync()
    {
        switch (this.Context.OperationId)
        {
            case "SearchItems":
                return await HandleSearchItems().ConfigureAwait(false);
            case "TransformData":
                return await HandleTransformData().ConfigureAwait(false);
            default:
                // Forward all other operations unchanged
                return await this.Context.SendAsync(
                    this.Context.Request,
                    this.CancellationToken
                ).ConfigureAwait(false);
        }
    }

    private async Task<HttpResponseMessage> HandleSearchItems()
    {
        // Forward request to backend
        var response = await this.Context.SendAsync(
            this.Context.Request,
            this.CancellationToken
        ).ConfigureAwait(false);

        // Transform the response
        if (response.IsSuccessStatusCode)
        {
            var content = await response.Content.ReadAsStringAsync().ConfigureAwait(false);
            var result = JObject.Parse(content);

            // Flatten nested results
            var items = result["data"]?["results"] ?? new JArray();
            var newResult = new JObject { ["items"] = items };
            response.Content = CreateJsonContent(newResult.ToString());
        }

        return response;
    }

    private async Task<HttpResponseMessage> HandleTransformData()
    {
        // Read the incoming request body
        var body = await this.Context.Request.Content
            .ReadAsStringAsync().ConfigureAwait(false);
        var input = JObject.Parse(body);

        // Create a new response directly (no backend call)
        var output = new JObject
        {
            ["processed"] = true,
            ["result"] = input["value"]?.ToString().ToUpper()
        };

        var response = new HttpResponseMessage(HttpStatusCode.OK);
        response.Content = CreateJsonContent(output.ToString());
        return response;
    }
}
```

### Pattern 2: Forward and Transform Response

Forward the request unchanged, then reshape the response:

```csharp
public class Script : ScriptBase
{
    public override async Task<HttpResponseMessage> ExecuteAsync()
    {
        // Forward to backend
        var response = await this.Context.SendAsync(
            this.Context.Request,
            this.CancellationToken
        ).ConfigureAwait(false);

        if (response.IsSuccessStatusCode)
        {
            var content = await response.Content.ReadAsStringAsync().ConfigureAwait(false);
            var original = JObject.Parse(content);

            // Wrap the response in a new structure
            var wrapped = new JObject
            {
                ["data"] = original,
                ["timestamp"] = DateTime.UtcNow.ToString("o")
            };

            response.Content = CreateJsonContent(wrapped.ToString());
        }

        return response;
    }
}
```

### Pattern 3: Modify Request Before Forwarding

```csharp
public class Script : ScriptBase
{
    public override async Task<HttpResponseMessage> ExecuteAsync()
    {
        if (this.Context.OperationId == "CreateItem")
        {
            // Change HTTP method if needed
            this.Context.Request.Method = HttpMethod.Put;

            // Modify request body
            var body = await this.Context.Request.Content
                .ReadAsStringAsync().ConfigureAwait(false);
            var input = JObject.Parse(body);
            input["source"] = "PowerAutomate";
            this.Context.Request.Content = CreateJsonContent(input.ToString());
        }

        return await this.Context.SendAsync(
            this.Context.Request,
            this.CancellationToken
        ).ConfigureAwait(false);
    }
}
```

### Pattern 4: Regex Processing

```csharp
public class Script : ScriptBase
{
    public override async Task<HttpResponseMessage> ExecuteAsync()
    {
        if (this.Context.OperationId == "RegexIsMatch")
        {
            var content = await this.Context.Request.Content
                .ReadAsStringAsync().ConfigureAwait(false);
            var input = JObject.Parse(content);

            var textToCheck = (string)input["textToCheck"];
            var pattern = (string)input["regex"];
            var rx = new Regex(pattern);

            var output = new JObject
            {
                ["textToCheck"] = textToCheck,
                ["isMatch"] = rx.IsMatch(textToCheck)
            };

            var response = new HttpResponseMessage(HttpStatusCode.OK);
            response.Content = CreateJsonContent(output.ToString());
            return response;
        }

        return new HttpResponseMessage(HttpStatusCode.BadRequest)
        {
            Content = CreateJsonContent($"Unknown operation: '{this.Context.OperationId}'")
        };
    }
}
```

### Pattern 5: Multi-Value Query Parameter Workaround

Power Platform does not support `collectionFormat: "multi"` on array parameters. The workaround is to accept a comma-separated string and split it into repeated query parameters in custom code.

In the OpenAPI definition, change the parameter from `array` to `string`:

```json
{
  "name": "services[]",
  "in": "query",
  "type": "string",
  "description": "A comma-separated list of services to filter by.",
  "x-ms-summary": "Services"
}
```

In `script.csx`, split the comma-separated values and rebuild the query string:

```csharp
public class Script : ScriptBase
{
    // Map operationId → parameter names that need multi-value splitting
    private readonly Dictionary<string, string[]> specialHandlingMap =
        new Dictionary<string, string[]>
        {
            { "GetFacilities", new[] { "facilityIds", "services[]", "bbox[]" } },
            { "GetNearbyFacilities", new[] { "services[]" } }
        };

    public override async Task<HttpResponseMessage> ExecuteAsync()
    {
        var operationId = this.Context.OperationId;

        if (specialHandlingMap.TryGetValue(operationId, out var queryParamNames))
        {
            var query = HttpUtility.ParseQueryString(
                this.Context.Request.RequestUri.Query);

            foreach (var paramName in queryParamNames)
            {
                if (query.AllKeys.Contains(paramName))
                {
                    var values = query[paramName]
                        .Split(',')
                        .Select(v => v.Trim())
                        .ToArray();

                    query.Remove(paramName);
                    foreach (var value in values)
                    {
                        query.Add(paramName, value);
                    }
                }
            }

            var uriBuilder = new UriBuilder(this.Context.Request.RequestUri)
            {
                Query = query.ToString()
            };
            this.Context.Request.RequestUri = uriBuilder.Uri;
        }

        return await this.Context.SendAsync(
            this.Context.Request, this.CancellationToken
        ).ConfigureAwait(false);
    }
}
```

**Key points:**
- The `specialHandlingMap` lets you centrally define which operations and parameters need splitting
- Always call `this.Context.SendAsync()` to forward the modified request — custom code replaces the default pipeline
- Update parameter descriptions to instruct users: "A comma-separated list of..."
- This pattern works with `System.Web.HttpUtility` which is available in the supported namespaces

---

## Base64 OperationId Workaround

In some regions, `OperationId` may be Base64-encoded. Decode it before matching:

```csharp
public override async Task<HttpResponseMessage> ExecuteAsync()
{
    string operationId = this.Context.OperationId;

    // Decode if Base64 encoded
    try
    {
        byte[] data = Convert.FromBase64String(operationId);
        operationId = Encoding.UTF8.GetString(data);
    }
    catch (FormatException) { /* Not Base64, use as-is */ }

    switch (operationId)
    {
        case "MyOperation":
            return await HandleMyOperation().ConfigureAwait(false);
        default:
            return await this.Context.SendAsync(
                this.Context.Request, this.CancellationToken
            ).ConfigureAwait(false);
    }
}
```

---

## Supported Namespaces

Only these C# namespaces are available (.NET Standard 2.0):

```csharp
using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Security;
using System.Security.Authentication;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using System.Web;
using System.Xml;
using System.Xml.Linq;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
```

---

## Deploying with Custom Code

```bash
# Create connector with script
paconn create \
  --api-def apiDefinition.swagger.json \
  --api-prop apiProperties.json \
  --script script.csx

# With icon too
paconn create \
  --api-def apiDefinition.swagger.json \
  --api-prop apiProperties.json \
  --script script.csx \
  --icon icon.png
```

When custom code is enabled, it takes **precedence** over the codeless definition — the platform runs the code and does NOT send requests to the backend automatically. Your code must explicitly call `this.Context.SendAsync()` to forward requests.
