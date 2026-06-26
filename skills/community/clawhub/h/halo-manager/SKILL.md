---
name: halo-manager
description: Halo博客管理技能 - 使用官方@halo-dev/api-client发布文章。支持Markdown语法自动转为HTML富文本格式。Triggers: halo, 博客, 发布文章
---

# Halo Manager

Halo博客文章管理技能

## 功能

- ✅ 创建并发布文章
- ✅ Markdown转HTML富文本（加粗、斜体、列表、代码等）
- ✅ 查看文章列表
- ✅ 删除文章

## 安装

```bash
cd halo-manager
npm install
```

## 配置

设置环境变量：
```bash
export HALO_URL=https://你的博客地址
export HALO_TOKEN=你的PersonalAccessToken
```

获取Token：Halo后台 → 设置 → Token → 创建个人令牌

## 使用

```bash
# 发布文章
halo publish "标题" "内容"

# 查看列表
halo list

# 删除文章
halo delete "关键词"
```

## Markdown语法

- `**加粗**` → **加粗**
- `*斜体*` → *斜体*
- `# 标题` → 大标题
- `` `代码` `` → `代码`
- `- 列表` → 列表项
- 换行用空行分隔段落

## 示例

```bash
halo publish "我的第一篇文章" "这是**加粗**和*斜体*测试

- 列表项1
- 列表项2

代码: `echo hello`"
```

## 技术说明

- 使用官方 @halo-dev/api-client
- 内容自动转换为HTML富文本格式
- 正确处理headSnapshot参数发布
