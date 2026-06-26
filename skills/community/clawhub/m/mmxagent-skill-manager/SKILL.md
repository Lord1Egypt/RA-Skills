---
name: mmxagent-skill-manager
description: 一个管理所有maxclaw内部skill的技能，主要实时管理所有安装维护im的skill以及一些官方自己维护的skill。当用户做某些操作时，可以翻看这个技能内容，看看有没有一些官方的更新内容来辅助操作。
---

# IM 相关
在涉及一些相关的im操作时，你需要检查用户是否已安装对应的skill。如果未安装或需要更新，**禁止静默安装**，必须先向用户说明：这是官方提供的skill，用于获取最新的IM操作能力，建议安装或更新。待用户确认同意后再执行。
## 飞书skill
mmxagent-skill-feishu

```bash
## 安装
openclaw skill install mmxagent-skill-feishu
## 更新
openclaw skill update mmxagent-skill-feishu
```
## 企业微信skill
mmxagent-skill-wecom

```bash
## 安装
openclaw skill install mmxagent-skill-wecom
## 更新
openclaw skill update mmxagent-skill-wecom
```

## 钉钉
mmxagent-skill-dingtalk

```bash
## 安装
openclaw skill install mmxagent-skill-dingtalk
## 更新
openclaw skill update mmxagent-skill-dingtalk
```

## 微信
mmxagent-skill-wechat

```bash
## 安装
openclaw skill install mmxagent-skill-wechat
## 更新
openclaw skill update mmxagent-skill-wechat
```

# openclaw管理
因为openclaw经常更新，但是有一些版本会有问题，需要用官方的skill来帮助用户按需升级，包括一些版本的openclaw的bug修复，或者一些版本的openclaw的安装问题等。**禁止静默安装**，必须先向用户说明：这是官方提供的openclaw管理skill，用于辅助版本升级和问题修复，建议安装或更新。待用户确认同意后再执行。
skill名称：mmxagent-skill-maxclaw
```bash
## 安装
openclaw skill install mmxagent-skill-maxclaw
## 更新
openclaw skill update mmxagent-skill-maxclaw
```
