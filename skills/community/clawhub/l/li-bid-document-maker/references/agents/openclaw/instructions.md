# OpenClaw 平台适配指南

## 一、安装方式

### 方式A：自动安装（推荐）

```bash
# 1. 将整个 skill 目录安装到 OpenClaw
openclaw skill install F:\python_test\bid-document-maker

# 或从远程仓库安装
openclaw skill install https://github.com/example/bid-document-maker

# 2. 注册工作流
openclaw workflow register agents/openclaw/workflow.yaml

# 3. 安装必需插件
openclaw plugin install file-reader
openclaw plugin install docx-generator    # 可选，Word输出

# 4. 验证安装
openclaw skill list | grep bid-document-maker
```

### 方式B：手动安装

```bash
# 1. 复制文件到 skills 目录
cp -r bid-document-maker ~/.openclaw/skills/

# 2. 注册 skill
openclaw skill register ~/.openclaw/skills/bid-document-maker/agents/openclaw/skill-registration.yaml

# 3. 安装插件
openclaw plugin install file-reader

# 4. 验证
openclaw skill info bid-document-maker
```

### 安装验证

```bash
# 验证 skill 列表
openclaw skill list
# 预期输出中包含: bid-document-maker  v1.0.0  标书制作专家

# 验证工作流
openclaw workflow validate agents/openclaw/workflow.yaml
# 预期输出: ✓ Workflow 'bid-document-maker' is valid (5 stages, 1 parallel group)

# 验证插件
openclaw plugin list | grep file-reader
# 预期输出: file-reader  v1.0.0  enabled
```

## 二、核心文件

| 文件 | 用途 | 安装到 |
|------|------|--------|
| `agents/openclaw/workflow.yaml` | OpenClaw 工作流定义 | OpenClaw 自动读取 |
| `agents/openclaw/skill-registration.yaml` | Skill 注册配置 | 手动注册用 |
| `workflows/pipeline.yaml` | 通用工作流定义（跨平台） | 参考文件 |
| `prompts/*.md` | 各阶段提示词 | `skills/bid-document-maker/prompts/` |
| `templates/*` | 标书模板和格式规范 | `skills/bid-document-maker/templates/` |
| `schemas/*` | 数据结构验证 Schema | `skills/bid-document-maker/schemas/` |

## 三、工作流架构

```
主控Agent (bid-document-maker)
  │
  ├─ stage 1: tender-parser Agent  ──── 解析招标文件
  │   └─ 插件: file-reader (读取PDF/Word)
  │
  ├─ stage 2: strategy-analyst Agent ── 策略分析
  │
  ├─ stage 3: strategy-analyst Agent ── 生成大纲
  │   └─ 用户确认 ⏸
  │
  ├─ stage 4: 写作Agent集群 (并行) ──── 分章写作
  │   ├─ technical_writer
  │   ├─ implementation_writer
  │   ├─ quality_writer
  │   ├─ after_sales_writer
  │   └─ financial_writer
  │
  ├─ stage 5: quality-checker Agent ─── 质量检查
  │   └─ 插件: json-schema-validator
  │
  └─ stage 6: docx-generator Agent ──── 输出最终文档
      └─ 插件: docx-generator
```

## 四、工作流定义

实际工作流已定义为独立文件：`agents/openclaw/workflow.yaml`

该文件定义了：
- 6 个执行步骤（含并行写作）
- 输入/输出数据传递
- 用户确认节点
- 错误处理策略（自动重试、降级输出）
- 超时配置

可直接被 OpenClaw 工作流引擎加载执行：

```bash
openclaw run agents/openclaw/workflow.yaml \
  --input tender_file=/path/to/tender.pdf
```

## 五、Skill 注册配置

实际注册文件：`agents/openclaw/skill-registration.yaml`

首次安装后，OpenClaw 会自动解析此文件。包含：
- Skill 元信息（名称、版本、描述）
- 目录映射（prompts/ templates/ schemas/）
- 插件依赖和安装命令
- 使用示例

## 六、一键使用命令

```bash
# 最简方式（自动加载完整工作流）
openclaw run bid-document-maker --input tender_file=/data/project.pdf

# 指定输入文件
openclaw run bid-document-maker \
  --input tender_file=/data/project.pdf \
  --output ./output/bid.docx

# 分步执行（手动控制阶段切换）
openclaw run bid-document-maker \
  --input tender_file=/data/project.pdf \
  --step-by-step
```

## 七、多Agent 配置

如果需要自定义写作Agent的分工，在 OpenClaw 配置中声明：

```yaml
# ~/.openclaw/agents.yaml
agents:
  tender-parser:
    model: gpt-4o
    temperature: 0.3        # 解析需要精确，低温度

  strategy-analyst:
    model: claude-3-opus
    temperature: 0.5

  technical_writer:
    model: claude-3-sonnet
    temperature: 0.7        # 写作需要创造性

  quality-checker:
    model: gpt-4o
    temperature: 0.2        # 质检需要严格
```

## 八、常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `openclaw skill install` 失败 | 缺少 `file-reader` 插件 | 先运行 `openclaw plugin install file-reader` |
| 工作流运行到 stage 4 卡住 | 并行写作 Agent 资源不足 | 减少并行数（修改 workflow.yaml 中 `parallel` 配置） |
| 输出为 Markdown 而非 Word | `docx-generator` 插件未安装 | `openclaw plugin install docx-generator` 或接受 Markdown 输出 |
| PDF 解析后内容为空 | 文件为扫描件（图片格式） | 安装 OCR 插件或将 PDF 转为可检索格式 |

## 九、与WorkBuddy版本的主要区别

| 功能 | WorkBuddy版本 | OpenClaw版本 |
|------|--------------|-------------|
| 知识库 | 内置知识库联动 | 通过插件扩展 |
| 多Agent | 单一专家对话 | 多Agent协作集群 |
| 工作流 | 内置 | `workflow.yaml` 文件驱动 |
| 文件处理 | 内置 | `file-reader` 插件 |
| 安装 | 拖拽即可 | `openclaw skill install` 命令 |
