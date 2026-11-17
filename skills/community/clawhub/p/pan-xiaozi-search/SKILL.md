---
name: pan-xiaozi-search
description: Search cloud drive resources (Quark, Baidu, Aliyun, Xunlei) indexed on pan.xiaozi.cc. Use when users want to find shared files, movies, TV shows, software, or documents across Chinese cloud storage platforms.
version: 1.0.4
tags: search, netdisk, resource-finder, panxiaozi
---

# 盘小子搜索 Skill

## 概述

通过盘小子搜索夸克网盘、百度网盘等第三方网盘公开分享的资源索引。盘小子本身不存储文件，仅聚合第三方公开分享的标题、分类与链接信息。

## 触发场景

当用户提到以下关键词或意图时，使用本 Skill：

- "盘小子搜一下 xxx"
- "帮我在 pan.xiaozi.cc 上找 xxx"
- "搜一下网盘资源：xxx"
- "有没有 xxx 的网盘链接"
- "找 xxx 的夸克/百度网盘资源"
- 任何需要在网盘上搜索共享资源的请求

## 搜索工作流

### 第 1 步：构造搜索请求

使用 `WebFetch` 工具访问搜索页面，URL 格式：

```
https://pan.xiaozi.cc/resource?q=KEYWORD
```

**prompt 指令（必须严格使用）：**

> 列出所有搜索结果，每项按以下结构提取并输出为表格：
> - 序号
> - 资源标题
> - 详情链接（完整 URL：https://pan.xiaozi.cc/resource/RESOURCE_ID ）
> - 更新时间
> - 分类/类别
> - 网盘类型（夸克/百度/阿里/迅雷等）
> - 简介/描述文本（如有）
>
> 同时提取以下汇总信息：
> - 总搜索结果数量
> - 是否有多页结果（如有，列出分页参数）

### 第 2 步：格式化呈现

将 WebFetch 返回的搜索结果整理为清晰的结构化列表呈现给用户。

对每个结果必须包含：
- 标题（加粗，作为可点击的超链接，指向资源详情页）
- 网盘类型标签
- 更新时间
- 资源详情页完整 URL（紧跟其后，另起一行用 🔗 标注）

如果只有 1 个结果，直接展示该结果的完整信息（含简介）。如果多于 1 个结果，先展示汇总数量，再逐条列出。

**格式示例：**

```
🔍 盘小子搜索 "庆余年" — 共 1 条结果

1. [**庆余年 全2季 国语中字 2019-2024 4K【国剧】**](https://pan.xiaozi.cc/resource/352955)
   📂 分类：国剧 | 🗄️ 网盘：夸克 | 🕐 更新：2026-07-03
   🔗 https://pan.xiaozi.cc/resource/352955
   📝 该剧改编自猫腻同名畅销小说...
```

**CRITICAL**: 每条结果必须同时展示标题超链接和底部 🔗 链接地址，两者缺一不可。
多结果时可用表格形式，但表格中标题列必须包含超链接，另增一列展示链接地址。

### 第 3 步（可选）：查看资源详情

如果用户想查看某个资源的详细信息和网盘链接，使用 `WebFetch` 访问该资源的详情页：

```
https://pan.xiaozi.cc/resource/RESOURCE_ID
```

**详情页 prompt 指令：**

> 提取以下信息：
> - 完整标题
> - 资源描述/简介
> - 截图时间
> - 网盘类型与访问入口（按钮文案、跳转方式）
> - 是否有提取码说明
> - 封面图 URL
> - 分类/标签

然后向用户展示详情，并提醒：盘小子不存储文件本身，实际链接在第三方网盘页面，访问时注意安全。

## 注意事项

1. **不要编造结果**：仅展示 WebFetch 实际返回的内容
2. **链接完整性**：资源链接使用完整 URL 格式 `https://pan.xiaozi.cc/resource/RESOURCE_ID`
3. **搜索无结果**：如果搜索返回 0 条结果，告知用户并建议更换关键词或缩短搜索词
4. **安全提醒**：在详情页展示后，提醒用户注意第三方链接安全（核对域名、不输入账号密码）
5. **中文关键词**：搜索关键词无需编码，WebFetch 会自动处理
6. **第三方内容风险**：盘小子索引的均为第三方网盘公开分享链接，可能涉及版权问题或失效链接。提醒用户遵守当地法律法规，仅用于合法用途
