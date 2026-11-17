---
name: huo15-xhs-pgy-test
displayName: 火一五蒲公英博主探店
description: "Use when the user wants to search bloggers on Xiaohongshu PGY (蒲公英) platform pgy.xiaohongshu.com — login, search by keyword/region, extract blogger profile data (content type, followers, views, likes, fan demographics, pricing), and compile structured reports. Also use when the user mentions 蒲公英, PGY, pgy.xiaohongshu, 找博主, 探店博主, or asks to collect blogger data from Xiaohongshu's brand collaboration platform."
version: 0.1.0
aliases:
  - 火一五蒲公英
  - 火一五PGY
  - 蒲公英博主
  - PGY探店
  - pgy
---

# 火一五蒲公英博主探店 v0.1

通过浏览器自动化登录小红书蒲公英平台（pgy.xiaohongshu.com），按关键词/地区搜索博主，提取博主详情数据并整理成结构化报告。

## 前置条件

- OpenClaw browser 工具可用（内置 Chromium 浏览器）
- 用户提供 PGY 平台账号和密码
- 知道要搜索的关键词（如"韩国探店"）和筛选条件

## 工作流

### 1. 启动浏览器并打开蒲公英

```
browser action=start
browser action=open url=https://pgy.xiaohongshu.com label=pgy
```

### 2. 登录

登录流程（PGY 平台登录页）：

1. 点击页面右上角"登录"按钮
2. 登录弹窗默认是"短信登录"，需要点击"账号登录"切换
3. 填写邮箱和密码
4. 勾选用户协议复选框
5. 点击"登录"按钮

**关键点：**
- 登录弹窗的 ref 可能因为页面加载时机变化，建议用 `snapshot refs=aria` 先获取最新 ref
- 邮箱输入框和密码输入框用 `kind=type` 填写
- 复选框需要先点击勾选，再填写表单

### 3. 跳过引导教程

首次登录后会弹出引导教程（1/7），点击"跳过"按钮。

### 4. 进入"找博主"页面

点击顶部导航栏的"找博主"按钮，进入博主广场。

### 5. 搜索博主

在搜索框中输入关键词（如"韩国探店"），按回车搜索。

**搜索框选择器：** `input[placeholder*="笔记关键词"]`

**填充搜索框的可靠方法（JS evaluate）：**

```javascript
() => {
  const input = document.querySelector('input[placeholder*="笔记关键词"]');
  if (!input) return 'no input';
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(input, '关键词');
  input.dispatchEvent(new Event('input', { bubbles: true }));
  input.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true, key: 'Enter', keyCode: 13, which: 13 }));
  return 'done';
}
```

> ⚠️ 直接用 `browser kind=type` 填充搜索框可能不触发 Vue 的响应式更新，需用上述 native setter 方案。

### 6. 筛选和选择博主

搜索结果会以卡片列表展示，每张卡片包含：
- 博主头像和昵称
- 地区标签（如"韩国"）
- 身份标签（如"海外华人"、"留学背景"）
- 内容类型标签（如"时尚"、"探店"）
- 粉丝数
- 笔记数
- 阅读中位数 / 互动中位数
- 起价

**筛选策略：**
- 看地区标签是否匹配目标地区（如"韩国"）
- 看内容标签是否包含"探店"
- 优先选粉丝数高、笔记数多的博主

### 7. 进入博主详情页

点击博主头像或昵称，会在新标签页打开详情页。

**详情页 URL 格式：**
```
https://pgy.xiaohongshu.com/solar/pre-trade/blogger-detail/{bloggerId}
```

**使用 `browser action=tabs` 查看新标签页的 targetId。**

### 8. 提取博主详情数据

详情页内容为 SPA 布局，aria snapshot 可能只显示部分内容。**最可靠的方式是用 `evaluate` 提取 `document.body.innerText`：**

```javascript
() => {
  return document.body.innerText.substring(0, 8000);
}
```

**提取的数据字段及对应文本标识：**

| 字段 | 页面文本标识 |
|------|-------------|
| 昵称 | 页面顶部 heading |
| 小红书号 | "小红书号：" 后的数字 |
| 地区 | 地区标签（如"韩国"） |
| 身份标签 | "海外华人"、"留学背景"等 |
| 机构 | "他山文化" / "无机构" |
| 内容类型 | "内容类目及占比" 行 |
| 粉丝数 | "粉丝数" 后的数值（如 4.1w） |
| 获赞与收藏 | "获赞与收藏" 后的数值 |
| 图文报价 | "图文笔记一口价" 后的金额 |
| 视频报价 | "视频笔记一口价" 后的金额 |
| 笔记案例 | 每条笔记的标题、阅读量、点赞、收藏、发布时间 |
| 粉丝性别 | "性别分布" 行 |
| 粉丝年龄 | "年龄分布" 行 |
| 粉丝地域 | "地域分布" 行 |
| 用户设备 | "用户设备分布" 行 |
| 用户兴趣 | "用户兴趣" 行 |

### 9. 整理报告

将提取的数据整理成 Markdown 表格报告，包含：
- 基本信息表（昵称、小红书号、地区、粉丝数、机构等）
- 最近5条笔记数据表（标题、阅读量、点赞、发布日期）
- 粉丝画像（性别、年龄、地域分布）
- 报价信息（图文一口价、视频一口价）
- 补充说明（如二次使用授权需单独沟通）

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| snapshot 只显示部分页面内容 | 用 `evaluate` 提取 `document.body.innerText` |
| 搜索框输入不生效 | 用 native setter + dispatchEvent 方案 |
| 点击博主没有跳转 | 检查 `browser action=tabs` 是否打开了新标签页 |
| 页面内容没加载完 | 等待几秒后重新 snapshot |
| 截图失败（无图像模型） | 用 innerText 提取代替截图 |

## 限制

- **二次使用授权报价**：PGY 平台不公开展示，需通过"发起邀约"与博主/机构单独沟通
- **账号 URL**：PGY 只展示"小红书号"（数字ID），不直接提供小红书 App 主页 URL
- **数据更新延迟**：平台数据标注"数据更新至"日期，非实时
- **登录态过期**：长时间操作后可能需要重新登录

## 浏览器操作要点

1. **ref 失效**：每次页面导航或 DOM 变化后，ref 会过期，需重新 `snapshot`
2. **targetId 管理**：点击博主会打开新标签页，用 `tabs` 获取新的 targetId
3. **标签页切换**：在多个博主间切换时，记住每个标签页的 targetId
4. **evaluate 优先**：对于 SPA 页面，`evaluate` 提取 innerText 比 snapshot 更可靠

## 技术支持

青岛火一五信息科技有限公司
