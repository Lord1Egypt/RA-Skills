# LZ Skill Vetter Pro 🔒🦀

> OpenClaw 技能自动化审计器 —— 安装任何第三方技能前必跑的安全/性能/质量三维度扫描器。

**38 条规则** · 三维度扫描 · JSON 报告 · CI 退出码 · 豁免机制 · 引擎类适配

[![ClawHub](https://img.shields.io/badge/ClawHub-lz--skill--vetter--20260819-orange)](https://clawhub.ai/zuoyunlai/skills/lz-skill-vetter-20260819)
[![License](https://img.shields.io/badge/License-MIT--0-green)](./LICENSE)

---

## 这是什么

`skill-vetter` 是一个安全审计器，用于在安装任何 ClawHub / GitHub / 第三方 OpenClaw 技能**之前**，自动扫描其中的安全红线、性能问题和质量缺陷。

基于 [spclaudehome/skill-vetter](https://clawhub.ai/spclaudehome/skills/skill-vetter) v1.0.0（4 步人工审计协议）深度升级，MIT 协议 fork。

## 特性

完整 38 条规则索引见 [`references/_rules_documentation.md`](./references/_rules_documentation.md)（v2.1.2 起 scanner 自动排除该文件，避免自指）。

### 三大类扫描

- 🔒 **安全扫描（24 条）**：代码执行 / 网络外发 / 凭据泄露 / 混淆 / 系统权限 / 持久化 / 注入 / 隐藏指令
- ⚡ **性能审计（5 条）**：SKILL.md 体积 / frontmatter / token 用量 / scripts shebang
- ✨ **质量审计（9 条）**：YAML / 禁用文件 / license / 触发词 / 使用示例

### 🛡️ 豁免机制（4 层 · v2.1.2 起）

1. `file_glob`（YAML） —— 规则只扫特定文件类型
2. `exception_pattern`（YAML） —— 同行正则豁免
3. `<!-- safe-pattern: <reason> -->` —— 单行豁免（**reason 必须白名单**）
4. `.safe-pattern-manifest.json` —— 文件级白名单（**v2.1.2 新增**，只在白名单文件认 safe-pattern）

## 快速开始

```bash
# 文本报告（人类可读）
python3 scripts/audit.py /path/to/skill

# JSON 报告（机器可消费 + CI）
python3 scripts/audit.py /path/to/skill --format json

# 仅看严重问题
python3 scripts/audit.py /path/to/skill --severity high

# CI 退出码模式（0=pass, 1=warning, 2=fail）
python3 scripts/audit.py /path/to/skill --exit-code
```

### 批量审计所有已装技能

```bash
scripts/batch_audit.sh
```

### CI 集成（GitHub Actions）

```yaml
name: Skill Audit
on: [push, pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.12'}
      - run: pip install pyyaml
      - name: Audit
        run: python3 skill-vetter/scripts/audit.py . --exit-code
```

## 目录结构

```
skill-vetter/
├── SKILL.md                    # 技能定义（OpenClaw 加载入口）
├── skill-card.md               # ClawHub 发布卡片
├── _meta.json                  # 元数据（slug/version/license/fork 来源）
├── scripts/
│   ├── audit.py                # 核心扫描器（Python）
│   ├── scan.sh                 # Bash 包装（grep fallback）
│   ├── batch_audit.sh          # 批量审计
│   └── patterns/
│       └── red_flags.yml       # 38 条规则模式库（可扩展）
├── references/
│   ├── audit_protocol.md       # 4 步人工审计协议（v1.0 保留）
│   ├── patterns.md             # 模式库索引
│   └── output_format.md        # JSON Schema + CI 示例
└── assets/
    └── report_template.json    # JSON 报告模板
```

## 风险分级

| 命中 | verdict |
|---|---|
| ≥1 critical | ⛔ ❌ DO NOT INSTALL |
| ≥1 high | 🔴 ⚠️ INSTALL WITH CAUTION |
| ≥1 medium | 🟡 ⚠️ REVIEW MEDIUM ISSUES |
| ≥1 low/info | 🟢 ✅ SAFE TO INSTALL (minor notes) |
| 无命中 | 🟢 ✅ SAFE TO INSTALL |

## 版本历史

- **v2.1.2** (2026-08-20) — ClawHub scanner 91% finding 闭环：A 移位 + B 收紧豁免 + C 文件级签名（教训 #110）
- **v2.1.0** (2026-08-19) — 独立审计修复 9 问题（original_severity bug / dot-key 词边界 / QUAL-STRUCT-002 实现 / 版本命名漂移清理）
- **v2.0.1** (2026-08-19) — 3 误判修复 + severity-cap 机制
- **v2.0.0** (2026-08-19) — 从 v1.0 人工协议升级为 38 条自动化规则
- **v1.0.0** (2026-08-03) — 原始版（spclaudehome）：4 步人工审计协议 + 15 红线

## 发布渠道

- **ClawHub**: [lz-skill-vetter-20260819](https://clawhub.ai/zuoyunlai/skills/lz-skill-vetter-20260819)
- **GitHub**: 本仓库（源码真源）
- **Fork 来源**: [spclaudehome/skill-vetter](https://clawhub.ai/spclaudehome/skills/skill-vetter) v1.0.0 (MIT)

## License

MIT-0 —— 自由使用、修改、再分发，无需署名。

---

*Paranoia is a feature.* 🔒🦀
