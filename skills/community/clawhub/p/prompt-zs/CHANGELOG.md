# 更新日志

## [1.0.1] - 2025-03-17

### 重构内容

#### 文件结构优化
- 创建 `scripts/` 目录存放辅助脚本
- 创建 `examples/` 目录存放使用示例
- 创建 `evals/` 目录存放测试用例
- 移动 `prompt-zs-基础提示词生成器.py` 到 `scripts/`
- 移动 `prompt-zs-专业提示词.json` 到 `examples/basic-example.json`

#### SKILL.md 改进
- **优化描述字段**：添加更多触发关键词，提高技能触发率
- **添加版本号**：在 frontmatter 中声明版本 1.0.1
- **重构内容结构**：
  - 添加"快速决策流程"图示
  - 添加"使用脚本"章节
  - 添加"全局约束"章节
  - 添加"版本历史"章节
- **改进输出格式说明**：更清晰的 JSON 结构示例
- **完善触发场景**：为每个模式添加更详细的触发条件描述

#### 新增文件
- `README.md`：技能使用说明文档
- `CHANGELOG.md`：版本更新日志
- `examples/expert2-example.json`：专业摄影风格示例
- `examples/video-text-example.md`：文生视频示例
- `examples/video-image-example.md`：图生视频示例
- `evals/evals.json`：测试用例定义

#### 描述优化
**旧版本：**
> 专业的AI绘画、视频创作与翻译提示词助手，支持输出高度定制化的 JSON 格式与特定参数要求。

**新版本：**
> 专业AI绘画与视频创作提示词生成助手。当用户需要生成AI绘画提示词、Midjourney/Stable Diffusion提示词、AI绘画描述、图像生成提示词时使用。也适用于文生视频提示词、图生视频提示词、视频创作描述、Runway/Pika视频提示词等场景。支持生成JSON格式提示词、标签化提示词、摄影风格描述。当用户提到"生成提示词"、"优化提示词"、"prompt优化"、"AI绘画"、"图像生成"、"视频生成"时必须使用此技能。

改进点：
- 添加具体工具名称（Midjourney、Stable Diffusion、Runway、Pika）
- 添加更多触发关键词
- 明确使用场景
- 使用"必须使用此技能"等强调性语言

#### 触发关键词扩展
新增触发关键词：
- Midjourney、Stable Diffusion、DALL-E
- Runway、Pika、Sora
- 优化提示词、prompt优化
- AI绘画、图像生成、视频生成

### 向后兼容性
- 所有原有功能保持不变
- 输出格式完全兼容
- 可直接替换旧版本使用

### 使用建议
1. 替换旧版本的 SKILL.md 文件
2. 新增的示例文件可供参考
3. 测试用例可用于验证功能正确性

---

## [1.0.0] - 初始版本

### 核心功能
- 基础 JSON 提示词生成（Expert 1）
- 精准 JSON 提示词生成（Expert 2）
- 极简翻译
- 文生视频提示词扩展
- 图生视频提示词扩展
