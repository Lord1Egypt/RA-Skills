# 分页策略

翻页前必须先**识别页面分页类型**，选对翻页方式。

> 📝 **文档语言与本地化**：本文件为**简体中文**。识别信号表中的中文 / 英文关键词（"下一页"/"Next"、"加载更多"/"Load more"）仅为**启发式示例，并非穷举**——非中文页面的实际文案会不同。跨语言页面请优先用 `snap` 返回的 `ref` 或 CSS 选择器（`page.locator('.xxx')`）定位，避免依赖可见文本。完整语言说明见 `SKILL.md`「📝 文档语言与本地化说明」。

## 步骤 1：识别分页类型

从 `pw-browser snap` 的输出判断：

| 类型 | 识别信号 | 翻页方式 |
|------|---------|---------|
| **页码分页** | 底部有页码（1,2,3...）、"下一页"/"Next"/">" | `click` 页码或"下一页" |
| **无限滚动** | 底部无分页控件，内容随滚动增加 | `mousewheel` |
| **加载更多** | 底部有"加载更多"/"Load more"/"查看更多" | `click` 该按钮 |

### 常见网站参考

| 网站 | 分页类型 | 翻页方式 |
|------|---------|---------|
| 百度搜索 | 页码分页 | 点击页码 |
| 淘宝搜索 | 页码分页 | 点击页码 |
| 京东搜索 | 页码分页 | 点击页码 |
| 知乎 | 页码分页 | 点击页码 |
| 小红书 | 无限滚动 | 滚动加载 |
| 抖音 | 无限滚动 | 滚动加载 |

## 步骤 2：执行翻页

### A. 页码分页

```bash
# 从 snap 找到"下一页"按钮 ref
pw-browser snap
pw-browser click e42          # 点击"下一页"
pw-browser sleep 2
pw-browser snap               # 验证
```

备选方式 — 直接点页码：

```bash
pw-browser snap
# 找到页码数字（如 "2"）对应的 ref
pw-browser click e50
pw-browser sleep 2 && pw-browser snap
```

### B. 无限滚动

```bash
pw-browser mousewheel 0 800
pw-browser sleep 2
pw-browser snap
```

连续多次滚动直到内容不再增加。

### C. 加载更多按钮

```bash
pw-browser snap
# 找到按钮 ref
pw-browser click e30
pw-browser sleep 2
pw-browser snap
```

## 步骤 3：判断翻页成功

| 分页方式 | 成功信号 | 结束信号 |
|---------|---------|---------|
| 页码 | snap 内容变化，URL 可能变化 | "下一页"按钮消失或 disabled |
| 滚动 | snap 出现新元素 | 内容不变，出现"没有更多了" |
| 按钮 | 新内容加载 | 出现"已加载全部"，按钮消失 |

## 批量翻页提取

```bash
# 使用 run-code 批量翻页
pw-browser run-code "
  const allResults = [];
  let hasNext = true;
  while (hasNext) {
    const items = await page.locator('.item').all();
    for (const item of items) {
      allResults.push(await item.textContent());
    }
    const nextBtn = page.locator('text=下一页');
    if (await nextBtn.count() === 0 || await nextBtn.isDisabled()) {
      hasNext = false;
    } else {
      await nextBtn.click();
      await page.waitForTimeout(2000);
    }
  }
  return JSON.stringify(allResults);
"
```

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 滚动后不加载新内容 | 实际上是页码分页 | 检查 snap 底部是否有页码，改为 click |
| 点击页码没反应 | 按钮 disabled 或需要等待 | `sleep 1` 后再点击 |
| 翻页后内容相同 | AJAX 加载，需要等待 | 延长 sleep 时间或用 `wait-for` |
| 页码按钮被遮挡 | 需先滚动到底部 | `mousewheel 0 1000` 再 snap |
