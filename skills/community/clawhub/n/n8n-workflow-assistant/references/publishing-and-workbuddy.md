# 验证、发布和WorkBuddy分发

## 工作流发布

离线检查通过后，在用户已授权的目标环境导入、重新绑定凭据/子流程/表/模型，保存并重导出回读。测试真实表达式、分支、分页与副作用；达标后再发布。没有环境访问就交付候选与明确待验证项。

交付包含基线、实际JSON、变更和SHA-256、需重绑项、测试摘要和回滚方式。不要复制原始密钥或生产运行日志到公开包。工作流ID、Webhook路径冲突和重复调度需在导入前处理。

## 本技能分发

完整源码在skill/n8n-workflow-assistant。发布维护者运行tools/test_release.py，再运行tools/build_release.py；这两个工具仅存在完整GitHub源码，导入包运行scripts/smoke_test.py。

WorkBuddy专用ZIP根目录直接放SKILL.md，资源只能是目录/文件；文件路径不超过2段。目录内不再嵌套。专用frontmatter包含name、version、display_name、display_name_en、description、description_zh、description_en、author，支持中英文使用示例。

发布物包含核心功能需要的全部脚本、模板和本地引用，不把另一套技能或开发机安装目录当内置资源。打包器检查实际ZIP目录深度、本地Markdown链接、元数据、版本和CRC；不自动安装任何其他技能。

此规范结合官方结构说明和实际上传器反馈；平台可能继续调整规则。离线结构、资源检查与解压运行均通过，也不能声称WorkBuddy审核通过。审批状态必须由目标平台真实结果确认。
