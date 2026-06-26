---
name: kse-dev
description: 基于 kiro-spec-engine (kse) 的 CLI 开发工作流。使用 spec 驱动开发，通过 kse 命令创建规格文档、管理项目结构、自动化开发流程。当用户需要：(1) 用 kse CLI 进行 spec-driven 开发，(2) 创建和管理项目 specs，(3) 使用 enhance 提升文档质量，(4) 运行 doctor 检查系统环境，(5) 初始化新项目或 adoption 现有项目。
---

# KSE CLI 开发工作流

## 概述

KSE (Kiro Spec Engine) 是一个 npm 包，提供 CLI 工具支持规格驱动开发。

**安装：**
```bash
npm install -g kiro-spec-engine
```
**命令：** `kse`

## 快速开始

### 1. 初始化新项目

```bash
cd <your-project-folder>
kse init
```

### 2. 创建 Spec

```bash
kse spec create <spec-name>
```

### 3. 编写规格文档

在 `.kiro/specs/<spec-name>/` 下创建：
- `requirements.md` - 需求定义和验收标准
- `design.md` - 技术设计
- `tasks.md` - 任务清单

### 4. 增强文档质量

```bash
kse enhance requirements <file-path>
kse enhance design <file-path>
```

### 5. 检查系统

```bash
kse doctor
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `kse init` | 初始化 Kiro 项目结构 |
| `kse spec create <name>` | 创建新 spec |
| `kse enhance <stage> <file>` | 增强文档 |
| `kse doctor` | 检查系统环境 |
| `kse status` | 查看项目状态 |

## 开发流程

1. **创建项目文件夹** → 创建独立的项目目录
2. **初始化** → `cd <project> && kse init`
3. **创建 Spec** → `kse spec create <feature-name>`
4. **编写需求** → 编辑 `requirements.md`
5. **实现代码** → 按需求实现
6. **验证** → 运行代码确认符合验收标准

## 注意事项

- 项目放在独立子文件夹中，避免互相污染
- 不使用 GUI，纯 CLI 开发
- 遵循 spec-driven 开发流程
