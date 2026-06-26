---
name: lzcreate
description: "支持从 AWS、阿里云、GCP、华为云、Azure 向腾讯云迁移的 Landing Zone 全流程客户端。通过远程 MCP Server 自动完成：扫描源云资源(5朵云13种资源)、AI智能填充调研问卷、生成设计文档、生成Terraform代码。当用户提到云迁移、Landing Zone、Terraform、扫描AWS/阿里云/GCP资源、调研问卷、lzcreate时使用。"
---

# LZ Create — 多云迁移到腾讯云 Landing Zone 客户端

支持从 **AWS、阿里云、GCP、华为云、Azure** 向腾讯云迁移的全流程自动化工具。
自动扫描源云 13 种资源（VPC/CVM/RDS/Redis/TKE/CLB/COS 等），AI 生成设计文档和 Terraform 代码。

## MCP Server 地址

```
默认: http://159.75.221.23/mcp
```

如用户指定了其他 MCP 地址，使用用户指定的地址。

## 前置准备

执行任何操作前，先运行连接脚本确认 MCP Server 可用：

```bash
python3 {SKILL_DIR}/scripts/mcp_client.py connect --url http://159.75.221.23/mcp
```

## 核心工作流

### 流程 A：只给凭据，全自动完成（推荐）

用户只需提供源云 AK/SK，无需手动填写任何 Excel。程序自动：生成问卷 → 注入凭据 → 扫描资源 → AI 最佳实践填充全部 26 道题 → 输出已填好的 Excel。

```bash
# 一步到位：传入凭据，自动完成一切
python3 {SKILL_DIR}/scripts/mcp_client.py complete-form \
  --ak "ASIA..." --sk "AvTR..." --token "IQoJ..." \
  --cloud AWS --region ap-southeast-3 \
  --account-name myxl-shared \
  --model qwen3.5:397b-cloud \
  --output ./FILLED_survey.xlsx
```

用户也可以传入已填好凭据的 Excel（不传 --ak/--sk 时）：

```bash
python3 {SKILL_DIR}/scripts/mcp_client.py complete-form \
  --excel ./survey_with_creds.xlsx \
  --output ./FILLED_survey.xlsx
```

### 流程 B：标准全流程（分步执行）

适合需要精细控制每个步骤的场景。先用 complete-form 智能填充，它会自动将填好的版本覆盖回 session 中的原始问卷，后续步骤直接用同一个 session_id 即可。

```bash
# 1. 智能填充问卷（凭据→扫描→AI 填好→覆盖回 session）
python3 {SKILL_DIR}/scripts/mcp_client.py complete-form \
  --ak "..." --sk "..." --token "..." \
  --cloud AWS --region ap-southeast-3 \
  --output ./FILLED_survey.xlsx
# 记下输出的 Session ID，后续步骤复用

# 2. 生成设计文档（直接复用 session，自动读取已填好的问卷 + 扫描结果）
python3 {SKILL_DIR}/scripts/mcp_client.py design-doc \
  --session <session_id> \
  --model qwen3.5:397b-cloud \
  --output ./

# 3. 生成 Terraform 代码（同一 session，设计文档已就绪）
python3 {SKILL_DIR}/scripts/mcp_client.py terraform \
  --session <session_id> \
  --env nonprod \
  --model qwen3.5:397b-cloud \
  --output ./terraform/
```

### 流程 C：从已有 Session 继续

如果之前已执行过扫描/设计文档，可通过 session_id 继续后续步骤，无需重新扫描。

```bash
python3 {SKILL_DIR}/scripts/mcp_client.py terraform \
  --session <之前的 session_id> \
  --env prod \
  --model qwen3.5:397b-cloud
```

## 命令参考

| 命令 | 功能 | 耗时 |
|------|------|------|
| `connect` | 测试 MCP 连接 | <1s |
| `generate-survey` | 生成空白问卷 | <2s |
| `complete-form` | 一键智能填充 | 1-2min |
| `scan` | 扫描源云资源 | 30-120s |
| `query-specs` | 查询腾讯云规格 | 10-30s |
| `design-doc` | AI 生成设计文档 | 5-15min |
| `terraform` | AI 生成 Terraform | 10-30min |
| `list-files` | 列出工作区文件 | <1s |
| `download` | 下载工作区文件 | <1s |

## AI 模型

| 模型 | 推荐场景 |
|------|----------|
| `qwen3.5:397b-cloud` | **生产推荐** |
| `minimax-m2.7:cloud` | 快速测试 |
| `qwen3-coder-next:cloud` | Terraform 代码 |

## 错误处理

- `Session not found` → 重新执行，会自动创建新 Session
- `凭据读取失败` → 检查 Excel 凭据清单 Sheet 的 AK/SK 是否正确
- `STS Token 过期` → 重新获取临时凭据
- `扫描 0 资源` → 检查 Region 是否正确、凭据是否有只读权限
- `AI 调用失败` → 换模型或稍后重试

## 详细参考

关于每个 MCP Tool 的完整参数和返回值，参见 `{SKILL_DIR}/references/mcp_api.md`。
