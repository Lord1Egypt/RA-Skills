# 私域专家团 · 马甲实战版

[![Skill Version](https://img.shields.io/badge/skill-v2.1.1-0b5cad.svg)](https://github.com/maojiebc/majia-siyu-team/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/maojiebc/majia-siyu-team/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-majia--siyu--team-171515.svg)](https://github.com/maojiebc/majia-siyu-team)

> **私域专家团 · 马甲实战版**
>
> 把马甲做私域的判断装进你的 AI。日常文案直接出活；遇到拿不准的事，按他真做过的事给判断。入口只有一个：`/siyu`。

## 和通用 AI 差在哪

马甲在一家几百家店的连锁咖啡，从短信一条条发，做到企业微信社群三个月攒下一百万好友；后来又给餐饮老板做咨询。包里的案例讲的就是这些事：当时什么情况，他怎么判断，结果怎样，换到你家店该怎么改。你问的处境对得上，AI 会先说马甲会怎么判断，再讲当年那件事。

## 这个入口做什么

`/siyu` 是私域工具箱的统一入口，三种模式：

1. **新手教程** —— 第一次用，先讲清楚能干什么  
2. **任务前路由** —— 读你的真实处境，只选当前最该做的一个能力并直接执行  
3. **任务后导航** —— 干完按真实结论告诉你下一步  

经营动作归本入口；会员指标、SQL、数仓请用 `majia-huiyuan`。

## 一次安装拿到的能力

- **高频执行（边写边合规）**：`siyu-pyq` 朋友圈 · `siyu-qunfa` 群发 · `siyu-huashu` 破冰话术  
- **问诊与调研**：`siyu-wenzhen` 五层问诊 · `siyu-market-research` 厂商/竞品/报价实时留证  
- **全盘诊断**：`siyu-onboard` 四位专家分头看 + 方法库（信任资产 / 促活 / 从进店到再买 / 危机 / 合规）  
- **客户档案**：`siyu-save` / `siyu-restore` / `siyu-report`  
- **升级**：`siyu-update`（只同步官方项目，不碰本地客户档案）  

子能力在包内 `modules/` 路由，**不需要、也不应该**拆成多个商店条目分别安装。

## 安装

```bash
# ClawHub（slug = majia-siyu，展示名 = 私域专家团 · 马甲实战版）
clawhub install majia-siyu

# SkillHub（历史条目 slug = siyu，展示名必须是 私域专家团 · 马甲实战版）
skillhub install siyu

# WorkBuddy / CodeBuddy：一个插件 = 完整专家团
/plugin marketplace add maojiebc/majia-siyu-team
/plugin install majia-siyu@majia-siyu
```

> **身份对照（防标题漂成 slug）**  
> - 安装 / 目录 / frontmatter `name:` → `majia-siyu`（代码身份）  
> - SkillHub 历史商店条目 → slug `siyu`（保留下载量与版本历史）  
> - 对外卡片标题 / H1 / `displayName` → **私域专家团 · 马甲实战版**  
> 三者不要混用：`siyu` 只是历史安装名，不是标题。

完整说明、角色导航、开发验证与源码：**https://github.com/maojiebc/majia-siyu-team**

## 📋 版本记录

- **v2.1.1**（2026-10-22）移除未运行的 Python 运行时，保留 17 个 Markdown 技能与合规检查，加入经本人审阅的真实案例及盲评记录。旧 Python 命令行入口停止提供，改用 Markdown 技能。
- **v1.8.1**（2026-10-20）文案与配图表达修复：先交成品，加入完整模拟示范、场景语气与常用构图。
- **v1.8.0**（2026-10-20）同活动的朋友圈、群发、私聊按需接力，沿用已完成稿件；精简补充文案和配图方法，完整素材分析留给独立收费项目。
- **v1.7.0**（2026-10-19）选型核验风险与平台覆盖；49条有条件知识；分渠道文案、欢迎、评论和配图简报进入执行技能。H1/H2/H3未验证。
- **v1.6.0**（2026-10-12）Q4 至春节模板、模型出活自测与内容修正、只读档案复用；修复社区假更新与旧包提示。H1/H2/H3 未验证。
- **v1.5.0**（2026-09-14）门店会员执行知识与场景检索；41 条严格知识随包分发；补齐六场景安装验证，更新发布和使用说明。
- **v1.4.3** — WorkBuddy 专家团适配、自包含 ZIP 和平台契约检查。

完整历史见 [CHANGELOG](https://github.com/maojiebc/majia-siyu-team/blob/main/CHANGELOG.md)。

## 方法论：私域即公关 · 内容即产品 · 运营即广告

## 👤 作者 / 联系

**马甲（@maojiebc）** · 超级马甲

| 渠道 | 链接 |
|---|---|
| 📧 Email | [m9224@163.com](mailto:m9224@163.com) |
| 🐙 GitHub | [github.com/maojiebc](https://github.com/maojiebc) |
| 🪝 ClawHub | [clawhub.ai/p/maojiebc](https://clawhub.ai/p/maojiebc) |
| 🐦 X | [@maojiebc](https://x.com/maojiebc) |
| 📕 小红书 | [超级马甲](https://xhslink.com/m/4fQMJeHHWKC) |
| 📰 微信公众号 | [超级马甲](https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzY5NzIzODk2NA==#wechat_redirect) |

> 这份 skill 是 14 年用户运营 + 数据中台 + BI 工程实战沉淀出来的，问题/合作随时聊。
