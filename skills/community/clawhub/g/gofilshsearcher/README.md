# xianyu-search - 闲鱼自动搜索技能

## 📖 快速开始

### 安装
技能已预装在：`~/.openclaw/workspace/skills/xianyu-search/`

### 使用
直接在聊天中输入：
```
闲鱼搜索 [产品名称]
```

**示例：**
```
闲鱼搜索 RTX 5090
闲鱼搜索 金士顿 DDR5 16G 6000 --max-price 1200 --region 广东
```

---

## 🎯 功能特性

### 自动筛选
- ✅ 仅限个人闲置（排除商家/鱼小铺）
- ✅ 单一价格（排除价格区间）
- ✅ 排除回收广告/笔记本/包装盒
- ✅ 价格升序排序

### 自定义筛选
支持命令行参数：
- `--max-price XXX` - 最高价格
- `--min-price XXX` - 最低价格
- `--region XXX` - 指定地区
- `--condition XXX` - 成色要求
- `--shipping` - 仅包邮
- `--verified` - 仅验货宝

---

## 📊 输出示例

```
🦞 闲鱼 RTX 5090 搜索结果

已应用严格筛选：**仅限个人闲置** + **单一价格** + **排除商家/回收广告**

### 📦 商品列表（价格升序）

| # | 价格 | 商品标题 | 地区 | 想要 | 链接 |
|---|------|----------|------|------|------|
| 1 | **¥1.74 万** | 技嘉 RTX 5090 D V2 魔鹰 OC 24G | 广东 | - | [🔗查看](链接) |
| 2 | **¥1.79 万** | 影驰 RTX5090 D V2 星曜白色 | 湖南 | - | [🔗查看](链接) |
| ... | ... | ... | ... | ... | ... |
```

---

## 🔧 技术细节

### 浏览器自动化
使用 `playwright-browser` 技能：
1. 启动浏览器（headless: true）
2. 访问闲鱼网站
3. 执行搜索
4. 点击"个人闲置"筛选
5. 提取商品数据
6. 关闭浏览器

### 数据提取
- 商品标题：CSS 选择器 `.title`
- 价格：CSS 选择器 `.price`
- 地区：CSS 选择器 `.location`
- 想要人数：CSS 选择器 `[class*="wanted"]`
- 商品链接：`href` 属性提取

### 筛选逻辑
```javascript
// 排除商家
if (seller.includes('鱼小铺')) return false;

// 排除价格区间
if (price.includes('-')) return false;

// 排除回收广告
if (title.includes('回收')) return false;
```

---

## 📁 文件结构

```
xianyu-search/
├── SKILL.md          # 技能定义（主文件）
├── README.md         # 使用说明（本文件）
└── package.json      # 技能配置（如需要）
```

---

## 🔗 相关文档

- **工作流文档：** `memory/workflows/wechat-xianyu-search.md`
- **技能配置：** `TOOLS.md`（工具棚记录）
- **用户偏好：** `memory/preferences.md`

---

## ⚠️ 注意事项

1. **无需登录** - 游客模式即可搜索
2. **浏览器依赖** - 需要 `playwright-browser` 技能支持
3. **网络超时** - 默认 30 秒超时，失败自动重试 2 次
4. **反爬虫** - 闲鱼可能有访问限制，失败时手动访问

---

## 🐛 故障排除

### 浏览器启动失败
```bash
openclaw gateway restart
```

### 搜索结果空白
- 检查网络连接
- 稍后重试（可能触发反爬虫）
- 手动访问：https://www.goofish.com

### 筛选条件不生效
- 闲鱼页面结构可能变更
- 技能需要更新选择器
- 联系技能维护者

---

## 📞 支持

**技能维护：** OpenClaw 社区  
**问题反馈：** GitHub Issues 或 Discord  
**最后更新：** 2026-03-10 (v2.0)

---

_自动严格筛选，买二手不踩坑。🦞_
