# paper-style-review

> Review Chinese theses with structure-aware checks, style learning from reference papers, and Word comment injection.
>
> 面向中文论文 / 学位论文的结构化审校 skill：学习参考论文风格，统一结构图谱，执行格式、术语、逻辑、风格融合审查，并把结果回挂为 Word 批注。

`paper-style-review` 是这个 skill 的**公开安全发布版（public-safe release）**。它保留了可运行的主链脚本、可分发的 schema / 派生规则和技能说明，适合社区展示、仓库开源与 ClawHub 发布；同时刻意排除了真实论文、历史输出、原始附件和本地工作区痕迹。

## Why this repo exists

这个公开仓库主要解决两件事：

- 让社区能看清这个 skill **到底做什么、怎么跑、边界在哪里**。
- 让公开发布时只暴露**可公开的工程资产**，不夹带私有语料、用户论文、运行残留或绝对路径。

## Core capabilities

- **统一结构图谱**：为 target / refs 建立一致的章节—段落结构表示
- **refs 风格学习**：从用户提供的参考论文中提炼 `style-profile.json`
- **融合式 target 审查**：覆盖格式、术语、逻辑和风格偏离
- **Word 批注回挂**：把结构化审查结果写回 `<target>-annotated.docx`
- **阶段化调试**：支持单独运行 `style_profile` / `style_annotation` / `annotation`

## Best-fit scenarios

适合：

- 中文硕士 / 本科论文的结构化审校
- 用户已有若干篇参考论文，希望学习其写作风格
- 需要把审校结果重新写回 Word 批注，方便人工复核
- 调试论文审校流水线、结构映射、批注定位链路

不适合：

- 期待仓库内自带真实论文样本
- 希望公开版直接附带用户原始文档或历史输出
- 把它当成“无需输入资料即可自动评审任何论文”的黑盒服务

## Workflow overview

```text
input target + refs
  -> build paper structure map
  -> build / reuse style-profile.json
  -> run format + terminology + logic + style review
  -> assemble structured annotations
  -> inject comments back into Word
```

## Public-safe boundary

### Included

- runnable pipeline under `scripts/`
- skill instructions in `SKILL.md`
- publishable derived references under `references/`
- example config using publishable relative paths
- packaged skill artifact under `dist/`

### Excluded

- real papers and named sample corpora
- historical outputs, archives, and annotated deliverables
- original `.doc` attachments and raw extraction artifacts
- `tmp/` state, caches, bytecode, and local workspace traces
- absolute local paths or private runtime credentials

## Repository layout

- `SKILL.md` — 面向 OpenClaw / 技能调用的正式说明
- `scripts/run_review.py` — 主入口，运行完整流水线或指定阶段
- `scripts/orchestrators/` — 主链与分阶段编排
- `scripts/profilers/` — refs 风格学习
- `scripts/detectors/` — 格式检查与段落目录
- `scripts/classifiers/` — 章节 / 段落功能识别
- `references/` — 公开可分发的规则、schema、示例配置
- `dist/paper-style-review.skill` — 当前打包产物

## Quick start

### Prerequisites

建议准备：

- Python 3.10+
- 可用的 OpenAI-compatible 接口配置
- 运行脚本所需 Python 依赖（至少会用到 `openai`、`python-docx`、`lxml`、`PyMuPDF`）
- 你自己的 `target.docx` 和若干 `refs/*.docx`

### LLM configuration

脚本会优先从运行配置或环境变量中读取模型信息，支持例如：

- `PAPER_STYLE_REVIEW_LLM_API_BASE`
- `PAPER_STYLE_REVIEW_LLM_API_KEY`
- `PAPER_STYLE_REVIEW_LLM_MODEL`
- 或兼容的 `OPENAI_BASE_URL` / `OPENAI_API_KEY` / `OPENAI_MODEL`

### Run the full pipeline

```bash
python3 scripts/run_review.py --config ./references/review-config.example.json
```

### Run a single stage

```bash
python3 scripts/run_review.py --config ./references/review-config.example.json --stage style_profile
python3 scripts/run_review.py --config ./references/review-config.example.json --stage style_annotation
python3 scripts/run_review.py --config ./references/review-config.example.json --stage annotation
```

### Limit target-side review to selected chapters

```bash
python3 scripts/run_review.py --config ./references/review-config.example.json --chapters abstract,1
```

## Minimal config shape

```json
{
  "target": {
    "path": "./inputs/target.docx"
  },
  "refs": [
    {
      "id": "ref-style-01",
      "path": "./inputs/ref-style-01.docx",
      "enabled": true,
      "styleProfileEnabled": true
    }
  ],
  "outputDir": "./outputs"
}
```

更多字段可参考：`references/review-config.example.json`

## Repackage this skill

如果你要在本地重新生成 `.skill` 包，可使用 OpenClaw 自带打包脚本：

```bash
python3 ~/.npm-global/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  /path/to/paper-style-review \
  /path/to/output-dir
```

例如在当前仓库内重新打包：

```bash
python3 ~/.npm-global/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  . \
  ./dist
```

## Important constraints

- 仓库**不内置任何真实论文样本**，请自行提供 `target` 与 `refs`
- target 阶段的风格判断**只消费 `style-profile.json`**，不应回读 refs 原文
- `chapterScope` 只收窄 target-side LLM 审查；格式检查仍是文档级
- `references/` 中保留的是**可公开分发的派生规则**，不是原始规范附件的再分发
- 公开版的目标是**可展示、可打包、可审查**，不是附带私有语料的完整工作区镜像

## Privacy and publication note

这个仓库是为公开发布准备的 release track。若你要基于它继续扩展：

- 不要提交真实论文、批注文档、历史输出和本地绝对路径
- 不要把个人 API key、机构内部资料或带版权风险的原始附件打进仓库
- 若新增规则材料，优先提交**派生摘要 / 可公开抽象结果**，而不是原文件副本

## License

MIT
