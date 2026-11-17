# 部署与分享指南（feishu-mail-workboard）

面向要把邮件看板部署到自己 WorkBuddy、或分享给同事的两种场景。

## 一、同事在自己 WorkBuddy 部署（最简路径：一键安装）

1. 收到 `feishu-mail-workboard.skill` 文件后，拖入 WorkBuddy 窗口或双击，
   自动安装到 `~/.workbuddy/skills/feishu-mail-workboard/`。
2. 确认 WorkBuddy 已连接**飞书**连接器（设置 → 连接器 → 飞书 → 已授权）。
3. 一键安装（建 config + 注册每日自动化）：

   ```bash
   cd ~/.workbuddy/skills/feishu-mail-workboard
   python scripts/install.py
   # 按提示填：昵称 / 邮箱 / 飞书 open_id；随后自动注册每天 08:00 的自动化
   ```

   不想注册自动化：`python scripts/install.py --no-automation`；想改时间：`--hour 9`。

4. 先本地预览（不推送）：

   ```bash
   cd scripts
   python daily_mail_board.py --no-push
   # 打开生成的 mail_workboard2.html 检查
   ```

5. 确认无误后正式推送：

   ```bash
   python daily_mail_board.py
   ```

### 手动路径（不用 install.py）

```bash
cd ~/.workbuddy/skills/feishu-mail-workboard/scripts
cp config.example.json config.json
# 编辑 config.json：mailbox / feishu_open_id / feishu_name
python daily_mail_board.py --no-push   # 预览
python daily_mail_board.py             # 推送
```

## 二、查自己的飞书 open_id

```bash
lark-cli im +contacts --query "你的姓名或邮箱" --format json
# 从返回里取 user_id（形如 ou_xxxxxxxxxxxxxxxx）
```

把这个值填进 `config.json` 的 `feishu_open_id`。看板卡片与 @提醒会发往该账号。

## 三、每日自动化（推荐）

`install.py` 会幂等注册到 `~/.workbuddy/workbuddy.db`（名称「每日邮件看板推送」，`FREQ=DAILY;BYHOUR=8;BYMINUTE=0`）。
它跑完整流程：拉邮件 → 生成看板 → 推飞书 → 导出待译清单 → 中文翻译 → 重推含中文摘要的看板。

如需手动建自动化：
- 名称：每日邮件看板推送
- 计划：recurring，rrule `FREQ=DAILY;BYHOUR=8;BYMINUTE=0`
- 提示词（含中文翻译）：
  `运行 feishu-mail-workboard 技能：依次执行 daily_mail_board.py（拉取+生成+推送）、build_cn_inbox.py、cn_translate.py 导出待译清单并按 references/cn-translate.md 翻译、cn_translate.py --apply 写回、PUSH_TAG=-cn daily_mail_board.py --skip-pull 重推。`

脚本内置基于日期的 `PUSH_TAG` 幂等键，同日多次运行不会重复推送同一条消息。
如需避开某天，设环境变量 `PUSH_TAG=-v2-xxx` 可绕过同日去重。

## 三·五、中文翻译层（可选增强）

```bash
cd ~/.workbuddy/skills/feishu-mail-workboard/scripts
python cn_translate.py               # 导出待译清单 cn_inbox.json
python cn_translate.py --full        # 全量（含其他待办 / 西葡）
# ……交给 LLM 翻译，产出 译文.json ……
python cn_translate.py --apply 译文.json   # 校验并写回 workboard2_cn.json
python cn_translate.py --show        # 查看词典概况
```

翻译规则见 `references/cn-translate.md`。无 `workboard2_cn.json` 时看板中文模块占位，不影响其他功能。

## 四、命令速查

| 命令 | 作用 |
|------|------|
| `python install.py` | 一键建 config + 注册每日自动化 |
| `python daily_mail_board.py --no-push` | 仅生成 HTML 看板，不推送 |
| `python daily_mail_board.py` | 生成并推送飞书（卡片 + 附件） |
| `python daily_mail_board.py --dry` | 校验卡片 JSON 合法性，不真发 |
| `python daily_mail_board.py --skip-pull` | 复用已有邮件数据重新生成 |
| `python daily_mail_board.py --skip-pull --no-push` | 纯本地重渲染 |
| `python cn_translate.py` | 导出待译清单 |
| `python cn_translate.py --apply 译文.json` | 校验并写回中文词典 |

## 五、排错

- **`lark-cli failed` / 拉不到邮件**：飞书连接器未登录或过期 → 重新授权。
- **推送报 `parse card json err`**：卡片 JSON 被 shell 引号拆坏。脚本已统一用双引号 `<font>` 并移除 `column.corner_radius`；若仍报错，先用 `--dry` 看 stderr。
- **`@` 不到人**：open_id 错 → 用 `lark-cli im +contacts` 复核。
- **看板空白**：先跑 `--no-push`；若 `email_detail.json` 为空，说明近 7 天无旗标/聚焦邮件，或邮箱拉取失败。

## 六、分享给同事的两种方式

- **方式 A（推荐）**：在本机执行技能目录的 `package_skill.py`（或由 WorkBuddy 导出），
  得到 `feishu-mail-workboard.skill`，发给同事双击安装。
- **方式 B（手动）**：把 `scripts/` 全部 `.py` + `config.example.json` + `references/` 打包发同事，
  对方放到任意目录并自建 `config.json` 即可，无需安装技能框架。
