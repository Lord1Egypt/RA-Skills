---
name: omnipublisher
description: Omni 内容发布器：一篇文章适配公众号/小红书/知乎/抖音，批量生成多平台版本
metadata:
  {
    "openclaw":
      {
        "emoji": "🔄",
        "requires": { "python": "3.7+" },
      },
  }
---

# omnipublisher - 多平台内容发布器

一次写作，到处发布。自动将同一文章转换成不同平台的格式。

## 平台支持

- 公众号（wechat）
- 小红书（xiaohongshu）
- 知乎（zhihu）
- 抖音（douyin）

## 使用

```bash
omnipublisher article.md --platforms wechat,xiaohongshu
```

输出：
- `article_wechat.md`
- `article_xiaohongshu.md`
- ...

详细文档见完整版（集成到 social-publisher 或独立文档）。

## 特点

- 纯 Python，无依赖
- 毫秒级转换
- 自动适配格式和风格

MIT 许可证.
