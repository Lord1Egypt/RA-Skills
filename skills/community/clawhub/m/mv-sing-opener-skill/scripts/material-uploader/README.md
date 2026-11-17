# 素材上传器 · Material Uploader

把 **`assets/source/`**（或 `--src` 指定路径）里的素材（含子文件夹）**原样复制**一份到 `/var/www/public/mv`，
**目标目录/文件已存在时默认直接覆盖**（先整目录删除再写入，避免旧文件残留），
把**外网路径**回显到终端，并在**上传成功后默认清空整个源目录**（文件 / 子目录 / 清单全部删除）；
源目录清空后若已空、且它不是暂存目录 `assets/source` 本身，则**连源目录本身也一起删掉**
（用 `--src` 指到项目文件夹时，传完整个项目文件夹消失，只留 `assets/source/`）。
只做上传素材：不下载、不出图、不剪片。

## 快速开始

```bash
cd scripts/material-uploader

# 1) 把要上传的素材（含子文件夹）放进 assets/source/
# 2) 先预览（会列出将覆盖的目标目录）
python3 upload_assets.py --dry-run
# 3) 正式上传（默认源=assets/source，不保留 source 这层；目标已存在则直接覆盖；上传成功后清空整个源目录）
python3 upload_assets.py
#    推荐：--src 指到项目文件夹，URL 命名空间＝项目文件夹名，传完文件夹被删掉
python3 upload_assets.py --src "assets/source/M02-chepiao"
#    想保留源目录的空文件夹壳：python3 upload_assets.py --keep-src-dir
#    想全保留（源文件+清单）：python3 upload_assets.py --keep-source
#    只保留清单、不清空目录：python3 upload_assets.py --no-purge-project
#    已存在就跳过、不覆盖：python3 upload_assets.py --no-overwrite-dir
# 4) 只清空 assets/source/（不上传，清完即退出）：python3 upload_assets.py --clear-source
```

外链：上传成功后在终端以 `外链清单（N 条）` 回显（默认清空项目 → 清单不落盘）。

源目录：默认在上传成功后**清空**；清空后若源目录已空、且不是 `assets/source` 本身，**连目录本身也删掉**
（所以 `--src` 指的项目文件夹会整个消失，只剩 `assets/source/`）。想保留空壳用 `--keep-src-dir`；
`--keep-source` 全保留（文件+清单），`--no-purge-project` 只保清单不清空目录。

## 已存在目标 → 默认直接覆盖

重传同一个项目时，目标目录已经存在，**默认整目录覆盖**（先删旧目录再写入），旧的多余/已改名文件不会残留：

| 场景 | 默认行为 |
|------|----------|
| 目标下有本次上传的同名目录（如 `第3期/`） | 整目录删除后重写 |
| 有独立目标目录（`--prefix`，目标目录 ≠ `/var/www/public/mv`） | 整个目标目录覆盖 |
| 目标下已存在同名文件 | 直接重写 |
| 与本次上传无关的文件/目录 | 不动，原样保留 |

安全护栏：**永远不会删除 `/var/www/public/mv` 本身，也不会删除 `/var/www/public/mv` 之外的路径**。
不想覆盖（已存在就跳过）：`--no-overwrite-dir`；`--dry-run` 会先列出将覆盖的目录。

## 映射规则

```
assets/source/第3期/图片/a.png
        │  复制（层级一致，不保留「source」这层）
        ▼
/var/www/public/mv/第3期/图片/a.png
外链 https://your-static-host.example.com/public/mv第3期/图片/a.png
```

外链 = 外链根 + 目标路径去掉 `/var/www/public/mv` 后的部分。
想让 URL 有一级文件夹名，就在 `assets/source/` 里建那样一层（如 `第3期/`）。

上传**其它路径**时用 `--src`（此时默认**保留源文件夹名**，可用 `--strip-root` 去掉）：

```
源   /x/我的项目/素材/图片/a.png
目标 /var/www/public/mv/素材/图片/a.png
外链 https://your-static-host.example.com/public/mv素材/图片/a.png
```

把项目文件夹当命名空间（推荐），传完该文件夹会被清掉：

```
--src ".../material-uploader/assets/source/M02-chepiao"
目标 /var/www/public/mv/M02-chepiao/...
外链 https://your-static-host.example.com/public/mvM02-chepiao/...
传完 assets/source/ 里只剩 .gitkeep（M02-chepiao/ 连文件夹一起删除）
```

## 常用参数

| 参数 | 说明 |
|------|------|
| `--src` | 源路径（文件夹或单文件）；不写则用 `assets/source/` |
| `--prefix` | 加命名空间文件夹（多项目隔离，如 `--prefix 第3期`） |
| `--strip-root` | 不保留源文件夹名（`assets/source` 默认即此行为） |
| `--overwrite-dir` / `--no-overwrite-dir` | 目标目录已存在时**默认整目录覆盖** / 关闭覆盖（已存在则跳过） |
| `--overwrite` | 覆盖已存在文件（默认已覆盖；用于 `--no-overwrite-dir` 时） |
| `--clear-source` | 仅清空源目录内容（**始终保留目录本身**），不做上传，清完退出（别名 `--clear`） |
| `--keep-source` | 上传成功后保留源素材（默认：上传成功后删除源素材） |
| `--purge-project` / `--no-purge-project` | 上传成功后**清空整个源目录**（源目录若因此变空、且非暂存目录，连目录本身也删）/ 关闭清空（默认开） |
| `--keep-src-dir` / `--rm-src-dir` | 保留源目录空壳 / 连源目录本身一起删（默认删） |
| `--ext` | 只传指定扩展名，如 `--ext .mp4,.png` |
| `--url-encode` | 外链百分号编码（中文/空格转义） |
| `--verify` | 复制后 HEAD 核验外链可达性 |
| `--json` | 额外生成结构化 JSON 清单 |
| `--dry-run` | 只预览 |

完整参数见 `python3 upload_assets.py --help`。

## 配置（`config.json`）

| 键 | 默认 |
|----|------|
| `source_dir` | `assets/source` |
| `dest_dir` | `/var/www/public/mv` |
| `url_base` | `https://your-static-host.example.com/public/mv` |
| `keep_root` | `true`（仅对显式 `--src` 生效） |
| `skip_hidden` | `true` |
| `keep_source` | `false`（设为 `true` 则上传后保留源素材） |
| `purge_project` | `true`（设为 `false` 则不做项目清空，保留目录与清单） |
| `keep_src_dir` | `false`（设为 `true` 则清空后保留源目录空壳，不删目录） |
| `overwrite_dir` | `true`（设为 `false` 则目标已存在时跳过，不整目录覆盖） |
| `manifest_name` | `素材外网路径` |

## 目录结构

```
material-uploader/
├── README.md
├── config.json
├── config.example.json
├── assets/source/          # ★ 素材放这里
└── upload_assets.py
```

## 清空源目录（独立功能）

不做上传，只把 `assets/source/`（或 `--src` 指定目录）里的文件/子目录/清单/隐藏文件全部删除，
**始终保留目录本身**（`.gitkeep` 也会被保留），清完即退出。
⚠️ 与上传流程不同：上传流程默认会连"清空后已空"的源目录本身一起删，此独立模式不删目录。

```bash
python3 upload_assets.py --clear-source          # 清空 assets/source/
python3 upload_assets.py --clear-source --dry-run # 先预览
python3 upload_assets.py --src "/x/素材" --clear-source  # 清空任意目录
```

## 说明与边界

- 标准库实现，零依赖，Python 3.8+。
- `copy2` 原样复制（保留时间等元数据）；**目标目录/文件已存在时默认直接覆盖**，**上传成功后默认清空整个源目录**，且源目录清空后若已空、又是 `--src` 指的项目文件夹，**连目录本身也删掉**（只删空目录）；加 `--keep-source` 可全保留（文件+清单），`--keep-src-dir` 可只保留空壳。
- 覆盖有护栏：**不删 `/var/www/public/mv` 本身，也不删 `/var/www/public/mv` 之外的路径**；与本次上传无关的文件原样保留。`--no-overwrite-dir` 可退回「已存在就跳过」。
- 开了 `--verify` 时，外链核验未通过的源文件会保守保留，不会被删。
- `--keep-source` 与项目清空互斥：保留源时不删。
- 默认跳过 `.DS_Store` 等隐藏文件，并自动忽略清单文件本身。
- 运行环境里 `/var/www/public/mv` 应是站点映射到 `https://your-static-host.example.com/public/mv` 的那个目录。
- **外链默认做百分号编码**（`--no-url-encode` 可关）：路径含中文时，裸中文 URL 很多服务端会直接 404。
- **传全量前先跑 `--probe`**：只写一个 1KB 探测文件并 HEAD 它的外链，打印「磁盘落点 / 目标 URL / 命名空间」三行对照；404=磁盘与 URL 不同层，403=被鉴权挡，`ERR:UnicodeEncodeError`=URL 没编码。

```bash
# 先探测落点（几秒，不传全量）
python3 upload_assets.py --src "/x/项目" --probe
# 通过后再传
python3 upload_assets.py --src "/x/项目" --url-encode --verify
```

