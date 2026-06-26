# Manim动画与LaTeX提示词专家技能

## 简介
这是一个Claude技能，用于将简单的Manim动画描述转化为详细的LaTeX提示词并生成可运行的Manim社区版代码。

## 功能特点
- 将简单描述转化为详细的动画脚本
- 生成可直接运行的Manim代码
- 自动检查代码语法和逻辑
- 提供完整的运行指令

## 使用方法
1. 将整个文件夹上传到Claude Code或Claude.ai
2. 当需要创建Manim动画时，技能会自动触发
3. 按照三步流程：描述→代码→检查

## 目录结构
- `SKILL.md`: 核心技能定义
- `scripts/`: 示例脚本
- `references/`: Manim快速参考
- `assets/`: 模板和资源

## 示例
- 用户: "创建一个展示勾股定理的动画"
- 技能:
- 生成详细动画描述
- 输出完整Manim代码
- 提供运行指令

## 依赖
- Manim社区版 (manim)
- Python 3.7+
- LaTeX发行版 (如TeX Live)