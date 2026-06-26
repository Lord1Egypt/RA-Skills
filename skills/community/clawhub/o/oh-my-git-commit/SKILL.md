---
name: git-commit
description: '执行 git commit，支持 conventional commit 消息分析、智能暂存和消息生成。用户要求提交更改、创建 git commit 或提到 "/commit" 时触发。支持：(1) 从变更自动检测 type 和 scope，(2) 从 diff 生成 conventional commit 消息，(3) 交互式 commit 支持覆盖 type/scope/description，(4) 按逻辑分组智能暂存文件'
license: MIT
allowed-tools: Bash
triggers:
  - commit
  - 提交
  - git commit
---

# Git Commit - Conventional Commits

## 概述

使用 Conventional Commits 规范创建标准化、语义化的 git commit。通过分析实际 diff 来确定合适的 type、scope 和 message。

## Conventional Commit 格式

```
<type>[可选 scope]: <描述>

[可选正文]

[可选脚注]
```

## Commit Type 对照表

| Type       | 用途                           |
| ---------- | ------------------------------ |
| `feat`     | 新功能                         |
| `fix`      | Bug 修复                       |
| `style`    | 代码格式/样式调整（无逻辑改动）|
| `refactor` | 代码重构（非 feature/fix）     |
| `perf`     | 性能优化                       |
| `test`     | 添加/更新测试                  |
| `build`    | 构建系统/依赖变更              |
| `ci`       | CI/配置变更                    |
| `chore`    | 维护/杂项                      |
| `revert`   | 回滚 commit                    |

## 破坏性变更

```
# 在 type/scope 后加感叹号
feat!: 移除已废弃的接口

# 或使用 BREAKING CHANGE 脚注
feat: 允许配置继承其他配置

BREAKING CHANGE: `extends` 键的行为已变更
```

## 工作流程

### 1. 分析 Diff

```bash
# 如果有已暂存的文件，使用 staged diff
git diff --staged

# 如果没有暂存文件，使用工作区 diff
git diff

# 同时查看状态
git status --porcelain
```

### 2. 暂存文件（如需要）

如果没有任何文件被暂存，或者你想按不同逻辑分组：

```bash
# 暂存指定文件
git add path/to/file1 path/to/file2

# 按模式暂存
git add *.test.*
git add src/components/*

# 交互式暂存
git add -p
```

**禁止提交机密信息**（.env、credentials.json、私钥等）。

### 3. 生成 Commit Message

先逐文件阅读 diff 内容，理解每处改动的具体功能和意图，然后生成结构化的 commit message。

**必须包含以下部分：**

- **Type**：这是什么类型的变更？
- **Scope**：影响哪个区域/模块？
- **Description**：一句话概括变更内容（现在时、祈使句，不超过 72 字符）
- **Body**（多文件或复杂变更时必须）：按文件/模块分组，列出每处核心改动的具体功能点

**Body 撰写要求：**
- 不要只写"优化样式"或"修复 bug"，要具体到改了什么、为什么改
- 多文件变更时，按文件分组，每行以 `- ` 开头
- 涉及算法/逻辑变更时，说明新行为的规则和边界条件
- 涉及 UI 变更时，说明具体的交互或视觉效果改动
- 如果 diff 中有 TODO、FIXME 或明显的 hack，在 body 中注明

message 使用**中文**撰写，但 type/scope 保持英文（遵循 conventional commits 规范）。

### 4. 执行 Commit

**简单变更（单文件、改动少）可用单行：**
```bash
git commit -m "<type>[scope]: <中文描述>"
```

**复杂变更（多文件、涉及逻辑或 UI）必须用多行，包含 body：**
```bash
git commit -m "$(cat <<'EOF'
<type>[scope]: <中文描述>

- <文件A>: <具体改动1>
- <文件A>: <具体改动2>
- <文件B>: <具体改动3>
- <文件C>: <具体改动4>
EOF
)"
```

## 最佳实践

- 一个 commit 只做一件逻辑上完整的事
- 使用现在时："添加" 而非 "添加了"
- 使用祈使句："修复 bug" 而非 "修复了 bug"
- 关联 issue：`Closes #123`、`Refs #456`
- 描述控制在 72 字符以内
- 中文描述应简洁明确，避免冗余

## Commit Message 质量示例

**差的示例（过于笼统，没有信息量）：**
```
feat: 优化组件
```

**好的示例（具体到功能点和文件）：**
```
feat(creative): 支持动态比例行布局并全面适配深色模式

- creative-grid.vue:
  - 新增 displayRatio 字段，区分布局比例与显示比例
  - 实现 canFitRatioItemsInRow 算法，根据图片比例动态决定每行显示数量
  - square 布局支持非 1:1 比例的媒体盒子，避免宽图被压缩为正方形
  - 修复失败/待处理资源导致整行被错误拆分为 square 的问题
- draw.vue:
  - 全局深色模式样式适配（背景、文字、边框统一使用 slate 色系）
  - 原图预览区域新增 +n 占位展示剩余省略图片
  - 视频创意编辑面板增加暗色边框和背景透明度
- BottomContent.vue:
  - 重构登录状态监听，拆分为两个独立 watch 避免重复触发过渡动画
- chatplus-form.vue: 移除 textarea 冗余边框样式，统一使用 focus ring
```

## Git 安全协议

- 绝不修改 git config
- 绝不在未明确要求时执行破坏性命令（--force、hard reset 等）
- 绝不跳过 hooks（--no-verify），除非用户明确要求
- 绝不对 main/master 执行 force push
- 如果 commit 因 hook 失败，修复问题后创建**新的 commit**（不要 amend）
