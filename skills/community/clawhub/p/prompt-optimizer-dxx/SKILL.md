# 🚀 Prompt Optimizer

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-技能包-blue?style=for-the-badge&logo=rocket" alt="OpenClaw">
  <img src="https://img.shields.io/badge/版本-3.1-green?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.12+-yellow?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/测试-31个通过-green?style=for-the-badge" alt="Tests">
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
| "写个API" | "你是一个专业工程师。写个API。请用 Markdown 格式输出..." |

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

# 从文件批量处理
python prompt_optimizer.py --file input.txt

# 查看版本
python prompt_optimizer.py --version

# 模块方式运行
python -m prompt_optimizer "帮我写个排序"
```

---

## 📖 CLI 用法

```
用法: python prompt_optimizer.py [options] [prompt]

选项:
  -f, --file FILE        从文件读取 prompt（每行一个）
  -o, --output FILE      输出文件路径
  -j, --json             输出 JSON 格式
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

## 📋 支持的任务类型 (13种)

| 类型 | 示例 |
|------|------|
| 写代码 | "帮我写个排序" |
| 代码审查 | "审查这段代码" |
| 改写代码 | "重构这段代码" |
| 写文档 | "帮我写个文档" |
| 写文案 | "写一段推广文案" |
| 总结摘要 | "帮我总结一下" |
| 翻译 | "翻译成英文" |
| 查资料 | "查一下深圳天气" |
| 数据分析 | "分析一下这份数据" |
| 头脑风暴 | "给我几个创业想法" |
| 生成内容 | "生成一张图片" |
| 数学计算 | "计算 123+456" |
| 对话聊天 | "聊聊AI的发展" |

---

## ⭐ 新功能 (v3.1)

### 🔧 重构优化
- **配置分离** - `config_data.py` 独立配置，便于维护
- **版本常量** - `__version__ = "3.1.0"`，统一管理
- **模块化 CLI** - 拆分 `handle_stats`, `handle_types` 等函数

### 🚀 性能与功能
- **LRU 缓存** - 相同 prompt 直接返回
- **配置文件** - 支持 `config.yaml` 自定义
- **日志系统** - 实时显示优化过程

---

## 📦 项目结构

```
prompt-optimizer/
├── prompt_optimizer.py    # 主程序 (v3.1)
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
📊 测试结果: 31 通过, 0 失败
```

---

## 📝 更新日志

### v3.1 (2026-04-07)
- ✅ **配置分离** - 独立 `config_data.py`
- ✅ **版本常量** - `__version__ = "3.1.0"`
- ✅ **重构 main** - 拆分成独立函数
- ✅ **__main__ 入口** - 支持 `python -m`
- ✅ **31 个测试** - 全部通过

### v3.0 (2026-04-07)
- ✅ LRU 缓存
- ✅ 配置文件支持
- ✅ 日志系统

### v2.1 (2026-04-07)
- ✅ CLI 入口
- ✅ 错误处理

---

<p align="center">
  <sub>Made with ❤️ by dxx</sub>
</p>