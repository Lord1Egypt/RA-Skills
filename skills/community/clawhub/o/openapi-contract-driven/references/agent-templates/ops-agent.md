# Ops Agent — OpenAPI 契约驱动规则

将此内容合并到 ops-agent 或 saas-ops-agent 的 AGENTS.md。

---

## 📋 部署后验证（两步）

**第 1 步：API 规则检查（规范层）**
```bash
bash scripts/check-api-rules.sh standards/{project}-openapi.yaml
```
7 条规则，error 阻塞部署，warn 不阻塞。

**第 2 步：端点可达性（运行时层）**
```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:PORT/api/v1/health
```
每个服务验证 health 端点 + 至少 1 个业务端点。
状态码 >= 200 且 < 500 → 通。无响应/502/503 → 不通。

## 输出格式
```
✅ N/M 规则通过  ❌ K 失败  ⚠️ J 警告
✅ N/M 端点可达  ❌ K 失败
```
失败项立即回报 coordinator。
