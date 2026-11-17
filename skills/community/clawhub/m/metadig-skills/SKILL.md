---
name: metadig
description: 用 metadig 命令行调用 MetaDig（元界深掘，waytometa.cn）平台生成 AI 图片、视频、语音（TTS）和音乐，产物自动落到用户的网页画布项目。当用户要出图、出片、配音、配乐、批量生成素材、查询可用模型与积分价格、查生成任务进度，或提到 metadig / MetaDig / 元界深掘 / waytometa 时使用。Use when the user wants AI images, videos, speech or music generated through MetaDig, or mentions the metadig CLI.
compatibility: 需要能执行 shell 命令并访问互联网。依赖 metadig CLI（macOS / Linux / Windows 单文件二进制，本文含安装步骤）与一个 MetaDig 账号（生成消耗账号积分）。
metadata:
  author: MetaDig
  homepage: https://waytometa.cn/cli
  docs: https://waytometa.cn/docs/skills/agent-skill
  repository: https://github.com/pythonthink/metadig-skills
---

# MetaDig CLI（metadig）

`metadig` 是 MetaDig（元界深掘，https://waytometa.cn）的命令行工具：登录一次，之后在终端里一行命令提交图片 / 视频 / 语音 / 音乐生成任务。产物默认直接落到用户网页画布项目的节点上（提交即出现「生成中」占位节点，完成后自动回填），用户可以在网页上继续编辑成片。生成消耗账号积分，计费、模型、折扣、会员门禁与网页端完全一致。

本 Skill 只走 `metadig` 命令。不要自己拼接 `waytometa.cn/api` 下的接口，也不要猜测模型 ID 或参数——模型、价格、参数档位都以 `metadig models` 的实时输出为准。

## 安装与登录（一次性）

先看是否已装好：`metadig --version`。没有则安装，装完**重开终端**让 PATH 生效。

```bash
# macOS / Linux
curl -fsSL https://waytometa.cn/cli/install.sh | bash

# Windows PowerShell
iwr https://waytometa.cn/cli/install.ps1 -useb | iex
```

登录走浏览器授权，终端不经手密码：

```bash
metadig login          # 打印授权链接并尝试打开浏览器，用户在网页上点「授权登录」
metadig whoami         # 确认账号与积分余额
```

- 无法打开浏览器（服务器 / 容器 / 远程会话）：`metadig login --no-open` 只打印链接，让用户在任何已登录设备上打开授权；仍不行时让用户设置环境变量 `METADIG_TOKEN`（值为访问令牌）或执行 `metadig login --token <令牌>`。
- 凭证存本机 `~/.metadig/credentials.json`（约 30 天有效）。命令报「尚未登录」或「登录已过期」→ 重新 `metadig login`。
- CLI 登录与用户的网页登录并存，不会把网页登录顶掉。

## 命令速查

```bash
metadig models                       # 全部模型 + 积分价格 + 标签（会员 / 停用 / 新 / 折扣）
metadig models --type video          # 只看视频模型（image / video / tts / music）
metadig models <模型ID>              # 单模型参数档位：比例 / 分辨率 / 时长 / 渠道 / 参考上限
metadig models --json                # 机器可读全量目录（Agent 优先用）

metadig gen image "<提示词>" --ratio 16:9 --resolution 2K -n 2
metadig gen image "<提示词>" -r ./ref.png -m <模型ID>          # 带参考图 = 图生图
metadig gen video "<提示词>" -m <模型ID> --resolution 720p -d 5   # 文生视频
metadig gen video "<提示词>" --first ./cover.png -d 5 -o ./exports # 首帧生视频
metadig gen video "<提示词>" --first a.png --last b.png             # 首尾帧
metadig gen video "<提示词>" -r role.png --ref-video demo.mp4       # 参考生视频
metadig gen speech "<文本>" --voice male-qn-qingse                  # 语音（TTS）
metadig gen music "<风格描述>" --lyrics "<歌词>" -d 40              # 音乐

metadig status <任务ID>                    # 状态 + 产物 URL
metadig status <任务ID> --wait -o ./exports # 等完成并下载
metadig download <任务ID> -o ./exports
metadig history                            # 近 7 天任务（不含 URL）
metadig upload ./a.png ./b.mp4             # 手动上传素材换公网 URL（一般不需要）

metadig project list | create "<名称>" | use <项目ID> | current
```

生成命令通用参数：`-m` 模型、`-p` 项目、`-o <目录>` 完成后下载、`--no-wait` 提交即返回、`--no-canvas` 不建画布节点（只进「历史文件」）、`--json` 机器可读输出。

## 关键工作流

### 出图

1. `metadig models --type image --json` 看可用模型、每张积分（`creditsMap` 按分辨率分档）、比例与分辨率档位。
2. 按用户需求选模型；用户没指定就用目录里第一个可用的（目录已按平台推荐排序）。
3. `metadig gen image "<提示词>" --ratio <比例> --resolution <档位> -n <张数> --json`。有参考图就加 `-r <本地文件或 URL>`（可重复），CLI 自动上传本地文件。
4. 从 JSON 的 `urls` 取图片链接，`files` 是 `-o` 时的本地路径，`nodeId` 是画布节点 ID。把链接和「已落到画布」一并告诉用户。

### 出片（视频）

1. `metadig models --type video --json` 看模型支持的方式（`modes`：文生 / 首帧 / 首尾帧 / 参考）、分辨率、时长与价格（`creditsMap` 键 `"<渠道>:<时长>s:<分辨率>"` 的值就是该时长总价，带声音另有 `creditsMapWithAudio`）。
2. 按素材定方式，不用单独指定：无素材 = 文生；一张图 = `--first`；首尾两张 = `--first` + `--last`；要保持人物 / 风格 / 用参考视频 = `-r` / `--ref-video` / `--ref-audio`。`--first` 与 `--ref` 系列不能混用。
3. **先报方案再提交**：视频一条通常几十积分起，高分辨率、长时长、带参考视频都会加价。把「模型 + 分辨率 + 时长 + 条数 + 预计积分」告诉用户，确认后再跑。
4. `metadig gen video "<提示词>" [素材参数] -m <模型ID> --resolution 720p -d 5 --json`，默认等待完成（几分钟很正常，进度在 stderr）。多条任务可先 `--no-wait` 全部提交，再逐个 `metadig status <任务ID> --wait --json`。

### 配音与音乐

- 语音：`metadig gen speech "<文本>" --voice <音色ID>`，按 200 字计价。音色 ID 见 `references/generation-guide.md`；用户没说就用默认音色。
- 音乐：`metadig gen music "<风格描述>" --lyrics "<歌词>" -d 40`，纯音乐加 `--instrumental`。按 5 秒计价的模型可以 `-d` 改时长（会钳进模型范围），按首计价的模型 `-d` 会被忽略。

### 批量生成

先 `metadig models` 查价并算总积分报给用户，确认后逐条提交。同一批任务用 `--no-wait --json` 提交后统一等待，避免一条卡住拖住全部。任务失败不扣积分，但不要原样重提——先看 `status` 里的说明再改参数。

### 本地素材

`-r` / `--first` / `--last` / `--ref-video` / `--ref-audio` 直接给本地路径，CLI 自动上传换成公网 URL；给 `http(s)://` 则原样使用。只有想提前拿到 URL 复用时才用 `metadig upload`。

### 归到指定项目

任务默认进自动创建的「CLI 项目」画布。用户想分项目管理时：`metadig project create "<名称>"` → `metadig project use <项目ID>`（绑定当前目录，写 `.metadig/project.json`，子目录也生效）；单次任务用 `-p <项目ID>`。

## 重要规则

1. **生成前先查模型**：模型、价格、档位会变，永远以 `metadig models` 实时输出为准，不凭记忆写模型 ID；`-m` 传了目录里没有的模型会直接报错并列出可用清单。
2. **机器解析用 `--json`**：结果只在 stdout，进度与提示都在 stderr，管道干净。
3. **视频先报价再跑**：批量或高价任务先向用户报方案与预计积分，用户确认后再提交。
4. **失败不扣费，但别原样重试**：任务失败 / 取消不扣积分；先看 `status` 的说明，改参数再试。
5. **提交超时 ≠ 失败**：提示「提交请求超时，结果不确定」时任务可能已受理并预扣积分，先 `metadig status <任务ID>` 查，别重复提交。相同参数在进行中重提会被拦截（「相同内容正在生成中」）。
6. **积分不足不重试**：报「积分不足」就停下来告诉用户去网页充值或订阅，CLI 里无法充值。
7. **会员专属 / 维护中**：换 `metadig models` 里其他可用模型；会员专属模型需要用户订阅，不要反复提交。
8. **不拼内部接口**：一切能力都经 `metadig` 命令；命令缺失或行为不符先重跑安装脚本升级 CLI，不要绕过去调 API。
9. **不臆造参数**：不确定的 flag 先 `metadig <命令> --help` 或查 `references/`。传了不在档位内的比例 / 分辨率 / 时长只会得到 stderr 警告，最终以服务端校验为准。
10. **产物默认进画布**：用户不想弄乱画布时加 `--no-canvas`（产物只进项目「历史文件」）。
11. **只在用户自己的设备上授权**：不要把授权链接发给第三方；令牌只放环境变量，不写进文件或对话。

## 排错速查

- `尚未登录` / `登录已过期或无效` → `metadig login`；无浏览器 → `METADIG_TOKEN`。
- `积分不足` → 停止，提醒用户充值。
- `该模型/渠道正在维护中` / `该模型为会员专属` → 换 `metadig models` 里其他模型。
- `模型 X 不支持<方式>` → 该模型不支持这种生成方式，按错误提示里的可用清单换模型。
- `--last 需要与 --first 搭配` / `--first/--last 与 --ref 系列不能同时使用` → 按素材重新选方式。
- `等待超时（2 小时）` → 任务可能仍在生成，稍后 `metadig status <任务ID>`。
- 想连本地 / 测试环境 → 全局参数 `--api-base http://localhost:6603` 或环境变量 `METADIG_API_BASE`。

更多见 `references/common-pitfalls.md`。

## 深度指南（references/）

| 文档 | 何时阅读 |
| --- | --- |
| `references/cli-command-guide.md` | 不确定某个命令的完整参数、环境变量、配置文件位置、JSON 输出字段或任务状态含义 |
| `references/generation-guide.md` | 需要按需求选模型、估算积分、确认视频方式与参数约束、音色 ID，或想知道产物如何落画布 / 项目 |
| `references/common-pitfalls.md` | 遇到登录、超时、积分、模型不可用、上传、下载等报错，或行为与预期不符 |
