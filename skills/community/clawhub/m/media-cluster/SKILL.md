---
name: media-cluster
description: Crawls social media by search keyword (MediaCrawler: 小红书/抖音/微博/B站等), summarizes content and outputs report plus short voice summary. User gives one sentence only (e.g. “爬一下小红书关键词比特币并总结”); agent runs full workflow automatically—env setup, crawl, report, TTS. Use when the user asks to search/crawl a topic on Chinese social platforms and summarize.
---

# Media Cluster – 社交平台关键词爬取与总结

**路径约定**：文中 `{baseDir}` 表示本技能所在目录（media-cluster 技能根目录）。Agent 执行命令时需将 `{baseDir}` 替换为实际路径。

基于 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 按「搜索关键词」爬取社交平台内容，汇总有哪些内容，并生成报告与简洁版语音总结。爬虫结果保存在 `{baseDir}/MediaCrawler/data/` 下。

## 使用者一句话指令（仅文本输入）

使用者只需输入一句自然语言，例如：

- 「帮我爬一下小红书关键词比特币，并总结」
- 「搜一下抖音上关于 AI 的内容并出报告」
- 「微博搜“编程副业”爬取并语音总结」

**Agent 收到此类请求后，应自动完成全流程**（无需用户再执行任何命令）：

1. **首次执行时下载 MediaCrawler**：若 `{baseDir}/MediaCrawler` 目录不存在，则先执行 `{baseDir}/scripts/ensure_mediacrawler.sh` 或手动 `git clone https://github.com/NanmiCoder/MediaCrawler.git {baseDir}/MediaCrawler`（将 `{baseDir}` 换为实际路径），然后再进行后续步骤。
2. **解析**：从用户文本中识别**平台**（小红书/xhs、抖音/dy、微博/wb、B站/bili、快手/ks、贴吧/tieba、知乎/zhihu）和**搜索关键词**；若未指明平台则默认小红书（xhs）。
3. **环境**：若尚未配置，先执行 `scripts/setup_env.sh`（或等价 conda create + pip install + playwright install）；否则跳过。
4. **爬取**：在 `MediaCrawler` 目录下执行 `python main.py --platform <平台> --lt qrcode --type search --keywords "<关键词>" --save_data_option jsonl`；提示用户首次需扫码登录。
5. **报告与语音**：爬取结束后执行 `scripts/summarize_and_voice.py`，带上对应的 `--platform`、`--keyword`，并加上 `--voice` 生成简洁版语音总结；将报告路径与语音稿内容回复给用户。

使用者只需一次文本输入，其余由 Agent 按上述步骤完成。

## 前置条件

- **Conda**：用于创建并激活 `media-cluster` 环境。
- **Node.js**：>= 16（爬抖音、知乎时需要）。  
- 工具已位于：`{baseDir}/MediaCrawler`。
- **语音总结（TTS）**：需在环境变量中配置 `SENSEAUDIO_API_KEY`（[接口密钥](https://senseaudio.cn/platform/api-key)）；可选 `SENSEAUDIO_VOICE_ID`。

## 0. 首次执行：下载 MediaCrawler

若本地尚未有 MediaCrawler 项目，需先从 GitHub 拉取到技能目录下。执行时将 `{baseDir}` 替换为实际技能根路径：

```bash
# macOS/Linux：使用脚本（推荐，会检测目录是否存在再克隆）
bash {baseDir}/scripts/ensure_mediacrawler.sh

# 所有平台（macOS/Windows/Linux）：手动克隆
git clone https://github.com/NanmiCoder/MediaCrawler.git {baseDir}/MediaCrawler
```

完成后目录结构为：`{baseDir}/MediaCrawler/`（含 `main.py`、`config/`、`requirements.txt` 等）。之后再执行环境配置与爬取。

## 1. 环境配置（首次或环境异常时执行）

以下命令适用于所有平台（macOS / Windows / Linux），在终端或命令提示符中执行：

```bash
# 创建 conda 环境（Python 3.11）
conda create -n media-cluster python=3.11 -y

# 激活环境
conda activate media-cluster

# 进入 MediaCrawler 目录
cd {baseDir}/MediaCrawler

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器驱动
playwright install
```

macOS/Linux 也可直接执行技能提供的脚本（将 `{baseDir}` 换为实际路径）：

```bash
bash {baseDir}/scripts/setup_env.sh
```

## 2. 爬取流程

### 2.1 确定参数

- **平台** `--platform`：`xhs`（小红书）| `dy`（抖音）| `ks`（快手）| `bili`（B站）| `wb`（微博）| `tieba`（贴吧）| `zhihu`（知乎）。
- **搜索关键词** `--keywords`：一个或多个，英文逗号分隔，如 `比特币` 或 `比特币,以太坊`。
- **爬取类型**：本技能使用关键词搜索，即 `--type search`。
- **登录方式**：默认 `--lt qrcode`（扫码登录）；首次运行会弹出浏览器，用对应 APP 扫码。

### 2.2 执行爬虫

先激活环境，再进入 `{baseDir}/MediaCrawler` 运行：

```bash
conda activate media-cluster
cd {baseDir}/MediaCrawler

# 示例：小红书搜索「比特币」
python main.py --platform xhs --lt qrcode --type search --keywords "比特币" --save_data_option jsonl
```

数据默认写入 MediaCrawler 下的 `data/`，即 `{baseDir}/MediaCrawler/data/<platform>/`。如需指定绝对路径，可加 `--save_data_path <绝对路径>`。

### 2.3 可选参数（按需）

- `--save_data_option jsonl`：推荐 jsonl，便于后续解析。
- `--get_comment yes/no`：是否爬评论，默认从 `config/base_config.py` 读取。
- `--save_data_path <path>`：自定义数据目录；不填则用默认 `data/`。

## 3. 报告与语音总结

爬取完成后：

1. **读数据**：从 `{baseDir}/MediaCrawler/data/<platform>/` 下读取最新生成的 jsonl（或 json/csv，视 `--save_data_option`）。
2. **生成报告**：  
   - 统计条数、关键词/平台、时间范围。  
   - 按主题/类型归纳「有哪些内容」（标题、摘要、作者、互动数等）。  
   - 小红书笔记示例字段：`note_id`, `type`, `title`, `desc`, `user_id`, `nickname`, `liked_count`, `collected_count`, `comment_count`, `share_count`, `ip_location`, `tag_list`, `note_url`, `source_keyword` 等。
3. **输出**：  
   - 写一份 **Markdown 报告** 到技能目录或用户指定路径（如 `media_cluster_report_<关键词>_<日期>.md`）。  
   - 生成一份 **简洁版语音稿**（3–5 句话）：概括平台、关键词、条数、主要几类内容。  
   - **语音输出**：使用 [SenseAudio API](https://senseaudio.cn/docs/) 将语音稿合成并保存为 mp3（可选播放）。需在环境变量中配置 `SENSEAUDIO_API_KEY`（在 [接口密钥](https://senseaudio.cn/platform/api-key) 创建）；可选 `SENSEAUDIO_VOICE_ID`。

报告结构建议：

```markdown
# 媒体爬取报告：<关键词>

- **平台**：<platform>
- **关键词**：<keywords>
- **爬取条数**：<count>
- **数据时间**：<时间范围>

## 内容概览
（按主题/类型归纳，列出代表性标题与摘要）

## 明细（可选）
（表格或列表：标题、作者、互动、链接等）
```

## 4. 小红书结果示例（JSON 单条）

爬虫得到的小红书笔记可能形如：

```json
{
  "note_id": "68f0ae5b0000000003020914",
  "type": "normal",
  "title": "原以为比特币绝对安全呢",
  "desc": "比特币不是去中心化吗？美国司法部是怎么没收...",
  "video_url": "",
  "time": 1760603739000,
  "user_id": "60337046000000000101fd66",
  "nickname": "贝格尔号",
  "liked_count": "1308",
  "collected_count": "963",
  "comment_count": "664",
  "share_count": "573",
  "tag_list": "",
  "note_url": "https://www.xiaohongshu.com/explore/...",
  "source_keyword": "比特币"
}
```

总结时重点用：`title`, `desc`, `nickname`, `liked_count`, `comment_count`, `source_keyword`。

## 5. 脚本说明

| 脚本 | 用途 |
|------|------|
| `scripts/ensure_mediacrawler.sh` | （macOS/Linux）首次执行时若不存在 `MediaCrawler` 目录，则从 GitHub 克隆到技能目录下；Windows 请直接 `git clone`。 |
| `scripts/setup_env.sh` | （macOS/Linux）创建 conda 环境、安装依赖与 Playwright；Windows 请按「环境配置」小节手动执行 conda/pip 命令。 |
| `scripts/summarize_and_voice.py` | 读取 `MediaCrawler/data/` 下数据，生成 Markdown 报告与简短语音稿，并用 SenseAudio API 合成语音（需环境变量 `SENSEAUDIO_API_KEY`）。 |

调用示例（将 `{baseDir}` 换为实际路径）：

```bash
conda activate media-cluster
python {baseDir}/scripts/summarize_and_voice.py \
  --data-dir {baseDir}/MediaCrawler/data \
  --platform xhs \
  --keyword "比特币" \
  --report report.md \
  --voice
# 可选：--voice-id <音色ID>、--voice-out <输出mp3路径>；API 文档 https://senseaudio.cn/docs/
```

## 6. 注意事项

- 仅用于学习与研究，遵守平台条款与法律法规。  
- 首次运行需扫码登录；登录态可被缓存，后续可减少扫码。  
- 若遇反爬或验证码，可尝试关闭无头模式（在 `config/base_config.py` 中设置 `HEADLESS = False`）。  
- 抖音/知乎需本机已安装 Node.js >= 16。  
- **语音总结**：TTS 使用 SenseAudio API，需在环境变量中配置 `SENSEAUDIO_API_KEY`（在 [senseaudio.cn 接口密钥](https://senseaudio.cn/platform/api-key) 创建）；可选 `SENSEAUDIO_VOICE_ID`。API 文档见 <https://senseaudio.cn/docs/>。

## 7. 参考

- MediaCrawler 用法与配置：[MediaCrawler/README.md](MediaCrawler/README.md)  
- 数据存储与字段说明见项目 `docs/data_storage_guide.md`（若有）。  
- 语音合成（TTS）：[SenseAudio API 文档](https://senseaudio.cn/docs/)、[语音合成 API](https://senseaudio.cn/docs/text_to_speech_api)、[接口密钥](https://senseaudio.cn/platform/api-key)。
