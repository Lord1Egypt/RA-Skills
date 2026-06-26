# 信息提取冒烟测试报告（小红书 / 微信文章 / 网站）

## 目标

- 验证 `knowledge-acquisition` 的三类渠道信息提取链路是否可用：小红书短链、微信公众号文章、普通网页。
- 输出每个渠道的提取结果摘要与失败/降级原因，给出可执行的改进建议。

## 测试输入

- 小红书：`http://xhslink.com/o/Ay5yQKu4qjp`
- 微信文章：`https://mp.weixin.qq.com/s/_476kHXL5tmS6ztI_tsfJw`
- 网站：`https://baijiahao.baidu.com/s?id=1842856644623565548&wfr=spider&for=pc`

## 测试方法

- 使用脚本：`skills/knowledge-acquisition/scripts/extract-smoke.js`
- 调用入口：`extractorInstance.extractContent(url, { timeout, maxContentLength })`
- 平台识别：`DynamicContentExtractor.detectPlatform`
- 处理器路由：动态插件系统（plugin-loader + platformHandlers）

## 关键修复（本次测试前已完成）

- 动态插件模块规范化：插件导出为 `{ instance }` 或 `class` 时，自动映射到统一的 `extractContent/handlePlatform` 形态，确保能被动态提取器注册为平台处理器。
- 通用提取器注册平台键修正：使通用提取器能作为 `generic/xiaohongshu/zhihu/bilibili/github` 的处理器参与路由。
- 小红书降级提取：当 Puppeteer 缺少可用 Chrome/Chromium 时，自动退化为无浏览器的 HTML 元信息/正文抽取，避免直接失败。

## 结果摘要

### 1) 小红书（xhslink）

- 状态：成功（降级路径）
- 平台识别：`xiaohongshu`
- 标题：`小红书 - 你访问的页面不见了`
- 作者：`未知作者`
- 正文长度：约 10k（包含站点页脚/导航等）
- 结论：已为 Puppeteer 安装 Chrome for Testing，但当前运行环境仍可能出现浏览器启动失败（crashpad 相关）。已在实现中加入自动降级到无浏览器抓取；同时由于目标页面返回“页面不见了”，因此内容质量不可用（属于源站访问/反爬/跳转限制导致）。

### 2) 微信文章（mp.weixin.qq.com）

- 状态：成功
- 平台识别：`wechat`
- 标题：`产品经理必读36本书单（2025年最新推荐书单）`
- 作者：`刘刚001`
- publishTime：空（页面未提供或未解析到）
- 正文长度：约 8.8k
- 结论：正文与标题/作者均可正确提取，链路可用。

### 3) 网站（baijiahao.baidu.com）

- 状态：成功
- 平台识别：`generic`
- 标题：`中国或将获一笔巨额款项，特朗普所征收的万亿关税或将全部退还`
- 作者：`未知作者`
- 正文长度：约 46k
- 结论：可提取正文与标题；但内容含“导航/推荐/站点组件”等噪音，属于通用网页抽取策略需要进一步净化的问题。

## 问题定位与建议

### A. 小红书内容质量（本次结果不可用）

- 现象：可走通提取，但返回“页面不见了”且正文噪音大。
- 可能原因：
  - xhslink 的重定向链/落地页需要 JS 执行或设备指纹，纯 HTTP 抓取拿不到真实笔记内容；
  - 源站对非浏览器 UA/无登录状态/频繁访问有限制，返回兜底页。
- 建议：
  - 在具备浏览器内核的环境下运行（为 Puppeteer 安装 Chrome/Chromium 或指定本机 Chrome 路径）；
  - 如果仍受限，考虑：请求头/Referer/等待策略、缓存与限速、必要时引入人工登录 Cookie（风险与合规需评估）。

### B. 通用网页噪音较多（baijiahao）

- 建议：
  - 提取时优先选择 `article/main` 区域（已有尝试），并增加“模板化站点（如百家号）”的去噪规则；
  - 对正文进行长度裁剪与重复块剔除（如导航栏、版权声明、推荐位）。

## 复现命令

```bash
cd skills/knowledge-acquisition
node scripts/extract-smoke.js
```
