---
name: feishu-mail-workboard
description: >-
  把飞书邮箱近 7 天邮件一键整理成「门店建店情报看板」，并每日自动推送飞书卡片。
  自动抽取重点门店线索（科隆/罗马/杜塞/苏黎世）、西葡业务与交期事项，生成含临期三档提醒
  （已逾期/临期/关注）、🇨🇳中文摘要翻译、已回复按钮的自包含 HTML 看板，一键安装并注册每日自动化。
  Use when 用户说“生成邮件看板”“做每日邮件汇总”“把飞书邮件整理成看板”“刷新并推送邮件看板”
  “部署邮件看板给同事”“邮件工作清单”时使用。
allowed-tools: Read,Write,Bash
license: MIT
metadata:
  display_name: "📬 邮件雷达 MailRadar"
  tags: [邮件, 看板, 飞书, 门店, 建店, 自动化]
---

# 飞书邮件工作看板（Feishu Mail Workboard）

把飞书邮箱近 7 天的邮件，自动整理成一份**可离线打开的 HTML 看板** + **每日飞书推送卡片**。
看板含 4 个模块：① 往来邮件 Summary（KPI + 图表 + 临期三档提醒）② 西南欧建店管理（4 城）
③ 西葡地区非建店业务跟踪 ④ 其他事项（下单/交付/交期）。

## 适用场景（触发词）

- “生成/刷新邮件看板”“做每日邮件汇总”“邮件工作清单”
- “部署邮件看板给同事”“把飞书邮件整理成看板”“推送邮件日报到飞书”
- 新建每日自动化（cron 每天 08:00 跑一次）

## 前置条件

1. WorkBuddy 已连接**飞书**（Feishu）连接器，`lark-cli` 可用且已登录。
2. Python 3（系统或 WorkBuddy 托管运行时均可）。
3. 看板会读取你飞书邮箱的 **flagged（旗标）** 与 **inbox** 邮件——确保需要跟进的邮件已加旗标。

## 快速开始

### 1. 安装

- 已打包为 `.skill` 文件：直接双击/拖入 WorkBuddy 即可安装到 `~/.workbuddy/skills/`；
- 或把本技能 `scripts/` 全部 `.py` 文件 + `config.json` 放到任意工作目录。

### 2. 配置（每个使用者只需改一次）

复制 `scripts/config.example.json` 为同目录 `config.json`，填入：

```json
{
  "mailbox": "你的飞书邮箱地址",
  "feishu_open_id": "接收看板推送的飞书 user open_id（用 lark-cli im +contacts 查）",
  "feishu_name": "你的飞书昵称（用于 @提醒）",
  "push_enabled": true
}
```

> 不想写文件也可走环境变量：`MAILBOARD_ME` / `MAILBOARD_OPEN_ID` / `MAILBOARD_NAME`。
> 留空 `feishu_open_id` 则只生成 HTML 看板、不推送飞书（适合先本地预览）。

### 3. 运行

```bash
# 仅生成数据 + HTML 看板（不推送，先本地看效果）
python daily_mail_board.py --no-push

# 生成并推送到飞书（卡片 + HTML 附件）
python daily_mail_board.py

# 复用上次拉取的邮件数据重新生成（不重新拉取）
python daily_mail_board.py --skip-pull --no-push

# 真发前先 dry-run 校验卡片 JSON 合法性
python daily_mail_board.py --dry
```

### 4. 一键安装 + 每日自动化（推荐）

本技能带 `install.py`，一条命令完成「建配置 + 注册每日自动化」：

```bash
python scripts/install.py               # 交互式：填昵称/邮箱/open_id → 自动注册每天 08:00 自动化
python scripts/install.py --hour 9      # 改成每天 09:00
python scripts/install.py --no-automation   # 只建 config，不注册自动化
python scripts/install.py --name 张三 --mailbox a@b.com --open-id ou_xxx  # 非交互
```

自动化会：拉邮件 → 生成看板 → 推送飞书 → 导出待译清单 → 完成中文翻译 → 重推含中文摘要的看板。
若不想自动化，也可手动在 WorkBuddy 建每日自动化，提示词参考 `references/deploy.md`。
脚本内置 `PUSH_TAG` 幂等键，同日重跑不会重复推同一条。

## 输出说明

- `mail_workboard2.html`：自包含看板（内联 CSS/JS，无外部 CDN），离线可开。
- 飞书消息：一条交互卡片（三栏 🔴已逾期 / 🟡临期 / 🔵关注）+ 一个 HTML 附件；
  若明日有“需催反馈”的截止项，额外推送一条 @提醒。

## 模块与业务逻辑（默认保留，可按需改）

看板默认围绕 **DREAME/MOVA 欧洲建店**组织：4 城（Cologne/Rome/Dusseldorf/Zurich）、
西葡非建店业务（Spain/Portugal/POSM/Endcap/Brandzone）。同事同做欧洲建店可直接复用；
若你的业务不同，改 `daily_mail_board.py` 的 `collect_ddl_items` 城市列表与
`gen_dashboard3.py` 的 `trSubj` 中文翻译表、`extract4.py` 的 `classify_store` 即可。

## 🇨🇳 中文翻译层（已捆绑）

看板的「🇨🇳 邮件摘要翻译」模块由 `workboard2_cn.json` 词典驱动。本分享版已打包完整翻译层：

| 脚本 | 作用 |
|------|------|
| `prep_cn.py` | 生成全量待译清单 `cn_inbox_full.json`（清洗正文 + 全部非自发送线程） |
| `build_cn_inbox.py` | 从全量筛选重点 `cn_inbox.json`（含 DDL 或近 14 天活跃，每店上限 6） |
| `cn_translate.py` | 导出待译清单 / 校验并合并 LLM 译文 → `workboard2_cn.json` |

流程（`daily_mail_board.py` 已自动跑前两步）：

```bash
python cn_translate.py               # 导出待译清单（供 LLM 翻译）
python cn_translate.py --full        # 全量（含其他待办 / 西葡）
python cn_translate.py --apply 译文.json   # 校验并写回 workboard2_cn.json
python cn_translate.py --show        # 查看当前词典概况
```

翻译规则与译文示例见 `references/cn-translate.md`。无 `workboard2_cn.json` 时看板该模块渲染占位，不影响其他功能。

## 常见问题

- **拉不到邮件**：先 `lark-cli` 登录；检查飞书连接器是否已连接。
- **推送发不到人**：`feishu_open_id` 填错 → `lark-cli im +contacts` 重新查正确的 open_id。
- **退信污染看板**：`is_bounce()` 已过滤中英文退信（邮件退信/退信/投递失败…），无需处理。
- **时间窗口**：默认只抓近 7 天；超 7 天的邮件不进统计。改 `build()` 的 `start_days=7` 可调整。
