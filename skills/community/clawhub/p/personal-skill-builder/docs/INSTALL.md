# 安装与使用

适用版本：**1.0.2 正式版**。

本文件随 ClawHub 的 MIT-0 分发版提供。下文 GitHub 安装命令及 ZIP 下载得到同版本 MIT 分发版；需要本平台的 MIT-0 文件时，从 [ClawHub 页面](https://clawhub.ai/fuetsui/skills/personal-skill-builder)选择 1.0.2。两份发行包的技能行为和脚本相同。

## 安装前准备

安装 Node.js 和 npm，并使用能够读取本地技能文件的 AI 工具。所用工具需要支持当前用户的 `.agents\skills` 目录；模型、账号和文件权限由该工具提供。

## 全局安装到通用 agents 目录

在终端运行：

```text
npx skills add https://github.com/FueTsui/personal-skill-builder --skill personal-skill-builder --agent codex --global
```

命令通过 [Skills CLI](https://github.com/vercel-labs/skills#install-a-skill)安装仓库当前版本。这个全局安装方式的目标为 `~/.agents/skills`，其中 `~` 表示当前用户目录。技能位置为：

```text
~/.agents/skills/personal-skill-builder
```

无需在命令中手动填写用户名。`--global` 指定用户级安装，`--agent codex` 对应的全局位置就是上述通用目录。此命令读取仓库当前版本；需要固定本次发行内容时，使用下方 `v1.0.2` 发布页的 ZIP，并核对随附校验值。

安装完成后，该文件夹中应直接包含 `SKILL.md`、`VERSION`、`references`、`assets`、`scripts` 和 `docs` 等文件与目录。打开 `VERSION`，确认内容为 `1.0.2`。

## 开始使用

刷新所用 AI 工具的技能列表，在下一轮对话或新会话中调用：

> 使用 personal-skill-builder，帮我把每周整理工作周报的流程制作成可复用技能。每次只问一个关键问题，吸收我主动补充的要求，信息足够后生成，并用样例验证。

支持 `$技能名` 语法的工具也可以使用 `$personal-skill-builder`。如果无法自动找到技能，让 AI 显式读取上述安装目录中的 `SKILL.md` 及其需要的引用资源。实际加载版本应以读取的 `VERSION` 和入口内容为准。

随后逐轮回答，也可以一次主动补充多项要求：

> 我会提供本周工作记录。周报保留“进展、问题、下周计划”三部分；没有来源的信息不要补写。这里有两份以往周报供你参考。

不知道怎样选择时，可以说“你先给建议”。需要固定保存位置时，直接提供输出路径。

## 修改与继续

修改已有技能：

> 根据这份新模板升级已有技能，保留仍有效的要求，保存旧版，并重新验证受影响的场景。

换会话继续：

> 读取这份技能和需求记录，从上次进度继续。先采用最新明确要求，不重复询问已经有答案的问题。

恢复进度依赖你提供的文件或当前工具能访问的历史。技能本身不会跨工具自动同步私有会话。

## 日常重复执行

工坊生成业务技能后，日常工作直接调用该业务技能。例如生成了 `weekly-report`，之后每周可以输入：

> 使用 weekly-report，根据附件中的本周记录生成周报，沿用已确认的格式，标出缺少依据的内容。

每批提供本次材料和必要参数。需要改变工作规则时，再使用工坊升级业务技能。

执行生成的处理程序前，备份输入，并把输入目录与输出目录分开；不要让输出文件与输入文件同名同路径。当前版本的一个 Terra 生成样本在这种情况下会覆盖源 CSV，详见[已知问题](KNOWN-ISSUES.md#dev10-p1terra-生成程序可能覆盖输入-csv)。

## 更新与恢复

更新前，将已有的 `personal-skill-builder` 文件夹完整备份到 `.agents\skill-backups` 等技能搜索目录之外，然后重新运行上面的全局安装命令。若曾在其他工具的技能目录安装同名版本，核对并移出旧副本，避免加载到不同版本。

更新后刷新技能列表，并读取实际安装目录下的 `VERSION`。需要恢复时，用备份的完整目录替回，保留其内部结构。

## 下载与更多说明

[v1.0.2 发布页](https://github.com/FueTsui/personal-skill-builder/releases/tag/v1.0.2)提供 `personal-skill-builder-1.0.2.zip` 和 `SHA256SUMS.txt`。ZIP 包含完整技能、功能介绍和使用说明，解压后为 `personal-skill-builder/`。

功能说明见[功能介绍](FEATURES.md)，当前限制与反馈方法见[已知问题](KNOWN-ISSUES.md)。
