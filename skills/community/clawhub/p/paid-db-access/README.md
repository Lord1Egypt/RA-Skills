# Paid Database Access

> 🚀 AI 接入付费学术数据库（IEEE/Scopus/Engineering Village/ACM）的权限桥接层。通过浏览器 CDP 借用用户登录态，让 AI Agent 替你搜索付费学术数据库。

**如果你只是想知道怎么用 → [QUICKSTART.md](QUICKSTART.md)**

---

## 解决了什么问题？

所有 AI 文献工具（Elicit、Consensus、SciSpace）只能搜公开论文。你机构花几十万订阅的 IEEE Xplore、Scopus、Engineering Village、ACM Digital Library，AI 一个都搜不到。

而数据库厂商自己的 AI（Scopus AI、WoS RA）只做单库，不出围墙。

**这个工具做的是：用一个 AI Agent 替你并行搜索四个付费数据库，3 分钟跑完一次文献综述。**

---

## 怎么做到的？

两个核心技术：

### 1. 浏览器 CDP 认证桥
不偷 cookie、不破解登录——直接用 Chrome DevTools Protocol 连接你**已经登录的**浏览器会话。对数据库服务器来说，请求来自你的 IP、你的 cookie、你的浏览器指纹。它就是你在浏览。

### 2. Zero-token 摘要架构
搜索结果用 JS 注入提取结构化 JSON（不用 snapshot，token 消耗 1/50）。摘要全部写文件系统，JSON 只存文件引用。摘要在整个管道中**从未进入过 LLM 上下文**。

---

## 管道

```
[0] 前置检查 → [0.5] OpenAlex 免费预检 → [1] 四库并行搜索
                                              ↓
[2] 合并 + 分层补摘要（Tier 0→1→2）→ [3] 评分 + 主题聚类 + 输出
```

详见 [SKILL.md](SKILL.md)。

---

## 支持的数据库

| 数据库 | 搜索方式 | 摘要来源 | 需要 |
|---|---|---|---|
| IEEE Xplore | 浏览器 + JS 提取器 | Tier 0/1/2 | 浏览器已登录 |
| Scopus | API | Tier 0/1/2 | API Key |
| Engineering Village | 浏览器 + JS 提取器 | Tier 0/1/2 | 浏览器已登录 |
| ACM Digital Library | 浏览器 + JS 提取器 | Tier 0/1/2 | 浏览器已登录 |

---

## 依赖

- Python 3.10+
- OpenClaw (浏览器 CDP + 子代理)
- 浏览器已登录目标数据库（机构 VPN/代理如需要）
- Scopus API Key（可选，仅 Scopus 需要）

---

## 快速开始

见 [QUICKSTART.md](QUICKSTART.md)。

---

## 声明

本工具通过用户已有的浏览器会话操作付费数据库，仅供个人学术研究使用。各数据库的自动化使用条款可能存在差异，请自行评估合规性。

---

## 许可

MIT License — 详见 [LICENSE](LICENSE)
