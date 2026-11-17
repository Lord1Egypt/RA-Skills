---
name: jimeng-drama
description: 用即梦（Dreamina）官方 CLI 生成 9:16 竖屏 AI 短剧。当用户要做短剧、AI 短片、竖屏分镜视频、把剧本变成成片、或提到"即梦出片""dreamina 短剧"时使用。覆盖剧本拆解、角色定妆、逐镜生成、配音字幕、成片拼接全流程。
---

# 即梦短剧生成

把一份剧本变成 9:16 竖屏短剧。底层调用即梦官方 CLI `dreamina`，编排引擎是本仓库的 `drama` 命令。

## 安装

```bash
git clone https://github.com/liuboacean/jimeng-drama.git
cd jimeng-drama
npm install
```

需要：Node ≥ 20、ffmpeg、即梦 CLI（`curl -fsSL https://jimeng.jianying.com/cli | bash`），以及**即梦会员账号**。

## 第一步永远是自检

```bash
npx tsx src/cli.ts doctor
```

六项全绿才继续：`node`、`ffmpeg`、`dreamina`、`登录态`、`硬字幕能力`、`中文 TTS`。

若 `登录态` 显示"会员等级 无"，立刻停下并告知用户：

> 即梦 CLI 的准入门槛是**会员身份，不是积分**。请用会员账号执行
> `dreamina logout && dreamina login`，授权完成后再继续。

## 铁律：不确认不烧积分

**任何会提交生成任务的命令，执行前必须先报预估积分并取得用户同意。**

```bash
npx tsx src/cli.ts plan <slug>       # 预估消耗，零成本
```

除用户明确说"直接跑"，否则默认先用 `--provider=mock` 把链路跑通（ffmpeg 合成占位素材，零积分），确认流程无误后再换 `--provider=dreamina`。

## 标准流程

```bash
# 1. 建项目
npx tsx src/cli.ts init <slug> --title "剧名·EP01" --ratio 9:16 --duration 100 --budget 400

# 2. 写剧本到 projects/<slug>/script.md（语法见下），拆分成镜
npx tsx src/cli.ts script <slug> --dialogue-mode multimodal2video

# 3. 角色定妆图（身份锚点，防人物跨镜头漂移）
npx tsx src/cli.ts chars <slug> --views 3

# 4. 对白配音（离线 TTS；真人录音放 audio/<shotId>.mp3 会自动优先复用）
npx tsx src/cli.ts audio <slug>

# 5. 逐镜生成（提交前先 plan 确认积分）
npx tsx src/cli.ts plan <slug>
npx tsx src/cli.ts run <slug> --concurrency 2

# 6. 成片
npx tsx src/cli.ts compose <slug>
```

或一条龙：`npx tsx src/cli.ts all <slug>`

## 剧本文法（确定性解析，不依赖 LLM）

```markdown
## 场景 1 · 雨夜街头          ← ## 开头是场景
[动作] 雨幕倾泻，霓虹倒映      ← [动作] 或纯描述行 = 空镜
林夏：你终于来了。            ← 名字：台词 = 对白镜
```

- 对白时长按 ≈4.5 字/秒自动估算，夹在 3–15s
- 空镜默认 4s，用 `--action-duration` 调
- 镜头默认「上一镜末帧 → 下一镜首帧」串联，`--no-chain` 可关
- 角色名与 `characters.json` 的 `name` 匹配后自动带进该镜 `cast`

## 关键约束（来自 CLI 实测，违反直接报错）

| 约束 | 说明 |
|---|---|
| `seedance2.5` 是 VIP-only | 会员等级不够会返回权限错误 |
| `image2video`/`frames2video` + seedance2.5 **禁传 `--ratio`** | 比例随首帧图，所以**首帧图必须直接按 9:16 生成**，别先生成方图再裁 |
| `multimodal2video` 可显式传 `--ratio=9:16` | 对白镜走这条 |
| 退出码 0 ≠ 成功 | 必须判 `gen_status=success`；引擎已处理 |
| `video_url` 只是预览链接 | 落盘必须用 `query_result --download_dir` |
| `AigcComplianceConfirmationRequired` | 该模型首次使用需先在即梦 Web 端跑通一次 |
| `ExceedConcurrencyLimit` | 任务**未被受理**，别再堆；可试一次 VIP 变体 |
| 成图带「AI生成」可见标识 | 合规强制标识，后期裁剪不要切掉 |

## 失败处理

- 单镜失败不拖垮整片，`status` 里能看 `failReason`
- 可重试错误（超时、拉图失败）引擎自动退避重试，上限 `--max-retries`
- 中断后直接 `run <slug>` 续跑，已完成镜头不会重复提交、不重复扣费
- 存量任务别丢：`dreamina list_task` → `query_result --submit_id=<id> --download_dir=<dir>` 补下载，**不要重新提交**

## 成本参考（实测，随版本可能变）

- 2k 竖屏图：3 积分/张
- 5s 视频：约 15~20 积分（首帧图另计）
- 单集 100s（约 29 镜）：≈ 500~700 积分
- 省钱做法：先 480p/720p 出样，定稿后 1080p 重跑

## 交付物

```
projects/<slug>/
├── project.json / characters.json / shots.json / script.md
├── assets/characters/          角色定妆图
├── assets/shots/<shotId>/      每镜头帧图与视频
├── audio/<shotId>.mp3          配音（真人录音放这里可覆盖 TTS）
├── audio/subs.srt              字幕
└── out/final.mp4               成片（9:16 / 1080p / 带软字幕轨与配音轨）
```
