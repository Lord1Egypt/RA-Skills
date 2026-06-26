---
name: ielts-review-upload
description: "上传雅思阅读复盘文件到服务器，查看个人进步趋势。当用户想要上传已有的复盘文件（JSON）到云端，或者查看个人复盘仪表板时使用。触发词：上传复盘、上传复盘文件、sync review、upload review、查看我的复盘记录、我的仪表板、dashboard。"
---

# IELTS Review Upload Skill

## Purpose

上传已有的雅思阅读复盘数据（JSON）到云端服务器，并在个人仪表板上查看所有复盘记录和进步趋势。

## ⚠️ 重要提示：告知用户查看结果的入口

**上传完成后，必须明确告知用户去哪里看复盘结果：**

🔗 **在线阅读复盘首页：https://tuyaya.online/ielts/reading.html**

在这里可以：
- 查看所有历史复盘记录（按时间排列）
- 查看进步趋势图表
- 跨设备访问（手机/电脑都能看）

每次上传完成后，回复中必须包含仪表板链接。

## When to Activate

- 用户说"上传复盘"、"上传复盘文件"
- 用户说"sync review"、"upload review"
- 用户想查看个人复盘仪表板
- 用户说"查看我的复盘记录"、"我的仪表板"

## Workflow

### Step 1: Collect Input

询问用户要上传的 JSON 数据文件路径。

**JSON 文件格式要求**：
```json
{
  "book": 5,
  "test": 4,
  "passage": 1,
  "score": 11,
  "total": 13,
  "date": "2026-04-09",
  "band": "6.5-7.0",
  "timeSpent": "34:10",
  "wrongQuestions": [3, 7, 12],
  "errorCategories": ["synonym_failure", "over_inference"]
}
```

### Step 2: Run Upload Script

运行上传脚本：

```bash
bash scripts/sync-review.sh <path-to-data.json>
```

**脚本功能**：
- 自动生成稳定的匿名用户 ID（基于机器的 hostname + username 的 SHA256 哈希）
- 上传数据到私有后端（需要 API key 认证）
- 打印个性化仪表板 URL

**如果脚本不存在**：
从当前 Skill 目录复制，或者从 GitHub 下载：
```bash
curl -o scripts/sync-review.sh https://raw.githubusercontent.com/dengjiawei1226/ielts-reading-review/main/scripts/sync-review.sh
chmod +x scripts/sync-review.sh
```

### Step 3: Return Dashboard URL

上传完成后，告诉用户他们的仪表板 URL：

**首次用户**：
```
✅ 上传成功！

你的个人复盘仪表板：
https://tuyaya.online/ielts/reading.html?user=xxx&key=xxx

建议收藏这个链接，方便随时查看你的进步趋势。
```

**返回用户**：
```
✅ 上传成功！已同步到你的仪表板。

查看所有复盘记录：
https://tuyaya.online/ielts/reading.html?user=xxx&key=xxx
```

### Step 4: View Dashboard (Optional)

如果用户想立即查看仪表板，可以：
1. 打开浏览器访问仪表板 URL
2. 或者生成二维码方便手机访问

## Configuration

### API Key

脚本中已内置默认的 API key：`ielts_8b0832b3cfd38884e44ab26ee68acaeed294623ef8da9b201871a7768b072606`

如果需要更换 API key，编辑 `scripts/sync-review.sh` 文件，修改 `API_KEY` 变量。

### Backend URL

默认后端 URL：`https://tuyaya.online/ielts-api`

如果需要更换，编辑 `scripts/sync-review.sh` 文件，修改 `API_BASE` 变量。

### User ID Generation

用户 ID 是自动生成的，基于：
- 机器的 hostname
- 当前用户名

生成算法：
```bash
echo -n "$(hostname)-$(whoami)" | shasum -a 256 | cut -c1-16
```

同样的机器总是生成同样的用户 ID。

## Reference Files

| File | Purpose |
|------|---------|
| `scripts/sync-review.sh` | 上传脚本（bash） |

## Troubleshooting

### "file not found" Error

确保你提供的 JSON 文件路径是正确的。

### "Upload failed" Error

检查：
1. 网络连接是否正常
2. API key 是否有效
3. 后端服务器是否可访问

### "JSON file must contain..." Error

确保你的 JSON 文件包含必要的字段：`book`, `test`, `passage`, `score`, `total`

## Style Guidelines

- 简洁直接 — 不要多余的解释
- 功能导向 — 每个句子都应该帮助用户完成上传
- 中文是主要语言，英文术语保留原样
- 上传完成后，总是提供仪表板 URL
