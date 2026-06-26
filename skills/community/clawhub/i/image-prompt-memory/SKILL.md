# 图片提示词记忆库

## 用途
保存成功的图片生成提示词，下次生成时快速调用。

## 数据文件
`/root/.openclaw/workspace/data/prompt_library.json`

## 数据结构
```json
{
  "prompts": [
    {
      "id": 1,
      "category": "商品图",
      "style": "日本简约风格",
      "description": "描述",
      "positive_prompt": "正向提示词",
      "negative_prompt": "反向提示词",
      "aspect_ratio": "1:1",
      "image_size": "1K",
      "feedback": "用户反馈",
      "created_at": "时间戳"
    }
  ],
  "styles": [
    {
      "id": 1,
      "name": "风格名",
      "characteristics": "特点",
      "tags": ["标签1", "标签2"]
    }
  ]
}
```

## 使用方法

### 1. 保存新提示词
用户确认图片满意后，自动保存到库中。

### 2. 查询相似提示词
根据用户需求搜索匹配的提示词。

### 3. 推荐提示词
根据类别/风格推荐最佳提示词。

## 搜索逻辑
- 按风格标签搜索
- 按类别搜索
- 按描述关键词搜索
