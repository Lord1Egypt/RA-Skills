# 文件结构与领域标签

## 文件结构

```
<AGENT_HOME>/workspace/
├── SOUL.md            # 行为风格、原则、安全底线
├── TOOLS.md           # 工具能力、API地址、内部配置
├── AGENTS.md          # 工作流、子Agent委派规则
├── MEMORY.md          # 长期记忆（主会话专用）
├── memory/            # 每日记忆文件
│   ├── YYYY-MM-DD.md  # 日记
│   ├── narratives/    # 周度叙事文件
│   │   └── YYYY-MM-DD.md
│   └── archive/       # 旧日记/叙事归档（超过30天自动移入）
└── .learnings/        # 本 skill 的日志文件
    ├── LEARNINGS.md
    ├── ERRORS.md
    ├── FEATURE_REQUESTS.md
    └── archive/       # 已提升/已解决/dormant条目归档
        ├── promoted-YYYY.md
        ├── resolved-YYYY.md
        ├── dormant-YYYY.md
        └── errors-resolved-YYYY.md
```

> Claude Code 环境下的路径映射见 [claude-code-compat.md](claude-code-compat.md)

## 领域标签

### 内置标签

| 标签 | 说明 |
|------|------|
| messaging | 消息、通知、群聊 |
| docs | 文档操作 |
| calendar | 日历/日程接口 |
| mcp | MCP Server |
| skill | Skill 管理 |
| browser | 浏览器自动化 |
| auth | Token/认证 |
| api | API 调用 |
| file | 文件操作 |
| 通用 | 跨场景通用经验 |

### 用户自定义标签

以上内置标签覆盖常见场景，但你可能需要为自己的工作流添加特定标签。例如：

- 如果你做 HR 系统：可以加 `hr`、`recruitment`、`onboarding`
- 如果你做 DevOps：可以加 `ci`、`deploy`、`monitoring`
- 如果你做数据分析：可以加 `etl`、`report`、`dashboard`

**自定义方法**：直接在记录的 `领域` 字段中使用你的自定义标签即可，无需注册。聚类扫描（6g）会自动识别所有出现过的标签。

## WHERE 标签（v3.0 病理键-环节）

| 标签 | 说明 |
|------|------|
| skill_load | Skill 加载/匹配阶段 |
| mcp_call | MCP Server 调用 |
| file_write | 文件写入操作 |
| api_call | 内部 API 调用 |
| browser_op | 浏览器自动化操作 |
| memory_op | 记忆读写操作 |
| agent_dispatch | 子Agent 派活/路由 |
| prompt_parse | 提示词解析 |
| auth | 认证/鉴权环节 |
| other | 其他 |

> 同样支持用户自定义 WHERE 标签，直接在记录中使用即可。

## WHY 标签（v3.0 病理键-根因）

| 标签 | 说明 |
|------|------|
| param_missing | 参数缺失/不完整 |
| token_expired | Token 过期/认证拦截 |
| timing_race | 时序竞态 |
| perm_denied | 权限不足 |
| knowledge_gap | 认知盲区/知识过时 |
| format_mismatch | 格式不匹配 |
| timeout | 超时/连接失败 |
| logic_error | 逻辑错误 |
| config_drift | 配置漂移/版本变更 |
| user_correction | 用户纠正（非系统错误） |
| other | 其他 |

> 同样支持用户自定义 WHY 标签，直接在记录中使用即可。
