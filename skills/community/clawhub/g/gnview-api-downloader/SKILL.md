---
name: gnview-api-downloader
description: 抖音数据API工具集，包含用户数据获取、Cookie更新等完整API接口。适用于抖音数据采集的场景。
---

# gnview-api-downloader

## 功能概述
本技能为抖音数据API工具集，提供完整的抖音数据采集与分析能力，核心功能包括：
- 单个/批量抖音视频数据获取
- 抖音用户信息与作品列表采集
- Cookie更新与会话维护

## Quick Reference
| 模块 | 参考文件 | 简介 |
|------|----------|------|
| 单个视频数据 | `references/GET_douyin_web_fetch_one_video.md` | 获取抖音单个作品的详细数据 |
| 用户作品列表 | `references/GET_douyin_web_fetch_user_post_videos.md` | 获取抖音用户主页的所有作品数据 |
| 用户sec_user_id | `references/GET_douyin_web_get_sec_user_id.md` | 从抖音用户主页链接提取sec_user_id |
| 用户信息 | `references/GET_douyin_web_handler_user_profile.md` | 获取抖音指定用户的详细信息 |
| Cookie管理 | `references/POST_hybrid_update_cookie.md` | 更新指定服务的Cookie值，维护会话状态 |

> 按需读取 `references/` 下的模块文档获取详细 API 用法和代码示例。

## 配置说明
所有配置项均统一存放在技能目录下的`config.json`文件中，需在使用前完成配置：

| 配置项路径                     | 类型   | 示例值                                                                 | 说明                     |
|--------------------------------|--------|----------------------------------------------------------------------|--------------------------|
| `base_url`                     | 字符串 | http://xxx/ | API服务基础地址           |


示例`config.json`：
```json
{
  "base_url": "http://xxx/",
}
```