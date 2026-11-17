---
name: llm-endpoint-switching
slug: llm-endpoint-switching
version: 1.1.0
displayName: 切换 LLM 端点（OpenAI 兼容第三方）
description: |
  把脚本里的 LLM 从一个 OpenAI 兼容端点/模型换到另一个时的排查手册。
  重点覆盖三类必踩的坑：**Cloudflare 拦 urllib 默认 UA 导致 403
  「error code: 1010」**（会被误判成 key 无效，换真 key 也照样403）、
  **切到免 key 端点时空串是真值陷阱**（`configure()` 用 `if api_key:`
  会让旧付费 key 沿用 → 必 401），以及**先 --ping 预检再跑批量**的做法。
  当用户说「换成 XX 模型」「加个模型」「这个 API 报 403 / 400 / 404」
  「AI 调用失败」「key 明明是对的却说无效」「怎么切模型」
  「换成免 key 的模型」「切过去之后 401」时使用。
category: development
agent_created: true
---

# 切换 LLM 端点（OpenAI 兼容第三方）

## 核心结论

OpenAI 兼容端点之间迁移，**通常只改 base + model 两个值**，请求体不用动。
但有两件事会咬人，且都会伪装成「key 无效」或「参数错误」。

## 坑一：⚠ 第三方端点前面挂 Cloudflare，urllib 默认 UA 被拦

**症状**：HTTP 403，响应体是 `error code: 1010`（有时只有这一个数字，
没有 JSON、没有 errmsg）。

**根因**：`urllib.request` 的默认 User-Agent 是
`Python-urllib/3.x`，Cloudflare 的 WAF 规则直接拦下。**这不是鉴权问题，
换真 key 也照样 403**——因为请求根本到不了鉴权那一步。

**2026-10-01 实测**（OpenCode Zen / Space Bunny）：

| 请求头 | 结果 |
|---|---|
| 默认（无 UA） | `HTTP 403  {"error code": 1010}` |
| `User-Agent: Mozilla/5.0 … Chrome/126.0` | `HTTP 401  Invalid API key` |

403 → 401 的转换本身就是结论：**请求形状已经通了，只差 key**。

**修法**（每次请求都带上，不是只在抓网页时带）：

```python
req = urllib.request.Request(
    url, data=body,
    headers={"Content-Type": "application/json",
             "Authorization": "Bearer " + key,
             "User-Agent": UA,          # ← 关键，别漏
             "Accept": "application/json"})
```

⚠ **别只在抓网页的函数里带 UA，LLM 请求单独漏掉**——这个漏项极隐蔽，
代码看着没问题，但一换端点就403，而且所有人都会先怀疑 key。

## 坑二：先ping 再跑批量

换端点后**先发一个极短请求验通**，别直接跑一批 20 条核验任务。
一次核验的思考 token 可能上千，key 不对就是白烧时间和额度。

实现要点：ping 不碰任何业务数据、不写任何文件，只发一个
「只回这个 JSON」的请求并打印耗时。

##状态码分诊（别一律报「调用失败」）

这四类指向完全不同的问题，混在一起会让人白排查半天：

| 状态码 | 真实原因 | 下一步 |
|---|---|---|
| **403** | Cloudflare/WAF 拦 UA | 补浏览器 UA（**不是 key 问题**） |
| **401** | key 无效 / 没这个订阅 | 换 key、查订阅状态 |
| **404** | base 或 model 名写错 | `GET <base>/models` 列可用值 |
| **400** | 参数被拒 | 多半是 `response_format` 或 `max_tokens` 超上限 |

**400 最常见的两个原因**：

1. 端点不支持 `response_format={"type":"json_object"}`
   —— 部分第三方端点（尤其聚合/中转站）不支持，
   而有些脚本的 JSON 解析链路硬依赖它。
   ⚠ 这时要权衡：要么换端点，要么给该端点单独走「提示词里要求返回 JSON
   + 代码里容错解析」的降级路径，**别默默把 JSON 模式关掉**。
2. `max_tokens` 超过端点上限 —— 换个更小的值试。

## 推理模型的 max_tokens 陷阱

**思考 token 也计入 `max_tokens`**。核验类任务（要塞进几万字网页原文、
要求结构化输出）实测一条要烧 4000+ token，其中思考可能占 3600。

⇒ 把上限放宽到能容纳「思考 + 正文」，并在 `finish_reason == "length"`
时**明确报错**（内容被截断，JSON 不完整，硬解析会得到莫名其妙的结果）：

```python
if ch.get("finish_reason") == "length":
    raise RuntimeError("LLM 回答被 max_tokens 截断（finish_reason=length）"
                       "——模型思考太长，正文没输出完整 JSON")
```

⚠ 别拿「超时」当失败结论，但 `finish_reason=length` 是**真实截断**，必须处理。

## base 拼接约定

```
base = "https://example.com/v1"     ← 填到 /v1，不要带 /chat/completions
url  = base + "/chat/completions"
```

**base 尾部斜杠会被 rstrip**，但 base 里**必须包含版本段**。
写了 `/v1/` 和 `/v1` 效果一样；写成不带 `/v1` 会在拼出
`/chat/completions` 时404。

## 配置注入的两种方式

```python
# 1) 环境变量（适合容器/CI，密钥不进代码）
BASE = os.environ.get("X_AI_BASE", "https://api.deepseek.com").rstrip("/")
MODEL = os.environ.get("X_AI_MODEL", "deepseek-chat")
KEY = os.environ.get("X_AI_KEY", "")

# 2) 运行期 configure()（适合后台 GUI 存密钥、CLI 临时切换）
def configure(api_key=None, base=None, model=None):
    """不传的项保持原值 —— 后台存 key 就靠这个语义。"""
    global KEY, BASE, MODEL
    if api_key: KEY = api_key
    if base:    BASE = base.rstrip("/")
    if model:   MODEL = model

configure(model="new-model")          # 只换模型，沿用原 base/key
```

⚠ **`configure()` 必须「不传的项保持原值」**——如果写成整体覆盖，
后台只存了 key 却把 base/model 清空了，会表现为「存了密钥反而连不上」。

## 测试怎么写

这几条值得钉死，否则下次重构会静默回归：

1. **请求头必须有浏览器 UA** —— 用假的 `urlopen` 捕获请求对象断言
   （这是本次唯一的真 bug，最该被回归钉住）。
2. `configure()` 只覆盖传入项（断言只传 model 时 base/key 不变）。
3. ⚠ **`configure(api_key="")` 必须真清空 key** —— 用真值判据会静默跳过空串，
   免 key 端点必401。这条是 2026-10-04 的事故，务必钉死。
4. `configure()` 会 rstrip base 的尾部斜杠。
5. ping 在没 key 时**不联网**且返回非零。
6. ping 对 403/401/404/400 给出**各自不同**的诊断文案。
7. ⚠ `ai_ready()` / `is_no_key_endpoint()` 的判断口径（无 key 但免 key 端点 → 就绪）。

⚠ 断言请求头时注意 `dict(req.headers)` 的键是**小写**，
`self.assertIn("Authorization", headers)` 会假失败。

## ⚠⚠ 坑三：切到**免 key 端点**时，空串是真值陷阱（2026-10-04 血案）

从付费端点（DeepSeek 等）切到免 key 端点时，**要改的不只是 base + model**。
下面每一条都实测撞过，不是理论风险。

### 3.1 `configure()` 用真值判据 ⇒ 旧 key 清不掉 ⇒ 必 401

```python
# ❌ 错的写法
def configure(api_key=None, base=None, model=None):
    if api_key:            # ← "" 是 falsy，空串被跳过！
        KEY = api_key

# ✅ 正解：判据是 is not None
def configure(api_key=None, base=None, model=None):
    if api_key is not None:
        KEY = api_key
```

**实测后果**（2026-10-04，OpenCode Zen / Space Bunny）：

| 场景 | 结果 |
|---|---|
| 空 Bearer（`AI_KEY = ""`） | ✅ 200 |
| 带着旧的 DeepSeek key | ❌ 401 `Invalid API key` |

后台 GUI「保存」时通常传空串表示「清空 key」—— 真值判据下这个请求
**静默不生效**，旧付费 key 被沿用，于是拿付费 key 打免 key 端点，必 401。
**排查这类 401 时第一件事是打印 `AI_KEY` 到底是不是空**，别盯着 key 有效性查。

⚠ 同一个坑还有 CLI 侧：`if args.ai_key or args.ai_base or args.ai_model`
会把 `--ai-key ""`（显式清空）当成「没传」。用
`any(v is not None for v in (...))`。

### 3.2 切端点时旧 key 要删干净，不能只改 base/model

配置文件里留着 `ai_key` 字段 = 每次调用都发付费 key → 401。
正确做法是**整个字段删掉**，不是留空串（留空串在某些读取侧等价于「有值」）。

### 3.3门禁别拿「有没有 key」当「能不能运行」

免 key 端点**压根没有 key**，所以任何 `if not key: return 400`
的门禁都会把这类配置全挡在门外 —— 表现为「配置明明对了但点运行就报错」。

```python
# ✅ 单一判据，CLI / 后台 / 前端共用
NO_KEY_HOSTS = ("opencode.ai/zen",)

def is_no_key_endpoint(base=None):
    return any(h in (base or AI_BASE or "") for h in NO_KEY_HOSTS)

def ai_ready(key=None, base=None):
    k = AI_KEY if key is None else key
    b = AI_BASE if base is None else base
    return bool(k) or is_no_key_endpoint(b)
```

⚠ 后台状态接口要同时给三个字段，**前端只能看 `ready`**：

```python
{"has_key": bool(k), "ready": ai_ready(k, b), "no_key_endpoint": is_no_key_endpoint(b)}
```

`has_key` 对免 key 配置恒为 False，前端拿它判「能不能跑」会把可用配置
误报成「未配置 Key」——用户会以为是配置错了，反复瞎填。

⚠ **门禁里引用配置变量前先确认它已赋值**：写成
`if not ai_ready(st["key"], ...)` 而 `st = resolve_ai_settings()` 在下一行，
会得到 `UnboundLocalError`（Python 把它当局部变量），前端表现为
**HTTP 000 / 连接被拒**，日志里才有真因。

### 3.4 免 key 与付费端点的能力差异要提前说清

免 key 模型往往**更慢**（实测单条核验 152 秒 vs 付费端点的秒级），
且自报模型名不可信（实测回显 `n="ChatGPT"`）。
换过去之前告诉用户代价，别让「能跑」被误解成「一样好用」。

## 「模型列表里有 free」≠「现在能调」（2026-10-01 实测）

要回答「现在有哪些免费模型能用」，**必须逐个发真实请求**，不能只分析模型名。

实测某端点：`GET /v1/models` **免 key** 就能列出 **84 个**模型，其中 11 个 id 含
`free` —— 逐个发真实请求后，**只有 1 个**真能免 key 调用：

| 真实原因 | 数量 | 能否绕过 |
|---|---|---|
| `free tier can only be used from within <客户端>` | 6 | ❌ 服务端校验客户端来源，伪造 `X-Client`/`Origin`/`UA` 全部无效 |
| `not available in your country` | 2 | ❌ 地区限制 |
| 上游 500 / 模型已下线 | 2 | ❌ 临时故障或下线 |

⇒「模型名带 free」**不能当可用性证据**。免费模型可用性会漂移，
所以要有个**独立探测项目**定期发真请求，消费方只读它的档案（`ok=true` 才用）。

### 免 key 的正确姿势：发**空 Bearer**，不是省略

| 写法 | 结果 |
|---|---|
| `Authorization: Bearer `（空值） | ✅ 200 |
| 完全省略 `Authorization` 头 | ❌ 挂到**超时**才报错 |
| `Authorization: Bearer free` | ❌ 401 |
| `Authorization: Bearer sk-xxx`（占位） | ❌ 401 |

服务端会校验 key 是否**真实存在**，只有空值才走免鉴权分支。
所以「我没有 key」**不能**表达成 `Bearer 无key`，只能表达成空值。
⚠ 省掉整个头是最容易踩的写法 —— 表现为超时，不像鉴权问题，很难联想到。

### ⚠ 档案文件绝不能包含密钥

探测项目若要输出「给别的项目消费」的档案，**档案里绝不能有 key**：
档案会被 HTTP 接口原样返回，也可能被消费方提交进仓库。
正确做法是**只写 `no_key: true/false` 标记**（这个源要不要 key），
key 由消费方自己配。再加一层出站脱敏兜底，防将来回归。

⚠ **写测试时别把漏洞行为固化成断言** —— 「带 key 时 auth 落进档案」这种
断言看着合理，实际是在给泄露开后门。改写成「带 key 时档案里也没有 key」。

## 关联

- 本机已有一个可复用的实现参考：`ai-case-library/scripts/ai_verify.py`
  的 `llm()` / `configure()` / `ping_llm()`，以及
  `scripts/test_ai_verify.py` 里的 `LlmEndpointTest`（7 项，
  含「空串必须真清空 key」回归钉）。

⚠ **本 skill 提到的免费模型探测项目已下线**（2026-10-04 清理）：
`free-llm-probe` / `llm.ydtgo.top` 的站点、仓库、DNS 记录、本地目录
全部删除，配套的「可用性档案」机制也已移除。
上面「档案」相关的内容保留为**方法论**（怎么判断一个端点值不值得用），
但**没有现成档案文件可读了** —— 要判断当前有哪些免费模型可用，
得自己写临时脚本逐个发真实请求。