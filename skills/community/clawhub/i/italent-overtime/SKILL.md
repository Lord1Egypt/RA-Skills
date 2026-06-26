---
name: italent-overtime
description: 北森 iTalent 加班管理。当用户需要推送加班、查询加班、撤销加班、管理考勤时使用此技能。支持通过北森开放平台 API 执行加班数据推送、查询、撤销等操作。需要用户提供 AppKey、AppSecret 和员工邮箱/StaffId。
---

# 北森 iTalent 加班管理 Skill

管理北森 iTalent 开放平台的加班数据，支持推送加班、查询加班、撤销加班等功能。

## 🚀 快速开始

### 1. 安装后首次使用

```bash
# 认证获取 access_token（包装器脚本会自动检测 Python）
~/.openclaw/skills/italent-overtime/scripts/italent-overtime auth \
    --key "你的 AppKey" \
    --secret "你的 AppSecret" \
    --save
```

### 2. 使用示例

**推送加班：**
```bash
~/.openclaw/skills/italent-overtime/scripts/italent-overtime push \
    --email "zhangsan@company.com" \
    --start "2024-01-01 18:00:00" \
    --end "2024-01-01 20:00:00" \
    --reason "项目上线"
```

**查询加班：**
```bash
~/.openclaw/skills/italent-overtime/scripts/italent-overtime list \
    --staff-ids 11xxxxx80 \
    --start 2024-01-01 \
    --end 2024-01-07
```

**撤销加班：**
```bash
~/.openclaw/skills/italent-overtime/scripts/italent-overtime cancel \
    --overtime-id "xxx-xxx-xxx"
```

---

## 📋 何时使用此 Skill

使用此 Skill 当用户需要：

- ✅ 推送加班数据到北森系统
- ✅ 查询员工的加班记录
- ✅ 撤销已提交的加班申请
- ✅ 管理考勤相关的加班数据
- ✅ 批量处理加班申请

**不要使用** 当用户需要：
- ❌ 查询请假记录（使用请假相关 Skill）
- ❌ 查询打卡记录（使用考勤相关 Skill）
- ❌ 修改北森系统配置（需要管理员权限）

---

## 🔧 命令参考

### auth - 获取访问令牌

首次使用必须先执行认证。

```bash
scripts/italent-overtime auth \
    --key "AppKey" \
    --secret "AppSecret" \
    --save
```

**参数：**
- `--key` - 北森开放平台 AppKey（必填）
- `--secret` - 北森开放平台 AppSecret（必填）
- `--save` - 保存 token 到配置文件（推荐）

---

### push - 推送加班

推送加班数据至北森系统，并发起审批。

```bash
scripts/italent-overtime push \
    --email "邮箱" \
    --start "2024-01-01 18:00:00" \
    --end "2024-01-01 20:00:00" \
    --reason "加班原因"
```

**参数：**
- `--email` - 员工邮箱（与 staff-id 二选一）
- `--staff-id` - 北森 StaffId（与 email 二选一）
- `--start` - 开始时间，格式：`2024-01-01 18:00:00`（必填）
- `--end` - 结束时间，格式：`2024-01-01 20:00:00`（必填）
- `--compensation` - 加班补偿方式（默认：1）
- `--reason` - 加班原因
- `--category` - 加班类别 (UUID)
- `--transfer-org` - 支援组织
- `--transfer-pos` - 支援职位 (UUID)
- `--transfer-task` - 支援任务 (UUID)
- `--identity-type` - 主键类型：0=员工邮箱，1=北森 UserId（默认：0）
- `--json` - 以 JSON 格式输出结果

---

### list - 查询加班

查询员工的安排加班数据。

```bash
scripts/italent-overtime list \
    --staff-ids 11xxxxx80,11xxxxx81 \
    --start 2024-01-01 \
    --end 2024-01-07
```

**参数：**
- `--staff-ids` - 员工 ID 列表，多个用逗号分隔（必填）
- `--start` - 开始日期，格式：`2024-01-01`（必填）
- `--end` - 结束日期，格式：`2024-01-07`（必填）
- `--json` - 以 JSON 格式输出结果

**注意：** 每次查询数量最多 100 条（员工数 × 天数 ≤ 100）

---

### cancel - 撤销加班

撤销指定加班，并发起审批。

```bash
scripts/italent-overtime cancel \
    --overtime-id "xxx-xxx-xxx"
```

**参数：**
- `--overtime-id` - 要撤销的加班 ID（必填）
- `--json` - 以 JSON 格式输出结果

---

## ⚠️ 注意事项

### Token 管理
- `access_token` 有效期为 **2 小时**（7200 秒）
- 过期后需要重新执行 `auth` 命令
- 使用 `--save` 参数会自动保存到 `~/.italent-overtime.conf`

### API 限制
- **频率限制：** 50 次/秒，1500 次/分钟
- **推送限制：** 单次只能推送一条加班数据
- **查询限制：** 每次最多查询 100 条记录

### 业务规则
- 不能提交历史考勤期间的单据
- 加班日期必须是企业配置的工作日
- 企业需要在北森后台配置加班项目

---

## 🐛 常见错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `未找到 access_token` | 未执行认证 | 执行 `auth` 命令 |
| `HTTP 错误：Unauthorized` | Token 过期 | 重新执行 `auth` 命令 |
| `不能提交历史考勤期间的单据` | 日期是过去 | 使用未来日期 |
| `您的企业没有 [工作日加班项目]` | 企业未配置 | 联系管理员配置 |
| `参数不可为空` | 缺少必填参数 | 检查命令参数 |

---

## 📁 文件结构

```
italent-overtime/
├── SKILL.md                      # 本文件
├── scripts/
│   ├── italent-overtime          # CLI 包装器（自动检测 Python，推荐使用）
│   └── italent-overtime-simple.py  # CLI 主程序（纯 Python）
├── references/
│   ├── api-docs.md               # API 接口文档
│   └── troubleshooting.md        # 故障排查指南
└── assets/
    └── logo.png                  # Skill 图标（可选）
```

---

## 🔗 参考资料

- [API 接口文档](references/api-docs.md)
- [故障排查指南](references/troubleshooting.md)
- 北森开放平台：https://open.italent.cn
- Token 接口：POST https://openapi.italent.cn/token

---

## 🤖 在 OpenClaw 中使用

在 OpenClaw 对话中直接说：

```
帮我推送一个加班：
- 员工邮箱：zhangsan@company.com
- 时间：今晚 18:00 到 20:00
- 原因：项目上线
```

OpenClaw 会自动调用此 Skill 执行。

---

**版本：** 1.1.0  
**作者：** 佳敏  
**更新时间：** 2026-03-31
