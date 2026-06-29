# Claude 平台适配指南

## 利用Claude特有能力

### 1. 使用 Artifacts 管理长文档

Claude的Artifacts功能非常适合标书的分章写作和整合：

```markdown
请创建一个名为"标书-技术方案"的Artifact，内容为第3章技术方案...
```

**分章策略：**
- 每章建立一个独立Artifact
- 最终质检时创建一个汇总Artifact整合所有章节
- 利用Artifact版本管理追踪修改

### 2. 使用Tool Use处理文件

利用Claude的Tool Use能力处理文件输入输出：

```
步骤1：调用 read_document 工具读取招标PDF
步骤2：调用 analyze_content 工具提取结构化信息
步骤3：调用 create_document 工具输出标书章节
```

### 3. 长上下文窗口管理

Claude支持100K+ tokens上下文，但需注意：
- 招标文件解析结果保持在上下文前端
- 生成完的章节可移出上下文（用Artifact暂存）
- 仅在质检阶段重新加载所有章节

### 4. 推荐提示词注入方式

```markdown
<system>
你正在运行 bid-document-maker 技能。
角色定义：prompts/system-prompt.md
工作流：workflows/pipeline.yaml（严格按stages顺序执行）
每个阶段前，先读取对应的 prompts/ 文件内容，然后执行该阶段任务。
</system>
```

### 5. 最佳实践

| 场景 | 做法 |
|------|------|
| 首次加载Skill | 一次性注入system-prompt.md + pipeline.yaml概览 |
| 解析阶段 | 使用Tool Use读取PDF，输出结构化JSON |
| 大纲确认 | 使用ListArtifact展示大纲 |
| 分章写作 | 每章一个Artifact + 用Tool Use写入本地文件 |
| 质检阶段 | 同时读取所有章节Artifact，生成质检报告 |

## 完整对话示例

```
用户：使用bid-document-maker技能，读取F:/tender/project.pdf并生成应标书

Claude：
[加载system-prompt.md角色定义]
[读取workflows/pipeline.yaml了解工作流]
[阶段1] 正在读取并解析招标文件...
[输出结构化解析摘要，请用户确认]
[阶段2-3] 正在分析评分策略并生成大纲...
[展示大纲，等待用户确认]
[阶段4] 正在编写各章节内容...
[使用Artifact逐章输出]
[阶段5] 正在执行质量检查...
[输出质检报告和最终文档]
```
