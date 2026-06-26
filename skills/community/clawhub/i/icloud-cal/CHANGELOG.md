# Changelog — iCloud Calendar Skill

## v1.4.0 → v2.0.0 全量变更

从 v1.4.0（基础创建功能）升级到 v2.0.0（全功能生产就绪）。以下是所有改进的整合列表，按类别分组。

---

### 🔐 安全加固（8 项）

| # | 变更 | 详情 |
|---|------|------|
| 1 | **凭据仅环境变量** | 彻底移除 `--email`/`--password` CLI 参数，不再通过命令行传递任何凭据 |
| 2 | **异常消息全面脱敏** | AuthError、连接失败、搜索错误等输出不再泄露 token/headers/bearer/internal details |
| 3 | **iCal 字段自动转义** | `escape_ical()` 处理 `\` `;` `,` `\n` `\r`，防止协议级注入攻击 |
| 4 | **RRULE 白名单校验** | 仅允许 `[A-Z0-9=;,\-_]` 字符，非法字符直接拒绝 |
| 5 | **创建路径 RRULE 验证** | `build_ical()` 前调用 `_validate_rrule()`，堵住了更新路径有但创建路径缺的漏洞 |
| 6 | **日志隐私保护** | `sanitize_for_log()` 截断事件标题/摘要/错误至 30 字符 |
| 7 | **删除操作安全门** | 强制 `CONFIRM_DELETE=1`，支持 `DELETE_DRY_RUN=1` 预览模式 |
| 8 | **更新操作安全门** | 新增 `CONFIRM_UPDATE=1` 环境变量确认 |

### 🌐 时区与协议（4 项）

| # | 变更 | 详情 |
|---|------|------|
| 9 | **DST 动态计算** | 用 `ZoneInfo.utcoffset()` 替代硬编码偏移，夏令时区域（美/欧）时间正确 |
| 10 | **全天事件修复** | 生成 `DTSTART;VALUE=DATE` 格式，跨时区不漂移 |
| 11 | **VTIMEZONE 自动生成** | 按输入时区动态生成完整 VTIMEZONE 组件，覆盖 35+ 城市 |
| 12 | **iCal 行尾标准化** | 统一使用 `\r\n`，符合 RFC 5545 Section 3.1 |

### 🔄 网络韧性（5 项）

| # | 变更 | 详情 |
|---|------|------|
| 13 | **Dual-Client 架构** | `fast_client`(10s) 处理 auth/CRUD（Fail-Fast），`slow_client`(60s) 专用于 `date_search(expand=True)` |
| 14 | **重试全覆盖** | 所有 8 个 CalDAV 网络调用点包裹 `_retry_on_caldav_error()` |
| 15 | **智能跳过重试** | 4xx 错误 (400/401/403/404/405/409/412/422) 立即放弃，不浪费 14 秒 |
| 16 | **幂等创建** | 预生成 UID 传 `build_ical()`，弱网重试发相同 UID，iCloud 自动去重 |
| 17 | **批量操作异常隔离** | 批量删除逐事件 try/catch，单个失败不影响其他，返回三态 `partial_success` |

### 🏗️ 架构改进（7 项）

| # | 变更 | 详情 |
|---|------|------|
| 18 | **跨日历移动安全** | 先复制（新 UID）后删除原事件，网络中断不丢数据 |
| 19 | **查询范围截断** | `MAX_EXPAND_DAYS=1095`（3 年），防无限 RRULE expand 撑爆内存 |
| 20 | **日志轮转** | `RotatingFileHandler` 512KB × 5 备份，防止磁盘打满 |
| 21 | **异常分类** | 区分 `AuthorizationError` / `NotFound` / 通用异常，返回结构化 `errors[]` |
| 22 | **裸 `except` 替换** | 全部改为 `except Exception:`，防止吞 `KeyboardInterrupt`/`SystemExit` |
| 23 | **User-Agent 注入** | 自定义 requests.Session 带 `OpenClaw-Calendar/2.0.0` 标识 |
| 24 | **依赖版本锁定** | `caldav>=1.3.0,<2.0`，避免大版本升级导致兼容性崩溃 |

### 🔧 功能增强（6 项）

| # | 变更 | 详情 |
|---|------|------|
| 25 | **搜索返回 errors[]** | 部分日历查询失败不阻断其他日历，错误信息完整返回 |
| 26 | **CALSCALE:GREGORIAN** | iCal 合规，部分客户端依赖此项 |
| 27 | **SSL 证书验证** | 启用默认验证，移除 `verify=False` 中间人风险 |
| 28 | **日历自动选择** | 按事件性质关键词自动选工作/个人日历 |
| 29 | **智能结束时间推断** | 会议 1h / 聚餐 2h / 航班 3h 等事件类型推断 |
| 30 | **搜索默认范围缩小** | 默认 180 天（原 365 天），减少 iCloud 响应时间和内存 |

### 🧹 代码清理（6 项）

| # | 变更 | 详情 |
|---|------|------|
| 31 | **`find_calendar` 空列表检查** | 无日历可访问时抛明确异常而非崩溃 |
| 32 | **`build_ical` 拆分** | 拆为 `build_vtimezone()` + `build_vevent()` 独立函数 |
| 33 | **pathlib 迁移** | LOG_DIR 使用 `Path(__file__).resolve().parent.parent` |
| 34 | **`parse_known_args` 替代 `parse_args`** | 忽略未知参数，兼容 Agent 传递额外参数 |
| 35 | **VALARM 描述含标题** | 提醒内容 `Reminder: {summary}` 而非空提醒 |
| 36 | **删除重复函数调用** | 避免同一次请求中的冗余网络调用 |

---

## 统计

- **总计：** 36 项变更
- **安全相关：** 8 项
- **时区/DST：** 4 项
- **网络韧性：** 5 项
- **架构改进：** 7 项
- **功能增强：** 6 项
- **代码清理：** 6 项
- **测试覆盖：** 95 个 case，全部通过
