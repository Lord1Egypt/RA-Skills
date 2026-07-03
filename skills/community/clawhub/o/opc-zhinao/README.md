<!-- @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-10 -->

# OPC智脑 - 五阶段创业诊断Skills

> 一人创业者（OPC, One Person Company）的全栈创业诊断专家

**零外部依赖** | **纯TypeScript** | **中文Prompt** | **开箱即用**

---

## 快速链接

- 🌐 **官方网站**：http://opc.soberli.com
- 📦 **开源仓库**：https://gitee.com/zx_allen_li/opc_skills.git
- 📖 **使用文档**：见下方"快速开始"

---

## 什么是OPC智脑？

OPC智脑是一套将**创业诊断方法论产品化**的AI Skills系统。

> OPC智脑 = 创业方法论 × AI智能体 × 可执行工具

- **方法论**：五阶段创业诊断模型（构思→原型→实体→验证→规模化）
- **AI智能体**：把方法论变成可交互的AI诊断师
- **可执行工具**：Prompt + TypeScript双轨实现，可部署到任何平台

---

## Skills架构

```
opc-skills/
├── skills/                              # 8个独立Skill模块
│   ├── skill1-idea-feasibility/         # Skill1：Idea可行性研判
│   │   ├── skill.json                  # Skill配置（元数据、触发词、输入输出）
│   │   ├── prompt.md                   # Prompt文本（AI可读）
│   │   └── index.ts                    # TypeScript代码（程序可调用）
│   ├── skill2-mvp-design/              # Skill2：MVP精益设计
│   │   ├── skill.json / prompt.md / index.ts
│   ├── skill3-opc-compliance/          # Skill3：OPC合规落地
│   │   ├── skill.json / prompt.md / index.ts
│   ├── skill4-seed-coldstart/          # Skill4：种子用户冷启动
│   │   ├── skill.json / prompt.md / index.ts
│   ├── skill5-scale-growth/            # Skill5：规模化增长
│   │   ├── skill.json / prompt.md / index.ts
│   ├── feasibility-scoring/            # 可行度打分系统（跨阶段）
│   │   ├── skill.json / prompt.md
│   ├── report-export/                  # 报告导出（跨阶段）
│   │   ├── skill.json / prompt.md
│   └── user-feedback/                  # 用户反馈收集（跨阶段）
│       ├── skill.json / prompt.md
├── src/                                 # 核心引擎
│   ├── core/
│   │   ├── types.ts                    # 核心类型定义
│   │   ├── stage-classifier.ts         # 五阶段判定引擎
│   │   └── output-schema.ts            # 结构化输出Schema
│   ├── prompts/                         # Prompt文件（兼容旧版）
│   ├── skills/                         # TypeScript代码（兼容旧版）
│   └── index.ts                        # 统一导出入口
├── skills-registry.json                # Skills注册表（全局配置）
├── examples/                           # 各平台集成示例
├── docs/                               # 使用文档
├── package.json
└── README.md
```

---

## 每个Skill的结构

```
skill-xxx/
├── skill.json    # Skill配置（必须）
├── prompt.md     # Prompt文本（必须）
└── index.ts      # TypeScript代码（可选，跨阶段Skill可能没有）
```

### skill.json配置说明

```json
{
  "id": "skill1-idea-feasibility",
  "name": "Idea可行性研判",
  "version": "1.2.0",
  "author": "李屹镒（公众号：科技新潮。视频号：小李君与AI）",
  "description": "验证需求真伪，确认个人匹配度，完成可行性研判",
  "stage": 1,
  "stageName": "构思期",
  "graduationCondition": "需求验证通过 + 个人匹配度≥60 + 存在可行赛道",
  "triggers": ["创业Idea", "想法", "点子", "可行性", "需求验证"],
  "inputs": [...],
  "outputs": [...],
  "files": {
    "prompt": "prompt.md",
    "code": "index.ts"
  }
}
```

---

## 五阶段模型

| 阶段 | 名称 | 核心目标 | 对应Skill | 毕业条件 |
|------|------|---------|----------|---------|
| 1 | **构思期** | 验证需求真伪，确认个人匹配度 | Skill1-Idea可行性研判 | 需求验证通过 + 匹配度≥60 |
| 2 | **原型期** | 设计MVP，确定产品体系，测算交付成本 | Skill2-MVP精益设计 | MVP可交付 + 首单冷交付成功 |
| 3 | **实体期** | 主体注册，财税规划，合规落地 | Skill3-OPC合规落地 | 主体注册完成 + 财税规划落地 |
| 4 | **验证期** | 获取种子用户，验证付费意愿 | Skill4-种子用户冷启动 | 种子用户≥10 + 付费用户≥1 |
| 5 | **规模化期** | 构建增长引擎，实现一人规模化 | Skill5-规模化增长 | 月营收稳定增长 + 增长引擎运转 |

---

## 快速开始

### 方式1：IDE一键安装（推荐）

**⚠️ 重要：OPC智脑的文件结构**

```
opc_skills/                            # 开源仓库根目录
├── AGENTS.md                          # Agent指令文件（完整版）⭐
├── install-codearts.sh                # 码道IDE安装脚本 ⭐
├── install-prompt.sh                  # 通用Prompt安装脚本
├── verify-install.sh                  # 安装验证脚本
├── skills/                            # 8个独立Skill模块
│   ├── skill1-idea-feasibility/
│   │   ├── SKILL.md                   # Skill实现（码道IDE使用）
│   │   ├── skill.json                 # Skill配置
│   │   ├── prompt.md                  # Prompt文本
│   │   └── index.ts                   # TypeScript代码
│   ├── skill2-mvp-design/
│   ├── skill3-opc-compliance/
│   ├── skill4-seed-coldstart/
│   ├── skill5-scale-growth/
│   ├── feasibility-scoring/
│   ├── report-export/
│   └── user-feedback/
├── src/                               # 核心引擎
│   ├── prompts/                       # Prompt源文件
│   │   ├── system-persona.md
│   │   └── core-hub.md
│   └── ...
├── skills-registry.json               # Skills注册表
└── README.md                          # 本文档
```

**⚠️ AGENTS.md维护说明**：
- `AGENTS.md` 是完整版，包含所有配置（五阶段Skills、报告导出、用户反馈等）
- 安装时直接复制到目标项目
- 如需修改，修改`AGENTS.md`后重新安装即可

---

#### 1.1 码道IDE安装（完整功能）

```bash
# 进入opc-skills目录
cd opc-skills

# 安装到新项目
bash install-codearts.sh /path/to/your-project

# 或在当前项目安装
bash install-codearts.sh .
```

**安装过程**：
1. ✅ 自动复制AGENTS.md（完整版）
2. ✅ 自动生成opc-zhinao.json、ProjectSkillStatus.txt
3. ✅ 自动复制所有skills
4. ✅ **询问是否删除opc-skills目录**（保持项目清爽）

**安装后自动生成**：
- ✅ `AGENTS.md` - 完整版配置文件
- ✅ `.codeartsdoer/agents/opc-zhinao.json` - 自动生成
- ✅ `.codeartsdoer/skills/ProjectSkillStatus.txt` - 自动生成（注册所有skills）
- ✅ `.codeartsdoer/skills/` - 从源目录复制

**安装后文件结构**：
```
your-project/
├── AGENTS.md                          # 完整版配置
└── .codeartsdoer/
    ├── agents/
    │   └── opc-zhinao.json            # 自动生成
    └── skills/                        # 自动复制
        ├── ProjectSkillStatus.txt     # 自动生成（注册所有skills）
        ├── skill1-idea-feasibility/
        ├── skill2-mvp-design/
        ├── skill3-opc-compliance/
        ├── skill4-seed-coldstart/
        ├── skill5-scale-growth/
        ├── feasibility-scoring/
        ├── report-export/
        └── user-feedback/
```

**⚠️ 说明**：
- `skills-registry.json`不会复制到项目根目录（码道IDE不需要）
- 项目根目录保持清爽，只有`AGENTS.md`和`.codeartsdoer/`

**ProjectSkillStatus.txt示例**：
```
skill1-idea-feasibility=true
skill2-mvp-design=true
skill3-opc-compliance=true
skill4-seed-coldstart=true
skill5-scale-growth=true
feasibility-scoring=true
report-export=true
user-feedback=true
```

---

#### 1.2 CodeBuddy/WorkBuddy安装

```bash
cd opc-skills
bash install-codebuddy.sh /path/to/your-project
```

**安装特性**：
- ✅ 只复制SKILL.md文件（不复制整个skill目录）
- ✅ 自动生成skills-registry.json
- ✅ **询问是否删除opc-skills目录**（需输入"DELETE"确认）

**安装后文件结构**：
```
your-project/
├── AGENTS.md
└── .codebuddy/
    ├── skills-registry.json      # 自动生成
    └── skills/                   # 只包含SKILL.md
        ├── skill1-idea-feasibility/
        │   └── SKILL.md
        ├── skill2-mvp-design/
        │   └── SKILL.md
        └── ...
```

---

#### 1.3 通用Prompt安装（适用任何AI平台）

```bash
cd opc-skills
bash install-prompt.sh /path/to/your-project
```

**支持的IDE列表**：

**国内主流IDE**：
- 码道IDE（CodeArts）
- 通义灵码（阿里云）
- 百度Comate
- 腾讯云AI代码助手
- 豆包MarsCode（字节跳动）
- CodeGeeX（智谱）
- 讯飞iFlyCode

**国际主流IDE**：
- Cursor
- VSCode + Copilot
- Windsurf
- CodeBuddy/WorkBuddy

**安装特性**：
- ✅ 自动检测12种IDE环境
- ✅ 提供友好的选择菜单
- ✅ 只复制SKILL.md文件（不复制整个skill目录）
- ✅ **询问是否删除opc-skills目录**（保持项目清爽）

**安装后自动生成**：
- ✅ `AGENTS.md` - 完整版配置文件
- ✅ `opc-zhinao-prompt.md` - 通用Prompt文件（通用模式）
- ✅ `skills/` - 所有Skills模块（只包含SKILL.md）

**使用方式**：
- **OpenAI/Claude**：复制到System Prompt
- **Coze/Dify**：作为Bot的System Prompt
- **LangChain**：作为PromptTemplate

---

### 方式2：作为npm包使用

```bash
npm install opc-skills
```

```typescript
import { classifyStage, executeSkill1 } from 'opc-skills';

// 阶段判定
const result = classifyStage({
  demandValidation: 30,
  solutionMaturity: 20,
  complianceReadiness: 10,
  userAcquisition: 5,
  scalabilityLevel: 0,
});

// 执行Skill
const skillResult = executeSkill1({ projectInfo: {...} });
console.log(skillResult.prompt); // 发送给任何大模型
```

---

### 方式4：直接使用Prompt文件

将 `skills/xxx/prompt.md` 的内容复制到任何AI平台：
- **Coze**：创建工作流，粘贴prompt.md
- **Dify**：创建Chatflow，粘贴prompt.md
- **OpenAI**：作为system prompt
- **码道IDE**：通过AGENTS.md + opc-zhinao.json

---

### 方式5：使用skill.json配置

读取 `skills-registry.json` 获取所有Skill的注册信息，按需加载：

```typescript
const registry = require('./skills-registry.json');
const skill1Config = require('./skills/skill1-idea-feasibility/skill.json');
const skill1Prompt = require('./skills/skill1-idea-feasibility/prompt.md');
```

---

## 常见问题

### Q1：安装后IDE没有识别到OPC智脑？

**检查清单**：
1. ✅ `.codeartsdoer/agents/opc-zhinao.json` 文件存在
2. ✅ `AGENTS.md` 文件存在
3. ✅ `.codeartsdoer/skills/` 目录下至少有一个skill
4. ✅ opc-zhinao.json中的`instructions`字段指向`AGENTS.md`

**验证命令**：
```bash
cat .codeartsdoer/agents/opc-zhinao.json
# 应该看到 "instructions": "AGENTS.md"
```

### Q2：如何验证skills是否安装成功？

```bash
# 检查skills数量
ls -d .codeartsdoer/skills/*/ | wc -l
# 应该输出：8（8个skills）

# 检查每个skill的SKILL.md是否存在
for skill in .codeartsdoer/skills/*/; do
  echo "$(basename $skill): $(ls $skill/*.md 2>/dev/null | wc -l) files"
done
```

### Q3：可以在已有项目中安装吗？

可以！OPC智脑不会覆盖你的现有文件，只会添加：
- `AGENTS.md`（如果已存在会提示）
- `.codeartsdoer/`目录（不会影响其他文件）

### Q4：如何卸载OPC智脑？

```bash
# 删除OPC智脑相关文件
rm AGENTS.md
rm -rf .codeartsdoer/agents/opc-zhinao.json
rm -rf .codeartsdoer/skills/
```

**更多问题**：详见 [FAQ文档](docs/faq.md)

---

## 实际使用场景

### 场景1：创业Idea验证

**用户画像**：有想法但不确定可行性

**使用步骤**：
1. 描述你的创业Idea（行业、痛点、目标用户）
2. OPC智脑自动触发Skill1（Idea可行性研判）
3. 获得三维评分（需求可行性、市场空间、个人匹配度）
4. 根据评分决策：继续推进 / 调整方向 / 放弃

### 场景2：MVP设计

**用户画像**：已验证需求，需要设计最小可行产品

**使用步骤**：
1. 告知已通过需求验证
2. OPC智脑自动触发Skill2（MVP精益设计）
3. 获得功能裁剪建议、交付成本测算、三层产品体系
4. 执行首单冷交付验证

### 场景3：合规落地

**用户画像**：准备注册公司/个体户

**使用步骤**：
1. 告知需要注册主体
2. OPC智脑自动触发Skill3（OPC合规落地）
3. 获得注册流程、财税规划、商用模板
4. 按步骤完成合规落地

**更多场景**：详见 [使用场景文档](docs/usage-scenarios.md)

---

## 故障排查

遇到问题？请查看 [故障排查指南](docs/troubleshooting.md)

---

## 跨阶段Skills

| Skill | 说明 | 适用阶段 |
|-------|------|---------|
| **feasibility-scoring** | 可行度打分系统（需求可行性×0.4 + 市场空间×0.3 + 个人匹配度×0.3） | 所有阶段 |
| **report-export** | 报告导出（Markdown + HTML） | 诊断完成后 |
| **user-feedback** | 用户反馈收集（快速5题/详细11题） | 报告导出后 |

---

## 集成方式

| 平台 | 集成方式 | 需要文件 |
|------|---------|---------|
| **码道IDE** | 自动识别 | opc-zhinao.json + AGENTS.md |
| **通义灵码** | 自动识别 | AGENTS.md + skills/ |
| **百度Comate** | 自动识别 | AGENTS.md + skills/ |
| **腾讯云AI代码助手** | 自动识别 | AGENTS.md + skills/ |
| **豆包MarsCode** | 自动识别 | AGENTS.md + skills/ |
| **CodeGeeX** | 自动识别 | AGENTS.md + skills/ |
| **讯飞iFlyCode** | 自动识别 | AGENTS.md + skills/ |
| **Cursor** | 自动识别 | .cursorrules + skills/ |
| **VSCode + Copilot** | 自动识别 | copilot-instructions.md + skills/ |
| **Windsurf** | 自动识别 | AGENTS.md + skills/ |
| **CodeBuddy/WorkBuddy** | 自动识别 | skills-registry.json + skills/ |
| **Coze** | 粘贴prompt.md | skills/xxx/prompt.md |
| **Dify** | 粘贴prompt.md | skills/xxx/prompt.md |
| **OpenAI API** | system prompt | skills/xxx/prompt.md |
| **LangChain** | 代码集成 | skills/xxx/index.ts |
| **npm** | 包安装 | npm install opc-skills |

详见：[集成指南](docs/integration-guide.md)

---

## 设计原则

1. **禁止跨阶段给方案**：处于构思期只给构思期建议，不跳阶段
2. **适配单人公司**：不假设有团队、合伙人、融资
3. **可执行性**：所有建议必须具体到可以立即执行
4. **量化输出**：不使用"可以考虑"等模糊表述
5. **安全余量**：时间和预算评估预留30%余量
6. **Prompt+Code双轨**：每个Skill同时提供Prompt（AI可读）和TypeScript（程序可调用）

---

## 文档

- [五阶段模型详解](docs/stage-model.md)
- [Skill参考手册](docs/skill-reference.md)
- [集成指南](docs/integration-guide.md)

---

## 许可证

MIT License © 2026 李屹镒
