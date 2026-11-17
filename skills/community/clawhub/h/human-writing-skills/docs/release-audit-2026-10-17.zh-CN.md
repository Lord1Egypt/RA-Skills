# 2026-10-17 发布检查

本次检查覆盖 DSH 市场条目、安装包、官方 Cordis/MCP 集成、Python 核心、
审核任务队列、可选 HTTP 接口和 GitHub 发布流程。

## 已修复

| 问题 | 修复 |
| --- | --- |
| MCP 提示词 arguments 为 null 时服务退出 | 校验参数并返回协议错误，后续请求继续工作 |
| 通知产生多余响应、批量请求不被支持 | 按声明的 MCP 2025-03-26 协议处理 |
| 覆盖检查读取包外报告，空必审任务可通过 | 统一目录边界和任务计划校验 |
| 多个审核进程可同时领取同一任务 | 操作系统文件锁与原子写入 |
| 领取结果只有路径、报告摘要与落盘内容不同 | 返回完整提示词，摘要按实际保存字节计算 |
| HTTP 不检查 Origin、长度缺少上限 | 拒绝浏览器来源、限制 1 MiB、校验请求类型和长度 |
| SkillHub 漏带许可证、残留失效的 DSH 清单 | 保留 LICENSE，排除 Node 清单 |
| DSH Release 可触发核心渠道发布 | 区分标签并校验核心版本，保留已有资产 |
| wheel 测试受当前源码目录影响 | 在 checkout 外隔离验证；tgz 解包后执行实际运行时 |

## 使用条件和未完成的质量验证

- DSH 安装前，本机须有 Python 3.9+；默认通过 PATH 的 `python` 启动，也可配置
  `pythonCommand`。Node/DSH 版本范围见插件 README；正式集成验证使用官方 0.2.1-alpha.2。
- 发布到 GitHub 与市场收录是独立步骤；市场 PR 合并及网站刷新由市场维护方控制。
- GitHub Actions 自带 token 创建的 Release 不会自动触发其他 release 工作流。
  ClawHub/SkillHub 需手动运行对应发布工作流；PyPI 需要 Trusted Publishing 配置。
  本次 GitHub Release 成功不代表上述渠道已经发布。
- 工具主要提供提示词、确定性检查和审核编排；实际文字由 DSH 配置的模型生成。
  lint 分数、覆盖回执和字面事实检查不能证明自然度、原创性或语义完整性。
- 多语言自然度仍需独立母语读者盲评。已有盲评工具，但当前没有足够证据宣称所有语言
  或所有模型均获得稳定提升；不承诺绕过 AI 检测器。

协议依据：[MCP 2025-03-26 Transports](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)。
