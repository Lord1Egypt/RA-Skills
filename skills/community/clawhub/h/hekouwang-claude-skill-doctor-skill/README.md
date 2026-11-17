# hekouwang-claude-skill-doctor-skill

> **会勇禾口王的AI笔记** 出品 · `@huiyonghkw`
> 不聊 AI 会不会取代你，只聊先用 AI 的人怎么取代你。

给 **Agent Skill（SKILL.md）** 做体检的工具。把"Skill 是按需加载的指令包、不是单文件巨石"
这条最佳实践，做成一个能跑在任何 skill 上的检查器：机检定量 + 模型定性，产出评分卡和可落地的修复建议。

## 30 秒验收

```bash
python3 check.py path/to/your-skill    # 体检任意 skill 目录
bash scripts/run-all-doctors.sh .      # 三件套（需已装 md-doctor + env-doctor）
```

姊妹工具：[`hekouwang-claude-md-doctor-skill`](https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill)（体检 AGENTS.md / CLAUDE.md）。

## 核心判据

> SKILL.md 是模型"决定要不要加载、加载后照着做"的运行时指令包。
> `description` 决定它何时被唤醒；正文越精简越准；厚重细节要能"按需展开"
> （references/ 用到再读），而不是每次触发就把全部细节灌进上下文。

## 用法

### 在 Claude Code 里（推荐）

直接用**自然语言**喊它，Claude 会自动加载本 skill、在底层跑机检、再做定性复核，给评分卡 + 按优先级的修复建议，并问要不要代为重构：

> - 「帮我体检 `~/.claude/skills/xxx` 这个 skill」
> - 「我的 SKILL.md 规范吗 / 是不是太长了 / 要不要拆 references」
> - 「audit this skill」「lint SKILL.md」

### 命令行直接跑（零依赖，仅需 Python 3）

```bash
python3 check.py <skill目录>          # 输出彩色报告
python3 check.py <skill目录> --json   # 机器可读 JSON（CI 可用）
python3 check.py <skill目录> --profile codex  # 严格校验 Codex 基础契约
```

退出码：有 FAIL → 1，否则 0（可用于 CI 卡关）。

### Codex 严格基础契约（可选）

默认 `agent` Profile 服务于 Claude/Codex/其他宿主共用的 Skill：合法的 `slug`、`version` 等宿主扩展字段不会被误伤。
如果你要按 Codex `skill-creator` 的基础规范验收一个纯 Codex Skill，附加 `--profile codex`：只允许
`name`、`description`、`license`、`allowed-tools`、`metadata`，并把不合规 kebab-case、description
中的尖括号和正文未完成的 `[TODO: ...]` 纳入 `gate`。报告 JSON 的 `profile` 字段会明确本次使用的档位。

这是一层可选的严格契约，不取代 Doctor 原有的跨宿主质量、安全、指针和扫描检查。

### 盘点多个 Skill

当传入的是宿主 Skill 根目录或仓库父目录时，用扫描模式。主机目录通常只看直接入口：

```bash
python3 check.py --scan --direct ~/.claude/skills --json
python3 check.py --scan /path/to/repository --json
python3 check.py --scan /path/to/codex-skills --profile codex --json
```

默认递归扫描会跳过测试夹具和构建目录；direct 模式只检查根目录下一层的宿主入口。
两种模式都会识别隐藏宿主目录、断开的软链、真实入口去重和重复 name。自动化应读取 JSON
里的 gate 字段；score/grade 只是质量参考，不能替代门禁判断。

### Docker（不想装 Python 也能跑）

```bash
# 拉已钉死 digest 的镜像；工作目录只读挂载（打 v* tag 时 Actions 同步发布到 GHCR）
IMG=ghcr.io/huiyonghkw/hekouwang-claude-skill-doctor-skill@sha256:<发布页当前 digest>
docker run --rm -v "$PWD:/work:ro" "$IMG"

# 或本地自建（Dockerfile 已 FROM python:3.12-slim@sha256:…）
docker build -t claude-skill-doctor .
docker run --rm -v "$PWD:/work:ro" claude-skill-doctor
docker run --rm -v "$PWD:/work:ro" claude-skill-doctor /work --json
```

### 接进 CI 卡关（GitHub Actions 示例）

```yaml
- uses: actions/setup-python@v5
  with: { python-version: "3.x" }
- name: SKILL.md 体检（不合格则拦 PR）
  run: |
    curl -sO https://raw.githubusercontent.com/huiyonghkw/hekouwang-claude-skill-doctor-skill/main/check.py
    python3 check.py path/to/your/skill
```

本仓库自身的 CI 见 [`.github/workflows/ci.yml`](.github/workflows/ci.yml)（语法 + good/bad 夹具 + JSON 合法性）。

## 检查项与门禁

| 权重 | 项 |
|---|---|
| **1.5（核心）** | 无硬编码密钥 · frontmatter 必填合法 · description 含「何时用」 · SKILL.md ≤500 行 · 渐进披露(拆 references/) · 可移植(无硬编码绝对路径) · 别替模型补它已会的 |
| 1.0（标准） | description ≤1024 · 指针无死链 · 脚本外置 scripts/ |
| 0.6（加内容） | allowed-tools 最小化 · 配套文档(README+CHANGELOG) |

分档：A ≥85 · B ≥70 · C ≥50 · D <50。

启用 `--profile codex` 时，Doctor 还会把 Codex 字段白名单、严格 name、description 与正文 TODO
纳入核心门禁；默认 `agent` Profile 不启用这层检查。除此之外，Doctor 还会把 frontmatter 解析错误、宿主调用策略冲突、文本读取失败、
目录身份不一致、断链和重名作为可审计结果输出。任何 FAIL 都会使 gate=FAIL。

## 机检 vs 定性

`check.py` 只判机器能确定的部分。**description 触发得准不准、正文是不是"图书馆"、
是不是在替模型补它已会的知识**——这些要人/模型读正文复核（脚本会标出疑点）。
完整定性流程见 `SKILL.md`。

## 免费 / 付费

| | 免费（开源） | 付费增值 |
|---|---|---|
| 机检 | `check.py` 文本/JSON + ASCII 评分条 | 品牌可视化报告卡 |
| CI | 退出码卡关 | — |
| 联系 | GitHub Issue | **@huiyonghkw**（ClawHub / GitHub） |

- **免费**：`check.py` 的文本 / JSON 报告 + 评分，随便用、可进 CI。
- **付费增值**：品牌可视化体检报告卡（精美分享图），找 `@huiyonghkw`。

## 体检器三件套

[`md-doctor`](https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill) · [`env-doctor`](https://github.com/huiyonghkw/hekouwang-env-doctor-skill) · 一键 `bash scripts/run-all-doctors.sh`（见 `references/doctor-suite.md`）。

---

—— 会勇禾口王的AI笔记 · @huiyonghkw
