# UGLIC 5 维速查

> Step 8 推荐调用既有 `glic-check` skill 跑完整 UGLIC mode，本文档只做速查。
> 关键原则：**0 ERR** 才放行；WARN 全修或文字说明保留理由。

## 维度定义

- **GLIC = G / L / I / C 共 4 维**（内部质量）
- **UGLIC = U + G + L + I + C 共 5 维**（加用户体验维度）

| 维度 | 重点 |
|---|---|
| **U** (User Experience 用户体验) | UGLIC 独有。从看 README / 触发 trigger / 装完 / 跑通的整条路径是否顺畅；CLI `--help` 是否覆盖所有 flag；错误文案是否给清晰下一步；SKILL.md 长度（>500 WARN / >800 ERR） |
| **G** (Grammar 语法/规范) | frontmatter 字段纪律、`python3 -c "import ast; ast.parse(...)"`、JSON 校验、Markdown 渲染 |
| **L** (Logic 逻辑) | 控制流可达、边界条件、错误恢复路径、循环不变量 |
| **I** (Integrity 完整性) | SKILL.md 引用的 script/config/章节全在；cross-section reference 不破；无 build artifact 残留 |
| **C** (Containment 安全/凭证) | grep token / 密钥 / 内网域名 / 内网邮箱 全部 0 命中 |

## 自审 + 三档样本（audit/check 类 skill 适用）

发完版主动 self-check + 跑简单/中等/复杂三档真实样本，反思每个 finding：

1. "我是从哪条规则得出的？" → 找规则
2. "找不到规则吗？" → 凭什么打的？（外部记忆 / 泛化 / 借用）
3. "重复出现吗？" → 是否需要专项条目

凭记忆 / 泛化条款打的 finding = **规则盲区** → 升下版子检查项。
**汇报盲区比汇报覆盖率更有价值**。

glic-check v1.0.0 → v1.0.1 实证产 6 个盲区（SKILL.md 长度归属 / cross-section ref / build artifact / frontmatter 名单 / 示例密度 / large target progressive read），全修入 v1.0.1。

## 双 audit 工具交叉（发版前必跑）

不只跑 UGLIC，**还要跑** `skill-release-audit` 的 healthcheck（多 target 模式）：

```bash
HC=~/.openclaw/workspace/skills/skill-release-audit/scripts/healthcheck.py

# 1. 通用 audit（发开源 skill 至少跑 generic + clawhub + github）
python3 "$HC" opensourceskills/<name>/ --target generic
python3 "$HC" opensourceskills/<name>/ --target clawhub
python3 "$HC" opensourceskills/<name>/ --target github

# 2. UGLIC mode（本份指南推荐）
#    调用 glic-check skill，UGLIC mode（5 维度 U/G/L/I/C）
```

支持的 `--target`: `anthropic | clawhub | generic | github | skillhub`。

**顺序很重要**（feedback_audit_tool_cross_check_before_release.md 实证）：
1. 先跑 UGLIC 改完业务/文档/UX 问题
2. 再跑 release-audit 验发布规范（slug 上限 / 必填章节 / 数据安全）
3. 避免发布规范修了又被 UGLIC 改业务时推翻

两套工具盲区互补：UGLIC 抓「悬空文档引用 / 步骤职责边界含糊 / 触发词冲突」，release-audit 抓 slug 合法性 / 必填章节 / 依赖声明 / 数据安全等发布层面规范。单跑一套必漏。

## 常见 U 维度问题

- `--help` 缺失某个 flag 的描述
- 错误文案只说"失败了"，不说怎么修
- SKILL.md 太长（>500 行 WARN，>800 ERR），缺 progressive disclosure
- 首次跑要 5 步配置，没有"快速尝鲜"路径
- locale 写死 zh，国际用户看不懂

## 常见 C 维度命中

- 漏删 `sign.key` / `.install-source.json`
- README 里贴了内网链接（`*.xiaohongshu.com`）
- 错误日志示例里有真实内网邮箱
- 测试 fixture 含真实 token / cookie
- `__pycache__/` 没进 `.gitignore`
