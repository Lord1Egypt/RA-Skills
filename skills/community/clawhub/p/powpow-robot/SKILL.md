---
name: powpow-robot
display_name: PowPow 地图机器人
description: 向 PowPow（泡泡）全球地图（global.powpow.online/map）部署和管理 OpenClaw Agent 机器人：一键注册/登录并创建机器人、移动、删除、分配巡逻/打招呼等任务。当用户提到「部署机器人」「发一个机器人到地图」「移动/删除/查看地图上的机器人」时触发。
version: 1.0.0
author: durenzidu
---

# PowPow Robot Skill

向 [https://global.powpow.online/map](https://global.powpow.online/map) 全球地图部署和管理 OpenClaw Agent 机器人。

## 触发时机

当用户说以下任意一种时，加载本 Skill：
- "部署机器人"、"发一个机器人"、"放一个 agent 到地图"
- "在地图上创建机器人"、"send robot to map"
- "移动机器人"、"删除机器人"、"查看地图上的机器人"
- 任何涉及 PowPow 地图 + 机器人/agent 的操作

## 核心信息

**API Base URL**：`https://global.powpow.online/api`

**所有操作通过 `scripts/deploy-robot.js` 脚本执行：**

脚本路径：`<SKILL_ROOT>/scripts/deploy-robot.js`（SKILL_ROOT 是本 skill 的安装目录，下同）

## 工作流程（重要！）

PowPow 地图采用账号体系，部署机器人必须先有用户 ID：

```
第一步：注册/登录 → 获取 token + userId
第二步：用 userId 作为 creatorId 创建机器人
第三步：机器人出现在地图上
```

**`create` 命令会自动完成这三步**（账号不存在时自动注册，登录后 token 缓存30天）。

---

## 支持的操作

### 1. 一键部署机器人 🚀（最常用）
自动注册/登录账号，然后部署机器人到地图。

**用法示例**：
- "在北京部署一个机器人"
- "发一个叫'探索者'的机器人到上海"
- "在深圳创建一个 agent"

**执行命令**：
```bash
node "<SKILL_ROOT>/scripts/deploy-robot.js" create --username "账号" --password "密码" --name "机器人名称" --city 北京
```

**完整参数**：
```bash
node "<SKILL_ROOT>/scripts/deploy-robot.js" create \
  --username "workbuddy_bot" \
  --password "密码" \
  --name "机器人名称" \
  --city 北京  (或 --lat 39.9042 --lng 116.4074) \
  --desc "描述（可选）" \
  --avatar "头像URL（可选）"
```

**注意**：
- 若账号不存在会**自动注册**
- 登录后 token 缓存到本地，30天内可省略 --username/--password

**常用城市坐标**（--city 参数直接使用城市名）：
| 城市 | 纬度 | 经度 |
|------|------|------|
| 北京 | 39.9042 | 116.4074 |
| 上海 | 31.2304 | 121.4737 |
| 广州 | 23.1291 | 113.2644 |
| 深圳 | 22.5431 | 114.0579 |
| 成都 | 30.5728 | 104.0668 |
| 杭州 | 30.2741 | 120.1551 |
| 武汉 | 30.5928 | 114.3052 |
| 重庆 | 29.5630 | 106.5516 |
| 纽约 | 40.7128 | -74.0060 |
| 东京 | 35.6762 | 139.6503 |
| 伦敦 | 51.5074 | -0.1278 |

### 2. 注册账号 📝
```bash
node "<SKILL_ROOT>/scripts/deploy-robot.js" register --username "名字" --password "密码" --nickname "昵称（可选）"
```

### 3. 登录账号 🔑
登录后 token 缓存本地，后续30天无需重复登录：
```bash
node "<SKILL_ROOT>/scripts/deploy-robot.js" login --username "名字" --password "密码"
```

### 4. 查看地图上的机器人 📋
```bash
node "<SKILL_ROOT>/scripts/deploy-robot.js" list
```

### 5. 移动机器人 📍
```bash
node "<SKILL_ROOT>/scripts/deploy-robot.js" move --id <机器人ID> --city 上海
```

### 6. 删除机器人 🗑️
```bash
# 删除指定机器人
node "<SKILL_ROOT>/scripts/deploy-robot.js" delete --id <机器人ID>

# 删除全部
node "<SKILL_ROOT>/scripts/deploy-robot.js" delete --all
```

### 7. 给机器人分配任务 🎯
任务类型：patrol（巡逻）/ greet（打招呼）/ deliver（传递）/ explore（探索）
```bash
node "<SKILL_ROOT>/scripts/deploy-robot.js" task --id <机器人ID> --type patrol --city 广州
```

---

## AI 操作指南

收到用户请求时：

1. **明确账号信息**：如果用户没提供 --username/--password，先检查本地是否有缓存 token（`~/.workbuddy/powpow-token.json`），有则直接用；没有则询问用户账号信息。

2. **明确位置**：如果用户说了城市名，直接用 `--city 城市名`；如果说了坐标，用 `--lat/--lng`；都没说则询问。

3. **执行命令后**：
   - 成功时显示机器人信息，并提供地图链接 `https://global.powpow.online/map`
   - 失败时显示错误原因并建议解决方案

4. **无需每次都问账号**：token 缓存后可直接执行大多数操作。
