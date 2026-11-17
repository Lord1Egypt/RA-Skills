---
name: GitHub Actions ClawHub Doctor
slug: github-actions-clawhub-doctor
description: Diagnose why GitHub Actions to ClawHub publishes fail. 检查 workflow 引用、owner、token、slug、pending-publication 和目录发现问题。
version: 1.0.5
metadata:
  openclaw:
    os: [macos]
    emoji: "🩺"
    requires:
      bins:
        - git
        - clawhub
    homepage: https://github.com/bonniegeng-max/openclaw-publisher
    install:
      - kind: node
        package: clawhub
        bins: [clawhub]
---

# GitHub Actions ClawHub Doctor

Your publish failed. The real question is: where did the chain break?

`github-actions-clawhub-doctor` 专门用来检查 GitHub Actions 到 ClawHub 这条发布链路为什么失败，不只告诉你“红了”，而是把问题拆到真正可修的那一层。

很多失败并不在 skill 内容本身，而是在这些地方：

- reusable workflow 引用失效
- `CLAWHUB_OWNER` 或 `CLAWHUB_TOKEN` 没配好
- skill 名字撞上保留前缀
- `pending-publication` 被 workflow 错误当成失败
- 目录结构导致 workflow 根本没发现你的 skill

## 一句话卖点

把 “GitHub Actions 红了” 变成 “我知道具体哪一层坏了，以及该怎么修”。

## 适合谁

- 已经把 skill 放进 GitHub 仓库并接了自动发布的人
- 被 Actions 红灯卡住，但不知道该看 workflow、skill 还是 ClawHub 的人
- 想把发布问题一次性定位清楚，而不是反复试错的人

## 我会重点看什么

### 工作流层

- `uses:` 指向的 reusable workflow 是否真实存在
- workflow YAML 是否能被 GitHub 正常解析
- 触发条件是否真的覆盖到了 skill 目录改动
- push 和 pull request 的发布逻辑是否分开

### 发布配置层

- `CLAWHUB_OWNER` 是否存在
- `CLAWHUB_TOKEN` 是否存在并被 publish job 使用
- workflow 是否把 token 传进了实际调用层
- categories / topics 是否跟着发布一起同步

### skill 层

- slug 和目录名是否可发布
- 是否使用了保留前缀或保留词
- `SKILL.md` 是否在正确目录
- frontmatter 是否能正常解析

### ClawHub 返回层

- 是 validation failed
- 还是 pending publication
- 还是 unchanged
- 还是 owner / 权限问题

## 你可以这样让我工作

- `帮我查为什么 github actions 发不到 clawhub`
- `看看这次 workflow 红灯到底卡在哪一层`
- `这个 pending-publication 到底算成功还是失败`
- `检查我的 skill 名称和 owner 有没有问题`

## 我理想中的输出

1. 问题所在层级：workflow / secret / owner / skill / registry
2. 直接原因：一句话说清楚
3. 证据：哪段配置、哪条日志、哪个状态
4. 最小修复方案：最值得先改的一处
5. 修复后验证命令：下一步马上跑什么

## 一个真实示例

用户说：

`为什么我的 skill 明明已经在 ClawHub 上了，GitHub Actions 还是红的？`

我会优先判断：

- workflow 是否把 `pending-publication` 当成了错误
- registry 实际状态是不是已经是 `published` 或 `unchanged`
- 失败到底是假失败，还是仍然有真实阻塞项

## 工作边界

- 我不会伪造发布结果
- 我不会跳过权限或 owner 校验
- 如果需要修改 workflow，我会明确指出改哪一行最值

## 配套文件

- `examples/pending_publication_false_failure.md`
  一个典型“其实已经发上去，但 Actions 还在报错”的例子
- `references/failure_map.md`
  常见失败模式和排查入口的映射表
- `CHANGELOG.md`
  版本记录

## 同系列 · skill 工程线（Skill Engineering Line）

本 skill 属于「skill 工程方法论」系列 —— 六件工具覆盖一个 skill 从定位到上线的完整链路，按需组合：

- `skill-positioning-audit` — 定方向：该卖给谁、差异化够不够
- `skill-summary-rewriter` — 写门面：摘要/简介改成能带来安装的版本
- `skill-publish-readiness` — 上线前：发布自查（结构 / 版本 / 页面 / 安全 / 值不值得发）
- **`github-actions-clawhub-doctor`** — 发不出去：定位 Actions / registry 到底卡在哪一层**（本 skill）**
- `release-proof-builder` — 上线后：证明「现在到底上线没有、能不能装」
- `skill-portfolio-growth-audit` — 看全局：整个作品集下一步押注什么

安装任意一个：`clawhub install @bonniegeng-max/<slug>`
