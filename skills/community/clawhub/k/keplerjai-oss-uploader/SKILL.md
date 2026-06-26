---
name: keplerjai-oss-uploader
description: 将本地文件上传到阿里云 OSS 并输出 bindHost 下的可访问 URL。用户提到 OSS 上传、静态资源、keplerjai OSS 时使用。
metadata:
  openclaw:
    emoji: "📤"
    always: true
    requires:
      bins:
        - python
---

# keplerjai OSS 上传（技能摘要）

**详细说明、环境变量表、安全与 OpenClaw 配置示例见同目录 `README.md`（人读文档；本文件刻意保持短小以降低技能加载 token）。**

## 环境变量前缀

必填：`KEPLERJAI_OSS_ACCESS_KEY_ID`、`KEPLERJAI_OSS_ACCESS_KEY_SECRET`、`KEPLERJAI_OSS_ENDPOINT`、`KEPLERJAI_OSS_BUCKET`。其余见 `README.md` 或 `config.example.env`；`config.json` 可补全非密钥项（`skill_config` 合并，shell 已设变量优先）。

## 上传命令（`{baseDir}` 为本技能根目录）

```bash
pip install -r "{baseDir}/requirements.txt"
python "{baseDir}/scripts/upload_to_oss.py" "/path/to/file.png"
```

常用：`--flat` 扁平随机名；`-k` 指定对象键；`--dry-run` 仅打印 key/URL；`--sync-lifecycle` 上传后写入生命周期（需天数配置与 RAM 权限）。

## Agent 要点

1. 密钥只经 env / SecretRef 注入，**不写进对话与 SKILL 正文**。
2. 上传成功后把脚本输出的 `public_url` 给用户。
3. 生命周期运维：`python "{baseDir}/scripts/put_bucket_lifecycle.py"`（详见 `README.md`）。

## OpenClaw

在 `skills.entries` 中使用键名 **`keplerjai-oss-uploader`**，与 `name` 字段一致；`env` 键名与上表 `KEPLERJAI_OSS_*` 一致。完整 JSON 片段见 `README.md`。

## 返回形式
以[可读文件名](url)的方式返回文件下载链接