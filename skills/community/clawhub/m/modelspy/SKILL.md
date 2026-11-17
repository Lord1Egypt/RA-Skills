---
name: modelspy
slug: modelspy
displayName: 模型换壳检测 ModelSpy
version: 0.1.0
summary: 对任意 OpenAI 兼容接口做行为取证，识别背后真正在跑的模型，检测中转站/套壳站是否换壳
license: MIT
description: '模型换壳检测 Skill。用户怀疑中转站/API 代理/"Plus 代充"前端宣称的模型是假的、想验证某个 OpenAI 兼容端点背后真正跑的是什么模型、或要求检测"换壳""路由掺假""模型身份鉴定"时使用。不依赖对方声明，从分词器指纹、陷阱题库、生成速度、工具调用完整性等多维行为证据推断真实模型并输出候选排名与置信度。'
disable-model-invocation: false
user-invocable: true
compatibility: '需要网络访问 GitHub Releases 下载单文件 CLI（Windows/Linux/macOS 均有，零依赖）；需要目标端点的 base URL 与 API key'
---

# 模型换壳检测 ModelSpy

对任意 OpenAI 兼容接口做**行为取证**：不问它"你是什么模型"，直接从多维行为证据推断背后真正在跑的模型家族与档位，输出候选排名 + 置信度。

## 何时使用

- 用户说"这个中转站是不是假的 / 有没有换壳 / 宣称 GPT-4o 实际是不是 mini"
- 需要验证 API 代理、"代充"前端、低价渠道的模型真实性
- 需要定期监控某个端点是否偷偷降级路由

## 工具获取

从 GitHub Releases 下载对应平台的单文件可执行程序（零依赖）：

- 仓库：`https://github.com/3378925604-a11y/modelspy`（Releases 页有 windows-amd64 / linux-amd64 / linux-arm64 / darwin-amd64 / darwin-arm64）
- 国内网络可用镜像前缀下载，例如：`https://gh-proxy.com/https://github.com/3378925604-a11y/modelspy/releases/download/v0.1.0/modelspy-windows-amd64.exe`

## 执行流程

1. 向用户要三样东西：端点 base URL（如 `https://xxx/v1`）、要测的模型名、API key（或确认环境变量 `OPENAI_API_KEY` 已设）。若对方"宣称"的模型名与被测名不同，用 `-expect` 传入宣称值。
2. 运行检测：

   ```bash
   modelspy-windows-amd64.exe -base https://你的中转域名/v1 -model gpt-4o -key sk-xxx
   ```

   常用参数：
   - `-expect <模型名>` 对方宣称的模型（用于一致性判定）
   - `-probes identity,tokenizer` 只跑指定探针（identity/tokenizer/capability/speed/cutoff/toolcall）
   - `-json` 机器可读输出；`-html` 导出可视化报告

3. 解读输出：
   - **候选排名**：各模型家族得分条 + 置信度
   - **结论行**：`一致` / `不一致(疑似换壳)` / `证据不足`
   - **退出码**：`0`=一致，`1`=不一致，`3`=证据不足——可直接接脚本做自动化监控

## 结果判定注意

- 置信度 < 50% 或多候选接近时，如实告知用户"证据不足"，建议多跑几轮（探针含随机措辞，多轮结果更稳）
- 同家族档位（如 4o vs 4.1）分词器相同，主要看陷阱题库与速度维度
- 中转可能"只对疑似测试的请求走真模型"，单次通过不代表长期可信，建议定期抽测
- 本工具只使用公开 API 行为，不抓包、不逆向、不产生合规风险

## 局限声明（转述给用户）

v0.1 指纹库为社区种子数据，未经大规模校准；结论是概率性的，不是黑白判定。
