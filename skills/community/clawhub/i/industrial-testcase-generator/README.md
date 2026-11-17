# 工业测试用例生成器（Industrial Test Case Generator）

面向**工业自动化监控系统（PLC/SCADA/HMI 应用层）**领域的 Agent Skill：从需求文档/描述输出**标准化、可追溯、可直接导入用例管理平台**的 Excel 测试用例。

## 特性

- **五阶段工作流**：输入判断 → 模块识别分层 → 需求提取分类 → 测试设计 → Excel 输出 → 交付检查
- **15 列标准用例结构** + 双 sheet（`用例` + `覆盖统计` RTM），优先级着色、冻结首行
- **四层深度硬约束**：主流程 P0 / 业务分层 P1 / 黑盒方法 ≥3 种 / 探索性 P3，不可跳过
- **标准合规门禁（V1.2.0）**：国标/行标/企标三级体系，**试验项级覆盖率 100% 硬性验收线**（GB/T 17626 系列、GB/T 2423 系列、IEC 61508/62061、IEC 62443、GB/T 30976、GB 5226.1）
- **隐含项兜底**：报警回差、并发风暴、确认/复位权限、记录持久化、越权阻断等需求未明示项自动覆盖或标注 `[隐含项]`
- **测试级别/回归硬性要求**：每模块 ≥2 级别、全 4 级别出现、每模块 ≥1 条回归用例
- **专项设备**：虚拟 PLC、半实物、高低温试验箱、老化机架、Modbus 仿真从站、工业防火墙+渗透机

## 目录结构

```
industrial-testcase-generator/
├── SKILL.md                    # 主技能（frontmatter + 五阶段工作流 + 硬约束门禁）
├── references/
│   ├── domain-knowledge.md     # 工业知识库（架构/协议/标准 + 标准-试验项矩阵）
│   └── format-spec.md          # 固定格式规范（15 列/编号/Excel 输出，生成时必读）
└── examples/
    ├── requirements.md         # 真实案例需求输入（产线高温报警系统）
    └── testcases.xlsx          # 对应输出 Excel（64 条，双 sheet）
```

## 使用方式

1. 将本目录复制到支持 [Agent Skills](https://agentskills.io) 标准的客户端技能目录（Claude Code、Cursor、OpenCode、Gemini CLI 等）
2. 输入需求文档（Markdown/PDF/Word/Excel）或需求描述
3. 技能按五阶段流程生成 `{项目名}_工业测试用例_{YYYYMMDD}.xlsx`

> 生成 Excel 需要 **Python 3 + openpyxl**（见 frontmatter `compatibility`）。

## 输出规格（速览）

- 15 列：用例编号 / 业务域模块 / 优先级 / 测试维度 / 用例类型 / 设计方法 / 测试场景 / 测试点 / 操作步骤 / 测试数据 / 前置条件 / 需求来源 / **协议/点位** / 测试环境 / 测试级别
- 编号规则 `TC-{模块前缀}-NNN`（10 个工业模块前缀，如 ALM/COMM/HMI/SCADA）
- 覆盖统计：需求覆盖率 100% · 模块×维度矩阵 · 试验项级标准覆盖率 · 级别/回归清单

## 示例

`examples/` 内含真实案例：产线高温报警系统需求 → 64 条测试用例 Excel（已通过官方校验脚本 10 项断言）。

## 校验

已通过官方 [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) `validate` 校验（frontmatter/命名/结构合规）。

## License

Apache-2.0。标准名称与编号仅作索引引用，原文版权归各归口单位。
