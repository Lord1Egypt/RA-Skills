---
name: key
description: |
  AI KEY·短命令 ——AI KEY（AI 钥匙）工具箱的短命令。`/key` 和 `/aikey` 完全一样，只是少敲三个字母 —— 它把你交给总入口，由总入口按你卡在哪挑技能。
  两套技能：做内容（选题 / 写稿 / 标题 / 开头 / 审核 / 剪辑 / 复盘）· 看生意（营收归因 / 大客户集中度 / 依赖风险 / 多产品线取舍 / 目标拆路径 / 趋势押什么 / 决策 / 到期追踪）。
  触发方式：/key、/key 新手指南、/钥匙
  ⚠️ **与 API key、密钥、密码、令牌无关**。用户问的是接口密钥、环境变量、凭据一类的事，**不要用本技能**。
  Short command for the AI KEY toolbox: `/key` is the same entry point as `/aikey`. Not about API keys, secrets or credentials.
  Trigger: /key, "/key 新手指南"
  —— AI KEY · 不给公式，给判据。每条规则都标了实测代价。
slug: key
displayName: AI KEY·短命令
metadata:
  openclaw:
    emoji: 📐
version: 1.0.0
---

# key：AI KEY 的短命令

**你就是 `/aikey`，不是另一个技能。**

## 你要做的只有一件事

读同级目录的 `aikey/SKILL.md`，**按它的流程执行**。路由判断、新手上路、任务后导航，全部归它。

🔴 **不要在这里重复它的内容。** 本文件只负责把人交过去 —— 判据写两份，改的时候一定会有一份过期。

## 读不到 `aikey/SKILL.md` 时

说明只装了别名、没装本体。**明说这一点**，并给安装命令，不要猜测它可能有哪些技能：

```bash
npx skills add iamzifei/aikey -g --all
```

## 这个别名为什么存在

用户实测：`aikey` 每次敲全太长，嘴上说「AI 钥匙」也拼不出命令。**短命令降低的是每天的摩擦，不是功能。**

⚠️ **别名只有这一个。** 再加第二个（`ai`、`k`、`钥匙`…）就会变成一堆指向同一处的入口，
用户不知道该用哪个，你也不知道该在哪儿改。
