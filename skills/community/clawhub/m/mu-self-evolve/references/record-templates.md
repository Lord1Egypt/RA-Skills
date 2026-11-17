# 记录格式模板

## 经验记录（LEARNINGS.md）

```
## [LRN-YYYYMMDD-XXX] category

**记录时间**: 2026-03-23T11:30:00+08:00
**优先级**: low | medium | high | critical
**状态**: pending | candidate | promoted | resolved
**领域**: messaging | docs | calendar | mcp | skill | auth | api | 通用 | <自定义>

### 摘要
一句话说清楚学到了什么

### 详情
发生了什么，哪里错了，正确做法是什么

### 建议行动
具体的修复或改进措施

### 病理键（v3.0必填）
- WHERE: skill_load | mcp_call | file_write | api_call | browser_op | memory_op | agent_dispatch | prompt_parse | auth | other | <自定义>
- WHY: param_missing | token_expired | timing_race | perm_denied | knowledge_gap | format_mismatch | timeout | logic_error | config_drift | user_correction | other | <自定义>

### 元信息
- 来源: conversation | error | user_feedback
- 相关文件: path/to/file
- 标签: tag1, tag2
- 参见: LRN-20260310-001（如有关联）
- Pattern-Key: mcp.token_expired | api.timeout（可选）
- Recurrence-Count: 1
- First-Seen: 2026-03-23
- Last-Seen: 2026-03-23
- VFM: 0（提升前自检填写，≥50才提升）

---
```

**category 可选值：**
- correction — 木老师纠正了我
- knowledge_gap — 对内部系统的认知盲区
- best_practice — 发现更好的做法
- mcp_gotcha — MCP/接口的坑
- auth_issue — Token/认证问题
- tool_pattern — 工具使用模式优化
- positive_signal — 正向反馈信号

**状态流转：**
```
pending → candidate → promoted → (移出至永久记忆)
    ↓         ↑
    └── 验算未通过，降级为candidate
```

## 错误记录（ERRORS.md）

```
## [ERR-YYYYMMDD-XXX] skill或命令名

**记录时间**: 2026-03-23T11:30:00+08:00
**优先级**: high
**状态**: pending | resolved
**领域**: messaging | docs | mcp | api | browser | auth | <自定义>

### 摘要
简述什么失败了

### 错误信息
实际报错内容

### 上下文
- 尝试的操作
- 使用的参数或输入
- 环境信息（token是否过期、认证状态等）

### 建议修复
修复方向

### 病理键（v3.0必填）
- WHERE: skill_load | mcp_call | file_write | api_call | browser_op | memory_op | agent_dispatch | prompt_parse | auth | other | <自定义>
- WHY: param_missing | token_expired | timing_race | perm_denied | knowledge_gap | format_mismatch | timeout | logic_error | config_drift | user_correction | other | <自定义>

### 元信息
- 可复现: yes | no | unknown
- 相关文件: path/to/file
- 参见: ERR-20260310-001
- Pattern-Key: mcp.token_expired（可选）
- Recurrence-Count: 1
- First-Seen: 2026-03-23
- Last-Seen: 2026-03-23

---
```

## 功能需求（FEATURE_REQUESTS.md）

```
## [FEAT-YYYYMMDD-XXX] capability_name

**记录时间**: 2026-03-23T11:30:00+08:00
**优先级**: medium
**状态**: pending
**领域**: skill | workflow | mcp | 通用 | <自定义>

### 需求描述
木老师想做什么

### 使用场景
为什么需要，解决什么问题

### 实现复杂度
simple | medium | complex

### 建议实现方案
可以怎么做，依赖哪些现有能力

### 元信息
- 频次: first_time | recurring
- 相关能力: existing_skill_name

---
```
