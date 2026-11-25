# job-screening · 校招选岗 Skill

[English](README.md) · [简体中文](README.zh-CN.md)

[ClawHub](https://clawhub.ai/ekko237/skills/job-screening) · [使用方法](#快速上手) · [反馈问题](https://github.com/Ekko237/job-screening-skill/issues) · [MIT 许可证](LICENSE)

给用 Claude Code、Codex、Cursor 等 AI 代理（`npx skills` 支持的工具）准备校招的在校生和应届生。发来一家公司的岗位列表，它会推荐 1–3 个值得投的岗位，说明哪个更有机会，以及其余岗位为什么不投。

投递名额有限时，光看岗位名容易看错实际工作，读完详情才发现学历或城市不合适也会白花时间。这个 Skill 先查硬门槛再排序，每条推荐都要有招聘方能在投递版简历里看到的证据。

## 安装

### Option 1 — Command

在当前目录把 Skill 安装到 `.agents/skills/job-screening`：

```bash
npx skills add https://github.com/Ekko237/job-screening-skill --skill job-screening
```

在非交互终端中，如有需要可加上 `-y`。

### Option 2 — Prompt

把下面的英文提示词粘贴到 Claude Code、Codex、Cursor 或另一个受支持的 Agent 中，即可按需运行，无需安装：

```text
Run `npx skills use "https://github.com/Ekko237/job-screening-skill" --skill "job-screening"` and follow the generated skill instructions now. Read its complete output, redirecting it to a temporary file first if necessary. Resolve relative paths from the supporting-files directory it provides.
```

## 运行要求

- 已登录的 AI Agent 会话（Claude Code、Codex、Cursor 或另一个受 `npx skills` 支持的 Agent），才能走完整流程。
- 使用上方 `Command` 或 `Prompt` 选项时，需要 `git` 和带 `npx` 的 Node.js。
- 使用 `install.sh` 时，需要 `git`、`bash` 和 `rsync`；脚本会查找 `~/.codex` 或 `~/.claude`。
- 准备好你的简历和一家公司的岗位列表。

## 快速上手

### 1. 安装 Skill

使用 `Command` 可把 Skill 安装到 `./.agents/skills/job-screening/`；使用 `Prompt` 可按需运行，无需安装。固定的 `v1.0.2` 和 `install.sh` 安装方式见[其他安装方式](#其他安装方式)，该脚本会安装到 `~/.codex/skills/job-screening/` 或 `~/.claude/skills/job-screening/`。

### 2. 打开 Agent，建一份档案

在 Claude Code、Codex、Cursor 或另一个受支持的 Agent 里说「用 job-screening」或「帮我筛一下秋招岗位」。首次建档约 10 分钟，只做一次。

1. 提供简历文件（PDF、Word 或图片），并说明实际投出去哪一版。
2. 回答一轮简短访谈，确认目标岗位、明确不投的方向、可接受的城市、毕业和到岗时间，以及其他投递偏好。
3. 看看 Skill 根据简历证据找出的其他岗位方向和搜索关键词。
4. 核对并修正档案后再开始筛岗。档案存在已安装 Skill 的本机 `profile/` 目录里，已被 Git 忽略。

### 3. 发来一家公司的岗位列表

可以粘贴文字、发截图、附上 PDF 或 Excel 岗位表，也可以发招聘链接。如果知道这家公司允许投几个岗位，就一起告诉它。它会给出有顺位的推荐、简历证据和风险，并逐个说明淘汰理由，方便你核对筛得对不对。

## 什么时候不适合用

- 选公司和写简历超出这个 Skill 的范围。
- 跑完整流程需要已登录的 AI Agent 会话（Claude Code、Codex、Cursor 或另一个受支持的 Agent）。
- 删掉你不愿交给 Agent 所配置模型或服务商的敏感信息。见[隐私](#隐私)。
- 浏览器的 `localStorage` 不适用。档案存在已安装 Skill 的本地文件里。

## 和其他做法比较

| 做法 | 你要做什么 | 你会得到什么 |
| --- | --- | --- |
| 自己筛 | 逐个打开岗位详情，自己记录要求并权衡 | 自己选出的名单和记下的理由 |
| 开个新对话问 Agent | 提供岗位表，重新说明限制条件和排序标准 | 根据当次提示词生成的答案 |
| 用 job-screening | 建一次档案，再每次发一家公司的岗位列表 | 用投递版简历核过的推荐，以及每个岗位的淘汰理由 |

## 输出示例

以下是虚构模板。岗位、人数、内推信息和简历内容均为占位示例。

```text
投这 2 个

1. XX 产品经理｜主投
- 匹配度：高
- 进面判断：高，培训生项目，招 42 人，有内推码
- 证据可见性：用到的三条证据都在投递版简历第二段。
- 为什么是它：[引用对应的简历证据。]
- 风险：[面试可能追问的问题。] 培训生可能被分到运营方向。

2. XX 产品经理｜保底
[列出匹配度、证据、推荐理由和风险。]

淘汰的（17 个）
- [XX 岗位]：要求硕士及以上学位。
- [XX 岗位]：属于你明确不投的运营序列。
[逐个补齐其他岗位和淘汰理由。]

要核对的事
[待确认的问题和风险。]
```

## 筛选流程

1. **先按硬条件筛。** 核对学历、城市等限制。每个拟推荐岗位都要看完整详情页，确认任职要求。
2. **按四层排序。** 先看职责的前三条来判断岗位序列，再看业务匹配度、竞争力和录取概率。第四层单独评估进不进得去，也会考虑培训生项目的招录规模等信号。
3. **检查证据可见性。** 用来证明匹配的经历必须写在招聘方能看到的那份简历上。只出现在作品集、个人网站或聊天记录里的经历不能支撑这条推荐。过不了这一关的推荐会降级或剔除。
4. **给出理由。** 说明为什么推荐，以及其余岗位各自为什么被淘汰。纠正「本科也能投」之类的资格事实，只会消除相应的淘汰条件。要把岗位往前排，需要有符合排序标准的理由。

## 目录结构

```text
job-screening/
├── SKILL.md                       筛选流程和输出格式
├── install.sh                     Codex 和 Claude Code 安装脚本
├── references/
│   ├── onboarding.md              收简历、访谈和建档
│   ├── opportunity-scan.md        从简历证据找其他可投方向
│   └── profile-template.md        候选人档案模板
└── profile/                       本机候选人档案（Git 忽略）
```

## 其他安装方式

固定稳定版 [v1.0.2](https://github.com/Ekko237/job-screening-skill/releases/tag/v1.0.2)：

```bash
git clone --branch v1.0.2 --depth 1 https://github.com/Ekko237/job-screening-skill.git job-screening-skill
cd job-screening-skill
bash install.sh
```

安装脚本会把 Skill 复制到本机已有的对应位置：

| Agent | Skill 目录 |
| --- | --- |
| Codex | `~/.codex/skills/job-screening/` |
| Claude Code | `~/.claude/skills/job-screening/` |

安装会保留 `profile/` 和目标目录里已有的额外文件。如果发现无法识别的同名安装，脚本会先把整个目录备份成 `job-screening.bak-<时间戳>`，然后停止。查看备份后，如果确定要替换，在刚拉取的固定版本目录里运行 `bash install.sh --force`，档案仍会保留。

也可以手动安装。把固定版本里的 `SKILL.md` 和 `references/` 复制到对应的 Skill 目录，保留已有的 `profile/`。

## 隐私

筛选在你自己的 Agent 会话里进行，Skill 没有单独的服务器。你交给 Agent 的简历文本会发给该 Agent 所配置的 AI 模型或服务商。

档案存在已安装 Skill 的 `profile/` 目录里，该目录已被 Git 忽略。简历原文件留在你原来的位置，档案可以记录文件的本机路径。这个仓库不含个人信息。如果你 fork 后要提交修改，先确认没有把简历或档案加进去。

## 关键词

选岗（job screening）、校招（campus recruiting）、Agent Skill（agent-skills）、Claude Code（claude-code）、Codex（codex）。

## 许可证

[MIT](LICENSE)
