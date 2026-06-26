---
name: mquant-coder
slug: mquant-coder
version: 1.0.5
description: Matic MQuant strategy development assistant. Generates Python strategy code for Matic-MQuant platform.
author: chouchounii
license: MIT-0
---

# MQuant Strategy Development Assistant

## Overview

This skill generates **runnable** Python strategy code for the Matic-MQuant quantitative trading platform.

**核心理念**：
- 代码**可直接运行**优先，策略逻辑可由用户后续调整
- 生成代码经过模板验证，确保语法正确、API调用无误
- 用户可在实盘前通过Matic模拟盘验证策略效果

**⚠️ 注意**：由于Matic平台**不支持回测**，策略验证应通过测试环境调试。

## Reference Structure

### SKILL文档（Skill 维护）

| 文档 | 路径 | 说明 |
|------|------|------|
| **API 速查手册** ⭐ | `reference/API_REFERENCE.md` | 常用 API、结构体字段、常见错误 |
| **日志格式规范** ⭐ | `reference/LOG_FORMAT.md` | 日志格式、级别、代码实现 |
| **API 完整定义** | `reference/mquant_api.py` | MQuant 官方 API 定义 |
| **数据结构定义** | `reference/mquant_struct.py` | MQuant 官方结构体定义 |
| **策略模板** | `reference/python template.py` | MQuant 官方策略模板 |
| **常见问题** | `reference/mquantFAQ.md` | 官方 FAQ |
| **策略示例** | `reference/mquant_inside_python_strategy/` | DualThrust、网格策略等示例 |

> ⭐ 快速参考文档，生成策略时优先查阅

### 用户自定义文档（用户自行维护）

| 文档 | 路径 | 说明 |
|------|------|------|
| **策略模板库** | `custom_docs/strategy_templates.user.md` | 你的代码模板、公共函数 |
| **API 用法笔记** | `custom_docs/api_cookbook.user.md` | 你的 API 使用经验 |
| **上线检查清单** | `custom_docs/deployment_checklist.user.md` | 你的实盘检查项 |
| **问题排查手册** | `custom_docs/debugging_guide.user.md` | 你遇到的问题和解决 |
| **交易所特性** | `custom_docs/exchange_notes.user.md` | 你的交易所规则笔记 |
| **其他** | `custom_docs/...` | 用户需要的其他文档 |

**区别**：
- `reference/` = Skill 文档（随版本更新）
- `custom_docs/` = 用户的私人笔记（完全自主，Skill 永不更新）
- 生成策略时优先参考 `custom_docs/` 中的内容

## Workflow

### Step 0: User Environment Initialization (First Run)

**首次使用时，自动创建以下内容：**

1. **个人笔记文件**（如果不存在）：
   - `COMMON_ERRORS.user.md` - 个人错误笔记
   - `TRADING_RULES.user.md` - 个人交易规则
   - `TRADING_PHILOSOPHY.user.md` - 个人交易理念

2. **`custom_docs/` 用户自定义文档**（如果不存在）：
   - `README.md` - 目录说明
   - `strategy_templates.user.md` - 策略模板库（含示例模板）
   - `api_cookbook.user.md` - API 速查手册
   - `deployment_checklist.user.md` - 上线检查清单
   - `debugging_guide.user.md` - 问题排查手册
   - `exchange_notes.user.md` - 交易所特性笔记

> **提示**：`custom_docs/` 中的文档完全由用户管理，可随时编辑添加，也可由SKILL自助。

---

### Step 1: Directory Configuration (User Provided)

**需要用户提供 M-quant 策略目录路径**

出于安全考虑，不进行全盘扫描。请用户自行提供保存路径。

**路径示例：**
```
Windows: D:\Matic\M-quant\admin\
         D:\Trading\Matic\M-quant\trader01\
         C:\Program Files\Matic\M-quant\user\

```

**路径确认流程：**
1. 询问用户策略保存路径
2. 验证路径是否存在且可写
3. 如路径无效 -> 提示重新输入或仅输出代码到对话
4. 用户不提供路径 -> 直接输出代码到对话，不保存文件

---

### Step 2: Version Control

**命名格式**：`xxxxx_vN.py`（文件名 ≤ 11 个字符）

```
举例:
首次生成: ma_v1.py + ma_v1.log
再次生成: ma_v2.py + ma_v2.log
```

**规则**：
- 最多保留 5 个版本，超出时自动删除最旧版本
- 生成新版本时自动对比变更（Version Diff）

---

### Step 3: Strategy Parameter Configuration

**确认策略类型后，询问用户参数需求：**

举例:
```
您需要【xx交易策略】，请选择参数设置方式：
1. 自定义参数
2. AI 根据描述自动生成
```

- **自定义参数**：用户指定具体数值，未填项使用默认值
- **AI 生成**：用户描述需求（如"茅台 1600-1800 网格交易"），AI 自动推断参数

---

### Step 4: Code Generation

**生成原则：可运行 > 完美**

确保生成的代码：
- 语法正确，可直接运行
- API 调用符合 Matic 规范（接口速查详见 `reference/API_REFERENCE.md`）
- 包含日志写入功能
- 包含基本异常处理

**参考文档优先级**：

1. `custom_docs/strategy_templates.user.md` - 用户模板（如存在）
2. `custom_docs/api_cookbook.user.md` - 用户API 使用习惯（如存在）
3. `custom_docs/exchange_notes.user.md` - 用户交易所特性（如存在）
4. `reference/mquant_api.py` - MQuant内置 API 定义
5. `reference/mquant_struct.py` - MQuant内置 数据结构

> **代码规范**：生成的策略必须包含日志功能，详细实现请参阅 `reference/LOG_FORMAT.md`
> 
> **API 规范**：详细 API 用法和常见错误请参阅 `reference/API_REFERENCE.md`

**保存与展示：**
1. 在对话中完整展示生成的代码
2. 保存 `.py` 文件到选定目录
3. 同步保存 `.log` 元数据文件
4. 展示完成后提示保存路径：
   ```
   代码已生成并保存！
   
   文件位置：[完整路径]\strategy_name_v1.py
   日志文件：[完整路径]\strategy_name_v1.log
   
   你可以直接在 Matic-MQuant 中加载此策略。
   ```

---

### Step 5: Debugging & Error Fixing

**错误分类**：
- **Syntax Error**：语法错误
- **Import Error**：模块导入失败
- **API Error**：Matic API 调用错误
- **Logic Error**：逻辑错误
- **Runtime Error**：运行时错误

**排查步骤**：
1. 读取 `.log` 文件查看生成参数和运行时日志
2. 查阅 `custom_docs/debugging_guide.user.md` 是否有类似问题
3. 查阅 `custom_docs/exchange_notes.user.md` 确认是否交易所特性导致

**修复后建议**：
- 新问题 -> 记录到 `custom_docs/debugging_guide.user.md`
- 交易所特性 -> 更新 `custom_docs/exchange_notes.user.md`
- 模板改进 -> 更新 `custom_docs/strategy_templates.user.md`
