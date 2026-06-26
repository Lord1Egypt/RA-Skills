# HTTP Test Artifact Example

This reference keeps a lightweight publishable example. For runnable assets and richer walkthroughs, start with `templates/` or `examples/`.

## `.http`

```http
@host = https://api.example.test
@resourceId = sample-123
@cookie = <set via COOKIE>

### Detail positive: should expose enabled status
# auth = cookie
# expect.status = 200
# expect.json_path = data.status
# expect.equals = enabled
# output.fields = code,message,data.id,data.status
GET {{host}}/v1/resources/{{resourceId}}
Cookie: {{cookie}}

### Detail unauthenticated: should return login error
# expect.status = 401
# expect.contains = login_required
GET {{host}}/v1/resources/{{resourceId}}
```

## Script Output

```text
[PASS] Detail positive: should expose enabled status
  URL: https://api.example.test/v1/resources/sample-123
  method: GET
  expectation: json_path data.status == enabled
  HTTP=200 cost=203ms
  key fields: code=0,message='',data.id='sample-123',data.status='enabled'

Summary: PASS=1 FAIL=0 SKIP=0
```

## User Prompt Pattern

When required information is missing, ask concise questions:

```text
需要你提供三类信息：
1. 目标接口 URL 或 host + path。
2. 认证方式：完整 Cookie、Bearer Token、自定义 Header，或说明接口不需要登录。
3. 每个用例的预期：HTTP 状态码、JSON 字段、响应标记、错误码或其他断言。
```
