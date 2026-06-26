---
name: mockplus-reader
description: 读取和分析 MockPlus 在线设计页面。用于：（1）打开并解析 MockPlus 网页链接，（2）提取页面中的设计信息、结构、组件，（3）分析原型稿内容和交互说明。当用户发送 MockPlus 链接或要求分析原型稿时使用此技能。
version: 1.0.0
author: 虾皮
---

# MockPlus Reader

读取和分析 MockPlus 在线设计页面。

## 使用方法

### 1. 打开 MockPlus 链接

使用 browser 工具打开 MockPlus 网页链接：

```bash
browser action=open url="<MockPlus链接>"
```

### 2. 获取页面快照

打开后获取页面内容：

```bash
browser action=snapshot targetId="<targetId>"
```

### 3. 分析内容

MockPlus 页面通常包含：
- **项目名称** - 页面标题
- **设计稿缩略图** - 右侧面板的项目截图
- **组件树** - 左侧面板的页面结构
- **交互说明** - 组件的交互描述（点击、跳转等）
- **评论区** - 用户的反馈和评论

### 4. 常见 MockPlus 域名

- `https://www.mockplus.com/`
- `https:// MockPlus.cn`
- `https://rp.mockplus.com/`

## 输出格式

解析后按以下格式整理信息：

```
## 项目信息
- 项目名称：
- 更新时间：

## 页面结构
（列出主要页面和组件）

## 交互说明
（提取关键交互流程）

## 备注
（其他重要信息）
```

## 已实现项目

基于 MockPlus 链接已生成 uni-app + Vue3 项目：

**项目路径：** `C:\Users\Ding\.openclaw\workspace\lutixia\`

**已实现页面：**
- pages/index/index.vue - 开屏页
- pages/library/library.vue - 题库首页
- pages/practice/practice.vue - 练习页
- pages/exam/exam.vue - AI模考页
- pages/profile/profile.vue - 用户中心
- pages/login/login.vue - 登录注册页

**运行方式：**
```bash
cd lutixia
npm install -g @dcloudio/uni-cli
npm install
npm run dev:%PLATFORM%
```

## 注意事项

- MockPlus 页面可能需要登录才能查看完整内容
- 某些项目链接可能有访问权限限制
- 移动端原型可能无法完全展示交互效果