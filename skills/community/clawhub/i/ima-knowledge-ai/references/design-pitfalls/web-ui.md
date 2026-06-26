# 网页/UI 设计禁忌 (Web/UI Design Pitfalls)

**用途**: IMA Studio AI 内容生成的避免指南  
**版本**: v2.0 (2026-03-04)  
**贡献者**: 李鹤（资深设计师）  
**基于**: 设计行业标准、最佳实践、常见失败案例

[← 返回索引](./README.md)

---

## 网页/UI设计禁忌（5条）

### 1. ⛔ 可读性灾难

**永远不要：**
- ❌ 浅色文字在浅色背景
- ❌ 字号过小（<14px正文）
- ❌ 行距过小（<1.5倍）
- ❌ 行长过长（>75字符）

**避免关键词：**
```
low contrast text, tiny font, poor readability,
line too long, cramped text, hard to read
```

**为什么：**
- 降低用户体验
- 增加阅读疲劳
- 影响转化率

**正确做法：**
- 对比度至少4.5:1（WCAG AA标准）
- 正文至少16px
- 行距1.5-1.8倍
- 行长45-75字符

---

### 2. ⛔ 导航混乱

**永远不要：**
- ❌ 导航隐藏太深
- ❌ 层级超过3层
- ❌ 导航文字不清晰
- ❌ 没有面包屑

**避免关键词：**
```
hidden navigation, confusing menu, too deep hierarchy,
unclear navigation labels
```

**为什么：**
- 用户找不到想要的内容
- 增加跳出率
- 降低转化率

**正确做法：**
- 清晰的导航结构（最多3层）
- 明确的标签文字
- 提供搜索功能
- 使用面包屑导航

---

### 3. ⛔ 响应式失败

**永远不要：**
- ❌ 移动端无法正常使用
- ❌ 元素重叠
- ❌ 水平滚动
- ❌ 按钮太小无法点击

**避免关键词：**
```
not mobile-friendly, overlapping elements,
horizontal scroll, tiny tap targets
```

**为什么：**
- 超过50%流量来自移动端
- Google惩罚不响应式网站
- 流失大量用户

**正确做法：**
- 移动优先设计
- 测试多种设备
- 按钮至少44x44px
- 避免固定宽度

---

### 4. ⛔ 加载速度慢

**永远不要：**
- ❌ 巨大的图片文件（>1MB）
- ❌ 过多的动画效果
- ❌ 未优化的资源
- ❌ 阻塞渲染

**避免关键词：**
```
huge images, slow loading, unoptimized, too many animations,
render-blocking resources
```

**为什么：**
- 用户会在3秒内离开
- 影响SEO排名
- 降低转化率

**正确做法：**
- 压缩图片（使用WebP）
- 懒加载（lazy loading）
- 代码分割
- CDN加速

---

### 5. ⛔ 自动播放灾难

**永远不要：**
- ❌ 视频自动播放（带声音）
- ❌ 弹窗广告覆盖内容
- ❌ 轮播图自动切换太快
- ❌ 背景音乐自动播放

**避免关键词：**
```
autoplay video with sound, popup ads, intrusive,
auto-rotating carousel too fast
```

**为什么：**
- 激怒用户
- 增加跳出率
- 影响用户体验

**正确做法：**
- 默认静音
- 轮播图用户控制
- 避免侵入式广告
- 给用户控制权

---


---

## 📚 相关文档

- [索引目录](./README.md)
- [色彩理论](../color-theory/README.md)
- [视觉一致性](../visual-consistency.md)

---

**最后更新**: 2026-03-04
