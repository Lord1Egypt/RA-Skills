---
name: terraform-module-library
description: Terraform 模块开发：编写、测试、发布可复用的 IaC 模块
source:
  type: derived
  repo: skills-repo/infrastructure-engineer
  path: skills/terraform-module-library/SKILL.md
  url: https://skills.sh/wshobson/agents/terraform-module-library
  version: 1.0.0
  updated: 2026-07-31
metadata:
  author: hope
  category: 云基础设施
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-31
tags:
  - terraform
  - iac
  - module
  - infrastructure
  - hcl
---

# Terraform Module Library — 模块开发

> 编写、测试和发布可复用的 Terraform 模块，覆盖模块结构设计、版本管理、测试策略和文档生成。

## 能力

- **模块结构**：标准化模块目录结构（main.tf, variables.tf, outputs.tf），命名规范和依赖管理
- **变量设计**：输入变量的类型约束、默认值、验证规则和敏感标记
- **测试策略**：使用 Terratest 或 terraform test 编写模块测试，覆盖创建、更新、销毁全流程
- **版本发布**：语义化版本管理，Git tag 触发 CI/CD 自动发布到 Terraform Registry
- **文档生成**：terraform-docs 自动生成模块的 README 和变量说明

## 使用方式

在 Claude Code 中使用 `/terraform-module-library` 调用。

```
/terraform-module-library 为 AWS VPC 创建一个可复用的 Terraform 模块
/terraform-module-library 审查这个模块的变量设计是否合理
/terraform-module-library 为这个模块编写 Terratest 测试
```

## 工作流

1. **需求分析** — 明确模块的输入、输出和依赖资源
2. **结构搭建** — 创建标准模块目录，编写 main.tf、variables.tf、outputs.tf
3. **实现逻辑** — 编写资源定义，处理条件创建和资源依赖
4. **测试验证** — 编写测试用例，在隔离环境中验证模块行为
5. **发布上线** — 生成文档，打 tag，发布到 Registry

## 适用场景

- 团队需要在多个项目中复用云基础设施模式
- 标准化公司内部的云资源创建规范
- 开源贡献者向 Terraform Registry 发布模块
- 独立开发者管理多个环境的云资源

## 限制

- 仅支持 Terraform/HCL，不适用于 Pulumi、CDK 等其他 IaC 工具
- 模块测试需要真实的云资源或 Mock 环境
- 复杂模块的依赖关系需要额外设计
- Provider 版本兼容性需要手动管理

## 相关参考（Playbook）

模块设计准则、接口/版本/测试策略 → [references/iac-module-design.md](../../references/iac-module-design.md)；
模块上线前的变更安全审查 → [references/terraform-change-safety.md](../../references/terraform-change-safety.md)。