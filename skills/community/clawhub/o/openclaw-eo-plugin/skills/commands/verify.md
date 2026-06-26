---
name: verify
source: eo-native
compatibility: full
description: 验证检查点指令，调度 QA 专家验证项目关键节点的交付物
whenToUse: 当需要验证阶段产出、检查里程碑完成情况时使用
allowedTools: ["Read", "Bash", "Grep"]
context: inline
expert: qa
aliases: ["/verify", "/验证", "/checkpoint", "/qa"]
version: 1.0.1
---

# /verify - 验证检查点指令

> **v1.0.1 新增**: frontmatter 标准化，包含 allowedTools 和 expert 映射

## 功能
调度 QA 专家，验证项目关键节点的交付物是否符合要求。

## 检查点类型

### milestone1 - 架构设计审批
- [ ] 架构文档完整
- [ ] 技术选型已确定
- [ ] 数据库设计通过评审
- [ ] API 设计文档完成

### milestone2 - 功能开发审批
- [ ] 核心功能代码完成
- [ ] 单元测试覆盖率 ≥ 80%
- [ ] 代码规范检查通过
- [ ] 安全扫描无高危漏洞

### final - 正式发布审批
- [ ] 所有功能测试通过
- [ ] E2E 测试覆盖核心流程
- [ ] 性能测试达标
- [ ] 安全评估通过

## 输出格式

```markdown
# ✅ 验证报告 - [检查点名称]

## 📋 检查项

| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| 1 | 架构文档完整 | ✅ 通过 | - |
| 2 | 技术选型已确定 | ✅ 通过 | - |
| 3 | 数据库设计通过评审 | ⚠️ 警告 | 建议添加索引 |
| 4 | API 设计文档完成 | ✅ 通过 | - |

## 📊 统计

| 指标 | 值 |
|------|-----|
| 总检查项 | 4 |
| 通过 | 3 |
| 警告 | 1 |
| 失败 | 0 |

## 🎯 结论

**状态**: ✅ **检查通过（带警告）**

可以进入下一阶段。建议在下次迭代中处理警告项。
```

## 对应专家
- QA Engineer
- Security Reviewer
- Code Reviewer
