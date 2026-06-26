---
name: git-repo-reader
description: >
  辅助阅读和快速理解 GitHub/Git 项目结构与核心价值的结构化方法论。
  当用户请求"分析这个 GitHub 项目"、"帮我读一下这个 repo"、"了解这个项目是做什么的"、
  "怎么用这个项目"、"怎么跑这个项目"、"这个项目用了哪些技术"，或任何涉及
  GitHub/Git 仓库阅读、理解、技术评估、快速上手的任务时触发使用。
  适用于：开源项目调研、技术选型评估、代码审查准备、学习优秀项目、贡献前了解项目。
---

# Git Repo Reader - 项目速读助手

## Overview

提供一个**五维结构化阅读框架**，帮助在 5-10 分钟内快速定位一个 GitHub 项目的核心价值、使用方式和技术复杂度。

**核心理念：** 不是一行行读代码，而是像产品经理一样"望闻问切"——先看骨架，再决定要不要深入肌理。

---

## 五维阅读法

### Step 1：看 README → 定位问题
**目标：** 这个项目解决什么问题？值不值得继续看？

**检查清单：**
- [ ] 标题 + 一句话描述（通常在 badge 下面）
- [ ] 解决了什么痛点（Motivation / Why）
- [ ] 与竞品/替代方案的区别（Differentiation）
- [ ] 项目成熟度：stars、forks、最近 commit 时间、版本号
- [ ] 许可证（License）—— 商用友好吗？

**输出格式：**
```
📍 定位：xxx
🎯 解决：xxx
⭐ 成熟度：x stars | 最后更新：YYYY-MM-DD
📄 许可证：MIT/Apache/GPL/...
```

---

### Step 2：看 Examples → 用法
**目标：** 如果我要用，代码长什么样？

**检查清单：**
- [ ] `examples/`、`demo/`、`samples/` 目录
- [ ] README 中的 Quick Start / Usage 代码块
- [ ] 测试文件（`tests/` 里的用例是最好的文档）
- [ ] 典型调用链：初始化 → 配置 → 执行 → 获取结果

**输出格式：**
```
💡 典型用法：
   1. 初始化：xxx
   2. 配置：xxx
   3. 执行：xxx
   4. 获取结果：xxx
```

---

### Step 3：看入口 → 怎么跑
**目标：** 如果我要本地跑起来，从哪里开始？

**识别入口的方法：**
| 语言 | 入口信号 | 常见位置 |
|------|---------|---------|
| Python | `if __name__ == "__main__"`、`console_scripts` | `__main__.py`、`cli.py`、`main.py` |
| Node.js | `package.json` 中 `bin` 或 `main` 字段 | `index.js`、`bin/` |
| Go | `func main()` | `cmd/`、`main.go` |
| Rust | `fn main()` | `src/main.rs`、`src/bin/` |
| Java | `public static void main` | 含 `Application` / `Main` 的类 |
| Docker | `Dockerfile`、`docker-compose.yml` | 根目录 |

**检查清单：**
- [ ] 安装命令：`pip install`、`npm install`、`go get`、`cargo install`
- [ ] 启动命令：`python -m xxx`、`npm start`、`go run`、`docker run`
- [ ] 环境变量或配置文件要求
- [ ] 端口/服务暴露情况

**输出格式：**
```
🚀 入口：xxx
📦 安装：xxx
▶️  启动：xxx
⚙️  配置：xxx（如有）
```

---

### Step 4：看核心模块 → 最有价值的地方
**目标：** 真正值得学习的代码在哪里？

**识别核心的方法：**
1. **目录结构扫描** - 看哪些目录代码量最大（`scripts/analyze_repo.py` 可辅助统计）
2. **Import 关系分析** - 被最多文件 import 的模块往往是核心
3. **README 重点提及** - 作者主动高亮的模块
4. **测试覆盖率** - 测试最密集的模块通常最核心

**重点关注：**
- [ ] 算法/数据结构实现（如果是算法库）
- [ ] 抽象层/接口设计（如果是框架）
- [ ] 关键转换/处理逻辑（如果是工具）
- [ ] 架构模式（MVC、管道、事件驱动等）

**输出格式：**
```
🔧 核心模块：
   - module_a.py：负责 xxx，用了 xxx 设计模式
   - module_b.py：实现了 xxx 算法/机制
   💎 最值得学习的代码：xxx
```

---

### Step 5：看依赖 → 技术复杂度
**目标：** 这个项目站在了哪些巨人的肩膀上？技术栈深不深？

**检查清单：**
| 语言 | 依赖文件 | 看什么 |
|------|---------|--------|
| Python | `requirements.txt`、`pyproject.toml` | 核心依赖、版本约束 |
| Node.js | `package.json` | dependencies vs devDependencies |
| Go | `go.mod` | 直接依赖、Go 版本 |
| Rust | `Cargo.toml` | crates、features |
| Java | `pom.xml`、`build.gradle` | 框架、中间件 |
| Ruby | `Gemfile` | gems |

**分析维度：**
- [ ] **关键依赖**：识别 3-5 个最重要的外部库，它们决定了项目的"基因"
- [ ] **技术栈推断**：根据依赖组合判断技术方向（AI？Web？数据？基础设施？）
- [ ] **复杂度评估**：
  - 依赖数量 < 10：轻量级，容易理解
  - 依赖数量 10-30：中等复杂度
  - 依赖数量 > 30 或有复杂子依赖：重量级，需要较多背景知识
- [ ] **版本新鲜度**：依赖是否维护良好？有没有 deprecated 的包？

**输出格式：**
```
📚 技术栈：
   核心依赖：xxx, xxx, xxx
   技术方向：AI / Web / Data / Infra / ...
   📊 复杂度：轻量/中等/重量级（依赖数：N）
```

---

## 执行策略

### 方式 A：用户给 GitHub URL
1. 用 `scripts/analyze_repo.py` 自动拉取项目元数据和文件列表
2. 按五维法依次分析，输出结构化报告

### 方式 B：用户给本地路径
1. 直接在本地执行分析脚本
2. 按五维法输出报告

### 方式 C：交互式深度阅读
用户针对某一步（如"只看核心模块"）深入时：
1. 聚焦该维度
2. 给出更详细的分析（代码片段、架构图描述、设计模式识别）

---

## 输出模板

每次分析应输出统一的速读报告：

```markdown
# 📖 项目速读：{project_name}

**URL**: {github_url}
**分析日期**: {date}

---

## 📍 Step 1: 定位（README）
...

## 💡 Step 2: 用法（Examples）
...

## 🚀 Step 3: 入口（CLI/Server）
...

## 🔧 Step 4: 核心模块
...

## 📚 Step 5: 依赖与技术栈
...

---

## 🎯 速读结论

| 维度 | 评分（1-5⭐） | 一句话 |
|------|-------------|--------|
| 文档清晰度 | ⭐⭐⭐⭐⭐ | ... |
| 上手难度 | ⭐⭐⭐ | ... |
| 代码质量 | ⭐⭐⭐⭐ | ... |
| 技术前沿性 | ⭐⭐⭐ | ... |

**适合场景**：xxx
**不适合场景**：xxx
```

---

## Resources

### scripts/
- **`analyze_repo.py`** - 自动分析 GitHub/本地 仓库结构，提取 README、依赖、入口、核心模块统计

### references/
- **`reading-patterns.md`** - 不同类型项目的阅读技巧（框架类、工具类、算法类、应用类）
