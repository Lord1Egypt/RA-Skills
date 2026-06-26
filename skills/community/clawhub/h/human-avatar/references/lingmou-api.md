# 灵眸（LingMou）API

官方文档：
- 基于模板创建播报视频：
  `https://help.aliyun.com/zh/avatar/avatar-application/developer-reference/api-lingmou-2025-05-27-createbroadcastvideofromtemplate`
- 批量查询播报视频：
  `https://help.aliyun.com/zh/avatar/avatar-application/developer-reference/api-lingmou-2025-05-27-listbroadcastvideosbyid`
- 查询播报模板详情：
  `https://api.aliyun.com/api/LingMou/2025-05-27/GetBroadcastTemplate`
- 列出播报模板：
  `https://api.aliyun.com/api/LingMou/2025-05-27/ListBroadcastTemplates`

## 鉴权与地域
- 鉴权：阿里云 AK/SK（OpenAPI 签名）
- 地域：`cn-beijing`
- Endpoint：`lingmou.cn-beijing.aliyuncs.com`
- API 版本：`2025-05-27`

## 已验证可用流程（当前环境 SDK 1.6.0）
1. 调 `ListBroadcastTemplates` 获取账号下已有模板
2. 若用户未指定 `templateId`，随机选一个已有模板
3. 调 `GetBroadcastTemplate` 查询模板详情和 `variables`
4. 选中可替换的 text 变量（优先 `text_content`）
5. 调 `CreateBroadcastVideoFromTemplate`
6. 用返回 `id` 轮询 `ListBroadcastVideosById`
7. `status=SUCCESS` 后读取 `videoURL`

## 新能力目标（已在 SDK 1.7.0 venv 中验证）
需求中的新增能力是：
1. 获取公共播报模板列表
2. 基于公共模板复制出自己的播报模板
3. 再用复制后的模板创作视频

期望工作流：
- 先 `list broadcast template`
- 若有模板：随机选择一个模板
- 若没有模板：获取公共模板，最多复制 3 个，再从已复制模板中随机选一个创建视频

**实测结论**：
- `alibabacloud-lingmou20250527==1.7.0` 中确实新增了：
  - `list_public_broadcast_scene_templates`
  - `copy_broadcast_scene_from_template`
- 两个接口都已真实调用成功
- 但“复制公共模板后立即直接创建视频”**不保证成功**；实测可能报错：`100010031001-400 无有效片段`
- 这意味着复制出来的对象虽然是一个新的 `BS...` 模板/场景 id，且能查到 variables，但它未必已经具备可直接渲染视频的完整片段配置
- 因此生产策略应为：
  - **优先随机使用账号下已有、已验证可直接生成的视频模板**
  - **仅在本地模板为空时**，才把公共模板复制作为兜底/准备动作
  - 一旦复制后仍无法直接生成，要明确提示用户该模板需要在灵眸侧进一步完善

## Python SDK 实测字段

### SDK 版本差异
- 系统 Python 环境原先为 `1.6.0`，没有公共模板相关方法
- 已在隔离虚拟环境 `.venv-human-avatar/` 中安装并验证 `1.7.0`
- 建议运行公共模板相关测试时使用：
  ```bash
  /root/.openclaw/workspace-ceo/.venv-human-avatar/bin/python scripts/avatar_video.py --list-public-templates
  ```

### ListBroadcastTemplates
返回对象包含：
- `data[].id`
- `data[].name`
- `data[].variables`（列表接口里通常为空或简略）

示例（实测账号）：
```json
[
  {"id": "BS1vs5wAhH7OvW7btG1M6VxEQ", "name": "boy-01"},
  {"id": "BS1V_mn-IwR6uZTgxuiKoWdPw", "name": "girl-01"},
  {"id": "BS1JqkX1Dm4VGjseLKkPkpmiw", "name": "boy-02"},
  {"id": "BS1bR7OvVfFY2OkNEy591084A", "name": "girl-02"}
]
```

### GetBroadcastTemplate
Python SDK 请求字段不是 `id`，而是：
```python
req = lm.GetBroadcastTemplateRequest()
req.template_id = "BS1vs5wAhH7OvW7btG1M6VxEQ"
resp = client.get_broadcast_template(req)
```

实测返回：
```json
{
  "id": "BS1vs5wAhH7OvW7btG1M6VxEQ",
  "name": "boy-01",
  "variables": [
    {
      "name": "text_content",
      "type": "text"
    }
  ]
}
```

## CreateBroadcastVideoFromTemplate 入参（关键）
```json
{
  "templateId": "BS1b2WNnRMu4ouRzT4clY9Jhg",
  "name": "播报视频合成测试",
  "variables": [
    {
      "name": "text_content",
      "type": "text",
      "properties": {"content": "待播报文案"}
    }
  ],
  "videoOptions": {
    "resolution": "720p",
    "fps": 30,
    "watermark": true
  }
}
```

## ListBroadcastVideosById 返回（关键）
- `data[].status`: `SUCCESS / ERROR / PROCESSING / ...`
- `data[].videoURL`
- `data[].captionURL`

## 变量类型
- `text`：文本
- `image`：图片资源
- `avatar`：数字人资源
- `voice`：音色资源

## 集成建议
- 对话层不要强依赖用户提供 `template_id`
- 没给就自动列模板并随机选择
- 若用户没有提供播报脚本，先确认脚本再生成
- 若用户坚持“必须用我上传的图片做人像口播”，优先改走 `LivePortrait` 或 `EMO`，因为模板播报与图片驱动是两种不同路径
