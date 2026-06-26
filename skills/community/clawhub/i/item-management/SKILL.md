---
name: item-management（物品架）
version: v1.2.0
description: 物品电子信息管理技能。用于记录、整理、查询个人物品数据。触发关键词：物品管理、记录物品、添加物品、物品清单、物品统计、物品到期、物品过期、物品搜索、整理物品、我的物品、物品架、盘点、断舍离、我的物品架、物品架管理、归物、my-item。
---

# 物品管理 (Item Management)

用自然语言管理个人物品数据库，支持添加、查询、编辑、统计、导出和到期提醒。

## 功能一览

| 功能 | 说明 |
|------|------|
| 增删改查 | 添加/编辑/删除物品，查看清单和详情 |
| 日均成本 | 自动计算购入至今的日均花费 |
| 到期提醒 | 即将到期/已过期进度条 |
| 子物品 | 套装内物品独立管理 |
| 历史追踪 | 记录价格、数量、状态变化 |
| 导出 | 支持 CSV / JSON / HTML 三种格式 |
| 备份恢复 | JSON 格式完整备份，支持合并/完整恢复 |
| 统计报告 | 生成可打印的 HTML 报告（Ctrl+P 转 PDF） |

## 数据存储位置（跨平台）

用户数据存储在**用户家目录**下，**独立于技能目录**，技能更新不会丢失数据：

| 操作系统 | 数据路径 |
|---------|----------|
| Windows | `C:\Users\用户名\item-management-data\` |
| macOS | `~/Library/Application Support/item-management/` |
| Linux | `~/.local/share/item-management/` |
| 自定义 | 可通过 `OPENCLAW_WORKSPACE` 或 `XDG_DATA_HOME` 环境变量指定 |

数据目录结构：
```
item-management-data/
  items.db          ← SQLite 数据库（所有物品数据）
  backups/          ← JSON 备份文件夹
    backup_20260428_180129.json
    backup_20260428_120000.json
```

**备份文件是纯 JSON**，可以用任何文本编辑器打开，也是跨平台迁移的关键。

## 备份与恢复（重要！）

### 为什么要备份？
技能数据存在用户本地，如果重装系统/换电脑，数据会丢失。
每次重要变更后建议备份，并上传到云端。

### 创建备份
```bash
item backup              # 一键备份到数据目录
item backup --path /path/to/backup.json  # 指定路径
```

### 恢复数据
```bash
item restore                                    # 从最新备份恢复
item restore backup_20260428_180129.json       # 指定文件
item restore --merge backup.json               # 合并模式（只添加不重复）
```

### 查看存储信息（含云备份）
```bash
item info               # 显示数据库路径、备份列表
```

**重要：执行 `item info` 后，AI 必须额外展示云备份板块。**

#### 云备份状态展示规则

AI 需要检查配置文件 `~/.qclaw/workspace/item-management-cloud-config.json`（工作区目录下），按以下规则展示：

**1. 配置文件不存在（未配置云备份）：**
```
☁️ **云备份：未配置**

推荐方案：
| 方案 | 特点 |
|------|------|
| 📁 OneDrive/iCloud | 放到云盘同步文件夹，全自动同步 |
| ⏰ 定时+云盘 | OpenClaw 定时备份 + 云盘自动同步 |
| 📧 邮箱 | 备份发到自己邮箱，最简单 |
| ☁️ 微云 | 腾讯生态，扫码授权即可 |
| 🐙 GitHub Gist | 有版本历史 |

想配置的话直接说「帮我配置云备份」
```

**2. 配置文件存在（已配置）：**
读取 JSON 配置并展示当前状态：
```
☁️ **云备份：已配置**
- 方式：{provider}（如 onedrive / weiyun / email / gist）
- 路径/目标：{path_or_target}
- 上次云端备份：{last_backup_time}
- 状态：✅ 正常 / ❌ 需要重新授权

💡 立即备份？说「备份物品到云端」
💡 想换方案？说「帮我配置云备份」
```

**配置文件格式（`item-management-cloud-config.json`）：**
```json
{
  "provider": "onedrive",
  "path": "D:\\OneDrive\\物品架",
  "last_backup": "2026-04-28 19:30:00",
  "auto_backup": true,
  "cron_job_id": "job_xxx"
}
```

> 当用户成功配置云备份后，AI 必须创建/更新此配置文件。

### 换电脑/重装后怎么做？
1. 在新设备上安装技能
2. 把备份 JSON 文件传到新设备
3. 运行 `item restore your_backup.json` 恢复所有数据

### 云端同步建议
备份文件（JSON）可以上传到：
- **微云/QQ网盘** - 腾讯系生态
- **iCloud / OneDrive / Google Drive** - 自动同步
- **邮箱附件** - 简单可靠
- **GitHub Gist** - 有版本控制

## 核心字段说明

| 字段 | 说明 |
|------|------|
| `name` | 物品名称（必填） |
| `brand` | 品牌 |
| `quantity` | 数量（默认1） |
| `unit` | 单位（默认"个"） |
| `production_date` | 生产日期（YYYY-MM-DD） |
| `expiry_date` | 保质期到期日 |
| `warranty_date` | 保修期到期日 |
| `opened_date` | 开封日期 |
| `location` | 存放位置 |
| `notes` | 备注 |
| `price` | 单价（元） |
| `tags` | 标签（逗号分隔） |
| `image_path` | 图片路径 |
| `status` | 状态：active / consumed（已用完）/ discarded（已丢弃） |

## 自然语言命令映射

### 添加物品
用户说："记录一个新物品"、"添加一个..."、"买了个..."、"记录一下"
→ 解析参数，调用 `item_cli.py add`

```python
# 示例解析
item_cli("add", "SK-II 护肤精华露", 
         brand="SK-II", qty=1, price=899.0,
         expiry="2026-10-01", location="卧室梳妆台",
         opened="2025-04-01",
         tags="护肤,化妆品,面部护理")
```

### 查看物品
- "查看我的物品"、"列出所有物品"、"物品清单" → `item list`
- "按品牌排序" → `item list --sort brand`
- "按过期日排序" → `item list --sort expiry_date`
- "只看护肤类的" → `item list --tag 护肤`

### 查看详情
- "查看某物品详情" → `item get <id>`
- "物品#3 详细信息" → `item get 3`

### 更新物品
- "把某物品数量改为2" → `item update <id> --qty 2`
- "标记某物品已开封" → `item update <id> --opened 2025-04-01`
- "标记某物品已用完" → `item update <id> --status consumed`

### 删除物品
- "删除某物品" → `item delete <id>`（先确认）

### 子物品（套装）
- "给物品5添加一个子物品：替换装" → `item sub-add 5 替换装 --qty 2`
- "列出物品5的所有子物品" → `item sub-list 5`

### 历史记录
- "查看某物品的变更历史" → `item history <item_id>`
  （自动记录：价格、开封日期、数量、状态变化）

### 到期提醒
- "哪些物品快过期了" → `item expiring --days 7`（默认7天）
- "已经过期的物品" → `item expired`

### 数据统计
- "物品统计数据"、"我有多少东西" → `item stats`
  （输出：总品类数、总件数、总估算价值、按月新增趋势）

### 导出
- "导出 CSV" → `item export --format csv`
- "导出 JSON" → `item export --format json`
- "导出 HTML 表格" → `item export --format html`
- `item export --out path.csv` 指定保存路径

### 统计报告
- "生成报告" → `item report` 输出完整 HTML 页面
  （含概览统计、即将到期、已过期、全量物品列表、月度趋势）
  用浏览器打开后按 **Ctrl+P → 另存为 PDF** 即可打印

### 搜索
- "搜一下我有几个SK-II的" → `item search SK-II`
- "找找化妆品" → `item search 化妆品`

## 日均成本

每个物品会自动计算日均花费（单价 ÷ 购入天数），显示在「单价」下方。
- 购入当天：日均 = 单价（购入不足1天）
- 保质期至不为空时：同时显示到期倒计时进度条

调用 `_date_progress(expiry_str)` 生成可视化状态：

```
days_until > 7    → ✅ 剩余 N 天到期（正常，绿色）
0 ≤ days_until ≤ 7 → ⏳ 即将到期：还剩 N 天（黄色预警）
days_until < 0    → ⚠️ 已过期 N 天（红色警告）
expiry_date 为空  → — 状态未知
```

## 执行方式

物品架是 **自然语言技能**，通过对话触发即可。

### 触发关键词

| 意图 | 触发词（任选其一） |
|------|------------------|
| 添加物品 | 「添加一个XX」「记录一个新物品」「买个了XX」 |
| 查看清单 | 「我的物品」「物品清单」「列出所有物品」 |
| 查看统计 | 「物品统计」「我有多少东西」 |
| 搜索物品 | 「搜一下XX」「找找XX」 |
| 物品详情 | 「查看XX详情」「XX详细信息」 |
| 更新物品 | 「把XX的数量改成N」「把XX标记为已开封」 |
| 删除物品 | 「删除XX」「把手表删掉」 |
| 到期提醒 | 「哪些快过期了」「已经过期的物品」 |
| 备份恢复 | 「备份物品」「恢复物品数据」「帮我配置云备份」「备份物品到云端」 |
| 存储信息 | 「查看物品存储信息」「数据存在哪」「云备份状态」 |
| 导出报告 | 「导出CSV」「生成报告」 |
| 搜索历史 | 「查看XX的变更记录」 |

### 手动调试

在终端中进入技能目录后执行：

```bash
# 进入技能目录（自动定位）
cd ~/.qclaw/skills/item-management/scripts

# 查看物品
python item_cli.py list

# 添加物品
python item_cli.py add 手表 --price 200 --prod 2026-04-28

# 备份
python item_cli.py backup
```

> 💡 CLI 会自动将数据写入用户家目录（`~/item-management-data/`），**无需指定路径**，也不依赖技能目录。

## 输出格式要求

- 输出使用中文
- 物品列表前显示总数（如"📦 共 12 种物品"）
- 每条物品之间用空行分隔
- 统计页面数字对齐展示
- **列表需要包含所有核心字段**

## ⚠️ 强制回复规则（必须遵守）

**每次回复用户物品相关内容时，回复末尾必须包含以下两行：**

```
*💡 试试对我说：查看物品统计 / 搜索XX / 备份物品*

*想备份数据防丢失？直接说「查看物品存储信息」*
```

**规则说明：**
- 第一行是**使用提示**，随机换一个有用的命令提示，如：查看所有物品 / 物品统计 / 搜索XX / 备份物品 / 哪些快过期了 / 导出报告
- 第二行是**备份提示**，固定文案：`*想备份数据防丢失？直接说「查看物品存储信息」*`
- 两行都用 Markdown **斜体**（`*...*`），视觉上弱化，不抢主内容
- **没有例外**，无论是添加、查看、统计、搜索、更新、删除，都必须带这两行
