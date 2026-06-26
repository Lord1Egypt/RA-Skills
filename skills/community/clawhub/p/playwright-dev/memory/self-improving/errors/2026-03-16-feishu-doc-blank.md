{
  "timestamp": "2026-03-16T17:36:11+08:00",
  "type": "error",
  "category": "feishu-doc",
  "title": "违反飞书文档创建规范 - 创建空白文档",
  "description": "创建文档 TFA0dI51Ionk6Oxk65Ccvemsn7g 时，没有使用 feishu-doc-block-writer 技能，导致空白文档（只有 2 个 Blocks）。违反了 AGENTS.md 中最高优先级的飞书文档创建规范。",
  "root_cause": "回复前没有检查 AGENTS.md 中的规范，制定规范后自己违反",
  "impact": "空白文档，Thomas 发现后需要指出，损害信任，展示不专业",
  "lesson": "必须严格遵守自己制定的规范，回复前必须检查 AGENTS.md，创建后必须验证 Blocks 数量",
  "action": "100% 使用 feishu-doc-block-writer 技能，每次回复前检查 AGENTS.md，创建后验证 Blocks > 2 个，Chrome 预览确认",
  "severity": "高",
  "permanent": true,
  "related_docs": ["TFA0dI51Ionk6Oxk65Ccvemsn7g", "OVO2dDz4AogEFtxaSlBccHeTn2f"],
  "violated_rules": ["飞书文档创建规范", "回复前强制检查"]
}
