# CyberPPT 多平台兼容性文档

[简体中文](PLATFORM_COMPATIBILITY.md) | [English](PLATFORM_COMPATIBILITY.en.md)

## 概述

CyberPPT 从 v1.0.0 版本开始支持多 AI Agent 平台。本文档详细说明多平台支持的架构设计、配置方法和使用指南。

## 支持的平台

### 完全支持的平台

| 平台 | 配置文件 | 安装路径 | 验证状态 |
|---|---|---|---|
| **OpenCode** | `agents/opencode.yaml` | `~/.opencode/skills/cyber-ppt` | ✅ 已验证 |
| **OpenAI Codex** | `agents/openai.yaml` | `~/.codex/skills/cyber-ppt` | ✅ 已验证 |
| **Hermes** | `agents/hermes.yaml` | `~/.hermes/skills/cyber-ppt` | ✅ 已支持 |
| **OpenClaw** | `agents/openclaw.yaml` | `~/.openclaw/skills/cyber-ppt` | ✅ 已支持 |
| **Anthropic/Claude** | `agents/anthropic.yaml` | `~/.anthropic/skills/cyber-ppt` | ✅ 已支持 |

### 通用支持

- **Generic Platform** - `agents/generic.yaml` - 适用于任何支持 skill 机制的 AI Agent 平台

## 架构设计

### 平台无关层

CyberPPT 的核心功能完全平台无关：

```
├── SKILL.md                    # 核心技能逻辑（平台无关）
├── scripts/                    # Python 脚本（平台无关）
│   ├── validate_pptx.py       # PPTX 验证脚本
│   ├── build_visual_qa_gate.py
│   ├── compare_render.py
│   └── ...
├── references/                 # 参考文档（平台无关）
│   ├── source-analysis.md
│   ├── storyline.md
│   ├── visual-system.md
│   ├── ppt-production.md
│   └── quality-assurance.md
└── assets/                     # 资源文件（平台无关）
    ├── palette-samples/
    └── ...
```

### 平台适配层

平台特定的配置位于 `agents/` 目录：

```
agents/
├── opencode.yaml              # OpenCode 平台配置
├── openai.yaml                # OpenAI Codex 配置
├── hermes.yaml                # Hermes 配置
├── openclaw.yaml              # OpenClaw 配置
├── anthropic.yaml             # Anthropic/Claude 配置
└── generic.yaml               # 通用平台模板
```

## 配置文件结构

### YAML 配置格式

每个平台的配置文件遵循统一的结构：

```yaml
interface:
  display_name: "CyberPPT"
  short_description: "生成基于证据、可编辑的咨询风格 PPT"
  default_prompt: "使用 $cyber-ppt，把我的源文档转成高密度、可编辑的咨询风格 PPT。"
  skill_type: "presentation_generation"
  version: "1.0.0"
  
compatibility:
  platforms:
    - [平台名称]
  min_version: "1.0.0"
  
configuration:
  trigger_patterns:
    - "做PPT"
    - "生成演示文稿"
    - "制作幻灯片"
    - "CyberPPT"
    - "咨询风格PPT"
    
  file_types:
    - ".docx"
    - ".pdf"
    - ".txt"
    - ".xlsx"
    
  output_format: ".pptx"
  
  workflow:
    stages:
      - name: "analysis"
        description: "资料分析与证据链构建"
        required: true
      - name: "blueprint"
        description: "风格选择与蓝图生成"
        required: true
      - name: "reconstruction"
        description: "PPT还原与质量保证"
        required: true
        
  quality_gates:
    - reference_gate
    - evidence_gate
    - storyline_gate
    - density_gate
    - style_gate
    - blueprint_gate
    - asset_admission_gate
    - editable_layer_gate
    - visual_semantics_gate
    - curve_trace_gate
    - spatial_registration_gate
    - container_overflow_gate
    - typography_gate
    - render_qa_gate
    - strict_qa_gate
```

### 配置字段说明

#### interface 部分

| 字段 | 类型 | 说明 | 是否必需 |
|---|---|---|---|
| `display_name` | string | Skill 显示名称 | ✅ 必需 |
| `short_description` | string | 简短描述 | ✅ 必需 |
| `default_prompt` | string | 默认提示词 | ✅ 必需 |
| `skill_type` | string | Skill 类型标识 | ✅ 必需 |
| `version` | string | 版本号（语义化版本） | ✅ 必需 |

#### compatibility 部分

| 字段 | 类型 | 说明 | 是否必需 |
|---|---|---|---|
| `platforms` | array | 支持的平台列表 | ✅ 必需 |
| `min_version` | string | 最低兼容版本 | ✅ 必需 |

#### configuration 部分

| 字段 | 类型 | 说明 | 是否必需 |
|---|---|---|---|
| `trigger_patterns` | array | 触发关键词列表 | ✅ 必需 |
| `file_types` | array | 支持的输入文件类型 | ✅ 必需 |
| `output_format` | string | 输出文件格式 | ✅ 必需 |
| `workflow` | object | 工作流定义 | ✅ 必需 |
| `quality_gates` | array | 质量门禁列表 | ✅ 必需 |

## 安装指南

### 自动安装

#### OpenCode

```powershell
# Windows
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.opencode\skills\cyber-ppt"

# macOS/Linux
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.opencode/skills/cyber-ppt"
```

#### OpenAI Codex

```powershell
# Windows
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\cyber-ppt"

# macOS/Linux
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.codex/skills/cyber-ppt"
```

#### Hermes

```powershell
# Windows
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.hermes\skills\cyber-ppt"

# macOS/Linux
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.hermes/skills/cyber-ppt"
```

#### OpenClaw

```powershell
# Windows
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.openclaw\skills\cyber-ppt"

# macOS/Linux
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.openclaw/skills/cyber-ppt"
```

#### Anthropic/Claude

```powershell
# Windows
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.anthropic\skills\cyber-ppt"

# macOS/Linux
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.anthropic/skills/cyber-ppt"
```

### 手动安装

1. 下载项目：
   ```bash
   # 使用 git
   git clone https://github.com/crazyykhllc-bit/CyberPPT.git
   
   # 或下载 ZIP
   curl -L https://github.com/crazyykhllc-bit/CyberPPT/archive/refs/heads/main.zip -o CyberPPT.zip
   ```

2. 复制到平台目录：
   - 将项目文件夹重命名为 `cyber-ppt`
   - 复制到对应平台的 skills 目录
   - 确保 `SKILL.md` 在根目录

3. 验证安装：
   ```
   与 Agent 对话：使用 CyberPPT skill
   ```

## 使用指南

### 触发方式

在所有平台上，可以使用以下方式触发 CyberPPT：

#### 关键词触发

- "做PPT"
- "生成演示文稿"
- "制作幻灯片"
- "CyberPPT"
- "咨询风格PPT"

#### 显式调用

```
使用 CyberPPT skill 将这份文档转成PPT
```

```
用 $cyber-ppt 生成咨询风格的演示文稿
```

### 工作流程

无论在哪个平台，CyberPPT 都遵循相同的三阶段流程：

#### 阶段 1：资料分析

```
输入：上传文档（DOCX/PDF/TXT/XLSX）
输出：MBB 证据表、故事线、逐页大纲
确认：用户批准页数、结构、密度
```

#### 阶段 2：蓝图生成

```
输入：用户选择视觉风格（8种之一）
输出：逐页 ImageGen 蓝图
确认：用户批准全部页面蓝图
```

#### 阶段 3：PPT还原

```
输入：已批准的蓝图
输出：可编辑 PPTX + QA 报告
确认：用户批准最终 PPT
```

### 质量保证

所有平台共享相同的质量门禁系统：

| 门禁 | 检查内容 | 失败后果 |
|---|---|---|
| Reference Gate | 阶段参考文件完整性 | 不得进入阶段 |
| Evidence Gate | 证据链可追溯性 | 标记缺口或返工 |
| Storyline Gate | 故事线脑暴与收敛 | 不得进入蓝图阶段 |
| Density Gate | 页面信息密度 | 补充内容或重排 |
| Style Gate | 视觉风格确认 | 不得进入蓝图阶段 |
| Blueprint Gate | 蓝图完整性 | 不得进入还原阶段 |
| Asset Admission Gate | 图片资产必要性 | 改为原生重建 |
| Editable Layer Gate | 信息层可编辑性 | 返工重建 |
| Visual Semantics Gate | 视觉语义保真度 | 视觉 QA 失败 |
| Curve Trace Gate | 曲线精确追踪 | 使用 path/custom geometry |
| Spatial Registration Gate | 空间锚点对齐 | 返工调整 |
| Container Overflow Gate | 容器边界检查 | 返工调整 |
| Typography Gate | 字号层级合规 | 返工调整 |
| Render QA Gate | 渲染对照检查 | 继续迭代 |
| Strict QA Gate | 结构化校验 | 出错即返工 |

## 平台特定功能

### OpenCode 特性

- ✅ 原生支持 YAML 配置
- ✅ 自动加载 `agents/opencode.yaml`
- ✅ 支持所有 16 个质量门禁
- ✅ 支持 ImageGen 蓝图生成
- ✅ 支持视觉 QA 检查

### OpenAI Codex 特性

- ✅ 原生平台（首个支持平台）
- ✅ 完整功能支持
- ✅ 最佳兼容性保证

### Hermes 特性

- ✅ 完全兼容
- ✅ 统一工作流
- ✅ 统一质量标准

### OpenClaw 特性

- ✅ 完全兼容
- ✅ 统一工作流
- ✅ 统一质量标准

### Anthropic/Claude 特性

- ✅ 完全兼容
- ✅ 针对长上下文优化
- ✅ 支持 Claude 特定功能

## 添加新平台支持

### 步骤 1：创建配置文件

```bash
cd agents/
cp generic.yaml [新平台名].yaml
```

### 步骤 2：编辑配置

编辑 `[新平台名].yaml`：

```yaml
compatibility:
  platforms:
    - [新平台名]
```

根据平台特性调整 `configuration` 部分。

### 步骤 3：测试验证

1. 安装到新平台的 skills 目录
2. 使用触发关键词测试
3. 执行完整的三阶段流程
4. 验证质量门禁正常工作

### 步骤 4：提交贡献

如需将新平台支持贡献回主仓库：

1. Fork 项目
2. 创建特性分支
3. 添加配置文件和文档更新
4. 提交 Pull Request

## 故障排查

### 常见问题

#### 问题：Agent 无法识别 CyberPPT

**可能原因：**
- 安装路径错误
- 文件夹名称不正确
- `SKILL.md` 文件缺失

**解决方案：**
1. 检查安装路径是否符合平台要求
2. 确认文件夹名为 `cyber-ppt`
3. 验证 `SKILL.md` 存在于根目录
4. 重启 Agent 或重新加载 skills

#### 问题：质量门禁不生效

**可能原因：**
- 配置文件缺失
- 配置格式错误
- `quality_gates` 列表不完整

**解决方案：**
1. 检查 `agents/[平台].yaml` 是否存在
2. 验证 YAML 格式正确
3. 确认 `quality_gates` 包含所有 16 个门禁

#### 问题：输出 PPTX 格式错误

**可能原因：**
- Python 环境未安装
- 依赖包缺失
- 脚本执行权限问题

**解决方案：**
1. 确认 Python 3.7+ 已安装
2. 安装依赖：`pip install python-pptx pillow`
3. 检查 `scripts/validate_pptx.py` 可执行权限

#### 问题：平台间功能不一致

**可能原因：**
- 配置文件差异
- 平台特定限制

**解决方案：**
1. 对比 `agents/` 下不同平台的配置
2. 检查平台官方文档了解限制
3. 调整配置以适配平台特性

## 更新与维护

### 更新 Skill

```bash
cd [你的安装目录]/cyber-ppt
git pull
```

### 版本兼容性

CyberPPT 使用语义化版本号（Semantic Versioning）：

- **主版本号**：不兼容的 API 变更
- **次版本号**：向后兼容的功能新增
- **修订号**：向后兼容的问题修正

### 迁移指南

当升级主版本时，请查看 `CHANGELOG.md` 了解变更和迁移步骤。

## 最佳实践

### 平台选择建议

| 使用场景 | 推荐平台 | 原因 |
|---|---|---|
| 日常使用 | OpenCode | 最佳验证支持 |
| 长文档处理 | Anthropic/Claude | 超长上下文支持 |
| 企业环境 | OpenAI Codex | 原生支持，最稳定 |
| 实验性功能 | Hermes/OpenClaw | 灵活配置 |

### 跨平台协作

1. **统一证据源**：所有平台使用相同的源材料
2. **共享蓝图**：生成的蓝图可在不同平台间共享
3. **标准化 QA**：使用统一的 QA 检查脚本
4. **版本控制**：使用 Git 管理工作成果

### 性能优化

- 使用 SSD 存储 skills 目录
- 保持 Python 环境干净
- 定期清理缓存文件
- 使用虚拟环境隔离依赖

## 技术支持

### 获取帮助

- **文档**：查看本项目 `docs/` 目录
- **Issues**：GitHub Issues
- **讨论**：GitHub Discussions

### 报告问题

提交 Issue 时请包含：

1. 使用的平台和版本
2. 完整的错误信息
3. 复现步骤
4. 相关配置文件内容

### 贡献代码

欢迎贡献新平台支持、Bug 修复和功能改进。请遵循：

1. Fork 项目
2. 创建特性分支
3. 遵循代码规范
4. 编写测试用例
5. 提交 Pull Request

## 许可证

MIT License. 详见 [LICENSE](LICENSE).

---

**版本**：v1.0.0  
**更新日期**：2026-07-23  
**维护者**：CyberPPT Team
