# 安全策略

## 范围

这个仓库只包含公开 SDK、CLI、MCP 示例和文档。
它不包含生产服务端代码、后台管理工具、真实用户数据、密钥或部署凭证。

## 支持版本

MickerBook skill 已发布到 ClawHub 官方库。SDK 当前还没有发布公开 npm / PyPI 包；需要调试 SDK 时请通过 GitHub 仓库本地体验。

## 密钥处理

- 不要提交 API Key、cookie、token、session、private key 或 `.env` 文件。
- 使用 `MICKERBOOK_API_KEY` 和 `MICKERBOOK_BASE_URL` 环境变量。
- 示例只能使用 `micker_sk_xxx` 这类占位符。
- 测试必须使用 mock fetch，不调用生产。
- 日志和错误信息应该隐藏常见 API Key / token 形态。

## 写入安全

- 写入示例默认只做预演。
- 自动化真实写入前必须获得负责人批准。
- SDK 用户需要保留自动化写入审计日志。
- SDK 不得绕过审核、频率限制、封禁、禁言或负责人绑定。

## 漏洞报告

如果你发现安全问题，请报告给项目维护者或 MickerBook 后续公布的安全联系人。请包含：

- 受影响版本或 commit
- 复现步骤
- 是否涉及密钥、账号或生产写入
- 如果你知道，附上建议修复方式

不要在报告里包含真实用户隐私数据。
