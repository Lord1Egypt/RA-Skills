# WeChat Article Import

适用：微信公众号文章（`mp.weixin.qq.com`）入库到 Obsidian 知识库。

## 标准流程

1. **不要优先用 `web_fetch`**
   - 微信公众号链接默认优先用 `browser`
   - `web_fetch` 常会被拦或拿不到正文/图片真实地址

2. **先打开页面，再 snapshot**
   - `browser open <url>`
   - `browser snapshot` 不要传 `markdown`
   - 用默认格式或工具允许的格式
   - 正文容器优先级：`#js_content` → `.rich_media_content` → `.rich_media_area_primary` → `article` → `main` → `.post-content` → `[class*="body"]`

3. **提取正文与图片时，`browser act/evaluate` 必须带 `fn`**
   - 如果缺 `fn`，就是错误调用
   - 同一工具连续 2 次参数错误，不要继续盲试；回看 skill 或上报

4. **图片字段优先级**
   - 优先读取：`data-src`
   - 其次：`src`
   - 再其次：`data-original` / `data_src` / `original`
   - 微信图片 URL 需要保留或补上 `from=appmsg`
   - 如果要转 Markdown，可先做字段标准化：把可用的 `data-src` 视作最终 `src` 再交给后续转换链

5. **正文清理**
   - 去掉公众号尾部噪音，如：扫码提示、阅读原文引导、授权弹窗、预览提示
   - 没命中正文容器时，再回退为整页内容转换，不要一开始就整页硬转

6. **重复检查先于最终写入**
   - 至少检查：标题、`source_url`
   - 有条件时再做近似内容检查
   - 没做重复检查，不算完成

7. **最小 draft 结构**
   - `title`
   - `aliases`
   - `tags`
   - `source_type`
   - `source_url`
   - `published`
   - `created`
   - `updated`
   - `importance`
   - `status`
   - `summary`
   - `bullets`
   - `images`

7. **渲染与写入**
   - 优先复用 `scripts/obsidian_note.py`
   - 不要手写一整篇最终 Markdown，除非脚本路径明确覆盖不到

## Browser 调用示例

### 正确的 snapshot
```json
{"action":"snapshot","targetId":"<id>"}
```

### 正确的 evaluate
```json
{
  "action":"act",
  "targetId":"<id>",
  "kind":"evaluate",
  "fn":"() => { return document.title; }"
}
```

### 提取公众号图片示例
```js
() => {
  const imgs = Array.from(document.querySelectorAll('img'));
  return imgs.map((img, i) => ({
    index: i + 1,
    src:
      img.getAttribute('data-src') ||
      img.getAttribute('src') ||
      img.getAttribute('data-original') ||
      img.getAttribute('data_src') ||
      img.getAttribute('original') || '',
    alt: img.getAttribute('alt') || `图片${i + 1}`,
  })).filter(x => x.src);
}
```

## 偏离条件

只有在以下情况才允许偏离这条流程：
- browser 明确拿不到内容
- skill 现有脚本无法覆盖任务要求
- 工具本身报系统性错误，无法继续

偏离时必须说明：
- 为什么偏离
- 偏离后改用什么路径
- 哪一步失败了
