# IDC Enterprise Agent COMPASS

基于IDC COMPASS模型的七步闭环诊断框架，帮助企业从真实业务流的效率约束出发，识别Agent落地的优先切入维度，并结合IDC MarketGlance供应商分类体系，匹配适合的技术合作伙伴方向。

## COMPASS 七维度

| 维度 | 英文 | 所属层级 | 核心问题 |
|------|------|---------|---------|
| **P** 感知与理解 | Perception | 信息输入 | 外部输入能否高效转化为结构化数据？ |
| **A** 分析与决策 | Analysis | 信息处理 | 多源数据能否快速汇聚形成决策建议？ |
| **O** 流程编排 | Orchestration | 信息处理 | 任务能否在多系统间自动衔接和动态路由？ |
| **M** 监控与响应 | Monitoring | 信息处理 | 异常能否被及时发现并自动触发响应？ |
| **C** 协调沟通 | Collaboration | 信息处理 | 跨部门信息对齐和状态同步是否高效？ |
| **S** 知识沉淀 | Sedimentation | 信息资产化 | 个人经验能否固化为组织级数字资产？ |
| **S** 规模弹性 | Scalability | 信息资产化 | 执行能力能否跨越人力编制的物理限制？ |

## 七步诊断流程

1. **理解企业当前状态** — 收集行业、痛点、系统基础等必要信息
2. **快速三问筛查** — 用三个问题将七个维度收敛到2-3个主矛盾
3. **定位约束层级** — 判断瓶颈落在信息输入、信息处理还是信息资产化层
4. **细化具体维度** — 锁定2-3个优先维度，用业务证据验证
5. **系统就绪度体检** — 评估接口能力、权限模型、操作留痕、数据语义
6. **匹配供应商方向** — 基于MarketGlance三大供应商类型推荐组合方案
7. **输出建议** — 诊断结果、切入场景、供应商方向、落地路径、人机协同边界

## 文件结构

```
idc-enterprise-agent-compass/
├── SKILL.md                              # 核心指令文件（七步流程骨架 + 红线规则）
├── LICENSE                               # MIT-0 分发许可
├── CHANGELOG.md                          # 版本变更记录
├── references/
│   ├── IDCcopyright.md                  # 版权与 CC-BY-SA-4.0 许可声明
│   ├── compass-dimensions.md             # 七维度详细定义与判断信号
│   ├── supplier-mapping.md               # MarketGlance供应商映射与组合模式
│   ├── system-readiness.md               # 系统就绪度四维评估框架
│   ├── human-agent-boundary.md           # 人机协同边界完整清单
│   ├── example-diagnosis.md              # 制造企业订单处理完整诊断示例
│   ├── vendor-industry.md                # 行业智能体厂商目录
│   ├── vendor-enterprise.md              # 企业级智能体厂商目录
│   └── vendor-platform.md                # 智能体开发平台厂商目录
└── README.md                             # 本文件
```

## 适用场景

- 企业想落地Agent，需要确定切入方向
- 业务流程存在跨系统、跨角色的效率瓶颈
- 需要从COMPASS维度优先级出发进行Agent规划
- 需要Agent供应商选型的方向性指引

## 不适用场景

- 单点自动化、规则化重复任务（用代码、工作流、RPA/BPM）
- 个体创意需求（用通用Agent助手）
- 简单FAQ问答（用标准问答机器人）
- IT基础设施问题（算力、网络、存储）

## 安装

### Claude Code

将 `idc-enterprise-agent-compass/` 目录放入项目的 `skills/` 文件夹即可自动发现：

```
my-project/
└── skills/
    └── idc-enterprise-agent-compass/
        ├── SKILL.md
        └── references/
```

### OpenClaw / ClawHub

```bash
# 通过 ClawHub 安装
clawhub install idc-enterprise-agent-compass

# 或手动放置到技能目录
```

### Claude.ai

将整个 `idc-enterprise-agent-compass/` 目录打包为 ZIP 文件上传。

## 使用方式

当用户提出以下类型的问题时，此技能会被自动触发：

- "我们企业想落地Agent，应该从哪里开始？"
- "帮我分析一下我们的业务流程，Agent能在哪些环节切入？"
- "COMPASS七个维度里，我们当前最该关注哪几个？"
- "有哪些类型的供应商适合我们当前的需求？"
- "我们目前最大的痛点是跨系统数据搬运，应该找什么类型的厂商？"

## 许可证

本 Skill 分发许可为 **MIT-0**（满足平台分发要求）。

IDC COMPASS 诊断模型、MarketGlance 供应商分类体系、厂商目录数据等核心方法论和数据资产受 **© 2026 IDC. All Rights Reserved.** 保护，并采用 **CC-BY-SA-4.0** 许可——使用时须署名 IDC，衍生作品须以相同方式共享。

详细版权声明请参阅 `references/IDCcopyright.md`。
