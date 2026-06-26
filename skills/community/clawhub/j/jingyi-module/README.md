# jingyi-module skill

An OpenClaw skill for 精易模块 retrieval and 易语言 code generation from official docs.

## 精易模块 OpenClaw 技能

`jingyi-module` 是一个面向 **精易模块 / 易语言** 的 OpenClaw 技能包，专门用于解决“模型知道需求，但不知道该用哪个精易模块命令”这个问题。

它的工作方式不是靠模型硬记命令，而是先检索精易模块命令索引，再抓取对应的官方说明，最后基于真实命令签名生成 **可直接复制运行** 的易语言代码。

这个技能适合这些场景：

- 构建“精易模块问答助手”
- 构建“易语言代码生成助手”
- 训练或增强“易语言大模型”
- 给 RAG / Agent / Skills 系统提供精易模块能力

### 核心能力

- 检索精易模块命令名称、路径与摘要
- 按命令名或命令 id 抓取官方说明
- 对官方空响应命令进行补录兜底
- 生成以 `.版本 2` 开头的可复制易语言代码
- 尽量避免模型编造命令、参数和返回值

### 为什么需要它

精易模块命令很多，直接依赖模型记忆很容易出现：

- 命令名写错
- 参数顺序写错
- 返回值类型搞错
- 把不存在的命令当成精易模块命令

`jingyi-module` 通过“**先检索，再生成**”的方式，把模型回答建立在真实文档之上，让生成结果更稳、更像真正能运行的易语言代码。

### 适合谁

- 想做易语言 AI 助手的开发者
- 想把精易模块接入大模型系统的人
- 想做技能市场、知识库、问答系统的人
- 想让 AI 更准确使用精易模块的易语言用户

## Features

- built-in compact command index (`6856` entries)
- official doc fetch by command id or name
- built-in supplements for the 3 known official empty-response commands
- retrieval-first design for better code generation quality

## Files

- `SKILL.md`: skill instructions
- `manifest.yaml`: package metadata
- `data/command_index.jsonl`: retrieval index
- `scripts/search_jingyi.py`: search commands
- `scripts/fetch_jingyi_doc.py`: fetch docs
- `scripts/build_command_index.py`: rebuild index
- `GITHUB_INTRO.zh-CN.md`: GitHub 中文封面介绍
- `PROMPT.zh-CN.md`: 给大模型调用的标准 prompt
- `PUBLISH.zh-CN.md`: ClawHub 上架说明

## Local build

```powershell
python .\scripts\build_command_index.py
```

## Local test

```powershell
python .\scripts\fetch_jingyi_doc.py --name "文本_取随机汉字"
```

Note:

- On some Windows PowerShell consoles, direct Chinese argv input may be affected by local code page settings.
- The index and scripts are stored as UTF-8.

## Publish

See:

- `PUBLISH.zh-CN.md`
- `GITHUB_INTRO.zh-CN.md`
- `PROMPT.zh-CN.md`

## Install

Typical commands:

```powershell
clawhub install jingyi-module
```

or:

```powershell
openclaw skills install jingyi-module
```
