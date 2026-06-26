---
name: lx-music-assistant
collection: root
version: 1.0.5
description: |
  控制洛雪音乐助手桌面版播放音乐。
  支持：搜索歌曲并唤醒程序、播放/暂停/切换、调节音量、查看播放状态和歌词、收藏歌曲、本地歌单查询。
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

API 地址和端口配置在 `{skill_dir}/cli/config.json`：

```json
{
  "host": "127.0.0.1",
  "port": 23330
}
```

- `host`: API 地址。`127.0.0.1` 或 `localhost` 表示本机；其他 IP 表示局域网
- `port`: Open API 端口

## 标准执行流程

每个命令执行后**必须**执行此流程：
1. 执行命令
2. 等待 500ms（确保 LX Music 有时间响应）
3. 查询状态：`node {skill_dir}/cli/lx-music-cli.js status`
4. 用 Markdown 表格汇报

## 常用命令

### 搜索（唤醒程序，在播放器内显示结果）

```bash
node {skill_dir}/cli/lx-music-cli.js search <关键词>        # 在播放器内显示搜索结果，可切换"歌曲"/"歌单"标签
node {skill_dir}/cli/lx-music-cli.js search <关键词> <源>    # 指定平台搜索
```

### 搜索并播放（直接播放，唤醒程序）

```bash
node {skill_dir}/cli/lx-music-cli.js searchPlay <歌名>              # 只有歌名：播放该歌曲或该艺术家热门曲目
node {skill_dir}/cli/lx-music-cli.js searchPlay <歌名> <歌手>       # 歌名+歌手：精确匹配播放
node {skill_dir}/cli/lx-music-cli.js searchPlay God is a girl      # 英文歌名含空格：自动 URL 编码，无需引号
```

### 智能播放（推荐）

当用户说"播放某某的歌"或"想听某某"时：

1. **认识歌手**：推荐代表作用 `searchPlay` 播放
   - 例："播放周杰伦" → `searchPlay 晴天 周杰伦`
   - 例："播放 God is a girl" → `searchPlay God is a girl`（自动 URL 编码）

2. **不认识歌手**：直接 `search` 搜索
   - 例："播放某某某" → `search 某某某`

3. **只给歌手名（无具体歌曲）**：推荐最知名的一首
   - 例："播放张学友" → `searchPlay 吻别 张学友`

### 播放控制

```bash
node {skill_dir}/cli/lx-music-cli.js play      # 播放
node {skill_dir}/cli/lx-music-cli.js pause     # 暂停
node {skill_dir}/cli/lx-music-cli.js toggle    # 切换播放/暂停
node {skill_dir}/cli/lx-music-cli.js next      # 下一首
node {skill_dir}/cli/lx-music-cli.js prev      # 上一首
node {skill_dir}/cli/lx-music-cli.js seek <秒> # 调整播放进度（单位：秒）
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

**⚠️ 音量 API 已知问题**：LX Music 启动后，音量参数未激活，API 返回 volume=0。需用户**手动拖动一次 LX Music 音量条**才能激活。激活前通过 API 设置音量不生效。每次查到 volume=0 时必须提醒用户：**请手动拖动 LX Music 音量条以激活参数**。

### 本地歌单查询

```bash
node {skill_dir}/cli/lx-music-cli.js list                           # 列出本地所有歌单
node {skill_dir}/cli/lx-music-cli.js listsongs <歌单ID>             # 查看歌单中的歌曲
node {skill_dir}/cli/lx-music-cli.js listplay <歌单ID>              # 播放本地歌单
```

**歌单 ID** 通过 `list` 命令获取，格式如 `tx_7939f091eb9f308211f7a3d562e35a98`。

- 数据库路径（Windows）：`%APPDATA%\lx-music-desktop\LxDatas\lx.data.db`
- 支持 `--db <路径>` 参数指定自定义数据库位置

### 在线歌单（唤醒程序）

```bash
node {skill_dir}/cli/lx-music-cli.js openlist <源> <歌单ID>            # 打开歌单页面（不自动播放）
node {skill_dir}/cli/lx-music-cli.js playlist <源> <歌单ID> [起始序号]  # 播放歌单（序号从1开始）
```

**⚠️ 在线歌单操作必须指定平台源，无法自动判断！** 用户未提供时必须询问。

**源代码**：`kw`(酷我), `kg`(酷狗), `tx`(腾讯/QQ), `wy`(网易), `mg`(咪咕)

**用户提供了歌单 URL 时，从中提取源和 ID：**
- 网易云：`https://music.163.com/playlist?id=987654321` → `wy 987654321`
- QQ音乐：`https://y.qq.com/n/ryqq/playlist/1234567890` → `tx 1234567890`
- 酷我：分享链接通常包含 `kw` 标识

### 收藏

```bash
node {skill_dir}/cli/lx-music-cli.js collect     # 收藏
node {skill_dir}/cli/lx-music-cli.js uncollect   # 取消收藏
node {skill_dir}/cli/lx-music-cli.js dislike     # 不喜欢
```

## 对话示例

### 播放歌曲
```
用户：播放青花瓷
→ 执行: searchPlay 青花瓷 → 等待 500ms → 查询 status → 汇报

用户：点播陈奕迅的十年
→ 执行: searchPlay 十年 陈奕迅 → 等待 500ms → 查询 status → 汇报

用户：播放郑秀文的歌
→ 我认识郑秀文，推荐《值得》
→ 执行: searchPlay 值得 郑秀文 → 等待 500ms → 查询 status → 汇报

用户：播放某某某的歌
→ 不认识 → 执行: search 某某某 → 等待 500ms → 查询 status → 汇报
```

### 搜索
```
用户：搜索周杰伦的歌
→ 执行: search 周杰伦 → 等待 500ms → 查询 status → 汇报: "已打开搜索页面，可在播放器内切换歌曲/歌单标签"
```

### 本地歌单查询
```
用户：查看我的歌单
→ 执行: list → 汇报歌单列表（名称、来源、歌曲数）

用户：看看周杰伦歌单里有什么
→ 执行: list → 获取歌单ID → 执行: listsongs <ID> → 汇报歌曲列表

用户：播放我的周杰伦歌单
→ 执行: list → 获取歌单ID → 执行: listplay <ID> → 等待 500ms → 查询 status → 汇报
```

### 在线歌单
```
用户：播放歌单 3373919903
→ 用户未提供平台源 → 询问: "请指定歌单来源平台：酷我(kw)、酷狗(kg)、QQ音乐(tx)、网易云(wy)、咪咕(mg)"
→ 用户回复: "酷我"
→ 执行: playlist kw 3373919903 → 等待 500ms → 查询 status → 汇报

用户：播放这个歌单 https://music.163.com/playlist?id=123456
→ 从 URL 识别: 网易云(wy) ID=123456
→ 执行: playlist wy 123456 → 等待 500ms → 查询 status → 汇报
```

### 播放控制
```
用户：下一首
→ 执行: next → 等待 500ms → 查询 status → 汇报
```

## 重要提示

1. **每个命令执行后必须查询状态并汇报**
2. **等待 500ms 后再查询** - 确保 LX Music 有时间响应
3. **如果 status 查询无有效反馈** - 提示用户 "API 未启动，请打开 API 功能（设置 → 开放 API → 启用开放 API 服务）"
4. **汇报格式必须使用 Markdown 表格**
5. **音量显示** - 状态汇报包含音量（API 返回准确）
6. **音量激活** - 每次查到 volume=0 时，提醒：**请手动拖动 LX Music 音量条以激活参数**
