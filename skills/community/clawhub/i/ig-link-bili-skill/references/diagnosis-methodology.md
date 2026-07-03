# 撞墙诊断方法论（2026-06-07 教训 · 元归因纪律）

**这一节是整个 ig-link-bili skill 的元规则**——比单条 pitfall 重要。**撞墙时先读这一节再读具体 pitfall**。

---

## 核心立场

**任何"上游抽风 / 风控 / 服务器挂 / 对方就是拒"的判断，必须有本机近 30 分钟的诊断证据支撑，且没被其他 agent 反例证伪。否则就是脑补。**

—— Arvin 2026-06-07

## 撞墙时的强制顺序

撞墙（upload 失败 / 验真 PENDING / 接口 403 / 错误页）时**不要先归因**——按以下顺序跑：

1. **先排除自己的问题**——cookie 三件套齐不齐 + 编码对不对 + shell 引号对不对 + agent 读到的状态是不是过期
2. **再看反例**——别的 agent（Codex / Claude Code / 别的 session）最近做过类似任务吗？他们的成功案例直接证伪"上游挂了"判断
3. **再**按 `references/pitfalls.md` §7 决策树跑 Step 1-3
4. **最后**才把"已跑过的诊断 + 看到的事实"交给 Arvin 决定

## ⚠️ 裸 curl 验证 ≠ 真实上传请求形态（2026-06-07 实测 · 必读）

**这是本节最重要的一条**——一个具体翻车模式：诊断 Step 3 跑了，但跑错形态。

### 翻车现场（2026-06-07 DZQCbihCu0f 那条 Reel）

我按 §7 决策树跑了：
```bash
curl -sS -m 10 "https://api.bilibili.com/x/web-interface/nav" \
  -b "SESSDATA=b3a3f104%2C...; bili_jct=f0f70e3a...; DedeUserID=34439351" \
  -o /tmp/nav_resp.json -w "http=%{http_code}\n"
# → http=200
```

读 JSON：
```
{"code":-101,"message":"账号未登录","ttl":1,"data":{"isLogin":false,...}}
```

→ 我归因"**风控对所有非浏览器来源一刀切**"→ 给 Arvin 列"风控拦截"选项 → **结论完全错了**。

### 真因

裸 curl 验证时**手拼 cookie 串 + 缺关键 header**：
- 没有 `User-Agent: Chrome/126`
- 没有 `Referer: https://www.bilibili.com/`
- 没有 `buvid3`
- 没有 `bili_ticket`

→ 实际请求形态跟上传库 httpx 客户端**完全不同** → nav API 按"低信任度请求"返 -101。

**但真实上传库请求**（带齐 headers + cookie）→ 同一个 cookie 串 → nav 返 `isLogin: True`！

### 诊断反例（2026-06-07）

- 我裸 curl 验：`-101 账号未登录`
- Codex 用上传库实跑：`NAV isLogin=True uname=<你的用户名>`
- Codex 用上传库实跑：`PREUPLOAD has_upos_uri=True has_auth=True`
- Arvin 一句话纠错："**他这个结论不成立，至少不适用于我们这台机器的当前状态**"

→ **裸 curl 验证的"事实"**被**真实上传库的反例**直接证伪。

### 正确做法：诊断必须用真实请求形态

撞墙时**不要用裸 curl 验登录态**——**直接用上传库本身跑诊断**：

```python
# /tmp/diag_real_request.py
import sys, json, asyncio
sys.path.insert(0, "/path/to/bilibili_uploader")
from main import BilibiliAllInOne

async def main():
    bilibili = BilibiliAllInOne(credential_file="/path/credentials.json")
    pub = bilibili.publisher

    # 1) 看预上传（这是上传库真实请求形态）
    try:
        result = await pub._preupload("/tmp/any.mp4")  # 不真传文件，只验接口
        print("PREUPLOAD:", json.dumps(result, ensure_ascii=False)[:200])
    except Exception as e:
        import traceback; traceback.print_exc()

asyncio.run(main())
```

或者更简单——**直接跑上传库的 verify 子命令**（如果它支持）：

```bash
python3 /path/to/upload_one.py verify
```

它内部用 httpx + 完整 headers 验证，返回 `success` 才算真成功。

### 决策树修正

```
撞墙了
├── 1. 排除自己：cookie 三件套齐不齐？同源同会话吗？
│     跑 /tmp/diag_real_request.py（用上传库）
│     ├── 上传库能 PREUPLOAD 200 + 有 upos_uri → 上传库正常，问题在 upload 流程别处
│     └── 上传库 PREUPLOAD 403 → 跳到 #2
├── 2. 看反例：别的 agent 最近成功过吗？
│     ├── 有反例 → 我诊断方式错（裸 curl 形态不对）→ 用真实库重新诊断
│     └── 都没做过 → 跳到 #3
├── 3. 按 pitfalls §7 跑 Step 1-3（**用真实库，不要用裸 curl**）
└── 4. 跑完才交给 Arvin 决定
```

## 撞墙时绝对不要做的事

- ❌ **不要裸 curl 验登录态**（缺 headers → 假阴性 -101）
- ❌ **不要循环重试 3-5 次"等它自己好"**（上游问题不会自愈）
- ❌ **不要凭 HTML 错误页文案归因**（CDN 抽风 / 未登录 / cookie 失效 三种情况文案完全一样）
- ❌ **不要归因"风控"**（除非本机近 30 分钟有反例证伪成功）
- ❌ **不要自己脑补"原因"**（Arvin 明确反对：硬编码到 SKILL.md / 状态文件里的"原因"必须等 Arvin 确认才写）

## Arvin 撞过的真翻车模式

| 模式 | 翻车 | 修复 |
|---|---|---|
| 凭单次失败归因上游 | "B 站挂了" ×3 重试 | 反例证伪后改用真实库诊断 |
| 裸 curl 验登录态 | 假阴性 -101 | 用上传库实跑 |
| cookie 字段拼接 | skill 自带 SESSDATA 空 → 误判上游 | 检查 credentials.json 三件套 |
| 字段跨源拼接 | SESSDATA + buvid3 来自不同窗口 → -101 | 三件套必须同源同会话 |
| 读自己环境状态当事实 | "我读到的 cookie 是空" | 反例：我自己 cookie 读失败 ≠ 真实 cookie 失效 |

## 写给未来 agent 的 4 条铁律

1. **撞墙时不要归因——先诊断**（顺序：自己问题 → 反例 → 真实库诊断）
2. **诊断必须用真实请求形态**（上传库本身，不是裸 curl）
3. **有反例直接证伪自己的判断**——不要死磕"上游理论"
4. **跑完诊断后把事实交给 Arvin 决定**——不要替他做"上游 vs 下游"判断
