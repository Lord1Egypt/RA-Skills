# Backend Agent — OpenAPI 契约驱动规则

将此内容合并到 backend-agent 或 legal-backend-agent 的 AGENTS.md。

---

## 🔗 OpenAPI 契约驱动

**动笔前必须：** `read standards/{project}-openapi.yaml`

所有 API 端点必须严格对应 OpenAPI 规范定义。
规范里没有的端点不写，规范里有的端点必须全写。

**每个服务必须实现 health 端点：**
```java
@GetMapping("/auth/health")
public ApiResponse<String> health() {
    return ApiResponse.ok("UP");
}
```

## 铁律

- ✅ 端点路径、method、参数、返回值必须与 OpenAPI YAML 一致
- ❌ 禁止自造 OpenAPI 规范之外的端点
- ❌ 禁止用 @RequestParam 拿 X-Company-Id（必须 @RequestHeader）
- ❌ 禁止 context-path 重复（application.yml 和 Controller 不同时写 /api）
- ❌ 禁止硬编码密钥/密码
