# Perplexity AI — 完整问题全景 + 能力分析

> 合并自 4 份研究报告 + 浏览器实操测绘。2026-08-29。

---

## 一、搜索质量问题（最高频）

### 1.1 编造答案（无依据）— 严重
- 用户报告 ~80% 答案声称的信息"根本不存在"；引用链接指向 404 或无相关内容
- 被质疑后 Perplexity 道歉并承认错误
- Reddit: "Perplexity is constantly lying" (297 个相关帖子)

### 1.2 答案错误 + 被动自纠 — 严重
- 基础查询和研究查询都会出错
- 用户要求复查后才承认错误并给出正确答案
- Labs 模式产生伪造图表（"合成数据"而非真实测量）
- 错误率在近期月份**上升**

### 1.3 引用/链接造假 — 严重，极高频
- 引用链接指向 404 或无相关内容
- 独立测试：Deep Research 编造论文和日期，承认找不到链接
- 大型新闻引用研究：Perplexity 37% 时间引用错误（8 个 AI 搜索工具中最好，但仍超 1/3）

### 1.4 医疗领域造假 — 严重安全问题
- 编造医生评论（假 5 星评分、不存在的引用）
- 2025 学术研究：72% 引用被核查为伪造（~3 个错误/引用）
- Dow Jones & NY Post 因伪造/错误归属新闻起诉

### 1.5 日期过滤失灵 — 中等
- 请求特定日期范围的新闻，返回错误日期的内容

---

## 二、Pro/订阅投诉（最高量，大量"诈骗"帖子）

### 2.1 自动续费 + AI 客服退款墙 — 严重
- $200 年费自动续费，AI 客服"Sam"拒绝退款（72 小时窗口期）
- AI 客服拒绝转人工（"任何团队成员都无法覆盖"）
- 区域退款政策泄露：EU/UK/Turkey 14 天，SK/Brazil 7 天，其他 72 小时

### 2.2 双重扣费 — 严重
- 多用户报告 Pro 被扣两次

### 2.3 降级后功能丧失 — 中等
- 取消 Pro 后回到免费版，功能大幅缩减

---

## 三、API 限制

### 3.1 Web 和 API 是**故意设计成不同产品**
- 官方明确表示**不打算让 API 输出质量匹配 UI**
- Web-only 功能：Pro Search、Collections/Spaces、Focus 模式、图片生成、Model Council、400+ 连接器
- API 可用：Deep Research (`sonar-deep-research`)、有限文档/图片上传

### 3.2 定价陷阱
- 双层模型：token 费率 **+ 固定每请求费** ($6–22/1K 按上下文)
- Deep Research 叠加：$2/1M 引用 + $3/1M 推理（一次发布调用 = $1.32）+ $5/1K 搜索查询
- `auto` search type 静默路由到昂贵的 pro 层

### 3.3 速率限制
- 使用层 0–5 由**终身信用购买**驱动 ($0–$5,000)，非消费计划
- Sonar 50→4,000 RPM；Deep Research 5→100 RPM；Search API 固定 50 QPS

---

## 四、浏览器/App Bug

### 4.1 搜索失败
- 搜索不触发，停留在首页
- 答案生成中断

### 4.2 上下文丢失
- 长对话丢失上下文
- 移动端线程尤其严重

### 4.3 文件处理弱
- 上传不持久化
- 长 PDF 无法端到端读取
- 超过 ~10 页分析可能失败

---

## 五、记忆/知识库限制

### 5.1 薄记忆 + 断线程
- 对话从接近零开始
- 线程坐在列表或 Collections 中，但**不是可搜索的知识库**
- 相关研究无法跨天累积

### 5.2 Collections/Spaces 限制
- 无 API 端点
- 不是真正的知识管理系统

---

## 六、配额不透明

- Pro/Max 限制被描述为"平均"或"高级"使用，而非硬数字
- Computer 积分通常不结转，工作在零时停止
- 消失的月度积分、账单惊喜、账户问题、慢速/自动客服

---

## 七、搜索绑定（非完整工作区）

- 答案继承公共网络的差距、偏见和滞后
- 过去 1-2 小时的突发新闻可能错过 Google 的新鲜度
- 图片生成、浏览器/语音功能、品牌文档/模板仍不完整
- **最佳用途：引用研究层，而非唯一工具**

---

## 八、替代品比较（用户转向）

- Claude/Gemini/ChatGPT 原生应用在长文、代码、推理方面通常优于 Perplexity 内的相同模型
- Google 开始输出结构化搜索结果，Perplexity 的差异化被摧毁
- 多用户取消订阅转向直接使用原生模型

---

## 九、浏览器自动化价值（核心发现）

### 为什么需要浏览器自动化？

| 功能 | Web UI | API |
|------|--------|-----|
| Pro Search (多步骤) | ✅ | ❌ |
| Collections/Spaces | ✅ | ❌ 端点 |
| Focus 模式 | ✅ | ❌ 参数 |
| 图片生成 | ✅ | ❌ 端点 |
| Model Council | ✅ | ❌ |
| 400+ 连接器 | ✅ | ❌ |
| 音频/视频上传 | ✅ | ❌ |
| Deep Research | ✅ | ✅ `sonar-deep-research` |
| 文档/图片上传 | ✅ | ✅ base64/URL |

**结论**: 浏览器自动化是榨干 Perplexity 的唯一完整路径。

---

## 十、已验证的自动化流程

```
navigate → snapshot → click textbox → fill query → 三事件 Enter → wait → "查看更多" → extract
```

### 关键坑

| 问题 | 解决方案 |
|------|---------|
| fill 不生效 | 必须先 click textbox 再 fill |
| Enter 不触发 | beforeinput + keydown + keyup 三事件 |
| 答案被截断 | 点击"查看更多"展开 |
| @e ref 每次不同 | snapshot + regex 动态查找 |
| JSON 有空格 | `separators=(",",":")` |

---

## 证据来源

- Reddit: 297 个帖子 URL (r/perplexity_ai, r/Perplexity, r/AIDangers, r/artificial, r/ChatGPTPro, r/LocalLLaMA)
- X/Twitter: 通过新闻转载引用（xAI 额度耗尽）
- 官方社区论坛: Discourse + GitHub api-discussion
- BBB/Trustpilot: 负面评价汇总
- 媒体/法律: Android Authority, PiunikaWeb, Dow Jones/NY Post 诉讼
- 浏览器实操: 2026-08-29 直接测试
