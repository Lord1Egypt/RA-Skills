# 安装 Onimi Pages Creator

默认 Onimi 安装会明确为当前 Agent 准备 Creator 与 Publish，并保留已有目录和个人修改。
安装在本地完成，不会连接账号、向 Onimi Pages 发送提示词或发布页面。
把这两个模块作为一次任务交给当前 Agent；创作和发布前预检使用它正在使用的模型，不需要另装本地模型。

## npm

只有[稳定清单](https://downloads.onimi.ai/skills/manifest.json)中 Publish npm 渠道可用且其渠道
版本等于当前 Publish 版本时，才使用 `latest` 套件；旧的可用包可能还没有 `install --suite`。
需要 Node.js 20 或更高版本。

```sh
npx --registry=https://registry.npmjs.org onimi-pages-publish@latest install --suite --agent codex
```

可把 `codex` 替换为 `claude-code` 或 `cursor`。其他客户端请查阅其个人 Skill 目录说明，并使用
`install --suite --dir /absolute/path/to/skills`。安装器只补缺失模块，不执行网络、账号或发布操作。
独立 `onimi-pages-creator` 包仍作为仅本地创作的高级选项保留。

## 直接下载

从[稳定清单](https://downloads.onimi.ai/skills/manifest.json)读取完整的
`skills.creator.archive.url`、`skills.creator.archive.sha256`、`skills.creator.archive.size`，以及
对应的 `skills.publish.archive.url`、`skills.publish.archive.sha256`、
`skills.publish.archive.size`，下载两个不可变归档并分别校验哈希与字节数。
只补缺失的完整文件夹，不覆盖任一已有模块或本地修改。
这个流程不依赖网站的 latest 跳转路由先完成部署。

| 客户端 | 个人 Skill 父目录 |
| --- | --- |
| Codex | `~/.agents/skills` |
| Claude Code | `~/.claude/skills` |
| Cursor | `~/.cursor/skills` |

## GitHub

官方仓库：https://github.com/zlch-oceanai/onimi-pages-creator

```sh
npx --registry=https://registry.npmjs.org skills@1.5.26 add zlch-oceanai/onimi-pages-creator --skill onimi-pages-creator --global
```

## ClawHub

只有稳定清单把该渠道标记为可用后再安装：
固定版本的 ClawHub CLI 需要 Node.js 22 或更高版本；Node.js 20 请改用其他已验证渠道。

```sh
npx --registry=https://registry.npmjs.org clawhub@0.23.3 install @mariohazy/onimi-pages-creator
```

## 验证与使用

如客户端需要，请重启或重新加载当前 Agent，然后让它创建一个本地 Page 或基于 Bento 的
Slides 作品。Skill 内含 `scripts/validate-html.mjs`；校验和浏览器预览都不会发布文件。

创作和发布是两个独立步骤。套件可能已经准备 Publish，但只有受控模板、云草稿、云 Slides
或发布任务实际需要时才启动浏览器 OAuth；同账号且 scope 足够的有效连接应直接复用。
公开安装说明不得替换为测试服务地址。

只有 `SKILL.md` 同级存在 `.onimi-skill.json` 的直接下载安装才使用内置管理器；
没有该收据时，请使用对应渠道的原生更新流程。从其 `SKILL.md` 路径定位已安装 Skill 目录，不要切换用户工作区，
并使用绝对路径运行管理器。可在本地运行
`node /absolute/path/to/onimi-pages-creator/scripts/manage.mjs status`，并用
`node /absolute/path/to/onimi-pages-creator/scripts/manage.mjs check` 做每日一次的非阻塞更新检查。
阅读版本信息并明确同意后，才运行
`node /absolute/path/to/onimi-pages-creator/scripts/manage.mjs update --confirm onimi-pages-creator@<version>`。
npm、GitHub 与 ClawHub
使用各自的更新机制。
