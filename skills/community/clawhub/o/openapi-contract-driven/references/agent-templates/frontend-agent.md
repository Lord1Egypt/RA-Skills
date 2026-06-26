# Frontend Agent — OpenAPI 契约驱动规则

将此内容合并到 frontend-agent 或 legal-frontend-agent 的 AGENTS.md。

---

## 🔗 禁止手写 API 调用

**唯一入口：**
```typescript
import { auth, user, contract, review } from '@/api/generated/apiClient';
import type { Contract, Review, UserInfo } from '@/api/generated/apiClient';
```

## 铁律

1. ❌ **禁止 fetch/axios 直接调用后端 API**
2. ❌ **禁止手写 src/services/xxxApi.ts**
3. ❌ **禁止自造端点** — apiClient 里没有 → 回报 coordinator → 改 YAML → 重新生成
4. ❌ **禁止手写 DTO 类型定义** — 从 apiClient 导入
5. 新增端点唯一路径：改 OpenAPI YAML → 重新生成 apiClient → 两端同步

## 初始化（App 入口一次）

```typescript
import { configureApiClient } from '@/api/generated/apiClient';

configureApiClient({
  baseUrl: 'https://your-api.example.com',
  getToken: () => localStorage.getItem('token'),
});
```
