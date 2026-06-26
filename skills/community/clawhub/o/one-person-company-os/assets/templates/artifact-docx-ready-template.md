# {{ARTIFACT_TITLE}}

## 文档封面信息

- 公司名称: {{COMPANY_NAME}}
- 产品名称: {{PRODUCT_NAME}}
- 当前经营模型: {{STAGE_LABEL}}
- 当前推进面: {{CURRENT_ROUND_NAME}}
- 文档类型: {{ARTIFACT_TYPE}}
- 负责人: {{ARTIFACT_OWNER}}
- 文档成熟度: {{ARTIFACT_STATUS}}
- 文件路径: {{ARTIFACT_FILE_PATH}}

## 0. 文档当前判断

{{ARTIFACT_PROGRESS_SUMMARY}}

## 0.1 当前仍应补齐的关键项

{{ARTIFACT_MISSING_ITEMS}}

## 1. 执行摘要

{{ARTIFACT_SUMMARY}}

## 2. 背景与目标

- 本次目标: {{ARTIFACT_OBJECTIVE}}
- 当前推进状态: {{ROUND_STATUS}}

## 3. 工作范围

### 3.1 本次纳入范围

{{ARTIFACT_SCOPE_IN}}

### 3.2 本次不纳入范围

{{ARTIFACT_SCOPE_OUT}}

## 4. 交付内容

{{ARTIFACT_DELIVERABLES}}

## 5. 实际软件与代码产出

{{ARTIFACT_SOFTWARE_OUTPUTS}}

## 6. 实际非软件产出

{{ARTIFACT_NON_SOFTWARE_OUTPUTS}}

## 7. 证据与验收路径

{{ARTIFACT_EVIDENCE}}

## 8. 部署资料

{{ARTIFACT_DEPLOYMENT_ITEMS}}

## 9. 生产与运行资料

{{ARTIFACT_PRODUCTION_ITEMS}}

## 10. 本次变化

{{ARTIFACT_CHANGES}}

## 11. 关键决策

{{ARTIFACT_DECISIONS}}

## 12. 风险、假设与待确认事项

{{ARTIFACT_RISKS}}

## 13. 后续动作

- {{ARTIFACT_NEXT_ACTION}}

## 14. DOCX 使用要求

- 文件名使用两位序号开头
- 文件名直接使用最终交付名，不再把状态写进文件名
- `产物/` 目录只保留 `.docx` 正式交付文件
- 软件产品必须补齐代码/脚本/配置/接口等至少一类真实产出
- 上线后必须补齐部署、回滚、监控、告警和生产运行资料
