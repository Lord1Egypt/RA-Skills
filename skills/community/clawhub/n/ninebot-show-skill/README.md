# Ninebot Show Skill

通用的九号/Ninebot 电动车只读 Agent Skill，采用 `SKILL.md` + `scripts/` + `references/` 的 Agent Skills 目录结构。可用于 Claude Code、Hermes Agent、OpenClaw，以及兼容 Agent Skills 标准的其他 Agent。

主要能力：车辆状态、电量/续航、充电、电池信息、智能服务剩余天数、位置、今日/本月骑行、最近骑行、地图截图和骑行轨迹图。

## 安装位置

将完整的 `ninebot-show-skill` 文件夹放到对应 Skills 目录：

- Claude Code：`~/.claude/skills/ninebot-show-skill/`
- Hermes：`~/.hermes/skills/ninebot-show-skill/`
- OpenClaw 工作区：`<workspace>/skills/ninebot-show-skill/`
- 通用 Agent Skills：`~/.agents/skills/ninebot-show-skill/`

也可以使用安装脚本，例如：

```bash
bash install.sh claude
bash install.sh hermes
bash install.sh openclaw
bash install.sh agents
```

如果已经由 ClawHub 或其他 Skill 管理器安装到正确目录，只需要执行：

```bash
bash scripts/setup.sh
```

## 首次配置

```bash
.venv/bin/ninecli login
.venv/bin/ninecli vehicles --json
```

将返回的车辆 `wnumber` 填入：

```text
~/.config/ninebot-show-skill/config.json
```

检查：

```bash
scripts/run.sh --check
```

生成报告：

```bash
scripts/run.sh
```

## 高德地图 Key

完整地址和高德静态地图是可选能力。设置 `AMAP_WEB_KEY` 或 `AMAP_WEBSERVICE_KEY`，也可以写入本机：

```text
~/.config/ninebot-show-skill/.env
```

不要把真实 `.env` 打进公开包。

## ClawHub 发布

本目录本身就是 ClawHub Skill 发布目录，根目录包含 `SKILL.md`。建议先 dry-run：

```bash
clawhub skill publish ./ninebot-show-skill \
  --slug ninebot-show-skill \
  --name "Ninebot Show Skill" \
  --version 3.2.1 \
  --changelog "Cross-agent Agent Skills package; privacy-safe examples; read-only Ninebot reports and smart-service remaining days." \
  --tags latest,ninebot,ebike \
  --dry-run
```

确认 dry-run 无问题后，去掉 `--dry-run` 正式发布。

## 隐私

公开包不得包含真实手机号、SN、VIN/车架号、MAC、UID/MID、device-id、Token、Cookie、蓝牙密钥、精确私人位置、真实骑行 ID、HAR、`.env`、实际 `config.json` 或日志。

公开示例统一使用 `references/example-data.md` 中的数据。详细规则见 `PRIVACY.md`。外部请求及其参数见 `references/network-privacy.md`。
