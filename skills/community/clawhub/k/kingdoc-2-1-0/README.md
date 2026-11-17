# KingDoc — 金山文档 AI 协作助手

> 让 AI 直接操作你的金山在线文档，创建、编辑、管理一站搞定。

## ✨ 特性

- 📝 **6 品类全覆盖** — 文字/表格/演示/多维表格/收集表/附件
- 🔗 **全生命周期** — 创建/编辑/删除/移动/复制/权限/版本历史/回收站
- 🆚 **对标腾讯文档** — 腾讯有的功能我们全有
- 🏆 **金山独有加分** — 回收站/版本历史/格式转换/纯文本提取/通知推送
- 🔒 **安全优先** — 软删除/权限前置/限流退避/审计日志

## 🚀 快速开始

### 1. 安装

```bash
# Linux / macOS
bash D:\skill\kingdoc\setup.sh

# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File D:\skill\kingdoc\setup.ps1
```

### 2. 配置 App Key

从 [金山开放平台](https://developer.kdocs.cn) 获取 AppID + AppSecret，安装脚本会引导您输入。

### 3. 直接使用

对 WorkBuddy 说：
- "帮我写一份会议纪要" → 自动创建金山文档
- "把这个 PDF 传到云端" → 自动上传
- "这份文档改坏了，回退到上周" → 版本回滚

## 📖 支持的文档类型

| 类型 | 创建 | 编辑 |
|------|------|------|
| 文字文档 | ✅ 自动排版 | ✅ 本地生成+上传覆盖 |
| 电子表格 | ✅ 自动创建 | ✅ 单元格/公式/图表精细编辑 |
| 演示文稿 | ✅ 自动排版 | ✅ 本地生成+上传覆盖 |
| 多维表格 | ✅ 自动创建 | ✅ 记录/字段/视图精细编辑 |
| 收集表 | ✅ 自动创建 | ✅ 配置+答卷管理 |
| 附件上传 | ✅ — | — |

## 📚 文档

- [SKILL.md](SKILL.md) — 完整功能参考
- [references/auth.md](references/auth.md) — 鉴权流程
- [references/workflows.md](references/workflows.md) — 常见工作流

## 🔒 安全

- 所有删除走回收站 API，可恢复
- 写入前权限校验
- 限流自动退避重试
- 操作审计日志
- Token 不落盘

## 🤝 贡献

欢迎提交 Issue 和 Pull Request。

## 📄 协议

MIT License — 详见 [LICENSE](LICENSE)
