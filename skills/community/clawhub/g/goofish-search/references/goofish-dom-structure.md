# 闲鱼 Goofish DOM 结构参考

## 搜索结果页 URL 格式

```
https://www.goofish.com/search?q={关键词}
```

## 页面结构

### 顶部导航栏
```
header
  ├── Logo (闲鱼站点Logo)
  ├── 搜索框 (textbox)
  ├── 搜索按钮 (button "搜索")
  ├── 热门搜索链接
  └── 用户信息 (登录/订单)
```

### 筛选栏
```
div (筛选区域)
  ├── 综合 (默认排序)
  ├── 新降价
  ├── 新发布
  ├── 价格 (可输入区间)
  ├── 区域 (下拉选择)
  ├── 个人闲置 (筛选按钮)
  ├── 验货宝
  ├── 验号担保
  ├── 包邮
  ├── 超赞鱼小铺
  ├── 全新
  ├── 严选
  └── 转卖
```

### 商品列表
```
div (商品卡片)
  ├── 图片 (image)
  ├── 标题 (StaticText)
  ├── 标签 (细微磕碰划痕/Canon/佳能/佳能RF卡口)
  ├── 价格 (¥ + 数字)
  ├── 想要人数 (N人想要)
  ├── 地区 (paragraph)
  └── 卖家信用 (卖家信用优秀/极好/百分百好评)
```

### 翻页栏
```
div (search-pagination-container)
  ├── 左箭头按钮 (button) ← 上一页
  ├── 页码容器 (search-pagination-pageitem-container)
  │   ├── div "1" (页码)
  │   ├── div "2" (当前页，含 active class)
  │   ├── div "3" (页码)
  │   └── ... (最多显示10页)
  ├── 右箭头按钮 (button) → 下一页
  └── 跳转输入框 (到第X页)
```

## 翻页栏 Class 名称

```
search-pagination-container--nnaHMrYo        ← 翻页容器
search-pagination-pageitem-container--adfiUKZP  ← 页码容器
search-pagination-page-box--AbqmJFFp         ← 页码按钮
search-pagination-page-box-active--vsBooIVl  ← 当前页（高亮）
search-pagination-arrow-container--lt2kCP6J  ← 箭头按钮容器
search-pagination-arrow-base--vhaWL_Aj       ← 箭头基础样式
search-pagination-arrow-left--QbI1dgXd       ← 左箭头
search-pagination-arrow-right--CKU78u4z      ← 右箭头
search-pagination-to-page-container--ynJ2CPn1 ← 跳转输入区域
```

## 注意事项

1. Class 名称中的哈希值（如 `--nnaHMrYo`）可能会变化
2. 使用 `[class*="search-pagination-page-box-active"]` 选择器更稳定
3. 翻页按钮可能绑定 `window.open()` 事件，导致打开新标签页
4. 必须使用 `browser_click` + ref ID 进行翻页，不要用 JavaScript DOM 操作

## 已验证的翻页选择器（2026-05-31 测试通过）

```
输入框: search-pagination-to-page-input--NDqqDgSl
确定按钮: search-pagination-to-page-confirm--b51GmTKS
当前页高亮: search-pagination-page-box-active--vsBooIVl
页码按钮: search-pagination-page-box--AbqmJFFp
```

**测试结果：**
- ✅ `browser_type` + `browser_click` 组合成功翻页
- ❌ JavaScript `document.querySelector` + `.click()` 导致浏览器跳转新标签页
- ❌ `nextElementSibling` 方式返回 null（DOM 结构不符预期）
- ✅ URL 参数 `?page={页码}` 也可作为备用方案
