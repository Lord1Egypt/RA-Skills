# hermes-doctor

> Hermes Agent (NousResearch) 故障诊断与抢救 skill — 适用于 Hermes / OpenClaw / 其他兼容 SKILL.md 格式的 agent runtime。

[![ClawHub](https://img.shields.io/badge/clawhub-hermes--doctor-blue)](https://clawhub.ai/skills/hermes-doctor)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platforms](https://img.shields.io/badge/platforms-windows%20%7C%20macos%20%7C%20linux-lightgrey)]()

## 它解决什么问题

Hermes Agent 出问题时,典型症状有几大类:

- `HTTP 401: Authentication Fails — your api key: ****xxx is invalid`(包括迷惑性的 `****ired`,**通常不是 expired 而是字面字符串 `no-key-required`** 被脱敏遮成 `ired` 后缀)
- `Authorization: Bearer no-key-required` 字面占位符出现在请求 header
- `hermes setup` 走到 provider 配置步骤直接显示绿色 ✓ 不让你输入 key(issue #16394)
- `/model` 切换 provider 后立刻 401/404(issue #3685 api_mode 残留)
- `gateway already running` 启动失败
- DeepSeek V4 Pro via OpenRouter 引发 gateway crash loop(issue #16677)
- WAL 文件巨大、stale config、broken symlink

这个 skill 把上面所有症状的**精确根因 + 可执行 workaround** 沉淀成可重复使用的诊断流程,让 agent(或人类 SRE)看到症状后秒诊。

## 它做了什么(progressive disclosure)

按 Anthropic Skills 三级渐进披露架构组织:

| 层级 | 内容 | 加载时机 |
|---|---|---|
| Tier 1 — Metadata | `SKILL.md` frontmatter(name + description ≤1024) | 启动时全列表加载,描述命中即触发 |
| Tier 2 — Main | `SKILL.md` 正文(何时触发、黄金 5 步、症状速查表、危险动作清单) | skill 被选中时 |
| Tier 3 — References | `references/*.md`、`templates/*.md`、`assets/*.json` | 按需加载 |

## 目录结构

```
hermes-doctor/
├── SKILL.md                                  # 主入口
├── references/
│   ├── auth-troubleshooting.md               # 401 / 占位符注入 / setup 静默跳过
│   ├── credential-pool-and-rotation.md       # hermes auth 子命令、4 种 rotation、池子坑
│   ├── fallback-and-rate-limit.md            # fallback 链、429 cooldown、模型路由
│   ├── doctor-and-dump.md                    # hermes doctor / dump 用法
│   ├── config-and-paths.md                   # HERMES_HOME 解析、文件清单
│   ├── provider-switch.md                    # /model 切换、api_mode 陷阱
│   └── backup-and-migrate.md                 # 备份恢复、跨机迁移
├── templates/
│   └── triage-checklist.md                   # 5 步排查模板
└── assets/
    └── known-issues.json                     # 16 条 GitHub issues 结构化清单
```

## 安装方式

### 通过 ClawHub CLI(推荐)

```bash
# 安装 clawhub CLI(如未装)
npm install -g clawhub

# 安装 skill 到当前工作目录的 skills/ 下
clawhub install hermes-doctor

# 或指定目录
clawhub install hermes-doctor --dir ~/.hermes/skills
```

### 手动克隆

```bash
git clone https://github.com/dongsheng123132/hermes-doctor.git
# Hermes Agent
cp -r hermes-doctor ~/.hermes/skills/hermes-doctor
# 或对应 HERMES_HOME(如 C:\Users\<USER>\AppData\Local\hermes\skills\hermes-doctor)
```

### 跟 OpenClaw / Claude Code 等其他兼容 runtime

把整个目录复制到对应 runtime 的 skill 目录即可。SKILL.md 用 Anthropic 标准 frontmatter,所有兼容 agent 都能加载。

## 快速使用

skill 加载后,任一 hermes 故障症状(401 / `no-key-required` / setup 跳过 / 切换后 404 等)都会自动触发。skill 主流程:

1. 锁定真 HERMES_HOME(Windows 上常被 HKCU 重定向)
2. `hermes dump --redact` 看运行时实际 provider/key 状态
3. 翻最新 `<HERMES_HOME>/sessions/request_dump_*.json` 的 `Authorization` 字段
4. 排查 4 处 key 残留点(HKCU env / shell env / auth.json / .env+config.yaml)
5. 备份后双写修复(.env + auth.json),重启 hermes 验证

完整流程见 [`templates/triage-checklist.md`](templates/triage-checklist.md)。

## 已知 issue 覆盖范围

| Issue | 标题 | Workaround |
|---|---|---|
| [#16394](https://github.com/NousResearch/hermes-agent/issues/16394) | hermes setup 静默跳过 API key 输入 | 删 .env 该 KEY 行后重跑 setup |
| [#16677](https://github.com/NousResearch/hermes-agent/issues/16677) | DeepSeek V4 Pro via OpenRouter 崩 | 改用 deepseek-chat |
| [#15914](https://github.com/NousResearch/hermes-agent/issues/15914) | fallback 链在 env 缺失时坍塌 | .env + auth.json 双写 |
| [#3685](https://github.com/NousResearch/hermes-agent/issues/3685) | /model 切换后 404(api_mode 残留) | 升级或手工删 api_mode |
| [#5561 / #5908](https://github.com/NousResearch/hermes-agent/issues/5561) | kimi-coding base_url 路由错 | 重添加凭证 |
| [#14218 / #6907 / #7863 / #8283 / #5807 / #6651 / #12146 / #15717 / #16608](#) | 其他凭证池 / 路由 / 模型相关 | 见 `assets/known-issues.json` |

## 贡献

欢迎补 known-issues、新症状、新 reference!

- 新症状的 PR:在 `assets/known-issues.json` 加一条,同时在 SKILL.md 速查表加一行
- 修过 hermes 故障的实战记录:在 `references/auth-troubleshooting.md` 或新 reference 文件加 "实战记录" 段
- 关联 issue 链接:每条 known issue 必须有 GitHub URL 或注明 `field-report-` 前缀的本地观察

提交前请:
1. `clawhub publish ./ --dry-run`(检查打包正确)
2. SKILL.md 的 description 字段 ≤1024 字符
3. 不带任何具体 API key、本地路径、私有信息

## 相关项目

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — Nous Research 的 self-improving AI agent
- [ClawHub](https://clawhub.ai) — OpenClaw 生态的公开 skill 注册表
- [Anthropic Skills](https://github.com/anthropics/skills) — Skill 格式参考实现

## License

MIT — 见 [LICENSE](LICENSE)
