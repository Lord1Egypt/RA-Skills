---
name: interaction-record-archive
description: 采集 Hook payload 中的用户输入与助手回复，连同会话元数据以 JSON 发送至允许的内部端点。用于授权环境归档；支持 SYNC_ENABLE=0 停用。
license: MIT
version: 2.0.0
---

# 会话归档同步

使用会话生命周期事件同步备份用户输入和模型输出。安装后会自动触发归档；启用前应确认项目数据可按既定合规要求发送到配置的内部端点。

## 使用范围

本技能仅限字节跳动内部授权环境使用，属于内部工具与配置资产。不得向外部主体传播、公开发布、上传至公共代码托管平台或用于非授权环境。

归档内容可能包含代码、业务信息和会话上下文。使用前应确认归档端点、访问权限和数据处理方式符合内部数据安全与合规要求。

## 数据处理与关闭方式

- 触发时机：`UserPromptSubmit` 在用户提交输入时触发，`Stop` 在助手输出完成时触发。
- 上传内容：`session_id`、当前工作目录（`cwd`/`project`）、事件类型、用户输入或助手输出，以及生成时间；助手输出未直接提供时，可能从 `transcript_path` 读取增量 JSONL 记录。
- 传输目的：仅向 `config/endpoint.conf` 中配置且通过内部域名校验的端点发送 JSON 请求。
- 关闭方式：设置环境变量 `SYNC_ENABLE=0` 后，脚本不读取 payload、不写入归档记录且不发起网络请求。
- 本地记录：请求结果会写入 `scripts/.archive.log`；助手输出的增量读取偏移会写入 `scripts/.state/`。

## 事件

- `UserPromptSubmit`：读取 Hook payload 的 `prompt`，归档一条 `role: user` 消息。
- `Stop`：优先读取 Hook payload 的 `last_assistant_message`，无该字段时读取 `text_content`，归档一条 `role: assistant` 消息。

两个事件使用 payload 中相同的 `session_id`。当输出事件未直接提供内容时，脚本可从 `transcript_path` 读取 JSONL 增量记录作为回退。

## 配置

端点仅从 `config/endpoint.conf` 读取，且只允许以下内部域：

- `*.bytedance.com`
- `*.bytedance.net`
- `*.byted.org`

设置 `SYNC_ENABLE=0` 可禁用所有归档。可选的 `SYNC_TOKEN` 将作为 Bearer token 发送，`SYNC_TIMEOUT` 默认为 5 秒。

审计日志写入 `scripts/.archive.log`，输出偏移写入 `scripts/.state/`。

## 安装

```bash
bash scripts/install.sh
```

安装脚本会将 `UserPromptSubmit` 和 `Stop` 注册到项目级 Hook 配置。
