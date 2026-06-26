# 存量项目接入 OpenAPI 契约驱动 — 迁移指南

> 目标读者：已有项目「已经跑起来了，前后端各写各的」，现在要引入契约驱动。

---

## 目录

- [迁移全景](#迁移全景)
- [Phase 1：盘点现状](#phase-1盘点现状)
- [Phase 2：补齐 YAML](#phase-2补齐-yaml)
- [Phase 3：接入检查](#phase-3接入检查)
- [Phase 4：前端切换](#phase-4前端切换)
- [最小可行路径（MVP）](#最小可行路径mvp)
- [常见问题](#常见问题)

---

## 迁移全景

```
存量项目: 前端手写 fetch/axios + 后端 Controller 各自实现
                  │
                  ▼
Phase 1: 盘点 ──► 列出所有端点，找出 YAML 缺口
                  │
                  ▼
Phase 2: 补 YAML ──► 从 Controller 逆推 YAML 定义
                  │
                  ▼
Phase 3: 接入检查 ──► check-api-rules.sh 跑通
                  │
                  ▼
Phase 4: 前端切换 ──► apiClient 替换手写 fetch
                  │
                  ▼
目标:  前后端通过 OpenAPI YAML 唯一契约对齐
```

> ⏱ 时间估算：Phase 1-2 需要 1-3 天（取决于端点数量），Phase 3-4 增量推行，不影响现有功能。

---

## Phase 1：盘点现状

### 目标

搞清楚：**现在到底有多少个端点？哪些已经在 OpenAPI YAML 里？哪些根本没有文档？**

### 操作步骤

#### 1.1 从后端代码提取端点列表

```bash
# Spring Boot 项目（Java）
grep -r '@\(GetMapping\|PostMapping\|PutMapping\|DeleteMapping\|PatchMapping\|RequestMapping\)' \
  src/main/java --include="*.java" -h | sort

# 或者更精确地提取路径和方法
grep -rP '@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping)\("([^"]*)"\)' \
  src/main/java --include="*.java" -h | sort

# Express / Node.js 项目
grep -rE 'router\.(get|post|put|delete|patch)\(' \
  src/ --include="*.ts" --include="*.js" -h | sort

# Go 项目 (Gin / Echo)
grep -rE '\.(GET|POST|PUT|DELETE|PATCH)\(' \
  . --include="*.go" -h | sort
```

**输出：**把端点列表导出到 `endpoints-inventory.txt`。

#### 1.2 从 YAML 提取已定义端点

```bash
# 从各 OpenAPI YAML 中提取已定义的路径
grep '^  /' standards/*.yaml | sed 's/standards\///' | sort
```

**输出：**把已有路径列表导出到 `endpoints-in-yaml.txt`。

#### 1.3 做差集

```bash
# 生成差集报告：哪些代码里有的端点没在 YAML 里
diff <(cat endpoints-inventory.txt | sort -u) \
     <(cat endpoints-in-yaml.txt | sort -u) \
     > endpoints-gap.txt
```

#### ✅ 检查点：Phase 1 完成标志

- [ ] `endpoints-gap.txt` 已生成，知道缺口大小
- [ ] 按服务/模块分组，标注优先级（高/中/低）
- [ ] 和团队确认：哪些端点确实在用，哪些是废弃的

---

## Phase 2：补齐 YAML

### 目标

把 Phase 1 发现的缺口全部补进 OpenAPI YAML 文件。

### 操作步骤

#### 2.1 复制模板

```bash
# 如果还没有 YAML，从模板开始
cp skills/openapi-contract-driven/references/openapi-template.yaml \
   standards/{项目名}-openapi.yaml
```

如果已有旧的 Swagger 2.0 或碎片化 YAML，用脚本合并。

#### 2.2 从 Controller 代码逆推 YAML

对于每一个从 `endpoints-gap.txt` 中发现的端点，需要补全以下信息到 YAML：

| 代码来源 | YAML 字段 | 示例 |
|---------|----------|------|
| `@PostMapping("/login")` | `paths: /api/v1/auth/login: post:` | 路径 + HTTP 方法 |
| `@RequestBody LoginDto dto` | `requestBody:` → schema | 入参结构 |
| 返回值 `ApiResponse<UserDTO>` | `responses: "200":` → `$ref ApiResponse` | 出参结构 |
| `@RequestParam int page` | `parameters:` → `$ref PageParam` | 分页参数 |
| Javadoc / 注释 | `summary:` + `description:` | 文档 |

**逆推示例：**

```java
// Controller 代码:
@PostMapping("/login")
public ApiResponse<LoginResult> login(@RequestBody LoginRequest req) { ... }
```

↓ 逆推为 YAML 片段 ↓

```yaml
/api/v1/auth/login:
  post:
    tags: [user-service - Auth]
    operationId: authLogin
    summary: 用户登录
    security: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/LoginRequest"
    responses:
      "200":
        description: 登录成功
        content:
          application/json:
            schema:
              allOf:
                - $ref: "#/components/schemas/ApiResponse"
                - type: object
                  properties:
                    data:
                      $ref: "#/components/schemas/LoginResult"
```

> 💡 如果端点数量 > 30，建议用一个脚本辅助提取 Controller 元信息，然后手动补全 schema 和文档。

#### 2.3 补齐 components/schemas

```bash
# 检查 YAML 中引用了哪些 schema，哪些还没定义
grep -r '\$ref.*schemas/' standards/*.yaml | grep -oP '#/components/schemas/\K[^"]+' | sort -u > refs.txt
grep -c '^    [A-Z]' standards/*.yaml | grep ':0'  # 看看哪些 schema 还未定义
```

#### ✅ 检查点：Phase 2 完成标志

- [ ] YAML 中的路径数量 ≥ 代码中的端点数量
- [ ] 所有 `$ref` 引用的 schema 都已定义
- [ ] 所有端点都有 `operationId`
- [ ] 所有成功响应都用 `ApiResponse` 包裹
- [ ] 每个服务有 health 端点

---

## Phase 3：接入检查

### 目标

让 `check-api-rules.sh` 跑通，7 条规则全部通过（date format 可先作为 warn）。

### 操作步骤

#### 3.1 本地运行检查

```bash
# 单文件检查
bash skills/openapi-contract-driven/references/check-api-rules.sh \
  standards/{项目名}-openapi.yaml
```

#### 3.2 加入 CI 流水线

```bash
# 复制 CI 工作流到项目
cp skills/openapi-contract-driven/references/ci-github-actions.yml \
   .github/workflows/openapi-check.yml

# 提交
git add .github/workflows/openapi-check.yml
git commit -m "ci: 接入 OpenAPI 契约自动检查"
git push
```

之后的每一次 push 到 main 和 PR 到 main 都会自动运行检查。

#### 3.3 修复检查失败

每项失败对应一个具体的修复方法：

| 规则 | 典型错误 | 修复方法 |
|------|---------|---------|
| 规则 1：operationId | `❌ 3 operationId / 5 HTTP 方法` | 给漏掉的端点补 `operationId` |
| 规则 2：ApiResponse | `❌ 未发现 ApiResponse 引用` | 在 components/schemas 定义 ApiResponse，路径响应引用之 |
| 规则 3：ErrorResponse | `⚠️ 未发现 ErrorResponse` | 补 ErrorResponse schema 并在 4xx/5xx 响应中引用 |
| 规则 4：分页参数 | `⚠️ 未发现 PageParam 引用` | 列表类端点用 `$ref: "#/components/parameters/PageParam"` |
| 规则 5：health | `⚠️ 未发现 health 端点` | 每个服务加一个 `GET /health` |
| 规则 6：日期 format | `⚠️ 日期字段 format 缺失: 3/5` | 给日期字段加 `format: date-time` |
| 规则 7：BearerAuth | `❌ 缺少 BearerAuth securityScheme` | 补 components/securitySchemes/BearerAuth |

#### ✅ 检查点：Phase 3 完成标志

- [ ] 本地 `check-api-rules.sh` 输出 `✅ 6/7 通过` 或更好
- [ ] CI 已接入，最近一次 PR 通过了检查
- [ ] 如果有 error 项（exit 1），已全部修复

---

## Phase 4：前端切换

### 目标

用基于 YAML 生成的 apiClient 逐步替换前端手写的 fetch/axios 调用。

### 操作步骤

#### 4.1 生成类型定义（推荐）

```bash
# 安装依赖
npm install -D openapi-typescript

# 生成 TypeScript 类型文件
npx openapi-typescript standards/{项目名}-openapi.yaml \
  -o frontend/src/api/generated/schema.d.ts
```

这颗给整个项目带来了**编译期类型安全**：即使不改 apiClient，IDE 也会提示你请求/响应的结构是否正确。

#### 4.2 创建 apiClient（如果还没有）

```bash
# 从模板创建
cp skills/openapi-contract-driven/references/apiClient-template.ts \
   frontend/src/api/apiClient.ts
```

根据项目的 API 前缀和认证方式做以下调整：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `BASE_URL` | API 前缀 | `/api/v1` 或 `http://localhost:8080` |
| `getToken()` | 获取 JWT | 从 `localStorage` 或 `useAuth()` 读取 |
| `ApiResponse<T>` | 泛型响应包装 | 与后端 YAML 中定义的结构一致 |

#### 4.3 逐个模块切换

**原则：渐进替换，每次只改一个模块，改完测过再继续。**

```bash
# 示例：先切换 auth 模块
# 旧代码（手写 fetch）
const res = await fetch('/api/v1/auth/login', {
  method: 'POST',
  body: JSON.stringify({ username, password })
});
const data = await res.json();

# 新代码（apiClient）
import { apiClient, ApiResponse } from '@/api/apiClient';

const data = await apiClient.post('/auth/login', { username, password });
// data 类型: ApiResponse<LoginResult> — IDE 自动提示
```

**切换顺序建议：**

```
Auth 模块         →  最简单，只有 2-3 个端点
User 模块         →  基础的 CRUD
列表/分页模块     →  验证 PageParam/SizeParam
表单提交模块      →  验证 requestBody schema
复杂业务流程      →  最后切换，因为涉及多个端点协同
```

#### 4.4 清理手写 fetch/axios

```bash
# 全部切换完毕后，搜一下有没有残留
grep -rn 'fetch(' frontend/src/ --include="*.ts" --include="*.tsx" | \
  grep -v 'apiClient' | grep -v 'node_modules'
grep -rn 'axios' frontend/src/ --include="*.ts" --include="*.tsx" | \
  grep -v 'apiClient' | grep -v 'node_modules'
```

> 💡 不需要一次性全部清除。可以先加一个 ESLint 规则禁止 `fetch()` 和 `axios()` 直接调用，白名单模块逐步缩小。

#### ✅ 检查点：Phase 4 完成标志

- [ ] `schema.d.ts` 已生成，与 YAML 同步
- [ ] 核心模块（Auth + 至少 1 个业务模块）已切换到 apiClient
- [ ] 旧的手写 fetch/axios 调用 ≤ 10 处（或已全部替换）
- [ ] IDE 的「Find All References」功能可以追踪从 YAML 到前端的所有调用链

---

## 最小可行路径（MVP）

如果你的项目端点很多（> 50），或者时间紧迫，**不要全量迁移**。按以下 MVP 路径做：

### 第一步（1 小时）

只给 **最核心的 1-2 个服务** 做契约化。通常是 Auth 服务 + 一个高频业务服务。

```bash
# 1. 从模板生成，只写核心服务的端点
cp skills/openapi-contract-driven/references/openapi-template.yaml \
   standards/core-openapi.yaml

# 2. 只定义核心服务的路径（比如 auth + order）
#   其他服务暂不纳入

# 3. 运行检查
bash skills/openapi-contract-driven/references/check-api-rules.sh \
  standards/core-openapi.yaml

# 4. 只为核心服务的端点生成前端类型（其他服务继续用 fetch）
npx openapi-typescript standards/core-openapi.yaml \
  -o frontend/src/api/generated/core-schema.d.ts
```

### 第二步（逐步增量）

每次新增或修改一个服务时，遵循「**先改 YAML，再改代码**」的契约驱动流程：

```
新需求来了 → 先改 YAML → 检查通过 → 生成类型 → 前后端并行开发
```

存量端点在不改功能的情况下**原地不动**，保持原来的 fetch/axios。

### 第三步（自然更新）

当存量端点因为 bug 或需求变更被触动时，趁机把它补进 YAML，然后：

1. 在 YAML 中补这个端点
2. 运行检查
3. 把前端的 fetch 调用改成 apiClient 调用

**时间线预期：** 3-6 个月内，大部分活跃端点都会自然迁移完成。不活跃的端点不需要迁移（它们反正没人改）。

---

## 常见问题

### Q1：我们的项目是微服务，每个服务有自己的代码仓库，YAML 放哪里？

**方案 A（推荐）：** 主仓库放一份完整的 OpenAPI YAML 作为「系统契约单」，每个微服务各自生成自己的 Client。

**方案 B：** 每个微服务仓库各维护一份自己的 YAML，用 Git Submodule 或 CI 脚本聚合。

### Q2：后端返回的不是 ApiResponse 格式，怎么办？

两种选择：
1. **短期**：修改检查脚本，跳过规则 2（不推荐，因为会失去统一响应格式的保护）
2. **中期**：在后端加一层统一的 ResponseWrapper，所有 Controller 返回 `ApiResponse<T>`。Spring Boot 可以用 `@ControllerAdvice` 实现。

### Q3：已经有了 Swagger/SpringDoc 自动生成的 YAML，还需要手动维护吗？

自动生成的问题是：它反映的是「实现」而非「契约」。建议：
- 手动维护一份「目标 YAML」作为契约
- 自动生成的 YAML 作为「现状快照」
- `check-api-rules.sh` 对比两者，发现偏差

### Q4：前端还没切到 apiClient，会影响什么？

不影响现有功能。契约驱动是**增量安全网**：
- Phase 1-3 对现有代码零影响
- Phase 4 逐个模块替换，每个替换都是向后兼容的
- 即使永远不做 Phase 4，Phase 1-3 已经能防止「后端改了接口不通知前端」

### Q5：后端是 Go / Python / Node.js，不是 Java，Phase 2 怎么逆推？

原理一样：从路由定义文件中提取路径和方法，从 struct/class/dataclass 中提取 schema。命令不同但思路一致：

```bash
# Go (Gin)
grep -rE '\.(GET|POST|PUT|DELETE)\(' router/ --include="*.go" -h

# Python (FastAPI)
grep -rE '@(app|router)\.(get|post|put|delete)\(' api/ --include="*.py" -h

# Node.js (Express)
grep -rE 'router\.(get|post|put|delete)\(' routes/ --include="*.ts" -h
```
