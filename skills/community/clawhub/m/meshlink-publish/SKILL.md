---
name: MeshLink 服务发布
slug: meshlink-publish
summary: 通过 ZTM（Zero Trust Mesh）将本地服务一键发布到集团内网，AI 驱动的隧道管理 Skill。
license: MIT
acceptLicenseTerms: true
tags:
  - devops
  - networking
  - ztm
  - meshlink
  - service-publishing
requires:
  - meshlink   # npm link 安装，或 npm i -g meshlink-cli
version: 0.1.0
---

# MeshLink 服务发布 Skill
## 使用 meshlink CLI 将服务发布到集团内网 Mesh

---

## 你拥有的能力

`meshlink` CLI 已安装，可直接用 Bash 执行：

```bash
meshlink <command> [flags]
```

所有命令输出 JSON 到 stdout，`ok: true` 表示成功，`ok: false` 包含 `error` 和 `message`。

环境变量（需提前设置）：
```bash
export ZTM_MESH_NAME=<你的mesh名>   # 例如 "mesh" 或 "company-mesh"
```

---

## 发布流程：严格按顺序执行，不得跳步

### 第 0 步：判断是否触发发布

只有用户明确表达"发布/分享/让某人访问我的服务"时才进入此流程。
询问"如何发布"只需解释，**不要执行任何命令**。

---

### 第 1 步：确认端口

- 如果上下文中端口已知且服务已启动 → 直接使用
- 否则询问用户："请告诉我服务运行的端口号"

---

### 第 2 步：检查 Agent 状态和端口（并行执行）

```bash
meshlink agent-status
meshlink check-port --port <port>
```

| 情况 | 处理 |
|------|------|
| `agent-status` → `ok: false` 或 `connected: false` | 告知用户 ZTM Agent 未运行，终止流程 |
| `check-port` → `listening: false` | "端口 {port} 未检测到服务，需要我帮您启动吗？" 等待用户处理后重试 |
| 两者都 ok | 继续第 3 步 |

---

### 第 3 步：生成服务名

规则：项目名 → **kebab-case 英文**（全小写，只含字母/数字/连字符）

示例：
- "客户反馈系统" → `customer-feedback`
- "AI 数据看板" → `ai-dashboard`
- "设计规范工具" → `design-spec-tool`

如果不确定，提供 2-3 个候选让用户选择，**不要强行猜测**。

---

### 第 4 步：展示发布预览（**必须，绝对不可跳过**）

在用户确认前，**绝对不能执行 `meshlink publish`**。

```
📋 发布预览
─────────────────────────────────────
服务名称  {service_name}
访问地址  http://127.0.0.1:{分配端口}（发布后本地可访问）
来源端口  :{port}（已检测到 {process_hint}）
发布范围  当前仅自己可访问（Phase 0 模式）
─────────────────────────────────────
确认发布？[y/n]
```

等待用户明确确认后再执行。

---

### 第 5 步：执行发布

用户确认后：

```bash
meshlink publish --name <service_name> --port <port>
```

解析输出：
- `ok: true` → 继续第 6 步
- `ok: false, error: "NAME_CONFLICT"` → 用 `suggestion` 字段的备选名询问用户，重试
- `ok: false, error: "AGENT_ERROR"` → "ZTM Agent 异常，请检查后重试"
- 其他失败 → 展示 `message`，告知用户无需额外操作（无脏数据）

---

### 第 6 步：输出发布结果

```
✅ 发布成功！

访问地址：http://127.0.0.1:{inbound_port}
服务名称：{name}
来源端口：:{target_port}

当前仅您自己可访问。需要分享给更多同事吗？（下一阶段功能）
```

---

## 其他命令使用时机

| 用户意图 | 执行命令 |
|---------|---------|
| "我发布了哪些服务" | `meshlink list` |
| "帮我下线 {name}" | `meshlink unpublish --name {name}` |
| "ZTM 连接正常吗" | `meshlink agent-status` |

---

## 你不能做的事

- 在用户确认前执行 `meshlink publish`
- 跳过 `check-port` 检查直接发布
- 自行构造 `curl localhost:7777/...`（用 meshlink CLI，不要绕过它）
- 修改其他用户的服务
