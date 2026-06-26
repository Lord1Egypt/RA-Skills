# 刘润公众号每日摘要 Skill

## 功能
每天自动抓取刘润公众号最新文章，生成结构化摘要。

## 触发条件
用户提到"刘润"、"公众号摘要"、"每日商业新闻"等关键词时触发。

## 执行流程

### Step 1: 搜索今日文章
- 通过搜狗微信搜索 `https://wx.sogou.com/weixin?type=2&query=刘润 {月}号`
- 提取第一条结果（当日发布的文章）

### Step 2: 获取全文
- 使用 browser 工具打开搜狗搜索结果页
- 点击文章链接跳转到微信原文
- 用 snapshot (aria) 提取完整文本内容

### Step 3: 生成摘要
- 按以下结构输出：
  1. 一句话总结
  2. 五大关键洞察（按板块分类）
  3. 对用户的个性化启示（结合Trade Arena持仓等）
  4. 趋势判断

### Step 4: 保存
- 摘要保存到：`liurun-fetcher/articles/summary_{YYYY-MM-DD}.md`
- 原文保存到：`liurun-fetcher/articles/raw_{YYYY-MM-DD}.txt`

## 技术要点
1. **搜狗微信搜索可达**：PowerShell Invoke-WebRequest 可正常访问
2. **浏览器点击文章**：browser 工具 navigate 到搜狗页面 → snapshot → click 文章链接 → 新标签页打开微信原文 → snapshot 提取内容
3. **反爬处理**：直接 HTTP 访问搜狗链接会被 antispider 拦截，必须通过浏览器操作
4. **日期格式**：搜索词用 `{M}月{D}号` 格式（如"4月20号"）

## 已知限制
- 微信原文需要浏览器已登录微信（或微信文章允许外部访问）
- 搜狗链接 token 有时效性，需实时获取
- 周末/节假日可能没有新文章（刘润商业频道工作日更新）

## 定时任务建议
- 执行时间：每天 10:00（文章通常早上9-10点发布）
- 通过 cron 工具设置定时任务

## 文件位置
- Skill目录：`C:\Users\Administrator\.qclaw\workspace\liurun-fetcher\`
- 文章存档：`liurun-fetcher/articles/`
- 测试脚本：
  - `test_sogou.ps1` - 搜狗搜索测试
  - `extract_links.ps1` - 链接提取
  - `baidu_search.ps1` - 百度备选搜索

---
*创建时间：2026-04-20*
*状态：✅ 验证通过*
