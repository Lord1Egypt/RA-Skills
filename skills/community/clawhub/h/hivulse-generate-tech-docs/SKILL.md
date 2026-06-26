---
name: hivulseAI
description: hivulse蜂巢 AI 是一款面向软件开发的自动化技术文档生成工具，通过指定目录代码一键生成多种规范化技术文档。目前已支持的文档类型包括：用户需求说明书、需求规格说明书、系统概要设计说明、系统详细设计说明等10几种报告。申请API Key请访问 www.hivulse.com

metadata:
  openclaw:
    emoji: "📄"
    requires:
      env: ["HIVULSE_API_KEY"]
    primaryEnv: "HIVULSE_API_KEY"
user-invocable: true
---

# hivulseAI - 自动化技术文档生成工具

通过API接口将指定目录的文件上传并生成各种技术文档的完整自动化工具。

## 🚀 快速开始

### 环境变量设置
```bash
export HIVULSE_API_KEY="your-api-key-here"
```

## 📋 支持的文档类型

| 编号 | 文档类型 | 描述 |
|------|----------|------|
| 19 | 用户需求说明书 | 用户需求分析文档 |
| 2 | 需求规格说明书 | 详细需求规格 |
| 4 | 系统概要设计说明 | 系统架构设计 |
| 5 | 系统详细设计说明 | 详细设计文档 |
| 8 | 软件单元测试计划 | 单元测试计划 |
| 9 | 软件单元测试用例 | 单元测试用例 |
| 10 | 软件单元测试报告 | 单元测试报告 |
| 1 | 系统测试计划 | 系统测试计划 |
| 12 | 系统测试用例 | 系统测试用例 |
| 15 | 系统测试报告 | 系统测试报告 |
| 13 | 网络安全漏洞自评报告 | 安全评估报告 |
| 20 | 软件用户测试用例 | 用户测试用例 |
| 21 | 软件用户测试报告 | 用户测试报告 |


## 🎯 触发关键词

在OpenClaw会话中，当用户提到以下关键词时会自动触发此技能：
- "生成技术文档"
- "创建文档"
- "文档生成"
- "hivulseAI"
- "上传代码生成文档"
- "需求规格说明书"
- "系统设计文档"

## 🔧 OpenClaw技能调用方式

### 方式1：直接触发
在对话中直接使用触发关键词，例如：
- "帮我生成技术文档"
- "使用hivulseAI生成需求规格说明书"
- "为这个项目创建系统设计文档"

## 执行方式
### 通过Python脚本执行
`python3 hivulseAI.py <目录路径> <文档类型编号> [--task-name "任务名称"]`


## 📋 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| 项目路径 | 要生成文档的代码项目目录 | `/Users/project/myapp` |
| 文档类型 | 文档类型编号（2-21） | `2`（需求规格说明书） |
| 任务名称 | 可选，文档任务名称 | `"项目需求分析"` |

## 🌐 API配置
- **API密钥**：通过配置文件设置，无需环境变量

### 配置文件位置：
`~/.hivulseai/config.json`

### 手动编辑配置：
```json
{
  "api_key": "your-api-key-here",
  "last_used_directory": ""
}
```

## 📁 文件过滤规则

系统会自动过滤以下目录和文件：
- `node_modules` - Node.js依赖目录
- `venv` - Python虚拟环境
- `.git` - Git版本控制
- `__pycache__` - Python缓存
- `.idea` - IDE配置
- `.vscode` - VS Code配置
- `*.pyc` - Python编译文件
- `*.log` - 日志文件

## 🔄 API调用流程

### 1. 文件上传阶段
```bash
POST /api/v1/claw/upload/file/
- 第一个文件：不带branch_id
- 后续文件：带branch_id（从第一个文件响应中获取default_branch_id）
```

### 2. 状态检查阶段
```bash
POST /api/v1/claw/upload/status/
- 参数：uuid（使用default_branch_id）
```

### 3. 文档生成阶段
```bash
POST /api/v1/claw/template_wiki/
- 参数：task_name, template_base_id, branch_id, repo_id, is_advanced
```

## ⚠️ 注意事项

1. **API密钥安全**：确保`HIVULSE_API_KEY`环境变量正确设置
2. **网络连接**：确保可以访问指定的API地址
3. **文件权限**：确保对目标目录有读取权限
4. **文件大小**：注意单个文件大小限制
5. **备份重要文件**：建议先备份重要代码

## 🛠️ 故障排除

### 常见错误
- "API密钥未设置" → 检查`HIVULSE_API_KEY`环境变量
- "目录不存在" → 检查路径是否正确
- "上传失败" → 检查网络连接和API服务状态
- "文档类型不支持" → 检查文档类型编号

## 📞 支持

如有问题，请检查：
1. API服务是否正常运行
2. 环境变量是否正确设置
3. 网络连接是否正常
4. 文件路径和权限是否正确
