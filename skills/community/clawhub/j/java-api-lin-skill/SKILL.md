---
name: java-api-lin-skill
description: 调用 JavaSkillController 提供的 HTTP 接口，供 OpenClaw/OpenLaw 执行业务操作、健康检查。
---

# Java Skill API

基于 **JavaSkillController** 的 OpenClaw/OpenLaw Skill 能力：通过 HTTP 调用本服务的执行入口与健康检查接口。

**配置与安全说明**：本 skill 不包含任何硬编码的 API 地址（`skill.json` 中无 `apiUrl`）。后端基地址**仅**通过环境变量 `JAVA_API_URL` 指定（如 `http://your-server:8080`），所有请求均发往您配置的地址，不会向任何第三方端点发送数据。使用脚本或平台调用前请设置 `JAVA_API_URL` 为可信的后端服务地址。

## When to use

- 用户或智能体需要「执行技能」「调用 Java 接口」「提交/查询业务」时
- 用户提到「调用 openLaw 接口」「执行法律/业务相关操作」时
- 需要探测或确认 Java Skill 服务是否可用时（健康检查）

## Instructions

1. **确认基地址**：从环境变量 `JAVA_API_URL` 读取 Java 服务根 URL（如 `http://your-server:8080`），接口前缀为 `/api/skill`。勿使用未在文档中声明的其他 URL。
2. **选择接口**：
   - 执行业务：使用 **POST** `/api/skill/execute` 或 **POST** `/api/skill/execute-v2`，Body 为 JSON（见 Parameters）。
   - 健康检查：使用 **GET** `/api/skill/health`，无需 Body。
3. **请求**：设置 `Content-Type: application/json`（POST 时），按参数构造 JSON。
4. **解析响应**：统一格式 `{ "code": 0, "msg": "success", "data": ... }`，`code === 0` 表示成功。

## API 说明（与 JavaSkillController 一致）

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/skill/execute` | POST | 通用执行入口，Body 为任意 JSON（建议含 action、userId） |
| `/api/skill/execute-v2` | POST | 使用 DTO 的入口，Body 为 SkillExecuteRequest 结构 |
| `/api/skill/health` | GET | 健康检查，返回 `data: "ok"` |

### 请求体（execute / execute-v2）

与 **SkillExecuteRequest** 对应：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| action | string | 否 | 操作类型，如 query / submit |
| userId | number | 否 | 用户 ID |
| extra | object | 否 | 扩展参数，键值对 |

示例：

```json
{
  "action": "query",
  "userId": 123,
  "extra": { "keyword": "合同" }
}
```

### 响应体（SkillExecuteResponse）

```json
{
  "code": 0,
  "msg": "success",
  "data": "用户ID:123，操作:query 执行完成"
}
```

- `code === 0`：成功；非 0 表示业务/系统失败。
- `msg`：提示信息；`data`：业务结果（字符串或对象）。

## 脚本调用（可选）

使用 `scripts/call_java_api.py` 可调用上述三个接口。**必须**设置环境变量 `JAVA_API_URL`（脚本运行时会校验，未配置则报错）。

```bash
# 设置基地址（不含 /api/skill/...），为必填项
export JAVA_API_URL=http://your-server:8080

# 执行（默认 POST /api/skill/execute）
python scripts/call_java_api.py --action query --userId 123

# 使用 execute-v2
python scripts/call_java_api.py --endpoint execute-v2 --action submit --userId 456

# 健康检查
python scripts/call_java_api.py --health
```

## Parameters（供 OpenClaw/skill.json 使用）

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| action | string | 否 | 操作类型 |
| userId | number | 否 | 用户 ID |
| extra | object | 否 | 扩展参数 |
