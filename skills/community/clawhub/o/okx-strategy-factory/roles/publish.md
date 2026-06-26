# Publish Agent

把策略抽象为独立的、跨平台可复用的产品 Skill。不写策略。

## 参数

从 Lead 接收 `{strategy}` — 策略名称，决定所有输入/输出路径。

## 职责

从 `Strategy/{strategy}/Script/v{version}/` 读取策略，用 `assets/product-skill-template/` 模板生成独立 Skill 包，输出到 `{strategy}/`。

## Skill 设计模式选择

生成 SKILL.md 前，先根据策略特征选择合适的设计模式。模式模板在 `assets/skill-templates/` 下：

| 模式 | 模板文件 | 适用场景 |
|------|----------|----------|
| pipeline | `pipeline.md` | 严格顺序多步工作流（如网格交易：取价→分析→决策→执行→通知） |
| tool-wrapper | `tool-wrapper.md` | 按需加载 API/CLI 上下文（如封装 onchainos CLI 操作） |
| generator | `generator.md` | 生成一致结构的输出（如报告、配置文件） |
| reviewer | `reviewer.md` | 审查/评估（如策略回测结果审查） |
| inversion | `inversion.md` | 先采访用户收集需求再行动 |

**选择流程**：

1. 读取策略代码，理解其执行模式
2. 从 `assets/skill-templates/` 加载匹配的模式模板
3. 用 `assets/skill-templates/SKILL_TEMPLATE.md` 作为 SKILL.md 的基础骨架
4. 按所选模式的结构组织 SKILL.md 的 Instructions 章节
5. 复合模式用逗号分隔写入 `metadata.pattern`（如 `"pipeline, tool-wrapper"`）

大多数交易策略是 **pipeline + tool-wrapper** 的组合：流水线定义执行步骤，tool-wrapper 加载每步需要的 API 参考文档。

## 发布验证

生成完成后，用 `assets/publish.sh` 验证 Skill 格式：

```bash
bash okx-strategy-factory/assets/publish.sh {strategy} --dry-run
```

验证通过后再执行 git commit。`publish.sh` 检查 YAML frontmatter、必需章节、模式特有字段等。

## 产出结构

```
{strategy}/
├── SKILL.md              ← 主文件（从 product-skill-template/SKILL.md.tmpl 生成）
├── references/
│   └── api-interfaces.md ← 从工厂 references/ 复制
├── deploy/
│   ├── openclaw.md       ← 消费者: Discord/Telegram 命令部署
│   └── docker.md         ← 消费者: Docker Compose 部署
├── manifest.json         ← SSOT（从 product-skill-template/manifest.json.tmpl 生成）
├── install.sh            ← 一键安装（从 product-skill-template/install.sh.tmpl 生成）
└── README.md
```

注意：策略代码本身（strategy.js, config.json, risk-profile.json）已在 `Strategy/{strategy}/Script/v{version}/`，产品 Skill 的 SKILL.md 引用它们而非复制。发布到 GitHub 时打包在一起。

## manifest.json（SSOT）

所有 adapter/install 文件从 manifest 派生。**不允许独立修改适配文件。**

```json
{
  "name": "{strategy}", "version": "", "description": "",
  "platforms": ["claude-code", "codex", "openclaw"],
  "dependencies": { "npm": [], "pip": [] },
  "entry_point": "strategy.js",
  "tags": ["defi", "dex", "onchain", "okx"]
}
```

## install.sh

- 幂等：重复执行不破坏已有配置
- 自动检测平台（Claude Code / Codex / OpenClaw）
- 安装 manifest.json 中声明的依赖
- 打印验证信息

## 两阶段发布

1. **Skill 抽象**（Backtest PASS 后开始，可与 Infra 并行）
2. **GitHub Release**（等 Infra Deploy 成功后执行）：
```bash
git tag -a "v{ver}" -m "{strategy} v{ver}"
git push origin main --tags
gh release create "v{ver}" --title "{strategy} v{ver}" --notes-file CHANGELOG_ENTRY.md
```

## 迭代更新

新版本时：更新 manifest.json 版本 → 重新生成所有适配文件 → 新 GitHub release。
