---
name: golang-skills
description: >
  Golang 开发 SKILL 集合。包含日志规范（SKILL-logging.md）和项目代码梳理与 API 流程分析（SKILL-flow-analysis.md）。
  适用于 zhaocaijianghu-skills 项目中所有 Golang 开发场景，包括 MCP 客户端、后端服务、数据处理等。
metadata:
  label: Golang SKILL 集合
---

# Golang SKILL 集合

本文件夹包含**两个标准化的独立 SKILL 文档**，用于指导 Golang 开发实践。

---

## 一、SKILL 导航

| SKILL 文档 | 适用场景 | 核心内容 |
|------------|----------|----------|
| [**SKILL-logging.md**](./SKILL-logging.md) | 添加日志 | xlogging 规范、日志 Level 选择、代码示例、禁止事项 |
| [**SKILL-flow-analysis.md**](./SKILL-flow-analysis.md) | 流程梳理 | API 运行流程、Mermaid 流程图、Golang 代码示例、通用模式 |

---

## 二、快速开始

### 场景 1：需要添加日志
→ 打开 [**SKILL-logging.md**](./SKILL-logging.md)

```go
// 标准错误日志
if err != nil {
    xlogging.D().Error(fmt.Sprintf("operation failed: %+v", err))
    return err
}
```

### 场景 2：需要理解 API 流程
→ 打开 [**SKILL-flow-analysis.md**](./SKILL-flow-analysis.md)

- 查看 Mermaid 流程图
- 参考 Golang 代码实现
- 了解错误处理和并发模式

---

## 三、通用原则

所有 Golang 开发必须遵守以下原则：

| 原则 | 说明 |
|------|------|
| **优先仿写** | 参考项目中现有 Golang 代码 |
| **强制规范** | 无法仿写时，严格遵循对应 SKILL 的规定形式 |
| **配置优先** | 必须先读取 `mcp-config.json` 获取服务地址 |
| **文档为准** | MCP 调用必须参考 `references/tools/*.md` |
| **完整日志** | 所有错误必须记录，禁止静默处理 |

---

## 四、相关资源

| 资源 | 路径 | 说明 |
|------|------|------|
| MCP 工具文档 | `../../supplier-sourcing-assistant/references/tools/` | 所有 MCP 工具接口定义 |
| MCP 配置 | `../../supplier-sourcing-assistant/mcp-config.json` | 服务 URL 配置示例 |
| Python SKILL 参考 | `../../supplier-sourcing-assistant/SKILL.md` | 业务流程参考 |

---

## 五、更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026/04/08 | 优化为标准 SKILL 格式（统一 front matter、规范结构、添加导航） |

---

**提示**：如需在实际 Golang 项目中应用、添加更多示例或修改具体部分，请提供具体场景。
