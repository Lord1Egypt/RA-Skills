---
name: douyin-deep-profile-collect
description: 深度采集抖音个人主页信息，包含基础资料、全部作品（含播放数）、喜欢列表、收藏列表、全量关注列表
version: 2.0.0
---

# 抖音个人主页深度采集

## 概述

本 Skill 用于深度采集抖音已登录用户的个人主页信息。通过访问 `douyin.com/user/self`，自动切换各 tab 页并滚动加载，提取用户的全维度数据。

**主要功能**：
- 基础资料：昵称、性别、地区、抖音号、关注/粉丝/获赞数、个人简介
- 作品列表：全部作品标题 + 播放数
- 喜欢列表：用户点赞过的视频标题 + 播放数
- 收藏列表：用户收藏的视频标题 + 播放数
- 关注列表：全量关注用户昵称 + 主页链接（虚拟滚动全量加载）

**适用场景**：
- know-your-owner 中的抖音数据采集子模块
- 用户画像构建与兴趣分析

> ⚠️ **执行约束**：本 Skill 中的所有 JS 脚本都必须**完整复制执行**，不可自行简化、改写或省略任何部分。每个脚本都是经过实际测试验证的，简化会导致数据不完整（如关注列表只拿到前40条而非全量）。

## 快速开始

无需任何参数，直接调用即可：
```
使用 douyin-deep-profile-collect 采集抖音个人信息
```

## 必需参数

无。本 Skill 自动采集当前浏览器登录用户的信息。

## 前置条件

- Chrome 浏览器已登录抖音账号
- ManoBrowser Chrome 插件已连接
- MCP 服务可用

## 执行流程

### 步骤1：导航到抖音个人主页

**工具**：`chrome_navigate`

**参数**：
- `url`: `https://www.douyin.com/user/self`

**说明**：已登录态下 `/user/self` 自动跳转到当前用户个人主页。**注意**：不要传 `active: false`，否则无法获取 tabId。导航后等待 5 秒让页面完全加载。

**输出**：`tab_id` — 后续所有步骤复用此 tabId。

---

### 步骤2：提取作品页（默认tab）

**工具**：`chrome_execute_script`

**参数**：
- `tabId`: 步骤1返回的 tab_id
- `world`: `MAIN`
- `timeout`: `20000`

**脚本逻辑**：
```javascript
async () => {
  // 滚动到底部加载全部作品
  window.scrollTo({top: 0, behavior: 'instant'});
  await new Promise(r => setTimeout(r, 300));
  const h = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
  window.scrollTo({top: h, behavior: 'smooth'});
  await new Promise(r => setTimeout(r, 2000));
  // 二次滚动确保加载完全
  const h2 = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
  if (h2 > h) {
    window.scrollTo({top: h2, behavior: 'smooth'});
    await new Promise(r => setTimeout(r, 1500));
  }
  window.scrollTo({top: 0, behavior: 'smooth'});
  await new Promise(r => setTimeout(r, 500));
  return JSON.stringify({
    url: window.location.href,
    title: document.title,
    fullText: document.body.innerText
  });
}
```

**说明**：个人主页默认显示「作品」tab。通过滚动触发懒加载，提取全文。返回数据中包含：
- 基础资料：昵称、关注/粉丝/获赞、抖音号、性别、地区、简介
- 全部作品标题 + 播放数

**数据提取要点**：
- 播放数在作品标题前面，格式为纯数字或 `x.x万`
- 作品标题通常包含 `#标签`
- 基础资料在页面上方

---

### 步骤3：切换到「喜欢」tab 并提取

**工具**：`chrome_execute_script`

**参数**：
- `tabId`: 步骤1返回的 tab_id
- `world`: `MAIN`
- `timeout`: `20000`

**脚本逻辑**：
```javascript
async () => {
  // 点击"喜欢" tab
  const tabs = document.querySelectorAll('.semi-tabs-tab');
  for (let t of tabs) {
    if (t.textContent.trim() === '喜欢') { t.click(); break; }
  }
  await new Promise(r => setTimeout(r, 3000));
  // 滚动加载更多
  window.scrollTo({top: 0, behavior: 'instant'});
  await new Promise(r => setTimeout(r, 300));
  const h = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
  window.scrollTo({top: h, behavior: 'smooth'});
  await new Promise(r => setTimeout(r, 2000));
  window.scrollTo({top: 0, behavior: 'smooth'});
  await new Promise(r => setTimeout(r, 500));
  return JSON.stringify({section: 'likes', fullText: document.body.innerText});
}
```

**说明**：抖音个人主页的 tab 使用 `semi-tabs-tab` CSS 类，通过遍历找到文本匹配的 tab 并点击切换。点击后等待 3 秒加载内容。

---

### 步骤4：切换到「收藏」tab 并提取

**工具**：`chrome_execute_script`

**参数**：
- `tabId`: 步骤1返回的 tab_id
- `world`: `MAIN`
- `timeout`: `20000`

**脚本逻辑**：与步骤3相同，但点击的是文本为 `'收藏'` 的 tab。

**说明**：收藏列表包含视频和音乐两个子分类。提取到的数据反映用户的深度兴趣偏好。

---

### 步骤5：打开关注侧边面板

**工具**：`chrome_execute_script`

**参数**：
- `tabId`: 步骤1返回的 tab_id
- `world`: `MAIN`
- `timeout`: `10000`

**脚本逻辑**：
```javascript
() => {
  const divs = document.querySelectorAll('div.uvGnYXqn');
  for (let d of divs) {
    if (d.textContent.trim() === '关注') {
      d.parentElement.click();
      return JSON.stringify({ok: true});
    }
  }
  return JSON.stringify({ok: false});
}
```

**说明**：点击个人资料区域的「关注」数字。**重要**：关注列表不是普通弹窗（modal/dialog），而是从右侧滑出的侧边面板（panel）。必须点击 `div.uvGnYXqn`（文字"关注"）的 `parentElement`。

---

### 步骤6：全量滚动关注面板并提取用户列表

**工具**：`chrome_execute_script`

**参数**：
- `tabId`: 步骤1返回的 tab_id
- `world`: `MAIN`
- `timeout`: `90000`

**脚本逻辑**：
```javascript
async () => {
  await new Promise(r => setTimeout(r, 2000));

  // 第一步：找到真正的可滚动容器
  // ⚠️ 不能只找"包含最多 /user/ 链接的 div"，那样会找到外层 overflow:visible 的 div
  // 必须找 overflowY 为 'auto' 或 'scroll' 且包含 /user/ 链接的容器
  let panel = null;
  const allDivs = document.querySelectorAll('div');
  for (let d of allDivs) {
    const style = window.getComputedStyle(d);
    const ov = style.overflowY;
    if ((ov === 'auto' || ov === 'scroll') && d.scrollHeight > d.clientHeight) {
      const links = d.querySelectorAll('a[href*="/user/"]').length;
      if (links > 0) {
        // 找最内层的可滚动容器（scrollHeight > clientHeight 说明有内容可滚）
        if (!panel || d.scrollHeight < panel.scrollHeight) {
          panel = d;
        }
      }
    }
  }
  // 兜底：如果上面没找到（样式被覆盖），回退到找包含最多链接且 scrollHeight > clientHeight 的 div
  if (!panel) {
    let maxLinks = 0;
    for (let d of allDivs) {
      const links = d.querySelectorAll('a[href*="/user/"]').length;
      if (links > maxLinks && d.scrollHeight > d.clientHeight + 100) {
        maxLinks = links;
        panel = d;
      }
    }
  }
  if (!panel) return JSON.stringify({error: 'no_panel'});

  // 第二步：激进滚动加载 — 必须用 WheelEvent 触发虚拟滚动
  const MAX_USERS = 500;
  let prevH = 0, same = 0;
  for (let i = 0; i < 200; i++) {
    panel.scrollTop = panel.scrollHeight;
    panel.dispatchEvent(new WheelEvent('wheel', {deltaY: 500, bubbles: true}));
    await new Promise(r => setTimeout(r, 300));
    const loaded = panel.querySelectorAll('a[href*="/user/"]').length;
    if (loaded >= MAX_USERS) break;
    if (panel.scrollHeight === prevH) {
      same++;
      if (same > 15) break;
    } else {
      same = 0;
    }
    prevH = panel.scrollHeight;
  }

  // 第三步：提取用户链接并去重
  const users = [], seen = new Set();
  panel.querySelectorAll('a[href*="/user/"]').forEach(a => {
    const href = a.getAttribute('href') || '';
    const name = a.textContent.trim();
    if (name.length > 0 && name.length < 60 && !seen.has(href)) {
      seen.add(href);
      users.push({name: name.substring(0, 40), href: href});
    }
  });
  const sampled = users.length >= MAX_USERS;
  return JSON.stringify({count: users.length, users: users.slice(0, MAX_USERS), sampled, total_following: '见个人主页关注数'});
}
```

**说明**：这是整个工作流最关键的步骤。

> ⚠️ **必须完整复制上方脚本执行，不可简化或自己重写！**

**面板定位的关键Bug修复（v2.5.3）**：
之前的逻辑是"找包含最多 `/user/` 链接的 div"，但这会找到**外层容器**（`overflow: visible`，`scrollHeight === clientHeight`），不是真正的滚动容器。对着这个外层 div 做 WheelEvent 和 scrollTop 完全无效，导致只拿到初始渲染的约40条。

**正确的定位方式**：找 `overflowY === 'auto'` 或 `'scroll'` 且 `scrollHeight > clientHeight` 的容器。这才是真正可以滚动的面板。

**关注面板的关键特性**：
- 面板是侧边滑出 panel（不是 modal/dialog）
- 面板内部有一个**真正可滚动的容器**（overflowY: auto/scroll），外面还包了一层不可滚动的外壳
- 必须对真正的滚动容器做 WheelEvent 才能触发虚拟滚动加载
- 停止条件：连续 15 轮 scrollHeight 不变（已到底）或达到500人上限

**最终结果**：此步骤返回全量关注用户列表（昵称 + 主页链接）。如果返回数量远少于个人主页显示的关注数，说明面板定位可能有误。

---

### 步骤7：关闭标签页

**工具**：`chrome_close_tabs`

**参数**：
- `tabIds`: [步骤1返回的 tab_id]

**说明**：清理浏览器资源。

## 输出示例

采集完成后，汇总各步骤数据（以下为字段结构示例，实际值取决于当前登录用户）：

```json
{
  "platform": "douyin",
  "profile": {
    "nickname": "用户昵称",
    "gender": "男/女",
    "location": "省份·城市",
    "douyinId": "抖音号",
    "bio": "个人简介",
    "following": "关注数",
    "fans": "粉丝数",
    "likes": "获赞数"
  },
  "works": [
    {"title": "作品标题 #标签1 #标签2", "plays": "播放数"}
  ],
  "liked_videos": [
    {"title": "点赞过的视频标题", "plays": "播放数"}
  ],
  "favorites": [
    {"title": "收藏的视频标题", "plays": "播放数"}
  ],
  "following_users": [
    {"name": "关注的用户昵称", "href": "//www.douyin.com/user/..."}
  ],
  "following_count": "全量关注用户数"
}
```

## 注意事项

### 平台特性

1. **Tab 切换机制**
   - 使用 `semi-tabs-tab` CSS 类
   - 通过 JS `.click()` 切换，不是 URL 变化
   - 切换后需等待 3 秒加载内容

2. **关注面板虚拟滚动**
   - 面板是侧边滑出 panel，不是 modal
   - 使用虚拟滚动，必须 WheelEvent 触发
   - ⚠️ 面板定位：必须找 `overflowY: auto/scroll` 且 `scrollHeight > clientHeight` 的可滚动容器，不能只找包含最多链接的 div（那会找到外层不可滚动的 div）

3. **tabId 获取**
   - `chrome_navigate` 不带 `active: false` 才能获取 tabId
   - 也可从 `_meta.context.relatedTabs` 提取

### 常见问题

#### 问题1：跳转到登录页
- 症状：URL 包含 `login` 或 `passport`
- 解决：请先在 Chrome 中打开 douyin.com 并登录

#### 问题2：关注面板打不开
- 症状：步骤5返回 `{ok: false}`
- 解决：`div.uvGnYXqn` 选择器可能因页面改版失效。用 `chrome_get_interactive_elements` 查找新的关注入口

#### 问题3：关注列表加载不完整（只有约40人）
- 症状：用户数远少于实际关注数（如关注214人只拿到40人）
- 原因：面板定位错误，找到了外层 `overflow: visible` 的 div 而非真正的滚动容器
- 解决：确认脚本使用 `overflowY === 'auto' || 'scroll'` 来定位面板，不是仅靠链接数量

#### 问题4：喜欢/收藏 tab 切换失效
- 症状：切换后页面内容不变
- 解决：`semi-tabs-tab` 类名可能更新。用 `chrome_get_interactive_elements` 查找 tab 元素

## 版本信息

- **当前版本**：2.0.0
- **创建日期**：2026-03-19
- **基于**：chrome-workflow-build 正规流程生成（LOG → WORKFLOW → SKILL）
- **测试状态**：已验证通过（全量关注用户加载）
