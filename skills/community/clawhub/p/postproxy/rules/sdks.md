# SDKs

Postproxy provides official SDKs for 7 languages. All examples in this skill use `curl`, which works everywhere — use an SDK when generating application code.

| Language | Package | Installation |
|----------|---------|--------------|
| Node/TypeScript | `postproxy-sdk` | `npm install postproxy-sdk` |
| Python | `postproxy-sdk` | `pip install postproxy-sdk` |
| Go | `postproxy-go` | `go get github.com/postproxy/postproxy-go` |
| Ruby | `postproxy-sdk` | `gem install postproxy-sdk` |
| PHP | `postproxy/postproxy-php` | `composer require postproxy/postproxy-php` |
| Java | `dev.postproxy:postproxy-java` | Gradle/Maven artifact |
| .NET | `PostProxy` | `dotnet add package PostProxy` |

## Initialization

```typescript
import PostProxy from "postproxy-sdk";
const client = new PostProxy(process.env.POSTPROXY_API_KEY);
```

```python
import os
from postproxy import PostProxy
client = PostProxy(os.environ["POSTPROXY_API_KEY"])
```

```go
import postproxy "github.com/postproxy/postproxy-go"
client := postproxy.New(os.Getenv("POSTPROXY_API_KEY"))
```

Full SDK documentation: https://postproxy.dev/getting-started/sdks/
