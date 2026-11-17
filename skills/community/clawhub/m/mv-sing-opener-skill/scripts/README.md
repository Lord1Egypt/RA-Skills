# scripts · 速查

本 skill 的脚本只做“把素材/JSON 变成文件”，不做创作。创作在 `SKILL.md` 的 ①–④ 站完成（任务解读 / 方案 / 钩子 / 歌词）。

## 0. 环境

```bash
pip install -r requirements.txt    # requests
brew install ffmpeg                # macOS；需要 ffmpeg / ffprobe
```

首次使用：

```bash
cp env.example .env
# 编辑 .env：NEWAPI_IMAGE_KEY / ASSET_URL_BASE / ASSET_DEST_DIR / VIDEO_GATEWAY_BASE
```

`.env` 已被 `.gitignore` 忽略，脚本启动时会自动读取。
网关默认 `http://127.0.0.1:4000`，模型 `doubao-seedance-2-5-260628`。

## 1. 新建项目

```bash
python3 scripts/new_project.py --slug xiaoyu --duration 30 --image ~/Desktop/me.jpg
```

无图时去掉 `--image`，先按 `references/05-素材与上传.md` 出默认风格参考图。

## 2. 出参考图（仅无图时）

项目根写 `文生图提示词.json`，然后：

```bash
python3 scripts/generate_images.py --project assets/output/MV01-xiaoyu --dry-run
python3 scripts/generate_images.py --project assets/output/MV01-xiaoyu --yes
```

默认一次一张；接口不可用时写 `04-图片/generate_image参数.json` 并退出 6，按清单走工具出图后：

```bash
python3 scripts/generate_images.py --project assets/output/MV01-xiaoyu --adopt <图片路径>
```

## 3. 上传（硬门）

```bash
# ② 站：JSON 还没写也能传（自动上传 04-图片/ 全部）
python3 scripts/upload_project.py assets/output/MV01-xiaoyu --verify

# ④ 站：写完 JSON 后回填直链（不重传）
python3 scripts/upload_project.py assets/output/MV01-xiaoyu --fill-only
python3 scripts/upload_project.py assets/output/MV01-xiaoyu --verify-json
```

要求 `❌ 0 条`；命名空间＝项目文件夹名；清单保存到 `03-上传/素材外网路径.json`。

## 4. 质检（写 JSON 后）

```bash
python3 scripts/qa.py assets/output/MV01-xiaoyu
```

出片后：

```bash
python3 scripts/qa.py assets/output/MV01-xiaoyu --require-clip --verify-links
```

## 5. 出片

```bash
python3 scripts/generate_video.py assets/output/MV01-xiaoyu/04-提示词/分镜JSON.json --dry-run
python3 scripts/generate_video.py assets/output/MV01-xiaoyu/04-提示词/分镜JSON.json
```

落点：`05-成片/S01.mp4`。重出：`--only S01`。

## 6. 合成 / 字幕

```bash
python3 scripts/assemble.py assets/output/MV01-xiaoyu
python3 scripts/assemble.py assets/output/MV01-xiaoyu --subtitle
python3 scripts/assemble.py assets/output/MV01-xiaoyu --subtitle --burn
```

落点：`05-成片/成片.mp4`（+ `字幕.srt`）。

## 7. 辅助

```bash
# 只补/改直链（一般不需要，upload_project --fill-json 已做）
python3 scripts/link_assets.py assets/output/MV01-xiaoyu --dry-run
python3 scripts/link_assets.py assets/output/MV01-xiaoyu --verify

# 图片接口自检
python3 scripts/test_image_api.py
```

## 文件职责

| 文件 | 职责 |
|---|---|
| `new_project.py` | 建项目骨架、复制图片、写状态/需求卡/过程记录、登记 |
| `log_step.py` | 追加过程记录、同步状态与项目登记（每站必跑） |
| `generate_images.py` | 无图时出参考图（一次一张） |
| `upload_project.py` | 上传 `04-图片/`、回填/核验 `refs_urls` |
| `generate_video.py` | 读 `分镜JSON.json` 单镜出片（`generate_audio` 默认 true） |
| `assemble.py` | 精确裁秒、生成/烧字幕、输出 `成片.mp4` |
| `qa.py` | 单镜/时长/音轨/歌词/直链机械校验 |
| `_common.py` | 路径与配置公共层 |
| `link_assets.py` | 直链补全/回退（辅助） |
| `material-uploader/` | 内置上传器 |
