---
name: huo15-openclaw-mit-48h-learning-method
version: 2.2.0
description: 麻省理工学院48小时学习法技能（青岛火一五信息科技有限公司）。使用 NotebookLM CLI 实现 MIT 研究生 Ihtesham Ali 的三问学习框架：
  1. 问心智模型：领域内专家共享的 5 个基本思维框架
  2. 问专家分歧：在哪 3 个问题上根本不同意
  3. 问暴露性问题：生成能区分真懂和假背的 10 个问题
  触发场景：（1）用户要求快速学习某个领域；（2）用户提到 MIT 学习法、48 小时学习、NotebookLM 三问；（3）用户需要生成播客/视频概览；（4）用户想用 AI 辅助构建知识体系。
---

# 火一五 MIT 48 小时学习法

MIT 研究生 Ihtesham Ali 的学习方法：48 小时内通过三问框架掌握任意领域。

## 核心工作流

```
学什么 → 创建 NotebookLM → 添加资料 → 三问框架 → 生成 Audio/Video
```

## 前置条件

**首次使用必须认证：**
```bash
~/.venv/notebooklm/bin/nlm login
```
（会打开浏览器，按提示完成 Google 账号授权）

**自动续登录：** 脚本会在每次执行命令前自动检测登录状态，如果检测到登录已失效，会自动重新运行 `nlm login`，无需手动干预。

## 依赖

- **CLI 工具**：`~/.venv/notebooklm/bin/nlm`
- **环境变量**：`NOTEBOOKLM_PROFILE`（可选，默认为 `default`）
- **语言设置**：`MIT_LEARN_LANG`（可选，默认为 `zh-CN`）

## 脚本位置

```
skills/huo15-mit-48h-learning-method/scripts/mit-learn.sh
```

## 使用方法

### 完整流程（推荐）

```bash
./scripts/mit-learn.sh full "学习主题" --url "https://..." --file ./notes.pdf --youtube "https://youtube.com/..."
```

完整流程包含：创建 notebook → 添加资料 → 三问框架（心智模型、专家分歧、暴露性问题）

### 分步流程

```bash
# 1. 创建笔记本
./scripts/mit-learn.sh init "机器学习基础"

# 2. 添加资料（可多次调用）
./scripts/mit-learn.sh add --url "https://..." --wait
./scripts/mit-learn.sh add --file ./paper.pdf --wait
./scripts/mit-learn.sh add --youtube "https://youtube.com/..."

# 3. 三问框架
./scripts/mit-learn.sh ask mental-models     # 问心智模型（5个框架）
./scripts/mit-learn.sh ask disagreements     # 问专家分歧（3个问题）
./scripts/mit-learn.sh ask probing           # 问暴露性问题（10个问题）
./scripts/mit-learn.sh ask all               # 完整三问

# 4. 生成概览
./scripts/mit-learn.sh audio                 # 生成播客音频
./scripts/mit-learn.sh video                 # 生成视频

# 5. 查看状态
./scripts/mit-learn.sh status                # 查看当前 notebook 状态
./scripts/mit-learn.sh list                  # 列出所有 notebooks
```

## 三问框架详解

### 问心智模型（Mental Models）

> "该领域专家共享的 5 个基本思维框架是什么？"

- 每个框架用一句话解释 + 具体应用例子
- 目的是快速建立领域内专家共同认可的思维工具箱

### 问专家分歧（Expert Disagreements）

> "在哪 3 个问题上，该领域专家根本不同意？"

- 识别核心理论、方法或结论上的根本性争议
- 了解分歧根源，明白这不是细枝末节而是根本矛盾
- **这是区分真学习和假学习的关键**：知道分歧意味着真正理解领域

### 问暴露性问题（Probing Questions）

> "生成 10 个能区分真懂和假背的问题"

- 苏格拉底式追问：开放性问题，无法通过简单回忆回答
- 每个问题需说明：假背者会怎么错 / 真懂的人会怎么答
- **这是检验学习效果的最终武器**

## NotebookLM 支持的资料类型

| 类型 | 参数 | 示例 |
|------|------|------|
| URL | `--url` / `-u` | `--url "https://..."` |
| 文件 | `--file` / `-f` | `--file ./notes.pdf` |
| YouTube | `--youtube` / `-y` | `--youtube "https://youtube.com/..."` |
| Google Drive | `--drive` | `--drive <doc-id>` |

## Audio/Video 选项

### Audio（播客音频）

```bash
./scripts/mit-learn.sh audio [format]
# format: deep_dive（默认）/ brief / critique / debate
# length: short / default / long
```

### Video（视频概览）

```bash
./scripts/mit-learn.sh video [style]
# style: auto_select（默认）/ classic / whiteboard / kawaii / anime / watercolor / retro_print / heritage / paper_craft
```

## 提示词设计原则

三问框架的提示词基于以下原则设计：

1. **心智模型**：要求专家视角 + 具体例子，不可泛泛而谈
2. **专家分歧**：要求根本性分歧，而非表面差异
3. **暴露性问题**：苏格拉底追问法，必须能区分真假理解

## 注意事项

- `init` 后当前 notebook ID 保存到 `~/.mit-learn-notebook-id`，后续命令复用
- 添加资料后可用 `--wait` 等待处理完成
- NotebookLM API 可能有速率限制，避免短时间内大量请求
- 三问结果建议保存到笔记中，用于后续复习
- 如果使用多个 Google 账号，可设置 `NOTEBOOKLM_PROFILE=your-profile` 环境变量切换
## v2.0.0 (2026-04-06)

### 新功能
- **支持 file:// URL**：自动转换为真实路径再添加
- **音频生成等待**：新增 wait_for_audio 确认音频生成完成再返回
- **重复 notebook 检测**：创建前先查找同名 notebook，避免重复
- **自动续登录**：登录失效前自动重新运行 `nlm login`，无需手动干预

### Bug 修复
- **full 命令参数传递 bug**：修复了 urls/files/yt_urls 三个数组错误传递的问题
- **增强错误处理**：cmd_add 不再隐藏错误信息，现在会明确显示失败原因

### 改进
- 新增 --skip-audio flag：full 命令可跳过音频生成
- cmd_init 重构为 get_or_create_notebook 函数
- wait_for_processing 稳定性提升
- debug 函数默认关闭，减少干扰

```bash
mit-learn.sh full "机器学习" --file ./notes.pdf --skip-audio
```
