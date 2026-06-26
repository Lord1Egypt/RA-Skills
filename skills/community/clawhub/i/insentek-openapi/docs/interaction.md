# Interaction Guide — 交互规范

> 完整交互流程、时间解析、输出格式、确认策略。
> 本文件按需加载，非每次调用必读。

---

## 0. Authentication Behavior

**MUST 遵守（与 `skill.md` Section 2 / 4 一致）：**

- Agent **禁止**向用户索要或接收 `appid` / `secret`
- 用户主动发送凭据时 → **拒绝接收**，引导 CLI `login`
- 脚本返回 `authentication_required` 或 HTTP 401/403 → **STOP**，原样展示固定引导文案：

```
这台电脑还没有连接 Insentek API，需要先完成一次本地配置，通常 1 分钟就好。

请在终端运行：

npx @insentek/openapi-skill login

按提示输入 appid 和 secret 即可（加密保存在本机，无需发到这个对话）。配置完成后回来继续提问，我接着帮你处理。
```

- 用户说"重新认证" → 引导 `npx @insentek/openapi-skill login` 或先 `logout` 再 `login`

### 0.1 脚本路径（与 `skill.md` Section 2 一致）

- API 调用用 `${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py`，其中 `${PYTHON}` 来自 `info --json` 的 `python.command`（缺省 `python3`），**禁止**相对路径 `scripts/...`
- 首次调用前或 ENOENT：`npx @insentek/openapi-skill info --json`，遍历 `runtimes[].scopes[]` 挑选 `installed: true` 的条目，读取 `installDir` / `scripts.cli` / `python.command`
- npm registry 上不存在 `insentek-openapi` / 已废弃旧名 `insentek-api-skill` 包，**禁止**使用 `npx insentek-openapi ...` 或 `npx insentek-api-skill ...`，所有 `npx` 调用必须用 scoped 包名 `@insentek/openapi-skill`

---

## 1. Intent Resolution

### 1.1 三层模型

| 层级 | 名称 | 说明 | 缺失时处理 |
|------|------|------|-----------|
| L1 | 核心意图 | 查数据 / 对比 / 导出 / 生成报告 | 反问："您想查询数据、对比设备，还是导出报告？" |
| L2 | 输出意图 | 对话展示 / 文件导出 | 提供选项让用户选择 |
| L3 | 格式意图 | CSV / Excel / JSON / HTML | L2=文件时询问；推荐 CSV 为默认 |

### 1.2 关键词映射

| 用户关键词 | 推断 L1 | 推断 L2 | 需确认 L3？ |
|-----------|---------|---------|-------------|
| "查一下"、"看看"、"多少" | 查询数据 | 对话展示 | 否 |
| "导出"、"下载"、"保存" | 查询数据 | 文件导出 | **是** |
| "生成报告"、"做一份报告" | 生成报告 | 文件导出 | **是** |
| "对比"、"比较"、"哪个高" | 对比设备 | 对话展示 | 否 |
| "把对比结果导出来" | 对比设备 | 文件导出 | **是** |

### 1.3 快捷意图（无需确认）

- "导出 [设备] [时间段] 数据为 [格式]"
- "下载 [设备] 的 [时间段] CSV"
- "生成 [设备] [时间段] 的 HTML 报告"
- "把 [设备A] 和 [设备B] [时间段] 的对比结果导出为 Excel"

---

## 2. Time Expression Parsing

| 表达式 | 开始 | 结束 | 示例 (today=2025-05-13) |
|--------|------|------|------------------------|
| "现在" / "最新" / "实时" | — | — | `GET /latest` |
| "昨天" | yesterday | yesterday | `20250512,20250512` |
| "最近7天" / "近一周" | today-7d | today | `20250506,20250513` |
| "上周" | last Monday | last Sunday | `20250505,20250511` |
| "本周" | this Monday | today | `20250512,20250513` |
| "本月" | 1st | today | `20250501,20250513` |
| "上月" | 1st of last month | last day of last month | `20250401,20250430` |
| "今年" | Jan 1 | today | `20250101,20250513` |
| "最近1个月" | today-30d | today | `20250413,20250513` |
| "最近3个月" | today-90d | today | `20250212,20250513` |
| "最近1年" | today-365d | today | `20240513,20250513` |
| *(default)* | today-1d | today | `20250512,20250513` |

**编码规则：** `YYYYMMDD`，Range: `startYYYYMMDD,endYYYYMMDD`。Moment: `YYYY-MM-DD HH:MM:SS` URL-encoded。

**月份边界：** "上月"在 1月31日说 → 12月全月；"本月"在当月任意日期 → 1号至今天。

---

## 3. Confirmation Patterns

**MUST 向用户确认的场景：**

1. L1/L2 意图不明确（见 1.1）
2. 数据可用性覆盖 < 50% 或 < 7 天（见 `skill.md` 3.2）
3. 多设备 alias 模糊匹配到多个结果
4. 导出数据量 > 50,000 条
5. 查询跨度 > 365 天

**可直接执行的场景：**
- 一句话完整表达（见 1.3）
- 同一会话内再次查询（已有缓存）
- 实时数据查询（/latest）

---

## 4. Output Format Guide

### 4.1 实时数据 → 简洁卡片

```
📍 [设备别名] ([SN后4位])
─────────────────────────
🌡️ [参数中文名]: [值] [单位]  @[时间]
💧 [参数中文名]: [值] [单位]
🔋 [参数中文名]: [值] [单位]
─────────────────────────
状态: [状态描述]  |  位置: [城市]
```

### 4.2 历史数据（对话）→ 表格 + 趋势

≤ 200 条：完整表格 + 趋势小结

> 200 条：统计摘要 + 首尾各 10 条抽样 + 提示导出

```
📊 数据概览（共 N 条，展示摘要）

统计摘要:
| 参数 | 平均 | 最大 | 最小 | 变化率 |
|------|------|------|------|--------|

💡 提示: 该时间段数据量较大，如需完整数据请说"导出为CSV"。
```

### 4.3 文件导出 → 确认信息

```
✅ 导出成功
📄 文件: [filename.csv]
📊 数据条数: [N] 条
📅 时间范围: [开始] 至 [结束]
📥 文件路径: [绝对路径]
```

### 4.4 对比分析 → 并排表格

```markdown
| 参数 | [设备A] | [设备B] | 差异 |
|------|---------|---------|------|
```

### 4.5 告警报告 → 标记列表

```
⚠️ 检测到 N 条异常数据:
1. [时间] [节点] [参数]: [值] — [异常原因]
```

---

## 5. Interaction Examples

### Flow 1: 查询历史数据（对话展示）

```
User: "3号设备上周的土壤湿度"
  → ${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py check (optional) or direct query
  → if authentication_required → STOP, show skill.md Section 2 fixed message
  → query_device(alias="3号") → resolve sn
  → query_data(sn, "上周") → /data
  → data points ≤ 200 → show table + trend
```

### Flow 2: 导出数据（文件导出）

```
User: "导出3号设备上个月数据为CSV"
  → if authentication_required → STOP, show skill.md Section 2 fixed message
  → query_device(alias="3号") → resolve sn
  → validate range (30d ≤ 365d) → OK
  → export_csv(sn, range, "data.csv") → return path
```

### Flow 3: 生成报告（数据不匹配 → 确认）

```
User: "分析3号近三个月数据，生成报告"
  → if authentication_required → STOP, show skill.md Section 2 fixed message
  → query_device(alias="3号") → resolve sn
  → query_data(sn, "最近3个月")
     → 请求: 90天 / 实际: 13天 → coverage 14%
  → STOP: "您请求近3个月共90天，该设备实际仅13天数据。是否继续？"
  → User: "继续"
  → analyze → construct HTML → write_html → return path
```

完整多设备对比、分批导出等示例见 `examples/flows.md`。
