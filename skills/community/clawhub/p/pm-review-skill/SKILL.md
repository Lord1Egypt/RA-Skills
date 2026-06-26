---
name: pm-review
description: 产品经理页面评审工具，用于评估网页或设计截图的产品质量。触发条件：用户要求评审页面、分析截图、评估设计、PM评审、产品评审、界面分析。支持两种输入方式：(1) 网址评审 - 通过 URL 评审在线页面 (2) 截图评审 - 通过图片文件评审设计稿。输出七维度专业评审报告（战略目标/用户体验/功能内容/数据度量/技术性能/市场竞品/迭代运营）。支持专项深度审查：颜色审查（六层模型）、排版审查、交互审查、无障碍审查（六层金字塔）、安全合规审查（七层模型）、性能优化审查（七层模型）。
---

# PM 页面评审技能

## 评审心态

**三个核心原则：**

1. **追问本质** - 用户说"按钮太小" → 可能是交互逻辑问题
2. **敢于说不** - 当所有人觉得"差不多"时，坚持找问题
3. **多元方案** - 不给单一结论，提供渐进/重塑/理想三套方案

---

## 工作流程

### 步骤 1：确定输入类型

**网址评审** - 用户提供了 URL

优先使用以下工具获取页面内容（按可用性排序）：
1. `mcp__web_reader__webReader` - Web Reader MCP 服务器
2. `mcp__web-reader__webReader` - 备用命名
3. WebSearch 搜索页面信息
4. 直接请求用户提供页面截图

提取内容后：
- 分析页面结构、文本、链接信息
- 进行完整的功能性评审

---

**截图评审** - 用户提供了图片文件

优先使用以下工具分析视觉内容（按可用性排序）：
1. `mcp__zai-mcp-server__analyze_image` - ZAI MCP 服务器
2. `mcp__MiniMax__understand_image` - MiniMax 图像理解
3. `mcp__4_5v_mcp__analyze_image` - 4.5v 图像分析
4. `Read` 工具直接读取图片（Claude 原生视觉能力）

分析重点：
- 视觉层级（焦点唯一性、层级≤3级）
- 信息密度（过密/适中/过疏）
- 交互状态（空/加载/错误/成功/边界态）
- 进行视觉和交互评审

---

**兜底方案：无工具可用**

如果没有可用的图像分析工具：
1. 请求用户描述截图内容
2. 引导用户提供关键信息（页面类型、核心功能、主要问题）
3. 基于描述进行评审分析
4. 建议用户安装相关 MCP 服务器以获得更好的体验

---

### 步骤 2：选择评审深度

**快速评审（5分钟）** - 适用于初步筛选
- 读取 [references/quick-review.md](references/quick-review.md)
- 输出：核心问题、优化建议、亮点

**深度评审（30分钟）** - 适用于重要页面
- 读取 [references/deep-review.md](references/deep-review.md)
- 输出：完整诊断报告 + 三套方案 + 执行计划

---

### 步骤 3：执行评审

根据评审需求选择合适的审查标准：

#### 基础评审（七维度框架）
读取核心评分标准和检查清单：
- [references/dimensions.md](references/dimensions.md) - 七维度评分标准（战略目标/用户体验/功能内容/数据度量/技术性能/市场竞品/迭代运营）

#### 专业深度评审（可选专项审查）
如需进行专项深度审查，可参考以下专业框架：

**视觉与设计审查：**
- [references/color-review.md](references/color-review.md) - 专业颜色审查框架（六层审查模型）
- [references/typography-review.md](references/typography-review.md) - 排版与字体审查指南
- [references/interaction-review.md](references/interaction-review.md) - 交互与动画审查标准

**可访问性与合规审查：**
- [references/accessibility-review.md](references/accessibility-review.md) - 无障碍访问审查清单（六层无障碍金字塔）
- [references/security-review.md](references/security-review.md) - 安全性与合规审查指南（七层安全模型）

**性能与优化审查：**
- [references/performance-review.md](references/performance-review.md) - 性能与优化审查标准（七层性能模型）

#### 专项审查策略：
1. **截图评审重点**：优先使用颜色、排版、交互审查
2. **网址评审重点**：优先使用性能、安全、无障碍审查  
3. **业务关键页面**：建议进行全维度深度审查
4. **时间有限时**：使用基础七维度快速审查

---

### 步骤 4：输出报告

使用报告模板：
- [references/templates.md](references/templates.md) - 评审报告模板

---

## 评审输出要点

### 基础输出（必须包含）

1. **问题分类** - 致命(P0) / 体验(P1) / 优化(P2)
2. **三套方案** - 渐进优化 / 结构重塑 / 理想方案
3. **优先级** - 影响度×努力度矩阵排序
4. **度量指标** - 可验证的成功标准

### 专业审查输出（深度评审时包含）

**视觉设计审查输出：**
- 颜色审查六层评估结果（技术合规/美学设计/功能体验/品牌战略/技术实现/业务适配）
- 排版审查评分（可读性、层次性、一致性）
- 交互审查结果（响应性、流畅度、状态完整性）

**可访问性审查输出：**
- 无障碍六层金字塔评估（基础保障/技术合规/感知认知/用户体验/技术实现/社会影响）
- 关键WCAG标准符合情况
- 辅助技术兼容性评估

**安全合规审查输出：**
- 安全七层模型评估（威胁建模/基础架构/通信安全/应用安全/访问控制/数据隐私/合规治理）
- 关键安全风险识别
- 合规性差距分析

**性能优化审查输出：**
- 性能七层模型评估（基础设施/服务端/应用代码/渲染处理/网络传输/用户体验/业务影响）
- Core Web Vitals达标情况
- 关键性能瓶颈识别

---

### 截图评审特有

- 视觉层级扫描（焦点唯一性、层级≤3级）
- 信息密度分析（过密/适中/过疏）
- 交互状态检查（空/加载/错误/成功/边界态）

---

### 网址评审特有

- 功能完整性检查
- 交互路径验证
- 加载性能评估
- 数据埋点分析

---

## 通用工具调用策略

### 图像分析工具（截图评审）

**优先级 1 - ZAI MCP**
```yaml
工具: mcp__zai-mcp-server__analyze_image
参数:
  image_source: 图片文件路径或 URL
  prompt: "分析这个页面的产品设计，包括视觉层级、信息架构、交互设计、功能完整性等方面"
```

**优先级 2 - MiniMax**
```yaml
工具: mcp__MiniMax__understand_image
参数:
  image_source: 图片文件路径或 URL
  prompt: "请详细分析这个页面的设计，包括视觉层级、信息密度、交互设计等方面"
```

**优先级 3 - 4.5v MCP**
```yaml
工具: mcp__4_5v_mcp__analyze_image
参数:
  imageSource: 图片 URL
  prompt: "分析页面的视觉设计、信息架构和交互体验"
```

**优先级 4 - Claude 原生 Read**
```yaml
工具: Read
参数:
  file_path: 图片文件绝对路径
# Claude 原生支持图像理解
```

---

### Web 内容获取工具（网址评审）

**优先级 1 - Web Reader MCP**
```yaml
工具: mcp__web_reader__webReader
参数:
  url: 用户提供的网址
  return_format: "markdown"      # 输出 Markdown 格式（支持中文）
  retain_images: true             # 保留图片
  with_images_summary: true       # 包含图片摘要
  with_links_summary: true        # 包含链接摘要
  no_gfm: false                   # 保持 GitHub Flavored Markdown（支持中文格式）
  no_cache: false                 # 使用缓存提升性能
```

**多语言配置说明：**
- 英文页面：保持原始英文内容输出
- 中文页面：自动识别并输出中文内容
- 其他语言：保持原始语言，支持多语言 markdown

**优先级 2 - Web 搜索**
```yaml
工具: WebSearch
参数:
  query: 网址或网站名称 + "页面功能"
```

---

## 工具可用性检测

**在执行评审前，先检测工具可用性：**

1. 检查是否有图像分析 MCP 工具可用
2. 检查是否有 Web Reader MCP 工具可用
3. 根据可用工具选择执行策略
4. 如果都不可用，使用兜底方案（请求用户描述）

**工具检测方法：**
- 尝试调用工具，如果失败则切换到下一个优先级
- 或根据用户环境配置判断可用工具

---

## 提示用户安装 MCP（可选）

如果用户频繁使用截图评审功能，可以建议：

```
建议安装以下 MCP 服务器以获得更好的图像分析体验：

1. ZAI MCP Server - 强大的图像分析能力
   配置位置: ~/.claude/mcp_settings.json

2. Web Reader MCP - 用于网页内容提取
   配置位置: ~/.claude/mcp_settings.json

安装指南可参考 Claude Code 官方文档。
```
