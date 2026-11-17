# owlwrite MCP 接入说明（可选 · 给需要 MCP 的客户端）

> **先看这里**：技能默认**不需要** MCP——装好技能、保存一次 key 就能用（见 `quickstart.md`）。
> 本文只给「不能执行命令、只支持自定义 MCP」的客户端（如 Claude Desktop / Cursor）用。
> 两条路径能力与返回字段完全一致，已有 MCP 配置的老用户无需任何改动。

## 0. 接入方式怎么选（三种，按省事程度排）

| 方式 | 适合谁 | 前提 |
|---|---|---|
| ① 技能包（推荐） | WorkBuddy、SkillHub / ClawHub 生态的 Agent | 平台内一键安装，无需任何配置 |
| ② 平台官方 MCP 连接器 | 平台已上架的（陆续接入中，以平台内搜到为准） | 没上架的平台用方式 ③ |
| ③ 自助 MCP 配置（本文） | 任何支持自定义 MCP 的 Agent：Claude Desktop / Claude Code / Cursor / Cline / Codex CLI 等 | 只要：注册拿 Key + 本机 Python ≥ 3.11 + 改一份配置文件 |

> 只支持**远程 MCP**（HTTP 地址直连）的 Agent（如千问办公网页版、扣子等）：需要服务端开放远程端点，
> 目前尚未开放。可先用方式 ①（若该平台支持装技能）或网页版个人中心（充值、检测、下载报告）。

## 0.1 装技能（只有两个官方入口）

| 渠道 | 地址 |
|---|---|
| SkillHub | https://skillhub.cn/skills/user_164f4c1f/owlwrite-paper |
| ClawHub | https://clawhub.ai/j-levee/skills/owlwrite-paper |

别从其他站点、镜像或第三方脚本装同名技能。装完先做下面三步自检，再往下配 Key：

1. `curl -s https://owl.skillsutra.cn/v1/meta` → `skill.latest_version` 不低于 `skill.min_supported_version`（以接口返回为准，别背数字）；
2. 同一响应里 `channels.weipu_ready` 决定能不能做检测（`false` 读 `weipu_detail` 转告用户）；
3. 配好 Key 后调 `owl_wallet`，能返回余额即连通。

## 1. 拿到 API Key（对话内即可完成）

注册需要邮箱验证码（15 分钟有效），两步：

```bash
# 1) 发验证码到你邮箱
curl -s -X POST https://owl.skillsutra.cn/v1/auth/send-code \
  -H "Content-Type: application/json" -d '{"email":"你的邮箱"}'

# 2) 把邮件里的 6 位码填进去，换 API Key
curl -s -X POST https://owl.skillsutra.cn/v1/auth/register \
  -H "Content-Type: application/json" -d '{"email":"你的邮箱","code":"123456"}'
```

返回里的 `api_key`（`owl_sk_` 开头）**只显示这一次**，立刻存好。
也可在官网 https://paper.skillsutra.cn 右上角「开始使用」注册，二选一。

> 体验额度以注册返回的 `wallet.balance_avail` 为准，不要预设金额。
> 退信/收不到：先查垃圾邮件箱；同邮箱 60 秒内只能发一次，同一网络 10 分钟最多 10 次。

## 2. MCP 客户端配置

### Claude Desktop / WorkBuddy（claude_desktop_config.json）

```json
{
  "mcpServers": {
    "owlwrite": {
      "command": "python",
      "args": ["<技能目录>/owlwrite-paper/scripts/mcp_server.py"],
      "env": {
        "OWL_BASE": "https://owl.skillsutra.cn",
        "OWL_API_KEY": "owl_sk_你的key"
      }
    }
  }
}
```

### Cursor（~/.cursor/mcp.json 或项目 .cursor/mcp.json）

```json
{ "mcpServers": { "owlwrite": {
  "command": "python",
  "args": ["<技能目录>/owlwrite-paper/scripts/mcp_server.py"],
  "env": { "OWL_BASE": "https://owl.skillsutra.cn", "OWL_API_KEY": "owl_sk_你的key" }
}}}
```

### Claude Code（命令行一条搞定）

```bash
claude mcp add owlwrite \
  --env OWL_BASE=https://owl.skillsutra.cn \
  --env OWL_API_KEY=owl_sk_你的key \
  -- python <技能目录>/owlwrite-paper/scripts/mcp_server.py
```

### Cline / 其他 VS Code 类插件

设置界面的 MCP JSON 与 Claude Desktop 结构完全相同（`mcpServers.owlwrite`，command/args/env 三件套）。

### Codex CLI（~/.codex/config.toml）

```toml
[mcp_servers.owlwrite]
command = "python"
args = ["<技能目录>/owlwrite-paper/scripts/mcp_server.py"]
env = { OWL_BASE = "https://owl.skillsutra.cn", OWL_API_KEY = "owl_sk_你的key" }
```

> 只支持远程 MCP 的平台（千问办公、扣子等）：暂未开放远程端点；平台若有技能/插件市场
> 可搜「owlwrite」安装（方式 ①），或用网页版个人中心完成充值、检测与报告下载。

- `<技能目录>` 换成你本机技能包实际路径（`scripts/mcp_server.py` 就在技能包里，无需另下文件）。
  Windows 路径用双反斜杠 `C:\\...` 或正斜杠；`python` 不存在时换成 `python3` 或完整安装路径。
- `OWL_BASE` 固定填 **`https://owl.skillsutra.cn`**（接口地址）。官网是 `paper.skillsutra.cn`，
  两者不同域，填错会连不上。
- Python ≥ 3.11，需 `pip install mcp httpx`（装在与配置里同一个 Python 里）。
- **上传大文件把客户端超时放宽**：`owl_upload` 传 30MB 论文在上行慢的网络可能超过 30 秒，
  远程接入时把 `timeout` 设到 `120000`（毫秒），否则会在本地先超时而服务端其实已收下。

### 配好后验证与冷启动注意

对话里说「查一下肠道菌群和代谢的文献」，能返回带 DOI 的文献列表即接入成功；
再说「看看我的余额」（owl_wallet，免费）可确认计费链路。

### 常见问题

| 现象 | 原因与处理 |
|---|---|
| 提示「未配置 OWL_API_KEY」 | env 里没写，或 Key 前后有空格/中文引号；重新复制粘贴 |
| 工具列表为空 / 连接失败 | 检查 Python 路径与 mcp_server.py 路径；确认 `pip install mcp httpx` 装在同一个 Python |
| 调用报 401 | Key 被吊销或填错；个人中心重建 Key 后改配置 |
| 上传 30MB 论文超时 | 客户端 MCP 超时调到 120000 毫秒，服务端其实已收下 |
| 检测类报不可用 | 调 owl_meta 看 `channels.weipu_detail`，转告用户即可，不是配置问题 |

- **冷启动陷阱**：MCP 客户端启动后第一次调工具可能报连接错误——是客户端在拉起本地进程，
  等几秒重试即可，不要改配置重装；连续失败才检查 `OWL_BASE`（服务端是 owl.skillsutra.cn，
  官网是 paper.skillsutra.cn，两者不同域，填错连不上）。
- **开工先调 `owl_meta`**：返回 `notices` 是平台公告（如检测服务状态、活动上线），
  有新公告要按相关度转告用户；`channels.weipu_ready=false` 时检测类能力暂不可用，别白跑报价。
  该字段是检测服务的**真实连通性**（`queryBalance`）检查结果，不是「凭据填没填」；原因看同级
  `channels.weipu_state`（`unconfigured` / `auth_failed` / `ip_blocked` / `account_issue` /
  `unverified`）与 `channels.weipu_detail`，对用户只转述 `weipu_detail` 这句人话。
- **版本判定**：`owl_meta` 的 `required_update=true` 且本地版本低于 `min_supported_version`
  时必须先让用户更新技能再继续付费动作。

## 3. 工具一览（22 个）

| 工具 | 作用 | 计费 |
|---|---|---|
| `owl_search` | 文献检索（相关性重排 + 核心刊标记 + 关键词扩展） | 实时报价（缓存 1 积分 / 0 结果 0 积分） |
| `owl_article` | 文献详情（DOI / 年卷期等完整元数据） | 实时报价；72 小时缓存 1 积分 |
| `owl_fulltext` | 中文期刊全文 PDF 直链（约 1 小时有效，立即下载） | 实时报价；72 小时内同篇重取 1 积分 |
| `owl_oa` | 外文 OA 免费全文（arXiv / OpenAlex / Unpaywall / Europe PMC） | **0 积分，免费** |
| `owl_citations` | 引文追溯（它引用了谁 / 谁引用了它） | 实时报价；72 小时缓存 1 积分 |
| `owl_figure` | 科研配图（TikZ 示意 / 数据图表 / AI 配图） | 25 积分/张，按实际交付张数；未出图 0 积分 |
| `owl_products` | 全平台实时价目（价格唯一可信来源） | 免费 |
| `owl_meta` | 技能最新版本 + 平台公告（开工校准；含 `channels.weipu_ready` 检测服务状态） | 免费 |
| `owl_disciplines` | 斟知智评学科码表（class_id 用，逐级筛给用户选） | 免费 |
| `owl_campaign` | 活动券码兑换 / 我的邀请码与战绩 | 免费 |
| `owl_upload` | 上传本机文件换 `file_id`（检测 / 图像 / 格式检测必用；≤30MB） | 免费 |
| `owl_quote` | 写作 / 检测 / 核验 / 排版报价（返回预估区间；检测需给 `hanzi`） | 免费（不扣积分） |
| `owl_run` | 执行已报价任务 | 写作/检测按**实际量**结算（无冻结、无封顶），其余按报价 |
| `owl_run_status` | 轮询任务状态（含 `pending_upstream`＝报告仍在生成，不是失败） | 免费 |
| `owl_run_report` | 核验逐条判定；检测报告四份（`part=main` 综合 / `compare` 逐句比对 / `simple` 简洁 PDF / `fulltext` 原文对照 PDF） | 免费 |
| `owl_run_content` | 写作完整正文与参考文献 | 免费 |
| `owl_wallet` | 查余额（含 30 天内到期积分、赠送积分余额） | 免费 |
| `owl_ledger` | 逐笔积分流水（含每笔后余额，对账用） | 免费 |
| `owl_recharge` | 发起充值（10/30/50/100/500 元） | 免费 |
| `owl_recharge_status` | 查充值单 / 核实到账 | 免费 |
| `owl_typeset` | 论文排版（LaTeX 工程 / Word 按学校模板 → 可提交 PDF + 同版式 Word + 格式体检单；支持盲审版与 GB/T 7714 双标准；72 小时内同稿重排只收工本） | 实拉（一篇一价） |
| `owl_claim_favorite` | 收藏活动领积分（在技能市场收藏本技能后提交截图） | 免费 |

1 积分 = 0.01 元；充值购买积分有效期 1 年，活动/赠送积分有效期 90 天，均先到期先扣；
全平台缓存命中统一 1 积分，**缓存窗口统一 72 小时**。
价格可能调整，一切以 `owl_products` / `owl_quote` 实时返回与官网 /price 页为准。
任务失败自动退款；检索无结果不收费；OA 探测不收费。

## 4. 官网能补什么（可选，不是必经）

- 个人中心 https://paper.skillsutra.cn/account.html：余额与流水、任务记录、报告与全文下载、API Key 管理与吊销。
- 报告验真：维普 https://vpcs.fanyu.com/systemVerify 、斟知 https://www.zhenzhi.com/verify 。
- 发票 / 企业采购 / 多账号 / API 对接：**vipsmart@vipslib.com**。

## 5. 安全须知

API Key 等同钱包钥匙：不要发到群里、不要贴给他人或截图外传，只出现在你自己设备的配置文件里；
怀疑泄露就到个人中心「API Key 管理」吊销重建（余额不受影响）。
