# 夜猫子论文工作台 · owlwrite-paper

> 面向 AI Agent 的论文全流程技能包：**找文献 → 写初稿 → 跑检测 → 核引文**，全程在对话里完成，产物落到用户自己的电脑。

- 版本：**1.3.2**（**装好即用：不配置 MCP 也能直接跑**；MCP 接入方式保留为可选）
- 官网与实时价目：https://paper.skillsutra.cn （价目页 `/price`，一切报价以接口实时返回为准）
- 服务端点：https://owl.skillsutra.cn （MCP / HTTP 接口）

## 安装（两个官方入口，任选其一）

| 渠道 | 地址 |
|---|---|
| SkillHub | https://skillhub.cn/skills/user_164f4c1f/owlwrite-paper |
| ClawHub | https://clawhub.ai/j-levee/skills/owlwrite-paper |

> 只有这两个入口。其他站点、镜像、第三方脚本或同名仿制品都不代表本服务。

装完自检四步：

1. `GET https://owl.skillsutra.cn/v1/meta` → `skill.latest_version` 不低于 `skill.min_supported_version`（以接口返回为准，别背数字）；
2. 同一响应的 `channels.weipu_ready` 为 `true` 才做检测类任务，为 `false` 时读 `channels.weipu_detail` 如实告知用户；
3. 调 `owl_wallet` 能返回余额 → API Key 与服务端连通；
4. `owl_*` 工具共 22 个（含 `owl_upload` 换 `file_id`、`owl_typeset` 排版出稿、`owl_claim_favorite` 领活动积分）。

**不配 MCP 的最小自检链路（命令行模式）**：`python scripts/owl.py init`（保存 key）→ `python scripts/owl.py doctor`（无 key 也能测连通性、查版本更新）→ `python scripts/owl.py search "检索词"`（跑一次真实检索）。三步详见 [`references/quickstart.md`](references/quickstart.md)。

### 手动装（离线 / 自建宿主）

1. 把本仓库内容放到 Agent 的技能目录（保留 `SKILL.md`、`references/`、`scripts/` 结构）。
2. MCP 客户端配置指向 `scripts/mcp_server.py`，填自己的 API Key：

```json
{
  "mcpServers": {
    "owlwrite": {
      "command": "python",
      "args": ["<本仓库路径>/scripts/mcp_server.py"],
      "env": { "OWL_BASE": "https://owl.skillsutra.cn", "OWL_API_KEY": "owl_sk_你的key" }
    }
  }
}
```

3. API Key 在 https://paper.skillsutra.cn 注册后获取（只显示一次）。

详细步骤见 [`references/mcp-setup.md`](references/mcp-setup.md)、命令行模式上手见 [`references/quickstart.md`](references/quickstart.md)，商品与能力边界见 [`references/product-matrix.md`](references/product-matrix.md) 与 [`references/coverage.md`](references/coverage.md)。

## 能力

| 类别 | 工具 | 说明 |
|---|---|---|
| 文献 | `owl_search` `owl_article` `owl_fulltext` `owl_oa` `owl_citations` | 中外文检索、详情、中文授权全文、外文 OA 免费全文、引文追溯 |
| 写作 | `owl_quote` `owl_run` `owl_run_status` `owl_run_content` | 一次性连续成文，按实际成文字数结算 |
| 配图 | `owl_figure` | TikZ 矢量示意 / 数据图表 / AI 配图，按实际交付张数结算 |
| 排版 | `owl_upload` `owl_quote`(typeset) `owl_typeset` | 按学校模板把 Word 论文或 LaTeX 工程排成可提交的 PDF（Word 稿另出同版式 Word + 格式体检单）；按篇一口价、按页分档，72 小时内同一篇稿改格式重排只收 1 积分工本，失败不收费 |
| 检测 | `owl_upload` `owl_products` `owl_quote` `owl_run` `owl_run_report` | 查重、AIGC、格式、智评、图像可信度、文献质量、斟校对（21 个商品）；本机文件先 `owl_upload` 换 `file_id` 再报价；报告四份 `part=main\|compare\|simple\|fulltext` |
| 核验 | `owl_quote`(verify) `owl_run` `owl_run_report` | 逐条核对引文元数据，附撤稿徽标 |
| 账户 | `owl_wallet` `owl_recharge` `owl_recharge_status` `owl_campaign` `owl_claim_favorite` `owl_meta` `owl_disciplines` | 余额、充值、券码、收藏积分领取、版本公告与检测服务状态、学科码表 |

共 **22 个 MCP 工具**。

> 以上能力在命令行模式同样可用（`owl.py` 对应子命令，对照关系见 [`references/quickstart.md`](references/quickstart.md)）。

## 计费原则

- 1 积分 = 0.01 元；**先报价、用户确认、再执行**，不静默扣费；报价 24 小时内有效。
- 写作与检测均为**后付费**：开工前只做余额软预检（不足按差额拦截），**不冻结任何积分**；结束后按实际量结算——写作按实际成文字数、检测按解析出的真实字符数，**无封顶、无下限**。配图按实际交付张数结算（未出图不收费）。
- 具体单价一律以 `owl_products` / 官网 `/price` 实时返回为准，本仓库不写死价格。

## 合规

- 产出内容按《人工智能生成合成内容标识办法》携带 AI 标识与 AIGC 元数据。
- 拒绝代写代考等违反学术诚信的请求；检测类工具用于作者自查与修正。
- 本服务通过 API 调用第三方大模型服务，该提供方已按国家规定履行生成式人工智能服务备案义务。

## 许可与反馈

使用问题与商务合作：vipsmart@vipslib.com
