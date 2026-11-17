# JEP Guard 3.0.0 候选安装与上传包

## 上传 ClawHub
解压后，在原技能的新版本页面选择 jep-guard 文件夹。该文件夹直接包含 SKILL.md、package.json、src 和 dist。Slug 保持 jep-guard，Version 填 3.0.0。不要选择 ZIP 外层下载目录。

本包已排除 ClawHub 自动生成的 skill-card.md。请保留 SKILL.md。

## 安装与验证
本包包含已编译的 dist 和固定依赖版本的 package-lock.json，不包含 node_modules 或任何可用凭据。在包目录执行 npm ci --ignore-scripts 后，node dist/cli/index.js --help 可查看命令。也可执行 npm run build 重新构建。

先阅读 README.md，按说明配置公钥、身份和策略。服务不会随安装自动运行。该候选仅支持显式调用它的运行时接入点，不是通用操作系统沙箱。

构建、CLI 帮助与 SDK 导入检查通过；本轮测试为 10 项通过，5 项真实 Unix socket 测试因当前执行环境 listen EPERM 无法执行。请在支持 Unix socket 的 Linux/macOS 运行 RUN_IPC_TESTS=1 npm test -- --runInBand，并验证目标 OpenClaw 宿主接入。尚无这些运行验证通过记录。

此文件包不是平台审查通过证明；上传后仍需复审。3.0.0 是具有不兼容安全变更的候选版本，不应直接替换未经迁移的生产配置。
