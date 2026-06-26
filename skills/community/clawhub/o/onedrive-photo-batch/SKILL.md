---
name: onedrive-photo-batch
description: OneDrive 照片批处理与索引技能。用于对 OneDrive 照片做按名称/日期/大小/格式/相册筛选、批量 OCR/多模态识别、full 全量索引、哈希增量跳过、语义检索、移动/上传/删除/恢复与回收站治理。用户提到 OneDrive 批量识别、照片索引、相册级模型策略、限速并发、删除恢复、15天回收站清理时触发。
---

# OneDrive Photo Batch

## Overview

使用 `scripts/onedrive_photo_batch.py` 执行 OneDrive 照片批处理。
保持“云端为主、临时落地、索引持久化”的原则：仅在处理时临时下载，识别后立即删除临时文件；删除云端照片时（非 hard）保存回收副本到 `tmp_photo/`。

## Hard Rules

1. 默认不长期保留云端照片本地副本。
2. 执行 `full` 时，每张照片完成识别并写入索引后，立即删除本地临时文件。
3. 删除云端照片时，除非显式 `--hard`，否则必须写入本地回收站 `tmp_photo/`。
4. 本地索引对删除照片使用逻辑删除（`logical_deleted=1`），不物理清空索引主体。
5. 每次运行技能前，静默执行 15 天回收站清理：删除超期本地回收副本。

## Required Files

- Runtime script: `scripts/onedrive_photo_batch.py`
- Config template: `references/config.example.json`

## Runtime Requirement (必须)

- 本技能依赖 `msal` 等 Python 包，**必须在已安装依赖的虚拟环境中运行**。
- 不要默认使用系统 `python3` 直接执行（可能报 `缺少依赖 msal`）。
- 推荐解释器：`/root/.openclaw/workspace/tmp/onedrive-demo-venv/bin/python`

示例：

```bash
/root/.openclaw/workspace/tmp/onedrive-demo-venv/bin/python \
  /root/.openclaw/workspace/skills/onedrive-photo-batch/scripts/onedrive_photo_batch.py \
  --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json search --limit 1
```

复制配置模板并填写真实值，例如：

```bash
cp /root/.openclaw/workspace/skills/onedrive-photo-batch/references/config.example.json /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json
```

## Command Quickstart

### 1) 云端筛选检索

```bash
python3 scripts/onedrive_photo_batch.py --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json \
  search --name "invoice" --name-mode fuzzy --formats jpg,png --limit 20
```

### 2) 全量索引（支持筛选、并发、限速、模型策略）

```bash
python3 scripts/onedrive_photo_batch.py --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json \
  full --parallel 2 --max-download-kbps 2048 --batch nightly_full
```

### 3) 语义检索 / 关键词精确检索

语义检索：

```bash
python3 scripts/onedrive_photo_batch.py --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json \
  search --semantic-query "带香港理工大学招聘信息的海报" --limit 10
```

关键词精确检索（命中 OCR/summary 原文，适合“必须包含某词”）：

```bash
python3 scripts/onedrive_photo_batch.py --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json \
  search --keyword "产品经理" --keyword-mode exact --keyword-field all --limit 20
```

### 4) 删除与回收站

软删除（默认，进入 `tmp_photo/`）：

```bash
python3 scripts/onedrive_photo_batch.py --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json \
  delete --name "old" --name-mode fuzzy --limit 5
```

硬删除（不进入回收站）：

```bash
python3 scripts/onedrive_photo_batch.py --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json \
  delete --name "old" --hard --limit 5
```

恢复（15天内）：

```bash
python3 scripts/onedrive_photo_batch.py --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json \
  restore --limit 10
```

清空回收站：

```bash
python3 scripts/onedrive_photo_batch.py --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json \
  trash-empty
```

### 5) 移动/上传/导出

```bash
python3 scripts/onedrive_photo_batch.py --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json \
  move --album "/Pictures/Inbox" --album-mode exact --target-album-path "/Pictures/Archive" --limit 20

python3 scripts/onedrive_photo_batch.py --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json \
  upload --target-album-path "/Pictures/Inbox" /path/a.jpg /path/b.png

python3 scripts/onedrive_photo_batch.py --config /root/.openclaw/workspace/tmp/onedrive_photo_batch/config.json \
  export --format csv --out /root/.openclaw/workspace/tmp/onedrive_photo_batch/export.csv
```

## Notes

- 默认配置是只读验收模式：`mode.read_only=true`，会屏蔽 `delete/restore/trash-empty/move/upload`。
- 需要启用写操作时，显式将配置改为：`mode.read_only=false`，并把 `auth.scopes` 升级到 `Files.ReadWrite`。
- 为了低性能主机可用，优先通过 `--parallel` 与 `--max-download-kbps` 控制负载。
- vNext 新增稳态参数（`performance`）：
  - `api_retry`：下载/API 调用重试次数
  - `backoff_sec`：重试退避基数秒
  - `download_timeout_sec`：下载超时时间（秒）
- 模型节流在配置中通过 `ocr.default_interval_sec` 与 `ocr.model_intervals_sec` 控制。
- 相册模型覆盖与批次模型覆盖在配置中通过 `ocr.album_overrides` 和 `ocr.batch_overrides` 定义。
- vNext 增加 preflight：运行前会检查关键配置与依赖，错误统一返回 JSON（`ok=false, error.code/message`）。
