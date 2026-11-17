---
name: internal-comms-midea
version: 1.1.1
description: "Draft Midea Group internal communications �� weekly/monthly reports, project updates, incident re..."
tags: [planning, general, report-generation, visual, file-based]

# 美的集团内部沟通模�?
本技能帮助撰写符合美的集团文化规范的内部沟通文档。根据文档类型自动分流到对应模板�?
## Dependencies

- 无外部依赖（纯文本模板技能）
- 模板文件位于 `examples/` 目录

## When to use this skill

当用户需要撰写以下类型的内部沟通文档时，使用此技能：

- **3P周报**（Progress进展/Plans计划/Problems问题�? 团队周度汇报
- **项目进展报告** - 项目里程碑汇�?- **事故/异常报告** - 生产事故、质量异常、安全事件的复盘报告
- **跨部门协作邮�?* - 向其他部门请求支持、同步信息、协调资�?- **FAQ回答** - 回答公司内部常见问题
- **通用沟�?* - 其他不符合上述类型的内部沟�?
## How to use this skill

撰写任何内部沟通文档时�?
1. **识别沟通类�?*：从用户请求中判断属于哪种类�?2. **加载对应的模板文�?*：从 `examples/` 目录加载
   - `examples/3p-weekly-report.md` - 3P周报模板
   - `examples/company-newsletter.md` - 公司newsletter模板
   - `examples/project-update.md` - 项目进展报告模板
   - `examples/incident-report.md` - 事故/异常报告模板
   - `examples/cross-dept-email.md` - 跨部门协作邮件模�?   - `examples/faq-answers.md` - FAQ回答模板
   - `examples/general-comms.md` - 通用沟通模�?3. **按照模板的具体指�?*：收集信息、格式化输出

如果沟通类型不匹配任何现有模板，询问用户更多关于期望格式的信息�?
## 语气原则

- **专业务实**：用数据说话，避免空话套�?- **简洁直�?*：结论先行，细节在后
- **避免过度修饰**：不�?高度重视"�?积极推进"等套话，用具体数据和行动替代

## Error Handling

| 错误场景 | 原因 | 解决方案 |
|---------|------|---------|
| 模板文件不存�?| `examples/` 目录缺少对应模板 | 使用 `general-comms.md` 通用模板替代 |
| 沟通类型无法判�?| 用户请求模糊，不属于已知类型 | 询问用户期望的文档格式和受众 |
| 用户提供的信息不�?| 缺少关键数据（如项目名、时间、负责人�?| 列出需要用户补充的信息清单 |
| 模板格式与用户需求不匹配 | 模板过于固定，无法适应用户场景 | 以模板为基础，根据用户要求调整结�?|

### Degradation Strategy

1. **完整模板可用**：按模板生成完整文档
2. **模板缺失**：使用通用沟通模�?(`general-comms.md`) 作为基础
3. **所有模板不可用**：根据美的集团语气原则，直接从零生成文档
4. **信息不足**：生成文档框�?+ 标注需要用户补充的占位�?
## Keywords

3P周报, 项目进展, 事故报告, 跨部门邮�? FAQ, 内部沟�? 周报, 月报, 进展汇报, 异常报告, 协作邮件
