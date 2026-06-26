# 反爬策略参考

## 各站点反爬等级与对策

### 低防护（直接 requests 即可）
- 惠农网 cnhnb.com
- 一亩田 ymt.com
- 花椒大数据网 860938.cn
- 导油网 oilcn.com
- 央广网 cnr.cn
- 观研天下 chinabaogao.com
- 中研网 chinairn.com
- 新浪财经 sina.com.cn
- 界面新闻 jiemian.com

**对策：** 标准 headers + 2-5s 随机延迟即可

### 中防护（需关注频率 + UA）
- 中商产业研究院 askci.com — 短时间高频会触发 IP 限制
- 智研咨询 chyxx.com — 图片验证码可能出现
- 国家林草局 forestry.gov.cn — 搜索接口有频率限制
- Business Research Insights — Cloudflare 5s 盾

**对策：** 降低频率（5-8s），必要时切换 IP

### 高防护（需 JS 渲染或特殊处理）
- 巨潮资讯网 cninfo.com.cn — API 需模拟浏览器，部分接口有签名
- 东方财富 eastmoney.com — API 参数加密，但数据接口开放
- 前瞻产业研究院 qianzhan.com — Cloudflare 防护
- 海关总署统计系统 stats.customs.gov.cn — 验证码 + JS 加密
- 新华指数 indices.cnfin.com — 图表数据通过 JS 动态加载
- 36氪 36kr.com — React SSR，需等 JS 完成渲染
- CBNData cbndata.com — SPA 应用
- 国标全文公开系统 openstd.samr.gov.cn — 需 JS + 可能有验证码

**对策：** 使用 Playwright headless browser

```python
# Playwright 示例
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.cninfo.com.cn/new/disclosure", wait_until="networkidle")
    content = page.content()
    browser.close()
```

## 通用最佳实践

1. **尊重 robots.txt** — 采集前检查 `/robots.txt`
2. **请求间隔** — 最低 2 秒，高防护站点 5-10 秒
3. **错误退避** — 429/403 后指数退避：2→4→8→16→32→60s
4. **Session 复用** — 使用 requests.Session() 复用连接
5. **Referer 链** — 模拟从首页→列表页→详情页的浏览路径
6. **缓存** — 已抓取的页面缓存到本地，避免重复请求
7. **代理轮换** — 大规模采集时使用代理池
8. **异常监控** — 记录每次请求状态码，连续失败时暂停
