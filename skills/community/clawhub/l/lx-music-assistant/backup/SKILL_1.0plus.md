---
name: lx-music-assistant
description: |
  控制洛雪音乐助手桌面版播放音乐。
  支持：搜索歌曲并唤醒程序、播放/暂停/切换、调节音量、查看播放状态和歌词、收藏歌曲。
  使用 Scheme URL 控制操作，HTTP API 查询状态。
  每次执行命令后自动查询状态并用 Markdown 表格汇报结果。
---

# 洛雪音乐助手技能

通过内嵌 CLI 工具控制洛雪音乐助手桌面版。**搜索&搜索并播放功能可唤醒程序**。

## 前置条件

1. 已安装洛雪音乐助手桌面版
2. 已开启 OpenAPI 服务：设置 → 开放 API → 启用开放 API 服务（端口 23330）

## 内嵌 CLI 路径

```
{skill_dir}/cli/lx-music-cli.js
```

## 配置

API 地址和端口配置在 `{skill_dir}/config.md`。

## 标准执行流程

**每个命令执行后必须执行此流程：**

```javascript
// 1. 执行命令
await execCommand(cmd);

// 2. 等待 500ms
await sleep(500);

// 3. 查询状态
const status = await execCommand('status');

// 4. 用 Markdown 汇报结果（不包含音量，因 API 音量显示不准确）
if (status.name) {
  "✅ 操作成功\n\n| 项目 | 值 |\n|------|-----|\n| 歌曲 | " + status.name + " |\n| 歌手 | " + status.singer + " |\n| 专辑 | " + status.album + " |\n| 进度 | " + formatDuration(status.progress) + " / " + formatDuration(status.duration) + " |\n| 状态 | " + (status.status == 'playing' ? '▶️ 播放中' : '⏸️ 暂停') + " |"
} else {
  "⚠️ 操作已执行，但 API 未启动\n\n请确认：\n1. LX Music 已启动\n2. 设置 → 基础设置 → 启用 OpenAPI 服务"
}
```

## 常用命令

### 搜索（唤醒程序，在播放器内显示结果）

```bash
# 打开搜索页面，在播放器内显示搜索结果
# 用户可在播放器内切换"歌曲"/"歌单"标签查看结果
node {skill_dir}/cli/lx-music-cli.js search <关键词>

# 指定平台搜索
node {skill_dir}/cli/lx-music-cli.js search <关键词> <源>
```

### 搜索并播放（直接播放）

```bash
# 直接播放指定歌曲（唤醒程序）
# 只有歌名无歌手：播放该歌曲或该艺术家热门曲目
node {skill_dir}/cli/lx-music-cli.js searchPlay <歌名>

# 歌名+歌手：精确匹配播放
node {skill_dir}/cli/lx-music-cli.js searchPlay <歌名-歌手>
```

### 播放控制

```bash
node {skill_dir}/cli/lx-music-cli.js play      # 播放
node {skill_dir}/cli/lx-music-cli.js pause     # 暂停
node {skill_dir}/cli/lx-music-cli.js toggle    # 切换播放/暂停
node {skill_dir}/cli/lx-music-cli.js next      # 下一首
node {skill_dir}/cli/lx-music-cli.js prev      # 上一首
```

### 状态查询

```bash
node {skill_dir}/cli/lx-music-cli.js status    # 完整状态
node {skill_dir}/cli/lx-music-cli.js now       # 当前歌曲
node {skill_dir}/cli/lx-music-cli.js lyric     # 歌词
```

### 音量控制

```bash
node {skill_dir}/cli/lx-music-cli.js volume <0-100>  # 设置音量
node {skill_dir}/cli/lx-music-cli.js mute            # 静音
node {skill_dir}/cli/lx-music-cli.js unmute          # 取消静音
```

### 歌单（唤醒程序）

**⚠️ 歌单操作必须指定平台源，无法自动判断！**

```bash
# 打开歌单页面（不自动播放）
node {skill_dir}/cli/lx-music-cli.js openlist <源> <歌单ID>

# 播放歌单（从指定位置开始，可选）
node {skill_dir}/cli/lx-music-cli.js playlist <源> <歌单ID> [起始序号]
```

**源代码**：`kw`(酷我), `kg`(酷狗), `tx`(腾讯/QQ), `wy`(网易), `mg`(咪咕)

**如果用户没有提供平台源，必须询问：**
"请指定歌单来源平台：酷我(kw)、酷狗(kg)、QQ音乐(tx)、网易云(wy)、咪咕(mg)"

**如果用户提供了歌单 URL，从中提取源和 ID：**
- 网易云：`https://music.163.com/playlist?id=987654321` → `wy 987654321`
- QQ音乐：`https://y.qq.com/n/ryqq/playlist/1234567890` → `tx 1234567890`
- 酷我：分享链接通常包含 `kw` 标识

### 收藏

```bash
node {skill_dir}/cli/lx-music-cli.js collect     # 收藏
node {skill_dir}/cli/lx-music-cli.js uncollect   # 取消收藏
node {skill_dir}/cli/lx-music-cli.js dislike     # 不喜欢
```

## 完整命令列表

| 命令 | 说明 | 示例 |
|------|------|------|
| `search <关键词> [源]` | 打开搜索页面（播放器内显示结果，可切歌单标签） | `search 周杰伦` / `search 周杰伦 kw` |
| `openlist <源> <ID>` | 打开歌单页面 | `openlist kw 3373919903` |
| `playlist <源> <ID> [序号]` | 播放歌单（可选从第N首开始） | `playlist kw 3373919903` / `playlist kw 3373919903 5` |
| `searchPlay <歌名-歌手>` | 直接播放歌曲（无歌手则播放该艺术家热门曲目） | `searchPlay 晴天` / `searchPlay 晴天-周杰伦` |
| `play` | 播放 | `play` |
| `pause` | 暂停 | `pause` |
| `toggle` | 切换播放/暂停 | `toggle` |
| `next` | 下一首 | `next` |
| `prev` | 上一首 | `prev` |
| `status` | 显示播放状态 | `status` |
| `now` | 显示当前歌曲 | `now` |
| `lyric` | 显示歌词 | `lyric` |
| `volume <0-100>` | 设置音量 | `volume 80` |
| `mute` | 静音 | `mute` |
| `unmute` | 取消静音 | `unmute` |
| `collect` | 收藏 | `collect` |
| `uncollect` | 取消收藏 | `uncollect` |
| `dislike` | 不喜欢 | `dislike` |

**参数说明：**
- `<关键词>`: 搜索关键词（必填）。搜索歌曲/歌单时均可使用，结果在播放器内显示
- `[源]`: 音乐平台代码，可选。常见：`kw`(酷我), `kg`(酷狗), `tx`(腾讯), `wy`(网易), `mg`(咪咕)
- `<歌名>`: 歌曲名称（必填）。只有歌名时播放该歌曲或该艺术家热门曲目
- `[歌手]`: 歌手名，可选。传入时格式为 `歌名-歌手`，精确匹配播放
- `<关键词>`: 搜索关键词（必填）
- `[源]`: 音乐平台代码，可选。常见：`kw`(酷我), `kg`(酷狗), `tx`(腾讯), `wy`(网易), `mg`(咪咕)
- `<歌名>`: 歌曲名称（必填）。只有歌名时播放该歌曲或该艺术家热门曲目
- `[歌手]`: 歌手名，可选。传入时格式为 `歌名-歌手`，精确匹配播放
- `<源>`: 歌单来源平台（**必填，无法自动判断**）
- `<ID>`: 歌单ID或URL（必填）
- `[序号]`: 起始歌曲序号，从 1 开始

## 对话示例

### 播放/点播歌曲
```
用户：播放青花瓷
→ 执行: node {skill_dir}/cli/lx-music-cli.js searchPlay 青花瓷
→ 等待 500ms
→ 执行: node {skill_dir}/cli/lx-music-cli.js status
→ 汇报结果

用户：播放周杰伦的歌（无具体歌名，播放热门曲目）
→ 执行: node {skill_dir}/cli/lx-music-cli.js searchPlay 周杰伦
→ 等待 500ms
→ 执行: node {skill_dir}/cli/lx-music-cli.js status
→ 汇报结果

用户：点播陈奕迅的十年
→ 执行: node {skill_dir}/cli/lx-music-cli.js searchPlay 十年-陈奕迅
→ 等待 500ms
→ 执行: node {skill_dir}/cli/lx-music-cli.js status
→ 汇报结果
```

### 搜索歌曲/歌单
```
用户：搜索周杰伦的歌
→ 执行: node {skill_dir}/cli/lx-music-cli.js search 周杰伦
→ 等待 500ms
→ 执行: node {skill_dir}/cli/lx-music-cli.js status
→ 汇报: "已打开搜索页面，显示周杰伦的搜索结果，可在播放器内切换歌曲/歌单标签"

用户：找周杰伦的歌单
→ 执行: node {skill_dir}/cli/lx-music-cli.js search 周杰伦
→ 等待 500ms
→ 执行: node {skill_dir}/cli/lx-music-cli.js status
→ 汇报: "已打开搜索页面，显示周杰伦的搜索结果，请切换到歌单标签查看"

用户：播放歌单 3373919903
→ 用户未提供平台源 → 询问: "请指定歌单来源平台..."
→ 用户回复: "酷我"
→ 执行: node {skill_dir}/cli/lx-music-cli.js playlist kw 3373919903
→ 等待 500ms
→ 执行: node {skill_dir}/cli/lx-music-cli.js status
→ 汇报结果

用户：播放歌单 3373919903 从第5首开始
→ 执行: node {skill_dir}/cli/lx-music-cli.js playlist kw 3373919903 5
→ 等待 500ms
→ 执行: node {skill_dir}/cli/lx-music-cli.js status
→ 汇报结果

用户：打开网易歌单 987654321
→ 执行: node {skill_dir}/cli/lx-music-cli.js openlist wy 987654321
→ 等待 500ms
→ 执行: node {skill_dir}/cli/lx-music-cli.js status
→ 汇报: "已打开歌单页面"

用户：播放这个歌单 https://music.163.com/playlist?id=123456
→ 从 URL 识别: 网易云(wy) ID=123456
→ 执行: node {skill_dir}/cli/lx-music-cli.js playlist wy 123456
→ 等待 500ms
→ 执行: node {skill_dir}/cli/lx-music-cli.js status
→ 汇报结果
```

### 播放控制
```
用户：播放
→ 执行: node {skill_dir}/cli/lx-music-cli.js play
→ 等待 500ms
→ 执行: node {skill_dir}/cli/lx-music-cli.js status
→ 汇报结果
```

## 重要提示

1. **每个命令执行后必须查询状态并汇报**
2. **等待 500ms 后再查询** - 确保 LX Music 有时间响应
3. **如果 status 查询无有效反馈** - 提示用户 "API 未启动，请打开 API 功能（设置 → 开放 API → 启用开放 API 服务）"
4. **汇报格式必须使用 Markdown 表格**
5. **音量不显示** - 状态汇报不包含音量（API 返回不准确）
