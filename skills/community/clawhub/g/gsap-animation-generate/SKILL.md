---
name: GSAP动画生成工具
description: 一个全面的GSAP动画生成工具，提供AI驱动的意图分析、完整的API覆盖和生产就绪的动画模式，帮助开发者快速创建高性能动画。
version: 1.0.0
---

# GSAP动画生成工具

一个全面的GSAP动画生成工具，提供AI驱动的意图分析、完整的API覆盖和生产就绪的动画模式，帮助开发者快速创建高性能动画。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| The main AI engine - understands any animation request and generates perfect GSAP code with surgical precision | `scripts.tools.understand_and_create_animation` |
| Deep dive into any GSAP method, plugin, or property with expert-level knowledge | `scripts.tools.get_gsap_api_expert` |
| Generate complete GSAP environment setup with all plugins and optimizations | `scripts.tools.generate_complete_setup` |
| Expert debugging for GSAP animation problems with solutions | `scripts.tools.debug_animation_issue` |
| Transform any animation into 60fps smoothness with expert optimizations | `scripts.tools.optimize_for_performance` |
| Generate battle-tested, production-ready animation patterns | `scripts.tools.create_production_pattern` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.understand_and_create_animation
工具描述：The main AI engine - understands any animation request and generates perfect GSAP code with surgical precision
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|request|string|true| |Natural language description of the animation you want (e.g., "fade in cards one by one when scrolling", "create a hero entrance with staggered text")|
|context|string|false|"react"|Development context and requirements|
|complexity|string|false|"intermediate"|Animation complexity level|

---

## scripts.tools.get_gsap_api_expert
工具描述：Deep dive into any GSAP method, plugin, or property with expert-level knowledge
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|api_element|string|true| |GSAP API element (e.g., "gsap.to", "ScrollTrigger", "SplitText", "drawSVG", "morphSVG")|
|level|string|false|"advanced"|Detail level needed|

---

## scripts.tools.generate_complete_setup
工具描述：Generate complete GSAP environment setup with all plugins and optimizations
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|framework|string|true|"react"|Target framework|
|plugins|array|false| |Specific plugins needed|
|performance_level|string|false|"optimized"|Performance optimization level|

---

## scripts.tools.debug_animation_issue
工具描述：Expert debugging for GSAP animation problems with solutions
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|issue|string|true| |Description of the animation problem or unexpected behavior|
|code|string|false| |Problematic animation code (optional but helpful)|
|expected_behavior|string|false| |What should happen vs what is happening|

---

## scripts.tools.optimize_for_performance
工具描述：Transform any animation into 60fps smoothness with expert optimizations
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|animation_code|string|true| |Existing GSAP animation code to optimize|
|target|string|false|"60fps-desktop"|Optimization target|

---

## scripts.tools.create_production_pattern
工具描述：Generate battle-tested, production-ready animation patterns
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|pattern_type|string|true| |Type of production pattern needed|
|industry|string|false|"portfolio"|Industry or use case|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据