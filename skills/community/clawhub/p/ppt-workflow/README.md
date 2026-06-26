# PPT 工作流技能

**版本**: 1.0.0  
**创建日期**: 2026-03-14

## 概述

基于标准化工作流的 PPT 制作技能，从内容搜索到美化优化全流程自动化。

## 使用方式

```
帮我做一个 PPT，主题是：[你的主题]
```

## 工作流

7 个阶段，自动匹配最优模型：
1. 需求确认 (Qwen3.5) - 1 分钟
2. 内容搜索 (Kimi 2.5) - 30 分钟
3. 框架设计 (Qwen3.5) - 20 分钟
4. 内容填充 (Qwen3.5) - 50 分钟
5. 幻灯片制作 (Qwen3.5) - 40 分钟
6. 美化优化 (Minimax 2.5) - 20 分钟
7. 输出交付 (Qwen3.5) - 10 分钟

## 模型配置

- 主力模型：Qwen3.5 (70%)
- 辅助模型：Kimi 2.5 (15%) + Minimax 2.5 (15%)

## 依赖技能

- pptx
- scientific-slides
- academic-writing
- citation-management
- web_search
- scientific-visualization

## 输出

标准交付包：
- presentation.pptx
- presentation.pdf
- presentation_notes.pdf
- figures/
- references.bib
- README.md

## 维护者

academic-assistant
