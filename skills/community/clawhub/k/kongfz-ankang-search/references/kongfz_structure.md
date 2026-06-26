# 孔夫子网站结构说明

## 基础URL结构（已验证 ✅）

- **主站**: `https://www.kongfz.com/`
- **拍卖栏目**: `https://www.kongfz.cn/`（新版独立域名）
  - 我的竞拍: `https://www.kongfz.cn/pm-buyer/bid-manage-pc/`
  - 收藏拍品: `https://www.kongfz.cn/pm-buyer/bid-manage-pc/favorite/`
  - 拍卖交易: `https://www.kongfz.cn/trade-views/management/buyer/list`
- **拍卖平台(艺拍联盟)**: `https://www.kongpm.com/`
  - 线上拍卖会: `https://www.kongpm.com/yplm/web/`
- **高级搜索**: `https://search.kongfz.com/adv.html?type=pm`（拍卖区）
- **搜索结果**: `https://search.kongfz.com/pm-search-web/pc/auction/search?key=关键词`
- **商品详情**: `https://item.kongfz.com/book/{ID}.html`
- **分类ID参考**: 34=红色文献, 3=历史, 12=国学古籍, 3003=地方史志

## 已废弃URL（404错误）

⚠️ `https://www.kongfz.com/auction/`（已废弃）
⚠️ `https://www.kongfz.com/auction/?keyword=...`（已废弃）
⚠️ `https://search.kongfz.com/product/search?q=...`（404错误）

## 浏览器自动化流程（已验证 ✅）

### 使用 xbrowser 的正确流程

```bash
# 1. 初始化
node "C:\Program Files\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs" init

# 2. 执行搜索（batch 命令，一次性执行）
node "C:\Program Files\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs" run --browser cft batch --bail \
  "open 'https://search.kongfz.com/adv.html?type=pm'" \
  "wait --load networkidle" \
  "snapshot -i" \
  "fill @e21 关键词" \
  "press Enter" \
  "wait --load networkidle" \
  "snapshot -i" \
  "get text body"
```

### 关键点

1. **必须用 batch 命令**：所有操作放在一个 batch 里，元素引用（@e21）才有效
2. **必须用 press Enter 提交**：点击搜索按钮可能无效，用 Enter 键提交表单
3. **元素引用会失效**：每次页面变化后需要重新 `snapshot -i` 获取新的引用
4. **搜索结果页 URL**：`https://search.kongfz.com/pm-search-web/pc/auction/search?key=关键词`

### 搜索结果页结构

- 拍品标题：`role: "heading"` 元素
- 作者信息：`作者:` 开头
- 出版社：`出版社:` 开头
- 当前价格：`￥` 开头
- 剩余时间：`X时X分X秒` 格式
- 拍主信息：`xxx件在拍` 格式

## 搜索结果示例（已验证 ✅）

搜索"文学"返回 704 件拍品，包含：
- 民国原版书籍
- 清刻本古籍
- 现代文学作品
- 签名本、手稿等

搜索"安康文字"返回 0 件拍品（暂无相关拍品）

## 注意事项

1. **反爬限制**：网站有反爬机制，建议使用 xbrowser 真实浏览器操作
2. **Cookie/登录**：某些功能可能需要登录，建议先手动登录
3. **元素引用变化**：页面结构可能更新，元素引用（e1, e2...）需要重新获取
4. **网络等待**：使用 `wait --load networkidle` 确保页面加载完成
