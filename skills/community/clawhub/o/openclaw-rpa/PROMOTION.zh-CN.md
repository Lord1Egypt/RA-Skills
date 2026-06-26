# OpenClaw RPA 技能 — 推广文案

> 可直接用于公众号、飞书、产品介绍或 ClawHub 简介；链接与模型建议见文末。

---

## 正文（短版）

在工作里用 OpenClaw 让大模型**直接驱动浏览器或本机**做重复事，常见有三类头疼：

1. **幻觉** — 偶尔会点错、找错元素，甚至「编造」不存在的步骤。  
2. **费用** — 每次跑任务都走大模型，token 和工具调用烧得很快。  
3. **速度** — 步步等推理，整体比脚本慢一个数量级。

**openclaw-rpa**（自动化机器人技能）用一条思路把上面三件事一起压住：

**录一次真实操作 → 自动生成可独立运行的 Playwright Python 脚本 → 以后只跑脚本。**

回放阶段**不再调大模型**：没有幻觉、路径一致、结果可预期，也快得多、成本接近零。

**能录什么（不止浏览器）**

| 能力 | 说明 |
|------|------|
| **浏览器** | 真实 Chrome 里逐步录，选择器从 DOM 来，不靠模型猜。 |
| **HTTP API** | `GET` / `POST` 任意 REST 接口，保存 JSON；密钥可写入生成脚本（触发含 **`#rpa-api`**）。 |
| **Excel（.xlsx）** | 新建/更新工作簿、多 Sheet、表头与冻结行；可从 JSON 等动态写行（openpyxl，无需装 Excel）。 |
| **Word（.docx）** | 段落 + 表格报告（python-docx，无需 Microsoft Office）。 |
| **自动登录** | **`#rpa-login`** 人工登录一次并保存 Cookie；后续录制与回放自动注入，减少短信/滑块/扫码反复折腾。 |
| **混合流程** | 网页 + API + Excel + Word 等可在**同一任务**里串起来（例如对账：拉接口 → 表格匹配 → Word 出表）。 |

**主要卖点**

- 多步任务可拆解，降低单次请求超时风险。  
- 产出普通 `.py` 文件，脱离 OpenClaw 也可用 `python3` 单独跑。  
- 支持浏览器 + 本机文件落地（如保存到桌面）。  
- 在 OpenClaw 配合飞书/IM 时，可发 **`#rpa-run:任务名`** 随时触发或配合定时执行。

**典型场景**

电商登录下单、行情/新闻抓取、豆瓣影评或新闻标题汇总、**纯 API 拉数**、**本地报表进 Excel/Word**……录一次，之后反复回放，每次路径稳定。

---

## 正文（更短 · 适合卡片/摘要）

用大模型每次点浏览器又慢又贵还容易错。**openclaw-rpa**：在真实环境里**录一遍**，自动生成 **Python + Playwright** 脚本；以后**只跑脚本**，不调模型。除**网页**外，还支持 **REST API**、**Excel / Word** 本地读写、**`#rpa-login` 一次登录 Cookie 复用**。适合重复性高、要稳定复现的流程。

---

## 案例（要点 + 直达地址）

**总目录**

- 中文 README「案例视频」整节：  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.zh-CN.md#%E6%A1%88%E4%BE%8B%E8%A7%86%E9%A2%91  
- 英文 README「Case videos」：  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.md#case-videos  

**Sauce 电商（浏览器录制）**

- 说明：登录 → 排序 → 加购 → 登出。  
- 文档：  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.zh-CN.md  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.md#1-sauce-online-shopping-website-demo-browser-recording  
- 视频：  
  https://www.bilibili.com/video/BV1YfXrBBE9u/  
  https://github.com/user-attachments/assets/d368a81e-425a-4830-bc29-fe11e89eda92  
  https://github.com/user-attachments/assets/965fbecc-a0fc-4795-9f63-a5ef126f97f8  

**豆瓣电影（浏览器 + 写桌面文件）**

- 说明：搜索影片 → 详情 → 抽字段 → 保存文本。  
- 文档：  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.zh-CN.md#douban-movie-demo  
- 视频：  
  https://github.com/user-attachments/assets/594c8970-2f11-4e2b-ae57-e563cafe6bbd  

**Yahoo 财经 NVDA 新闻（浏览器）**

- 说明：行情页 → 新闻 Tab → 标题落盘。  
- 文档：  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.md#yahoo-finance-nvda-demo  
- 视频：  
  https://github.com/user-attachments/assets/8da98e97-415c-4a60-b412-9a30ea87551a  

**行情 API + 新闻 + 本地简报（`#rpa-api`）**

- 说明：HTTP 拉 JSON + 浏览器新闻页 + 合并简报；本节以文案与 API 说明为主。  
- 文档：  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.zh-CN.md#api-quotes-news-brief-zh  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.zh-CN.md#api_call  

**飞书 / Lark：`#rpa-list` / `#rpa-run`**

- 说明：IM 里列任务、执行、定时类用法演示。  
- 文档：  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.zh-CN.md  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.md#openclaw--feishulark-rpa-list-rpa-run-and-scheduled-run  
- 视频：  
  https://github.com/user-attachments/assets/514e2d74-f42a-4243-8d49-52931fe6c22e  
  https://github.com/user-attachments/assets/08ccbdc6-508b-457a-87d6-49ac77e9a89e  

**自动登录（Cookie）：Sauce 回放**

- 说明：`#rpa-login` 存 Cookie → 录制/回放自动注入。  
- 文档：  
  https://github.com/laziobird/openclaw-rpa/blob/main/articles/autologin-tutorial.md  
- 视频：  
  https://github.com/user-attachments/assets/233659db-f5c4-44c1-9245-0bcf53b9dfa1  

**自动登录（Cookie）：携程酒店 → Word**

- 说明：登录态下抓酒店信息 → `hotel.docx`。  
- 文档：同上（教程内「案例二」）。  
- 视频：  
  https://github.com/user-attachments/assets/696e7b4b-5000-469f-abb8-9b8c2f023aea  

**应付对账（API + Excel + Word）**

- 说明：Mock GET + 本地 Excel 匹配 + Word 表格报告。  
- 文档：  
  https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-ap-reconciliation.md  
  https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-ap-reconciliation.en-US.md  
- 视频：  
  https://github.com/user-attachments/assets/13cfda68-5a67-4efa-aa6d-c1ecc501a30e  
  https://github.com/user-attachments/assets/61057986-edb6-47ef-81e1-72122f33f081  
  https://github.com/user-attachments/assets/c994d58a-9cbb-42e4-a01e-7d9899a39ebe  
  https://github.com/user-attachments/assets/61b4fc7c-a05a-4fc9-b41f-f29dbd48675d  

**自动登录（英文教程）**

- 文档：  
  https://github.com/laziobird/openclaw-rpa/blob/main/articles/autologin-tutorial.en-US.md  

---

## 链接与模型建议

- **详细介绍与安装**：[README.zh-CN.md](https://github.com/laziobird/openclaw-rpa/blob/main/README.zh-CN.md)（含案例视频）  
- **Skill / ClawHub**：[clawhub.ai/laziobird/openclaw-rpa](https://clawhub.ai/laziobird/openclaw-rpa)  
- **源码**：[github.com/laziobird/openclaw-rpa](https://github.com/laziobird/openclaw-rpa)

**推荐使用大模型（录制与拆解任务时）**：Minimax 2.7、Gemini Pro 3.0 及以上、Claude Sonnet 4.6 等能力较强的模型；**回放脚本阶段不依赖大模型**。

---

## 可选：一句话标题

- 「录一次，跑千遍：浏览器 + API + Excel + Word，脚本回放零 token。」  
- 「告别每次让 AI 点网页：RPA 技能把操作固化成 Python，稳定、省钱、快。」

---

## 技术 Discord 短介绍（多版本）

发到 **Playwright / Python / 自动化 / LLM** 等不同群时，按字数选一条。链接可包 `<>` 减少 Discord 预览。

**A. 一句话（约 120 字）**

openclaw-rpa（OpenClaw 技能）：真实浏览器 + API + Excel/Word **录一遍** → 生成独立 **Playwright + Python** 脚本；以后 **`python3` 回放不调大模型**。仓库：<https://github.com/laziobird/openclaw-rpa>

**B. 电梯稿（约 200 字）**

**openclaw-rpa**：面向 OpenClaw 的「录一次、跑千遍」RPA——在 **Chrome** 里逐步录、`#rpa-api` 录 **REST**、**openpyxl / python-docx** 写表格与 Word，最终产出普通 **`.py`**。回放阶段**不调用 LLM**，适合高频重复、要稳定路径的流程；复杂登录可用 `#rpa-login` + `#rpa-login-done` 存 Cookie 复用。说明与案例视频：<https://github.com/laziobird/openclaw-rpa/blob/main/README.zh-CN.md> · 完整协议：<https://github.com/laziobird/openclaw-rpa/blob/main/SKILL.zh-CN.md>

**C. 开发者向（约 100 字）**

本地优先：headed 录屏级自动化，产出 **单文件 Playwright Python**；可含 **httpx 式 API**、**xlsx/docx**。运行时无模型依赖（录制阶段才要 OpenClaw + 强模型）。<https://github.com/laziobird/openclaw-rpa>

**D. LLM / Computer-use 向（约 90 字）**

不想每次 **Computer Use** 都烧 token？把流程 **录成 Playwright 脚本** 再离线跑：网页 + API + Office 文件一步集成。OpenClaw 技能 **openclaw-rpa**：<https://github.com/laziobird/openclaw-rpa>

---

## Twitter / X（字数与电商视频）

**英文主推（≤280 字符，含 Sauce 电商录屏 + 仓库）** — 与 `PROMOTION.en-US.md` 同步：

```
openclaw-rpa: record real browser once → Playwright Python; replay with python3, no LLM.

🛒 E‑commerce demo (Sauce: login → sort → cart): https://github.com/user-attachments/assets/965fbecc-a0fc-4795-9f63-a5ef126f97f8

https://github.com/laziobird/openclaw-rpa
```

**中文主推（≤280 字符）** — 配 Sauce 电商录屏（登录→按价排序→加购）；痛点 + 差异点：

```
每次让 AI 点网页都烧 token？openclaw-rpa：真 Chrome 里录一遍 → 自动生成 Playwright Python，以后 python3 回放，不调大模型、不猜选择器。

🛒 Sauce 电商演示（登录→排序→加购）https://github.com/user-attachments/assets/965fbecc-a0fc-4795-9f63-a5ef126f97f8

https://github.com/laziobird/openclaw-rpa
```

**备选 A（更短，~205 字）** — 偏品牌句 + 视频：

```
openclaw-rpa｜OpenClaw 上的「录一次、跑千遍」：操作写进 Playwright 脚本，回放阶段零 LLM。

🛒 演示站完整购物流（录屏）https://github.com/user-attachments/assets/965fbecc-a0fc-4795-9f63-a5ef126f97f8

https://github.com/laziobird/openclaw-rpa
```

**备选 B（偏开发者）**：

```
还在每次 Computer Use？openclaw-rpa 把流程录成可执行 Python——省钱、更快、少幻觉。

🛒 电商 Demo（Sauce：登录→按价排序→加购）https://github.com/user-attachments/assets/965fbecc-a0fc-4795-9f63-a5ef126f97f8
https://github.com/laziobird/openclaw-rpa
```

**国内可改用 B 站镜像：** <https://www.bilibili.com/video/BV1YfXrBBE9u/>

**案例说明锚点：** <https://github.com/laziobird/openclaw-rpa/blob/main/README.md#1-sauce-online-shopping-website-demo-browser-recording>
