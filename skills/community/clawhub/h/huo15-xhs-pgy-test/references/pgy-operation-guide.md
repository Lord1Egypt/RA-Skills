# PGY 蒲公英平台博主搜索操作指南

## 登录流程详细步骤

### 1. 打开首页

```
browser action=open url=https://pgy.xiaohongshu.com label=pgy
```

### 2. 获取页面快照

```
browser action=snapshot refs=aria targetId=pgy
```

### 3. 点击登录按钮

登录按钮通常在页面右上角，ref 可能在 e59 附近（但 ref 会变化）。

### 4. 切换到账号登录

登录弹窗默认显示"短信登录"，需要点击"账号登录"切换到邮箱密码模式。

### 5. 填写表单

1. 先勾选用户协议复选框
2. 在邮箱输入框中 type 邮箱
3. 在密码输入框中 type 密码
4. 点击"登录"按钮

### 6. 验证登录成功

登录成功后页面会跳转到后台首页，可能弹出引导教程（1/7），点击"跳过"。

## 搜索流程详细步骤

### 1. 导航到博主广场

点击顶部导航栏的"找博主"按钮。

### 2. 定位搜索框

搜索框的 placeholder 包含"笔记关键词"，可以用 CSS 选择器定位：

```javascript
document.querySelector('input[placeholder*="笔记关键词"]')
```

### 3. 填充搜索框（关键步骤）

PGY 平台基于 Vue，直接 `input.value = 'xxx'` 不会触发响应式更新。必须用 native setter：

```javascript
const input = document.querySelector('input[placeholder*="笔记关键词"]');
const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
setter.call(input, '韩国探店');
input.dispatchEvent(new Event('input', { bubbles: true }));
```

### 4. 触发搜索

按回车键或点击搜索按钮：

```javascript
input.dispatchEvent(new KeyboardEvent('keydown', {
  bubbles: true, cancelable: true,
  key: 'Enter', code: 'Enter', keyCode: 13, which: 13
}));
```

## 博主详情页数据提取

### 整页文本提取（推荐方式）

```javascript
() => {
  return document.body.innerText.substring(0, 8000);
}
```

### 数据字段解析

从 innerText 中识别以下关键信息：

#### 基本信息
- 昵称：紧跟在"笔记主页"标签后
- 小红书号："小红书号：" 后的数字
- 地区：紧跟在身份标签后（如"韩国"）
- 机构：在地区后的机构名，或"无机构"
- 粉丝数："粉丝数" 后的数值（如 4.1w）
- 获赞与收藏："获赞与收藏" 后的数值

#### 报价信息
- 图文笔记一口价："图文笔记一口价" 后的金额
- 视频笔记一口价："视频笔记一口价" 后的金额

#### 笔记数据（最近发布）
每条笔记格式：
```
笔记标题
阅读
阅读量
点赞
点赞数
收藏
收藏数
发布时间
日期
```

#### 粉丝画像
- 性别分布："女性居多，占比XX.X%"
- 年龄分布："18-24居多，占比XX.X%"
- 地域分布："国内最高的三个省份：XX（X.X%）、XX（X.X%）、XX（X.X%）"
- 设备分布："苹果用户占比XX.XX%"
- 用户兴趣："用户最感兴趣的内容类型为XX、XX、XX"

#### 核心指标
- 曝光中位数
- 阅读中位数
- 互动中位数
- 互动率
- 视频完播率
- 图文3秒阅读率
- 近7天活跃天数
- 邀约48小时回复率
- 粉丝量变化幅度
- 活跃粉丝占比
- 阅读粉丝占比
- 互动粉丝占比
- 下单粉丝占比

## 报告模板

```markdown
## 博主：[昵称]

| 项目 | 详情 |
|------|------|
| 主要发布内容类型 | ... |
| 小红书号 | ... |
| 蒲公英主页 | URL |
| 粉丝数 | ... |
| 获赞与收藏 | ... |
| 机构 | ... |
| 身份标签 | ... |

**最近5条内容数据：**

| 笔记标题 | 阅读量 | 点赞 | 发布日期 |
|----------|--------|------|----------|
| ... | ... | ... | ... |

**粉丝画像：**
- 性别：...
- 年龄：...
- 地域：...

**报价：**
- 图文笔记一口价：...
- 视频笔记一口价：...
```

## 踩过的坑

1. **snapshot 不完整**：SPA 页面的 aria snapshot 只显示视口内的元素，大量数据在滚动区域外。用 `evaluate` 提取 innerText 解决。

2. **搜索框 type 不生效**：Vue 的响应式系统不监听直接赋值。用 `Object.getOwnPropertyDescriptor` 获取 native setter，再 dispatch input 事件。

3. **点击博主头像没反应**：实际上打开了新标签页，需要用 `browser action=tabs` 检查。不要假设还是在原标签页操作。

4. **ref 过期**：页面任何 DOM 变化后 ref 都可能失效。每次操作前先 snapshot 获取最新 ref。

5. **截图需要图像模型**：如果当前模型不支持图像（如 GLM-5.2），截图会失败。用 innerText 提取代替。

6. **页面加载延迟**：PGY 平台是 SPA，首次加载需要几秒。snapshot 失败时等待后重试。
