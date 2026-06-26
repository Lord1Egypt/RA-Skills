# 实战案例索引

本文件用于沉淀 Mapping-Skill 在真实任务中的实践案例，帮助后续快速判断该用哪一种抓取模式，而不是每次从零试错。

## 使用方式

阅读本文件时，重点关注：
- 任务场景
- 为什么选择该方法
- 关键结果
- 关键洞察
- 可复用模式

---

## 1. OpenReview 会议作者抓取

### 任务场景
抓取 ICLR / ICML / NeurIPS / ICLR 等 OpenReview 会议的论文与作者信息，并尽量补充主页、Scholar、邮箱。

### 推荐方法
优先使用 `scripts/openreview_scraper.py` 与 OpenReview API。

### 关键结果
- 可批量获取论文、作者、Profile、邮箱、主页等结构化信息
- 比网页搜索更稳定、更高效

### 关键洞察
- OpenReview 有 API，就不要先走网页搜索
- 邮箱要考虑 `preferredEmail -> emails[0] -> Hidden` 的回退逻辑
- Scholar / ORCID 等字段可能存在命名差异

---

## 2. CVF 论文抓取 + PDF 邮箱抽取

### 任务场景
抓取 CVPR / ICCV / WACV 的论文作者信息，并从 PDF 首页中提取邮箱。

### 推荐方法
优先使用 `scripts/cvf_paper_scraper.py`，先抓 HTML 元数据，再抓 PDF 首页文本。

### 关键结果
- 可从 HTML 拿到题目、作者、PDF 链接
- 可从 PDF 提取邮箱，补足页面中没有的联系信息

### 关键洞察
- CVF 不是 OpenReview，不要套用 API 方案
- 邮箱经常出现在 PDF 首页，且可能是花括号缩写模式
- `PyMuPDF` 才是正确依赖，不要误装 `fitz`

---

## 3. 实验室主页两阶段抓取

### 任务场景
列表页只有成员姓名或少量信息，详细资料在个人页中。

### 推荐方法
使用 `scripts/lab_member_scraper.py` 的两阶段模式。

### 关键洞察
- 列表页负责提取成员链接
- 个人页负责提取邮箱、教育经历、兴趣、社交链接
- 中国高校站点常见 `.ashx` 页面与 `[at]` 混淆邮箱

---

## 4. Hugo Academic 单页卡片模式

### 任务场景
实验室成员信息集中在一个卡片列表页中，例如 PKU.AI。

### 推荐方法
使用 `lab_member_scraper.py` 的 card 模式。

### 关键洞察
- 先判断 `.people-person`、`.network-icon`、`.portrait-title` 等结构
- 若卡片页已包含邮箱和社交链接，就不必访问个人页
- Cloudflare 邮箱保护需要 XOR 解密

---

## 5. 邮箱反向定位法

### 任务场景
页面结构混乱，没有稳定 CSS 类名，但能看到邮箱。

### 推荐方法
从邮箱文本节点反向向上找容器，再做字段抽取。

### 关键洞察
- 这是自定义 HTML 页面下的防御性策略
- 当模板识别失败时，这个方法经常有效

---

## 6. GitHub 研究者网络发现

### 任务场景
从某个 GitHub 用户的 following / followers 网络中找研究者。

### 推荐方法
使用 `scripts/github_network_scraper.py`，结合 API 主资料、社交接口和 README。

### 关键洞察
- GitHub README 往往比 API 主资料更完整
- 可从 README 补齐 Scholar、Homepage、LinkedIn

---

## 7. TongClass 两阶段 Hugo Academic 变体

### 任务场景
列表页只展示年级和成员链接，详细信息在个人页。

### 推荐方法
列表页抽 URL，个人页用正则抽 `Interests` / `Education` / 邮箱 / 社交链接。

### 关键结果
- 154 名成员中邮箱提取率约 94%
- 研究兴趣提取率约 94%

### 关键洞察
- 这是两阶段模式与 Hugo Academic 模板的结合体
- 列表页头部信息（如年级）是有价值的元数据
- `Interests\s*\n([\s\S]*?)(?=Education|$)` 这类模式有很强复用性
