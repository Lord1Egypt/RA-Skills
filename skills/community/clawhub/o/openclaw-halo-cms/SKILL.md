---
name: halo-cms
description: |
  博客文章管理技能。当用户提到"发文章"、"写博客"、"Halo"、"发帖"、
  "回复评论"、"博客管理"等关键词时使用此技能。
metadata:
  openclaw:
    emoji: "\U0001F4D6"
    requires:
      bins:
        - python3
      env:
        - HALO_PAT_TOKEN
    primaryEnv: HALO_PAT_TOKEN
---

# Halo 博客管理技能

通过 Halo REST API 管理博客文章、评论等。

## API 认证

PAT Token 存储在环境变量 `HALO_PAT_TOKEN` 中。使用时去掉 `pat_` 前缀，直接使用 JWT 部分。

认证方式：`Authorization: Bearer <JWT部分>`

## API 地址

- Halo 服务：`http://localhost:8090`
- 文章列表（公开）：`GET /apis/api.content.halo.run/v1alpha1/posts`
- 用户文章管理：`GET /apis/uc.api.content.halo.run/v1alpha1/posts`

## 使用方法

通过 `python3` 调用 `scripts/halo_api.py`，支持以下命令：

```bash
# 获取文章列表
python3 scripts/halo_api.py list_posts

# 获取分类列表
python3 scripts/halo_api.py list_categories

# 获取标签列表
python3 scripts/halo_api.py list_tags

# 发文章（创建草稿，不自动发布）
python3 scripts/halo_api.py create_post --title "标题" --content "# 内容" --slug "url-slug"

# 发文章并直接发布
python3 scripts/halo_api.py create_post --title "标题" --content "# 内容" --slug "url-slug" --publish

# 发文章带分类和标签（使用分类/标签的 displayName）
python3 scripts/halo_api.py create_post --title "标题" --content "# 内容" --slug "url-slug" --categories "默认分类" --tags "技术"

# 发布草稿
python3 scripts/halo_api.py publish_post --name "文章UUID"

# 回复评论
python3 scripts/halo_api.py reply_comment --comment "评论UUID" --content "回复内容"
```

## 安全约束（必须严格遵守）

1. **发布前确认**：发文章前必须告诉用户标题和内容摘要，得到明确确认后才发布
2. **默认创建草稿**：不指定 `--publish` 时，文章仅创建为草稿，不自动发布
3. **不泄露敏感信息**：绝不发布包含以下内容的文章：
   - API Key、密码、Token
   - 服务器 IP 地址、端口、域名配置
   - 系统配置信息、数据库连接串
   - 用户个人隐私信息
4. **隐私脱敏**：如果文章内容涉及他人，必须脱敏处理（隐去真实姓名、联系方式等）
5. **不擅自操作**：不删除文章、不修改他人评论，除非用户明确要求

## 注意事项

- `--slug` 是文章的 URL 路径，会自动从标题生成（使用拼音/英文），建议手动指定
- 分类和标签使用 `displayName`，脚本会自动查找对应的 UUID
- 如果指定的分类/标签不存在，会报错并列出可选的分类/标签

### 技能包开源发布  秉承开源精神，我们将完整的 Halo CMS 技能包发布到了 GitHub，方便更多人使用和二次开发。  
**仓库地址**：[ThomasOscar/openclaw-halo-skill](https://github.com/ThomasOscar/openclaw-halo-skill) 