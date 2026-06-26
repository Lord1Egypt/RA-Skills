# 完整工作流程

## 流程总览

```
输入 → [步骤 0: 预检查] ─┬─ 找到 EXTEND.md → 继续
                          └─ 未找到 → 首次配置 ⛔ 阻塞 → 保存 → 继续
                                                                    │
      ┌─────────────────────────────────────────────────────────────┘
      ↓
[步骤 1: 内容分析] ─┬─ 文章输入 → 提取知识点 → 拆分卡片
                    └─ 手动输入 → 结构化知识点
      ↓
[步骤 2: 确认设置] → [步骤 3: 大纲] → [步骤 4: 提示词+图片] → [步骤 5: 完成]
```

## 进度清单

```
知识卡片进度：
- [ ] 步骤 0: 预检查
  - [ ] 0.1 加载偏好设置（EXTEND.md）⛔ 阻塞
  - [ ] 0.2 加载角色配置（如有）
- [ ] 步骤 1: 内容分析
  - [ ] 1.1 判断输入模式（文章 / 手动）
  - [ ] 1.2 提取/结构化知识点
  - [ ] 1.3 匹配卡片类型
- [ ] 步骤 2: 确认设置 ⚠️ 必须
- [ ] 步骤 3: 生成大纲
- [ ] 步骤 4: 生成提示词 + 图片
  - [ ] 4.1 保存提示词文件
  - [ ] 4.2 选择图片生成技能
  - [ ] 4.3 逐张生成（有角色时带 --ref）
- [ ] 步骤 5: 完成报告
```

---

## 步骤 0: 预检查

### 0.1 加载偏好设置（EXTEND.md）⛔ 阻塞

检查 EXTEND.md 是否存在：

```bash
test -f .panda-skills/panda-knowledge-card/EXTEND.md && echo "project"
test -f "${XDG_CONFIG_HOME:-$HOME/.config}/panda-skills/panda-knowledge-card/EXTEND.md" && echo "xdg"
test -f "$HOME/.panda-skills/panda-knowledge-card/EXTEND.md" && echo "user"
```

| 结果 | 操作 |
|------|------|
| 找到 | 读取、解析、显示摘要 |
| 未找到 | ⛔ 运行 [首次配置](config/first-time-setup.md) → 保存 → 继续 |

**关键**：未找到时，必须先完成首次配置。

### 0.2 加载角色配置

从 EXTEND.md 的"角色"区块读取角色信息。角色融合规则引用 panda-article-illustrator 的 [character-roles.md](../../panda-article-illustrator/references/character-roles.md)。

| 情况 | 操作 |
|------|------|
| 角色区块存在且图片有效 | 加载角色，后续启用角色选项 |
| 角色区块存在但图片无效 | 警告，降级为无角色 |
| 无角色区块 | 无角色模式，跳过角色相关选项 |

### 0.3 读取参考文档

加载以下参考文档：
- [card-layouts.md](card-layouts.md)
- [prompt-construction.md](prompt-construction.md)
- [platform-presets.md](platform-presets.md)
- [extraction-rules.md](extraction-rules.md)（文章输入模式）

---

## 步骤 1: 内容分析

### 判断输入模式

| 输入方式 | 判断信号 | 后续处理 |
|----------|----------|----------|
| 文章文件路径 | 用户提供了 `.md` / `.txt` 等文件路径 | 进入文章提取模式 |
| 粘贴的长文 | 用户粘贴了大段文字（>300字） | 进入文章提取模式 |
| 粘贴的知识点 | 用户粘贴了简短要点或列表 | 进入手动输入模式 |
| 口头描述 | 用户描述了想要的卡片内容 | 进入手动输入模式 |

### 文章提取模式

遵循 [extraction-rules.md](extraction-rules.md) 进行：

1. **保存源文件**：如果是粘贴内容，保存为 `source-{slug}.md`
2. **内容分析**：识别文章类型、核心主题、目标受众
3. **提取知识点**：标记提取锚点，拆分为独立知识点
4. **匹配卡片类型**：为每个知识点匹配最适合的卡片类型
5. **确定系列结构**：封面 + N 张内容卡 + 总结

### 手动输入模式

1. **结构化内容**：将用户输入组织为结构化的知识点
2. **匹配卡片类型**：根据内容结构推荐卡片类型
3. **判断单/多张**：
   - 单个知识点 → 单张卡片（不需要封面和总结）
   - 多个知识点 → 卡片系列（添加封面和总结）

---

## 步骤 2: 确认设置 ⚠️

**使用 AskUserQuestion 工具，一次提问，最多 4 个问题。**

### 分析摘要展示

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
内容分析
  主题：[topic]
  来源：[文章提取 / 手动输入]
  知识点：[N] 个
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
推荐方案
  卡片类型：[主要使用的类型]
  风格：[推荐风格]
  张数：[封面 + N内容 + 总结 = 总数]
  角色：[名称/模式] 或 "无角色"
  平台：[platform]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 提问内容

| 问题 | 选项 |
|------|------|
| **Q1: 目标平台** | [EXTEND.md 默认](推荐), 小红书(3:4), 微信公众号(16:9), 微博(16:9), X/Twitter(16:9), 抖音(9:16), Instagram(1:1), 通用(16:9) |
| **Q2: 预设或卡片类型** | [推荐预设], [备选], 或手动选择类型 |
| **Q3: 风格** | [推荐], notion, cute, bold, study-notes, chalkboard, 其他 |
| **Q4: 张数** | 自动(推荐), 3张, 5张, 7张, 自定义 |
| **Q5: 角色模式** | 自动, 讲解者, 点缀, 无角色 — **仅在有角色时显示** |

**平台选择规则**：
- 如果 EXTEND.md 中已有 `默认平台`，Q1 默认选中该值，用户可更改
- 平台决定默认宽高比和排版规则，详见 [platform-presets.md](platform-presets.md)
- 不同平台会影响推荐的卡片类型（如 X 不推荐 steps 和 matrix）

**单张卡片模式**：Q4 跳过（固定为 1 张），Q2 基于内容自动推荐。

---

## 步骤 3: 生成大纲

保存 `outline.md` 到输出目录。

### 大纲格式

```yaml
---
topic: Git 常用命令速查
style: notion
platform: xhs
card_count: 5
character:
  name: 小熊猫
  role: narrator
---

## 卡片 1 / 5
**类型**: cover（封面卡）
**标题**: Git 常用命令速查
**视觉**: 终端窗口 + Git logo + 代码元素
**角色**: 讲解者 — 站在右侧，手持一本"Git指南"
**文件名**: 01-cover-git-commands.png

## 卡片 2 / 5
**类型**: tips（要点清单）
**标题**: 基础操作 5 个必会命令
**要点**:
  - ① git init — 初始化仓库
  - ② git add — 暂存更改
  - ③ git commit — 提交更改
  - ④ git push — 推送到远程
  - ⑤ git pull — 拉取更新
**角色**: 讲解者 — 底部居中，指向第一条
**文件名**: 02-tips-basic-commands.png

## 卡片 3 / 5
**类型**: comparison（对比卡）
**标题**: merge vs rebase
**左侧**: merge — 保留完整历史，有合并节点
**右侧**: rebase — 线性历史，更整洁
**角色**: 点缀 — 左下角，思考表情
**文件名**: 03-comparison-merge-rebase.png

## 卡片 4 / 5
**类型**: tips（要点清单）
**标题**: 3 个救命命令
**要点**:
  - ① git stash — 临时保存工作
  - ② git reflog — 找回丢失的提交
  - ③ git reset — 撤销错误操作
**角色**: 讲解者 — 右下角，提醒表情
**文件名**: 04-tips-rescue-commands.png

## 卡片 5 / 5
**类型**: summary（总结卡）
**标题**: 今天学到了什么？
**回顾**:
  - ✓ 5 个基础命令
  - ✓ merge vs rebase 的区别
  - ✓ 3 个救命命令
**CTA**: 收藏备用，转发给需要的人！
**角色**: 讲解者 — 底部居中，竖大拇指
**文件名**: 05-summary-git-commands.png
```

---

## 步骤 4: 生成提示词 + 图片

### 4.1 保存提示词文件 ⛔ 阻塞

为每张卡片创建提示词文件：

1. 遵循 [prompt-construction.md](prompt-construction.md) 构建提示词
2. 保存到 `{output-dir}/prompts/NN-{layout}-{slug}.md`
3. 包含 YAML 前置元数据（card_id、layout、style、character_role）
4. 使用卡片类型化模板
5. 有角色时注入"角色"区块
6. 标题和要点使用文章中的具体文字内容

### 4.2 选择图片生成技能

- 优先使用 `panda-imagine`（panda-skills 内置）
- 如果有 `baoyu-imagine`：也可使用
- 如果有多个技能：询问用户偏好
- 读取所选技能的 SKILL.md

### 4.3 处理参考图

| 情况 | 操作 |
|------|------|
| 有角色 + 技能支持 `--ref` | 每张图都传递角色图片 |
| 有角色 + 技能不支持 `--ref` | 在提示词中嵌入角色文字描述 |

### 4.4 生成图片

为每张卡片执行：

1. 备份同名文件（如存在）
2. 使用图片生成技能：`--promptfiles prompts/NN-{layout}-{slug}.md --image NN-{layout}-{slug}.png --ar [比例]`
3. 有角色时追加 `--ref [角色图片路径]`
4. 生成失败自动重试一次
5. 报告进度："已完成 X/N"

### 4.5 批量生成

所有提示词文件保存后，优先使用批量模式（`--batchfile`）。

---

## 步骤 5: 完成报告

```
知识卡片生成完成！

主题：[topic]
来源：[文章提取 / 手动输入]
风格：[style] | 平台：[platform] | 比例：[ratio]
角色：[名称] / [模式] 或 "无角色"
卡片：X 张已生成
位置：[输出目录路径]

文件列表：
✓ outline.md
✓ prompts/01-cover-{slug}.md
✓ prompts/02-tips-{slug}.md
✓ ...
✓ 01-cover-{slug}.png
✓ 02-tips-{slug}.png
✓ ...
✓ NN-summary-{slug}.png
```
