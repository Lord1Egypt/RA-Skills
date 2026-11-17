---
name: lz-skill-vetter-plus
version: 2.1.3
description: "OpenClaw 技能自动化审计器 Pro（安全/性能/质量三维度 38 条规则）。基于 spclaudehome v1.0.0 fork 深度升级，新增 JSON 报告、CI 退出码、豁免机制、severity-cap 引擎适配。安装第三方技能前必跑。触发词：vet skill, audit skill, 安全审计, 扫描 skill, skill 检查."
allowed-tools: [exec, read]
---

# LZ Skill Vetter Pro v2.1.3 🔒🦀

> 基于 [skill-vetter](https://clawhub.ai/spclaudehome/skills/skill-vetter)（spclaudehome v1.0.0）的深度升级版。  
> 原作者授权协议下 fork，38 条自动化规则 + 3 层豁免 + CI 集成 + 引擎类技能适配。

自动化 + 人工审计并行的 OpenClaw 技能安全审计器。

## When to Use

- 装任何 ClawHub / GitHub / 第三方 skill **之前**
- 写完自己的 skill 想发布**之前**
- 批量体检已装的 100+ skills
- CI 集成（GitHub Actions）

## Quick Start

```bash
# 1. 文本报告（人类可读）
python3 scripts/audit.py /path/to/skill

# 2. JSON 报告（机器可消费 + CI）
python3 scripts/audit.py /path/to/skill --format json

# 3. 仅看严重问题
python3 scripts/audit.py /path/to/skill --severity high

# 4. CI 退出码模式
python3 scripts/audit.py /path/to/skill --exit-code
# 退出码：0=pass, 1=warning, 2=fail
```

## What's New in v2.0

| 维度 | v1.0.0 | v2.0.0 | v2.0.1 | v2.1.x |
|---|---|---|---|---|
| **安全扫描** | 人工 4 步协议 | ✅ 自动化 24 条 | ✅ +3 误判豁免 | ✅ + safe-pattern 双层校验 |
| **性能审计** | ❌ | ✅ 5 条 | ✅ | ✅ |
| **质量审计** | ❌ | ✅ 9 条 | ✅ | ✅ |
| **JSON 报告** | ❌ | ✅ | ✅ | ✅ |
| **CI 集成** | ❌ | ✅ `--exit-code` | ✅ + batch_audit.sh | ✅ |
| **豁免机制** | ❌ | ✅ `# safe-pattern:` 注释 | ✅ + markdown 表格/标题智能豁免 | ✅ **reason 白名单 + 文件级 manifest**（v2.1.2）|
| **模式库** | 内置硬编码 | ✅ YAML 可扩展 | ✅ + 3 个误判修复 | ✅ + 1 修复（dot-key 词边界） |
| **人工审计** | ✅ 4 步协议 | ✅ 保留在 `references/audit_protocol.md` | ✅ | ✅ |

合计 **38 条** 自动审计规则。

### v2.0.1 误判修复（基于主人 102 技能批量试跑）

| 问题 | v2.0.0 | v2.0.1 |
|---|---|---|
| 1password `op://` 引用误判 | critical | ✅ exception_pattern 豁免 |
| Chrome/123.0.0.0 版本号误判为 IP | high | ** 正则加 `(?<![\w./])...(?!\w.)` 边界 |
| 工具类 updater 用 curl/wget | high | ✅ severity 降为 medium |

## 4 步审计协议（v1.0 沿用）

完整协议见 [`references/audit_protocol.md`](references/audit_protocol.md)。

1. **来源检查** — 作者/Stars/下载量/更新日期
2. **代码审查** — v2.0 已自动化 ✅
3. **权限范围** — 文件/网络/命令是否最小化
4. **风险分级** — v2.0 自动映射 🟢/🟡/🔴/⛔

## 风险分级（v2.0 自动）

| 命中 | verdict |
|---|---|
| ≥1 critical | ⛔ ❌ DO NOT INSTALL |
| ≥1 high | 🔴 ⚠️ INSTALL WITH CAUTION |
| ≥1 medium | 🟡 ⚠️ REVIEW MEDIUM ISSUES |
| ≥1 low/info | 🟢 ✅ SAFE TO INSTALL (minor notes) |
| 无任何命中 | 🟢 ✅ SAFE TO INSTALL |

## Bash 包装（无 Python 时回退）

```bash
scripts/scan.sh /path/to/skill
# 自动调 audit.py；若无 PyYAML 则用 grep fallback
```

## 豁免机制

### 1. `# safe-pattern:` 注释（双层校验 · v2.1.2）

任意一行带 `# safe-pattern: <reason>`（Python/Shell）或 `<!-- safe-pattern: <reason> -->`（Markdown）即**意图**豁免。**v2.1.2 起双层校验**：

- **第一层 · reason 白名单**：必须为 `documentation` / `rule-description` / `version-history` / `doc-example` / `test-fixture` 之一。无 reason 或 reason 未知 → **不豁免**。
- **第二层 · 文件级 manifest**：仅当该文件列于 `.safe-pattern-manifest.json` 的 `exemptions` 数组且 reason 匹配 → 才豁免。**未提供 manifest 的技能 = 任何 safe-pattern 都不豁免**（默认严格，防御「按内容豁免」攻击面）。

```python
# 这是文档示例，展示 setuid 用法（实际未启用）  # safe-pattern: doc-example
os.setuid(0)
```

### 2. `exception_pattern`（模式定义层）

模式库的 `exception_pattern` 字段提供正则豁免，例：

```yaml
- id: SEC-CRED-001
  regex: '(?i)(api_key|token)\s*[:=]\s*["\'][^"\']{16,}["\']'
  exception_pattern: '\$\{?[A-Z_]+\}?'  # 跳过环境变量引用
```

### 3. 文件路径默认排除

`audit.py` 自动跳过：
- `scripts/patterns/`（模式定义自身）
- `scripts/audit.py`（审计器自身）
- `references/_*.md`（下划线前缀的内部文档，包含 scanner 自身的规则说明——防御「规则描述误报」）

### 4. `.safe-pattern-manifest.json`（v2.1.2 新增 · 推荐）

需主动豁免的技能应在根目录创建此清单：

```json
{
  "version": 1,
  "exemptions": [
    {
      "file": "scripts/run.py",
      "reason": "rule-description",
      "lines": "10-20",
      "note": "scanner 自身的规则定义"
    }
  ]
}
```

Scanner 仅在 manifest 列出的文件中识别 `safe-pattern` 注释。**未创建 manifest = 默认严格**（不豁免任何 safe-pattern）。这是 v2.1.2 防御「safe-pattern 按内容豁免」攻击面的核心。

## CI 集成示例

```yaml
# .github/workflows/skill-audit.yml
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
        run: python3 lz-skill-vetter-plus/scripts/audit.py . --exit-code
```

## References（按需加载）

- [`references/audit_protocol.md`](references/audit_protocol.md) — 4 步人工审计协议
- [`references/patterns.md`](references/patterns.md) — 38 条模式库索引
- [`references/output_format.md`](references/output_format.md) — JSON Schema + CI 集成

## 记住

- **没有任何 skill 值得牺牲安全**
- 有疑虑就别装
- 高风险决策请主人拍板
- v2.0 自动化 ≠ 取代人工审计
- v2.0.1 误判豁免 ≠ 放松警惕

## License

MIT License — Copyright (c) 2026 左运来

## Changelog

### v2.1.3 (2026-08-20)
- **severity-cap 攻击面闭环**（ClawHub scanner 新 advisory 命中）：verdict 双路径计算（capped vs uncapped）+ 主 verdict 取严重者 + text 报告加 🚨 警告横幅
- 攻击回归：恶意 skill 设 `severity-cap: low` → 原 verdict = SAFE → 现 verdict = ❌ DO NOT INSTALL + 警告横幅显示 capped/uncapped 双值
- 自家 SKILL.md 不使用 severity-cap，无回归风险

### v2.1.2 (2026-08-20)
- **ClawHub scanner 91% Prompt-Injection finding 闭环**（教训 #110）：
  - **A 移位**：scanner 自家规则说明 `references/_rules_documentation.md` 从扫描范围排除（路径 `references/_*.md` 默认跳过）
  - **B 收紧豁免**：`safe-pattern` 必须 `reason` 字段，reason 必须在白名单（5 类）
  - **C 文件级签名**：`.safe-pattern-manifest.json` 机制，**未提供 = 默认严格**（不豁免任何 safe-pattern），攻击面消除
- 自家 manifest 含 5 处合法豁免（scan.sh / SKILL.md 示例 / 协议示例等）
- 攻击回归测试 3 次均 0 bypass

### v2.1.1 (2026-08-19)
- 关联 GitHub 源码仓库（zuoyunlai/lz-skill-vetter），ClawHub source-repo 打通
- 修正 skill-card.md GitHub 链接（去掉日期后缀）

### v2.1.0 (2026-08-19)
- 修 original_severity bug（severity-cap 降级后正确记录原始严重度）
- 修 SEC-CRED-005 敏感路径正则词边界（消除 keyboard/keys 误判）
- 实现 QUAL-STRUCT-002（scripts 可执行权限检测），38 条名副其实
- 清理版本漂移（5 处 2.0.0 残留）+ 命名漂移（6 处 skill-vetter 残留）
- 清理 dead code（SEVERITY_CAP_KEYS 未用常量 / 列表项空分支 / 未用变量）

### v2.0.1 (2026-08-19)
- 修复 3 个误判（基于主人 102 技能批量试跑）
- SEC-CRED-002 异常：增加 `op://` `vault://` `secret://` `keychain://`
- SEC-NET-003 正则：增加边界 `(?<![\w./])...(?!\w.)`，豁免 Chrome/版本号
- SEC-NET-001 严重度：high → medium（updater 工具类合规设计）
- batch_audit.sh 修复：stderr 分离，不再混入 JSON 管道
- 批量试跑：3 FAIL → 2 FAIL，22 CAUTION → 18 CAUTION

### v2.0.0 (2026-08-19)
- 初版：scripts/audit.py + 38 条规则 + 3 维扫描 + JSON 报告 + CI 退出码

### v1.0.0 (2026-08-03)
- 初版：4 步人工审计协议 + 15 红线

---

*Paranoia is a feature.* 🔒🦀