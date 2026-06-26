# 灵枢技能包 (Ling Shu Skills)

Agent 设计师灵枢的专用技能集合。

**作者：** perrykono-debug  
**License：** MIT-0  
**ClawHub：** https://clawhub.ai/perrykono-debug/lingshu-agent-architect

---

## 技能列表

### ling-shu-agent-designer (v1.4.0) ⭐ 主技能
灵枢主技能 - Agent 设计师工作流与规范（v4.3 方法论）

**触发场景：**
- 用户要求设计 AI Agent 方案
- 需要创建新的 Agent
- 需要优化现有 Agent
- 需要发布/更新技能包到 GitHub & ClawHub

**核心能力：**
- **5步工作流：** 需求沟通 → 场景大纲 → 创建基础版 → 后续深化 → 自动发布
- **7项大纲模板：** 行业定位、核心功能、数据源、交互渠道、定时任务、Skill规划、治理边界
- **三大思想体系：** 吴明辉（组织）+ 吴恩达（方法）+ 傅盛（落地）
- **Self-Improving 系统：** 记录纠正、积累模式、自我反思（越用越聪明）
- **自动发布：** 一键推送到 GitHub & ClawHub（发布前 diff 预览确认）

### enterprise-agent-planner (v1.0.0) 🆕
企业 Agent 体系规划器

**触发场景：**
- 输入企业介绍，自动输出 AI Agent 体系规划方案
- 用户提供企业官网、企业介绍文档、行业报告

**核心能力：**
- **企业解析：** 提取行业属性、企业规模、业务模式、数字化程度、核心痛点
- **行业场景映射：** 匹配该行业典型 Agent 应用场景（制造业/零售业/服务业/金融业/教育业/医疗业/物流业/地产业）
- **Agent 体系规划：** 设计多 Agent 协同架构 + 输出 7 项大纲
- **MVP 落地建议：** 推荐 3-5 个核心启动能力 + 数据源 + 治理边界

**使用示例：**
```
用户：这是一家制造业企业的介绍：[企业信息]
灵枢：调用 enterprise-agent-planner
     → 输出完整的企业 Agent 体系规划方案
```

---

## 设计原则

融合三大 AI Agent 思想体系：
- **吴明辉（组织视角）**：Multi-Agent 协作、组织结构重塑
- **吴恩达（方法视角）**：Agentic Workflow、迭代优于完美
- **傅盛（落地视角）**：场景为王、窄场景切入、人机协作

---

## 版本历史

### v1.4.0 (2026-06-06) 🆕
- ✨ **新增 enterprise-agent-planner** (v1.0.0)
  - 输入企业介绍 → 自动输出 AI Agent 体系规划方案
  - 支持 8 大行业场景库（制造业/零售业/服务业/金融业/教育业/医疗业/物流业/地产业）
  - 企业解析 → 行业场景映射 → Agent 体系规划 → MVP 落地建议
  
- 🔄 **升级 ling-shu-agent-designer** (v1.3.0 → v1.4.0)
  - 集成 Self-Improving 系统（记录纠正、积累模式、自我反思）
  - 完整 v4.3 设计方法论（含 Step 5 自动发布功能）
  - 新增常见错误 #5：未经确认直接发布到 GitHub / ClawHub
  
- 📝 **更新文档**
  - README.md 添加详细功能说明和使用示例
  - SKILL.md 更新版本号和作者信息
  - _meta.json 更新版本号至 v1.4.0

### v1.3.0 (2026-06-06)
- 自动发布能力融入主技能，支持一键推送到 GitHub & ClawHub
- 发布前必须 diff 预览确认

### v1.2.0 (2026-06-06)
- 新增 skill-publisher 技能（已合并入主技能）

### v1.1.0 (2026-06-06)
- 新增 enterprise-agent-planner 技能

### v1.0.0 (2026-05-29)
- 初始版本，ling-shu-agent-designer 基础功能

---

## 快速开始

### 安装
```bash
openclaw skills install lingshu-agent-architect
```

### 使用
```
# 方式1：设计新 Agent
用户：帮我设计一个面向制造业的 Agent
灵枢：启动需求沟通 → 产出 7 项大纲 → 创建基础版

# 方式2：企业规划（新增！）
用户：这是某企业的介绍：[企业信息]
灵枢：调用 enterprise-agent-planner → 输出完整规划方案

# 方式3：发布更新
用户：发布到 clawhub
灵枢：diff 预览 → 确认 → 推送 GitHub → 发布 ClawHub
```

---

## 文件结构

```
ling-shu-skills/
├── SKILL.md                          # 技能包索引
├── README.md                         # 本文件
├── _meta.json                        # 元数据（版本号等）
├── enterprise-agent-planner/
│   └── SKILL.md                      # 企业 Agent 规划器 (v1.0.0)
└── ling-shu-agent-designer/
    └── SKILL.md                      # 灵枢设计师主技能 (v1.4.0, 含 v4.3 方法论)
```

---

## License

MIT-0

## 作者

**perrykono-debug**  
🌐 ClawHub: https://clawhub.ai/perrykono-debug/lingshu-agent-architect
