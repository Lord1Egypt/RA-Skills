# 🚀 Prompt Optimizer

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-技能包-blue?style=for-the-badge&logo=rocket" alt="OpenClaw">
  <img src="https://img.shields.io/badge/版本-3.2-green?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.12+-yellow?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/测试-57个通过-green?style=for-the-badge" alt="Tests">
</p>

> [!TIP]
> AI 任务处理器 - 先优化 Prompt，再精准执行

---

## ✨ 一句话介绍

**一个能把您的模糊需求自动翻译成 AI 能精准执行的指令的工具！**

---

## 🎯 能做什么？

### 原始需求 → 精准指令

| 您说 | 优化后 |
|------|--------|
| "帮我写个排序" | "你是一个专业工程师。帮我写个排序。请用 Markdown 格式输出..." |
| "查下天气" | "请提供准确、全面的信息，标注信息来源。查下天气。用 Markdown..." |
| "帮我debug报错" | "你是一个资深调试专家。请分析问题原因，提供完整的错误分析..." |
| "帮我写个测试用例" | "你是一个资深测试工程师。请编写完整的测试用例，覆盖主要场景..." |

---

## 🚀 快速开始

### 安装

```bash
cp -r prompt-optimizer/ ~/.openclaw/workspace/skills/
```

### 使用

```bash
# 基本用法
python prompt_optimizer.py "帮我写个排序"

# JSON 输出
python prompt_optimizer.py "帮我写个排序" --json

# YAML 输出
python prompt_optimizer.py "帮我写个排序" --yaml

# 从文件批量处理
python prompt_optimizer.py --file input.txt

# 查看版本
python prompt_optimizer.py --version
```

---

## 📖 CLI 用法

```
用法: python prompt_optimizer.py [options] [prompt]

选项:
  -f, --file FILE        从文件读取 prompt（每行一个）
  -o, --output FILE      输出文件路径
  -j, --json             输出 JSON 格式
  -y, --yaml             输出 YAML 格式
  -v, --verbose          显示详细信息
  -q, --quiet            静默模式
  --stats                显示统计信息
  -t, --types            显示支持的任务类型
  --cache / --no-cache   启用/禁用缓存
  --clear-cache          清空缓存
  -c, --config FILE      配置文件路径
  --version              显示版本号
  -h, --help             显示帮助信息
```

---

## 📋 支持的任务类型 (20种) - v3.2 新增 7 种

| 类型 | 关键词示例 | 新增 |
|------|-----------|------|
| 写代码 | "帮我写个排序" | |
| 代码审查 | "审查这段代码" | |
| 改写代码 | "重构这段代码" | |
| 写文档 | "帮我写个文档" | |
| 写文案 | "写一段推广文案" | |
| 总结摘要 | "帮我总结一下" | |
| 翻译 | "翻译成英文" | |
| 查资料 | "查一下深圳天气" | |
| 数据分析 | "分析一下这份数据" | |
| 头脑风暴 | "给我几个创业想法" | |
| 生成内容 | "生成一张图片" | |
| 数学计算 | "计算 123+456" | |
| 对话聊天 | "聊聊AI的发展" | |
| 处理文件 | "处理文件" | |
| **写测试用例** | "帮我写测试用例" | 🆕 |
| **代码调试** | "帮我debug报错" | 🆕 |
| **性能优化** | "优化代码性能" | 🆕 |
| **安全检查** | "做安全检查" | 🆕 |
| **API设计** | "设计一个API" | 🆕 |
| **数据结构设计** | "用什么数据结构" | 🆕 |

---

## 🎨 新功能 (v3.2)

### ✨ 新增任务类型 (7种)
- **写测试用例** - 单元测试、集成测试
- **代码调试** - Bug 分析与修复
- **性能优化** - 性能瓶颈分析与优化
- **安全检查** - OWASP 安全审计
- **API设计** - RESTful 接口设计
- **数据结构设计** - 算法与数据结构选择

### 📄 多格式输出支持
- **Markdown** (默认)
- **JSON** - `--json` 参数
- **YAML** - `--yaml` 参数
- **XML** - 自动检测
- **表格** - 自动检测
- **PlantUML** - 自动检测

### 👥 目标受众识别 (7种)
- 技术人员 → 包含代码实现细节
- 产品经理 → 从业务角度分析
- 管理者 → 简洁清晰，决策要点
- 运维人员 → 部署和运维便利性
- 设计师 → 视觉和用户体验
- 初学者 → 通俗易懂，逐步引导
- 普通用户 → 简单直白

### 📏 约束条件支持
- **字数限制** - 简短(100字)、中等(300字)、详细(500+字)
- **条数限制** - 少量(3-5条)、中等(5-10条)、大量(10+条)

### 🎭 风格识别 (8种)
- 专业正式
- 轻松幽默
- 简洁明了
- 详细全面
- 技术风格
- 口语化
- 学术风格
- 教程风格

---

## 📝 使用示例

### 1. 基本优化
```bash
$ python prompt_optimizer.py "帮我写个排序"
你是一个专业工程师。

帮我写个排序。

请用 Markdown 格式输出，包含代码块和必要说明
请包含详细的代码注释
请注意代码性能和可读性
```

### 2. 指定输出格式
```bash
$ python prompt_optimizer.py "查天气" --json
```

### 3. 带约束条件
```bash
$ python prompt_optimizer.py "给我5个创业想法，200字以内"
```

### 4. 指定目标受众
```bash
$ python prompt_optimizer.py "解释什么是AI，给初学者看"
```

---

## 📦 项目结构

```
prompt-optimizer/
├── prompt_optimizer.py    # 主程序 (v3.2)
├── config_data.py         # 配置数据 (独立)
├── test_prompt_optimizer.py # 测试用例
├── config.yaml.example    # 配置示例
└── SKILL.md              # 文档
```

---

## 🧪 测试

```bash
python test_prompt_optimizer.py

# 结果
📊 测试结果: 57 通过, 0 失败
```

---

## ⚙️ 配置自定义

创建 `config.yaml` 文件：

```yaml
cache:
  maxsize: 256
  enabled: true

llm:
  enabled: false
  provider: openai
  model: gpt-4

task_patterns:
  自定义任务:
    keywords: ["关键词1", "关键词2"]
    priority: 10
    enhancements:
      - "你是专家"
      - "请详细说明"
```

然后运行：
```bash
python prompt_optimizer.py -c config.yaml "你的prompt"
```

---

## 📝 更新日志

### v3.2 (2026-04-14)
- ✅ **新增 7 种任务类型** - 写测试用例、代码调试、性能优化、安全检查、API设计、数据结构设计
- ✅ **输出格式支持** - JSON、YAML、XML、表格、PlantUML
- ✅ **目标受众识别** - 技术人员、产品经理、管理者、运维、设计师、初学者、普通用户
- ✅ **风格识别** - 8 种风格自动检测
- ✅ **约束条件** - 字数限制、条数限制
- ✅ **57 个测试** - 全部通过

### v3.1 (2026-04-07)
- ✅ 配置分离
- ✅ LRU 缓存
- ✅ 配置文件支持

---

<p align="center">
  <sub>Made with ❤️ by dxx</sub>
</p>