# JY_Knowledge_Skill 辅助文档

本目录包含 SKILL.md 的辅助参考文档。SKILL.md 是技能的主入口，模型应优先阅读；当 SKILL.md 无法解决当前问题时，再查阅本目录中的详细文档。

## 文档索引

| 文件 | 用途 | 何时查阅 |
|------|------|----------|
| `cold_start.md` | 冷启动完整指南（Python/依赖/Docker/MongoDB/EasyDataset 逐项部署） | 全新服务器、环境缺失、首次部署 |
| `skill_architecture.md` | 系统架构、7阶段管线详解、文件结构、配置结构、服务拓扑 | 理解整体设计、排查复杂问题 |
| `easydataset_deploy.md` | EasyDataset + MongoDB Docker 部署指南 | 服务连接失败、Docker 部署问题 |
| `easydataset_api.md` | EasyDataset 全部 130+ 个 API 端点文档 | 需要调用非标准 API、调试 API 参数 |
| `troubleshooting.md` | 常见问题排查（Python依赖/Docker/MongoDB/LLM/配置） | 任何报错、连接失败、未知异常 |

## 工具脚本 (tools/)

| 脚本 | 用途 |
|------|------|
| `tools/check_env.py` | 一键环境检测：Python版本 + 9个依赖 + 配置文件 + Docker + 服务状态 |
| `tools/diagnose.py` | 深度诊断：MongoDB连接、EasyDataset API、配置文件、最近日志 |
