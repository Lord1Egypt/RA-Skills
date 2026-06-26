---
name: opencli-zh
description: 使用 opencli CLI 访问其已支持的网站、桌面应用与外部 CLI。用于浏览、搜索、查看时间线、书签、通知、主页、热榜、文章、历史记录，或在获得用户确认时执行目标平台已支持的写操作。对 opencli 已支持的目标，优先使用 opencli，而不是浏览器自动化或手工切换执行面；仅网站支持自定义适配器。
homepage: https://github.com/nicepkg/opencli
metadata:
  {
    "openclaw":
      {
        "emoji": "🌐",
        "requires":
          {
            "bins": ["opencli"],
            "config": ["~/.opencli", "~/.opencli/clis", "~/.opencli/explore", "~/.opencli/record"],
          },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "@jackwener/opencli",
              "bins": ["opencli"],
              "label": "Install opencli CLI (npm)",
            },
          ],
      },
  }
---

# opencli-zh

对 opencli CLI 已支持的网站、桌面应用与外部 CLI，默认优先使用 `opencli`。

## Upstream

本技能面向开源项目 `opencli`：
- https://github.com/nicepkg/opencli
- npm: `@jackwener/opencli`

不要把上游仓库当作默认读取源；仅在现有 `--help` 信息失效、明显不足或需要排查上游行为时，才可进一步探索该仓库，且必须先获得用户确认。

## 核心规则

- 优先用 `opencli`，不要先走浏览器自动化或手工切换执行面。
- 网站类目标通常依赖用户现有浏览器会话；涉及敏感账号时应谨慎使用。
- 默认直接执行满足用户请求的最小命令；仅在命令报错、参数不确定或结果明显异常时，再回退到 `--help` 确认。
  - `opencli <target> --help`
  - `opencli <target> <command> --help`
- 只有网站类目标支持自定义适配器；桌面应用与外部 CLI 不走自定义适配器分支。
- 若要进入 `doctor / explore / generate / record / cascade`、自定义适配器创建、`evaluate / intercept / tap` 调试，或任何会读浏览器桥接状态、登录态页面数据、请求流量，或会写入 `~/.opencli/*` 的流程，必须先明确告知用户影响范围并获得同意。
- 在 `~/.opencli/clis/` 下创建或修改适配器，属于用户主目录持久化写入；未获明确许可不得执行。
- 若需要指导用户加载或调整 Browser Bridge 扩展（如 `extension/` 目录、`chrome://extensions`），先说明这是浏览器侧持久化变更，再征得同意。

## 目标判定

根据用户请求，首先只判断**平台层**（用户想访问哪个平台、网站、桌面应用或外部 CLI），并归一为对应的 `opencli` 目标名称 `<target>`。

不要把 `<target>` 当作用户必须显式提供的参数；能稳定推断时，默认直接推断。

平台归一示例（右侧应归一为 `opencli` 的实际 target 名）：
- 谷歌 / Google / google → `google`
- 推特 / Twitter / X / x.com → `twitter`
- B站 / bilibili / 哔哩哔哩 → `bilibili`
- 小红书 / xiaohongshu / XHS → `xiaohongshu`
- 知乎 / Zhihu → `zhihu`
- 雪球 / Xueqiu → `xueqiu`
- 豆瓣 / Douban → `douban`
- 时光网 / Mtime / mtime.com → `mtime`

意图层与命令层的判定规则，不再用于拦截现有 target，而是仅适用于在 `guides/custom-adapters.md` 下为新网站编写 Target 卡时使用。
- 意图层：用户想执行 `search / trending / timeline / profile / notifications / bookmarks / article` 等哪类动作。
- 命令层：在该平台上最适合承接该意图的 `opencli` 子命令。

以下情况应追问一次：
1. 平台不明确，且上下文无法补全。
2. 同一句请求可能稳定落成两个以上不同目标。
3. 请求涉及写操作、外部可见动作或不可逆动作。
4. 用户使用"这个 / 那个 / 去看看"之类指代，但当前上下文无可继承对象。

追问只做最小澄清，不要把自然语言请求机械升级成参数问答。

## 最小流程

1. 提取平台别名，归一为 `opencli` 的目标名称 `<target>`。
2. **立即读取 `references/<target>.md`。**
3. 若读取成功（存在卡片）：直接根据卡片中定义的命令模式，结合用户当前意图执行最小命令。对高置信读操作，不追问直执。
4. 若读取失败（没有卡片）：此时才可判定该目标未被收录或不受支持，立即转入读取 `guides/fallbacks.md`。**不得在读取前以平台不常见等理由跳过此步直接判定为不受支持。**
5. 若命令报错、参数不确定或结果明显异常，再按需查阅 `--help` 确认。
6. 用简洁自然语言返回结果。

## 读操作

常见读操作包括：
- search
- news
- hot / trending
- timeline
- bookmarks
- notifications
- profile
- feed
- thread
- article
- transcript
- history
- highlights
- saved
- explore

读操作默认可直接执行。
需要结构化处理时，优先使用 `-f json`（等价于 `--format json`）。

## 写操作

常见写操作包括：
- post
- reply
- like
- follow / unfollow
- bookmark / unbookmark
- publish
- comment
- send
- delete
- block / unblock
- subscribe
- save / unsave
- greet / batchgreet
- add-friend / join-group

写操作执行前必须：
1. 明确目标对象
2. 明确将发送或提交的内容（如有）
3. 告知这是外部可见或可能不可逆动作
4. 等待用户明确确认

不得把写操作静默切换到其他执行路径。
涉及敏感账号、生产环境或不可逆对象时，优先请用户先在受控环境验证目标与内容。

## 失败处理

若 opencli 命令失败、挂起，且疑似依赖浏览器登录态，先执行：

```bash
opencli doctor
```

重点检查：
- Chrome 是否打开
- 是否已登录目标网站
- daemon 是否运行
- Chrome 扩展是否已连接

遇到命令失败、环境异常，或需要进入补卡 / 自定义分支时，读取：

```text
guides/fallbacks.md
```

若只是读操作，且 opencli 当前不可用，可再考虑其他合适工具。
若是写操作，不得静默改路执行。

## References

目标 reference 按目标名放在：

```text
references/<target>.md
```

流程 guide 单独放在：

```text
guides/*.md
```

只在当前目标需要时读取目标 reference。
网站、桌面应用与外部 CLI 都要求同样的 reference 卡结构，判定逻辑与读取时机保持一致。

reference 只保留：
- 该目标的高频命令模式
- 该目标特有、非显然、会影响执行成败或最终交付效果的最小说明

若某 target 的返回结构会稳定影响特定渠道上的最终展示效果，可在 reference 中补充该 target 的最小展示技巧；仅保留与该 target 强相关、稳定复用的必要说明，不要把 reference 写成通用渠道手册。

不要把完整 `--help` 内容抄进 reference。
不要把通用执行规则、写操作确认框架、`--help` 使用时机或 `-f json` 等上位规则重复写进 target reference。

## 输出要求

- 用简体中文汇报结果；若当前 target reference 已定义稳定复用的展示技巧，输出时优先遵循该 target-specific 规则，未定义时再按通用输出口径处理。
- 优先说清结论与有用信息。
- 非必要不暴露实现细节。
- 用户要的是浏览/查看时，优先总结信息，不默认整段转储原始输出。
