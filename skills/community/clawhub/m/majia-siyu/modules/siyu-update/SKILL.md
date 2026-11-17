---
name: siyu-update
description: |
  更新私域专家团。用户说「更新私域专家团」「升级 siyu」「检查并安装最新版」或输入 /siyu-update 时使用。
  只同步 maojiebc/majia-siyu-team，不修改 ~/.siyu/ 客户档案，不更新其他 skill。
metadata:
  version: "2.1.1"
---

# siyu-update：更新私域专家团

用户明确要求实际更新时直接执行，不再做第二次文字确认；宿主的权限窗口仍由用户决定。

## 范围

- 只同步官方项目 `maojiebc/majia-siyu-team`。
- 绝不读取、移动、删除或覆盖 `~/.siyu/` 客户档案。
- 不更新其他 skill，不创建后台任务、定时任务或 hook。
- 用户只问版本或更新内容时，只回答，不执行更新。

## 判断顺序

1. 用户明确说明仓库已公开，或能确认 GitHub visibility 为 public：走公开通道。
2. 否则，若 `~/Projects/majia-siyu-team/.git` 存在：走本地仓库通道。
3. 本地仓库不存在且无法确认公开：停止，用一句话说明需要仓库访问权限或本地路径，不猜测。

## 公开通道

```bash
npx -y skills add maojiebc/majia-siyu-team -g --all
```

只安装该项目的正式能力。不要使用会更新其他 skill 的全局 update 命令。

## 私有期本地通道

先确认远端指向 `maojiebc/majia-siyu-team`，再执行：

```bash
git -C ~/Projects/majia-siyu-team pull --ff-only
npx -y skills add ~/Projects/majia-siyu-team -g --all
```

`pull` 失败、工作区冲突或远端不匹配时立即停止，不重置、不覆盖用户改动。

## 回复

成功只说：

> 私域专家团已更新。当前对话若还没读取到新能力，新建一次对话后使用。

失败只说：

> 私域专家团没有更新：{一句人话原因}。处理完 {权限、网络或本地改动} 后，再说一次「更新私域专家团」。

不粘贴完整日志，不加感叹号。

---

## 不知道下一步用哪个 skill？

输入 `/siyu`。

这是私域工具箱的导航入口。它会沿用已有事实和产物，按当前目标安排必要的步骤，
并在当前对话继续完成。迷路了就回 `/siyu`。
