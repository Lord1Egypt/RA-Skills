# ZingAPI 创意列表查询使用示例

本文档提供环境变量配置、常用查询命令和原始请求体示例。

## 配置凭证

PowerShell：

```powershell
$env:ZINGAPI_ACCESS_KEY_ID="your-access-key-id"
$env:ZINGAPI_ACCESS_KEY_SECRET="your-access-key-secret"
$env:ZINGAPI_CUSTOMER_NAME="your-customer-name"
```

Linux/macOS：

```bash
export ZINGAPI_ACCESS_KEY_ID="your-access-key-id"
export ZINGAPI_ACCESS_KEY_SECRET="your-access-key-secret"
export ZINGAPI_CUSTOMER_NAME="your-customer-name"
```

## 查询日本近 7 天游戏图片和视频创意

```powershell
python scripts/creative_list.py `
  --app-type 游戏 `
  --geo 日本 `
  --creative-type 图片,视频 `
  --seen-days 7 `
  --sort 最新 `
  --page-size 20
```

## 查询美国 Facebook 游戏视频创意并返回 AI 标签

```powershell
python scripts/creative_list.py `
  --app-type 游戏 `
  --platform Facebook `
  --geo 美国 `
  --creative-type 视频 `
  --seen-days 30 `
  --sort 最新 `
  --page-size 10 `
  --include-ai-tags
```

## 按关键词查询素材

```powershell
python scripts/creative_list.py `
  --app-type 游戏 `
  --keyword "match 3" `
  --keyword puzzle `
  --geo 美国,英国 `
  --platform Facebook,TikTok `
  --creative-type 视频 `
  --dedupe 素材去重
```

## 使用原始 JSON 请求体

创建 `request.json`：

```json
{
  "app_type": 1,
  "page": 1,
  "page_size": 20,
  "platform": ["facebook"],
  "geo": ["USA"],
  "ads_type": [2],
  "sort_field": "-impression",
  "duplicate_removal": 1,
  "include_ai_tags": true,
  "max_ai_tags_per_type": 5
}
```

执行：

```powershell
python scripts/creative_list.py --body '@request.json' --output summary
```

## 检查请求但不发送

```powershell
python scripts/creative_list.py `
  --app-type 游戏 `
  --keyword puzzle `
  --dry-run
```
