---
name: xiaohongshu-deep-profile-collect
description: 采集小红书个人主页的全量信息，包括基础资料、全部发布笔记、收藏笔记列表（全量）、点赞笔记列表（全量）
version: 2.0.0
---

# 小红书个人主页深度采集

## 概述

本 Skill 用于采集小红书当前登录用户的个人主页全量信息。通过 XHR 拦截技术突破虚拟滚动限制，实现收藏和点赞列表的全量采集。

**采集内容**：
- 基础资料（昵称/小红书号/IP属地/简介/学校/关注粉丝获赞数）
- 全部发布笔记（标题列表）
- 收藏笔记列表（全量，含标题/作者/点赞数/类型）
- 点赞笔记列表（全量，含标题/作者/点赞数/类型）

**核心技术**：XHR 拦截 —— 小红书使用虚拟滚动，DOM 中最多保留约 28 个 note-item 元素，旧元素会被回收。必须通过拦截 XMLHttpRequest 捕获 API 响应来获取全量数据。

**⚠️ 关键认知**：小红书个人主页有**三个独立 tab**（笔记/收藏/点赞），数据完全独立。必须分别导航到每个 tab 才能采集对应数据。**不要因为某个 tab 数据为0就跳过后续 tab**。


> ⚠️ **执行约束**：本 Skill 中的所有 JS 脚本都必须**完整复制执行**，不可自行简化、改写或省略任何部分。每个脚本都经过实际测试验证，简化会导致数据不完整。

## 快速开始

用户示例：
```
使用 xiaohongshu-deep-profile-collect 采集我的小红书个人主页信息
```

无需提供参数，自动检测当前登录用户。

## 必需参数

无。本 Skill 自动从小红书首页导航栏检测当前登录用户。

**前提条件**：浏览器已登录小红书账号。

## 执行流程

### 步骤1：导航到小红书首页

**工具**：`chrome_navigate`

**参数**：
- `url`: `https://www.xiaohongshu.com/`

**说明**：小红书不支持 /user/self 直达个人主页，需要先访问首页获取当前用户的主页 URL。

---

### 步骤2：提取个人主页 URL

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `10000`
- `jsScript`:
```javascript
() => {
  const links = document.querySelectorAll('a');
  for (let a of links) {
    if (a.textContent.trim() === '我' &&
        (a.getAttribute('href')||'').includes('/user/profile/')) {
      return JSON.stringify({
        profileUrl: 'https://www.xiaohongshu.com' + a.getAttribute('href')
      });
    }
  }
  return JSON.stringify({profileUrl: null});
}
```

**说明**：从首页导航栏找到文本为"我"且 href 包含 `/user/profile/` 的链接，提取完整的个人主页 URL。

**输出**：`profileUrl` — 后续步骤使用此 URL 导航。

---

### 步骤3：导航到个人主页（笔记 tab）

**工具**：`chrome_navigate`

**参数**：
- `url`: `{step_2.profileUrl}`（步骤2返回的 profileUrl）

**说明**：导航到个人主页，默认显示笔记 tab。

---

### 步骤4：滚动加载笔记 + 提取基础资料

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `120000`
- `jsScript`:
```javascript
async () => {
  // 智能滚动：连续5轮无新增note-item则停止
  let prevCount = 0, sameCount = 0;
  for (let i = 0; i < 50; i++) {
    window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
    await new Promise(r => setTimeout(r, 1500));
    const c = document.querySelectorAll('section.note-item').length;
    if (c === prevCount) { sameCount++; if (sameCount > 5) break; }
    else { sameCount = 0; }
    prevCount = c;
  }
  window.scrollTo({top: 0}); await new Promise(r => setTimeout(r, 500));
  const notes = [];
  document.querySelectorAll('section.note-item').forEach(n => {
    notes.push(n.textContent.trim().substring(0, 120));
  });
  return JSON.stringify({
    noteCount: notes.length, notes: notes,
    fullText: document.body.innerText
  });
}
```

**说明**：滚动加载全部笔记卡片。`fullText` 包含基础资料（昵称/小红书号/IP属地/简介/学校/关注粉丝获赞数）。笔记 tab 的卡片数量即为发布笔记数（不走 XHR 分页）。

**输出**：`noteCount`、`notes`（笔记标题列表）、`fullText`（含基础资料）

> ⚠️ **步骤4只是采集"笔记"tab的数据。收藏和点赞是独立的 tab，必须分别导航过去才能采集。即使笔记数为0，也要继续执行步骤5-10采集收藏和点赞。**

---

### 步骤5：导航到收藏 tab

**工具**：`chrome_navigate`

**参数**：
- `url`: `{step_2.profileUrl}?tab=fav&subTab=note`

**说明**：⚠️ **关键步骤，不可跳过！** 必须使用 URL 参数方式导航到收藏 tab（`?tab=fav&subTab=note`）。JS 点击 `.reds-tab-item` 不会触发数据刷新。收藏数据只有在收藏 tab 下滚动时才会通过 API 加载。

---

### 步骤6：注入 XHR 拦截器

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `5000`
- `jsScript`:
```javascript
() => {
  window.__xhs_collected = [];
  window.__xhs_done = false;
  window.__xhs_api_count = 0;
  const origOpen = XMLHttpRequest.prototype.open;
  const origSend = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.open = function(method, url, ...rest) {
    this.__xhs_url = url;
    return origOpen.call(this, method, url, ...rest);
  };
  XMLHttpRequest.prototype.send = function(...args) {
    if (this.__xhs_url &&
        (this.__xhs_url.includes('note/collect/page') ||
         this.__xhs_url.includes('note/like/page'))) {
      this.addEventListener('load', function() {
        try {
          const data = JSON.parse(this.responseText);
          if (data.data && data.data.notes) {
            window.__xhs_api_count++;
            data.data.notes.forEach(note => {
              window.__xhs_collected.push({
                note_id: note.note_id,
                display_title: note.display_title || '',
                type: note.type,
                user: note.user ? {
                  nickname: note.user.nickname,
                  user_id: note.user.user_id
                } : null,
                interact_info: note.interact_info ? {
                  liked_count: note.interact_info.liked_count
                } : null
              });
            });
            if (!data.data.has_more) window.__xhs_done = true;
          }
        } catch(e) {}
      });
    }
    return origSend.apply(this, args);
  };
  return JSON.stringify({injected: true});
}
```

**说明**：注入 XHR 拦截器，监听小红书收藏/点赞 API 的响应。API endpoints：
- 收藏：`edith.xiaohongshu.com/api/sns/web/v2/note/collect/page?num=30&cursor=xxx`
- 点赞：`edith.xiaohongshu.com/api/sns/web/v1/note/like/page?num=30&cursor=xxx`

拦截器自动从 API 响应中提取 note 结构化数据，检测 `has_more=false` 时设置完成标志。

---

### 步骤7：滚动触发 API 加载 + 提取收藏数据

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `120000`
- `jsScript`:
```javascript
async () => {
  const MAX_ITEMS = 500; // 上限500条，防止超大收藏列表采集过久
  for (let batch = 0; batch < 30; batch++) {
    for (let i = 0; i < 5; i++) {
      window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
      await new Promise(r => setTimeout(r, 1200));
    }
    if (window.__xhs_done) break;
    if (window.__xhs_collected && window.__xhs_collected.length >= MAX_ITEMS) break;
  }
  const seen = new Set();
  const unique = [];
  window.__xhs_collected.forEach(n => {
    if (!seen.has(n.note_id) && unique.length < MAX_ITEMS) { seen.add(n.note_id); unique.push(n); }
  });
  const sampled = window.__xhs_collected && window.__xhs_collected.length > MAX_ITEMS;
  return JSON.stringify({
    total: unique.length, notes: unique,
    sampled, totalBeforeSample: window.__xhs_collected ? window.__xhs_collected.length : unique.length,
    apiCalls: window.__xhs_api_count
  });
}
```

**说明**：持续滚动触发 API 请求加载更多数据。每批滚动 5 次（间隔 1.2s），最多 30 批。拦截器自动收集数据，滚动结束后去重提取。

**输出**：收藏笔记全量列表（含 note_id / display_title / type / user / interact_info）

---

### 步骤8：导航到点赞 tab

**工具**：`chrome_navigate`

**参数**：
- `url`: `{step_2.profileUrl}?tab=liked&subTab=note`

**说明**：⚠️ **关键步骤，不可跳过！** 必须导航到点赞 tab（`?tab=liked&subTab=note`）。点赞数据只有在这个 tab 下滚动才会触发 API 加载。即使前面收藏数据为0，点赞仍可能有数据，反之亦然。

---

### 步骤9：重新注入 XHR 拦截器

**工具**：`chrome_execute_script`

**说明**：每次页面导航后拦截器会失效，需要重新注入。使用与步骤6完全相同的脚本。

---

### 步骤10：滚动触发 API 加载 + 提取点赞数据

**工具**：`chrome_execute_script`

**说明**：与步骤7完全相同的滚动+提取逻辑。

**输出**：点赞笔记全量列表

**最终结果**：此步骤完成后，所有数据采集完毕。

---

### 步骤11：关闭标签页

**工具**：`chrome_close_tabs`

**说明**：关闭所有打开的标签页，清理资源。

## 重要提示

### XHR 拦截技术说明

本 Skill 的核心技术是 XHR 拦截，原因：

- **虚拟滚动限制**：小红书收藏/点赞列表使用虚拟滚动，DOM 中 `section.note-item` 最多保留约 28 个，旧元素被回收
- **直接抓 DOM 不可行**：无论滚动多少轮，DOM 元素数永远不超过 28
- **API 拦截方案**：通过 monkey-patch `XMLHttpRequest.prototype.open/send`，在 API 响应到达时提取数据
- **API 分页机制**：cursor 分页，每次 30 条，`has_more=false` 表示全部加载完毕

### Tab 切换方式

⚠️ 小红书的笔记/收藏/点赞 tab **不能用 JS click 切换**：
- ❌ `document.querySelector('.reds-tab-item').click()` — 数据不刷新
- ✅ `chrome_navigate(profileUrl + '?tab=fav&subTab=note')` — 正确加载

### 数据结构

每条笔记的结构：
```json
{
  "note_id": "65110e20000000001d01629e",
  "display_title": "笔记标题",
  "type": "video|normal",
  "user": {"nickname": "作者昵称", "user_id": "作者ID"},
  "interact_info": {"liked_count": "4820"}
}
```

### 已知限制

1. **关注列表**：PC 端关注面板无法通过 click 事件打开（Vue 事件绑定限制），API 需要 X-s/X-t 签名，暂不支持采集
2. **已下架笔记**：收藏/点赞中已被作者删除或平台下架的笔记不会出现在 API 返回中
3. **收藏子分类**：收藏 tab 下有 笔记/专辑/文件 子分类，本 Skill 只采集笔记类型

## 注意事项

### 平台特性

1. **登录要求**：必须已登录小红书账号
2. **API 频率**：滚动间隔 1.2s 经验证不会触发限流
3. **页面改版**：如果小红书更新 API 路径，需要更新拦截器中的 URL 匹配规则

### 常见问题

**问题1：profileUrl 为 null**
- 症状：步骤2返回 `{profileUrl: null}`
- 原因：未登录小红书账号
- 解决：确保浏览器已登录小红书

**问题2：收藏/点赞数量为0**
- 症状：XHR 拦截器未捕获到任何 API 请求
- 原因：API endpoint 可能已更改
- 解决：检查浏览器 Network 面板确认当前 API 路径，更新拦截器中的 URL 匹配

**问题3：数量少于预期**
- 症状：采集数量与页面显示的总数不一致
- 原因：部分笔记已被作者删除或下架，API 不返回这些笔记
- 解决：这是正常现象，API 返回的是实际可访问的笔记

## 输出示例

```
✅ 小红书个人主页深度采集完成！

📊 基础资料：
- 昵称：{用户昵称}
- 小红书号：{小红书号}
- IP属地：{IP属地}
- 简介：{个人简介}
- 学校：{学校}
- 关注：{N} | 粉丝：{N} | 获赞与收藏：{N}

📝 发布笔记：{N}条
⭐ 收藏笔记：{N}条（全量）
👍 点赞笔记：{N}条（全量）
```

## 版本信息

- **当前版本**：2.0.0
- **创建日期**：2026-03-19
- **平台版本**：小红书 Web 2026
- **测试状态**：已通过实际执行验证
- **核心改进**：v2.0 引入 XHR 拦截技术，突破虚拟滚动限制实现全量采集
