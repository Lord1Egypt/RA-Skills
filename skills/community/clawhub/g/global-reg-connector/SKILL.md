---
name: global-reg-connector
slug: global-reg-connector
displayName: 全球法规MCP连接器
display_name: 全球法规MCP连接器
version: 1.0.0
category: 医疗器械
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
author: 注册老炮
license: MIT
description: >-
  把 27 份全球医疗器械法规枢纽知识库（NMPA/FDA/MDR/PMDA/拉美/东南亚）封装成本地只读 MCP Server。
  开箱即用：装好依赖即可被 WorkBuddy/Agent/小艺 Skill 调用，检索法规返回片段+官方原文链接+待核验标注。
  零网络外发、零凭据、纯本地检索，适合法规工程师日常查证与产品注册路径速查。
description_zh: 全球法规MCP连接器——27 份全球医械法规枢纽知识库（中/美/欧/日+拉美+东南亚）封装成本地只读 MCP Server，4 个检索工具（list_hubs/search_regulation/get_hub/ask_classification），检索返回片段+官方原文链接+待核验标注，零外发零凭据纯本地。
description_en: Global Regulatory MCP Connector — wraps 27 medical device regulatory hub documents (CN/US/EU/JP + LATAM/ASEAN) into a local read-only MCP Server with 4 tools (list_hubs/search_regulation/get_hub/ask_classification), returning snippets + official links, zero network, zero credentials.
tags: [医疗器械, 法规, MCP, 连接器, 注册, NMPA, FDA, MDR, UDI, 全球市场]
xiaping_category: ["效率工具"]
---

# 全球法规MCP连接器（Global Reg-Connector）

把 **27 份全球医疗器械法规枢纽知识库**（中/美/欧/日 + 拉美 + 东南亚，含骨科产品全球注册路径实证）
封装成**本地只读 MCP Server**，让 WorkBuddy / Agent / 小艺 Skill 通过标准 MCP 协议直接检索全球法规知识。

- **形态**：本地 stdio 进程，零网络外发、零凭据、纯只读
- **知识库**：包内自带 `references/`（27 枢纽 + README），开箱即用
- **技术栈**：Python 3.10+ / FastMCP 3.x（无需第三方检索依赖，内置中文友好分词检索）

---

## 一、能力（4 个 MCP 工具）

| 工具 | 作用 | 典型问法 |
|------|------|----------|
| `list_hubs` | 列出全部 27 个法规枢纽及覆盖阶段 | 「有哪些枢纽？」 |
| `search_regulation(query, top_k, hub_filter)` | 关键词检索法规，返回片段+官方链接+相关度 | 「UDI 怎么实施」「MDR PMS 要求」「510k 流程」 |
| `get_hub(hub_key)` | 取某一枢纽完整内容（含官方原文链接） | 「把风险管理枢纽全文给我」 |
| `ask_classification(product)` | 产品分类与注册路径速查 | 「骨科接骨板怎么分类注册」 |

检索特点：中文 2-gram + 英文单词分词，标题命中加权，支持中/英/法规号混合查询（如「UDI」「510k」「委托生产」）。

## 二、安装（三步上手）

### 前置：Python 3.10+
```bash
python --version   # 需 3.10+
```

### 1. 安装依赖
```bash
# 建议在虚拟环境中安装（可选但推荐）
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install fastmcp
```

### 2. 配置为 MCP Server（二选一）
**方式 A：WorkBuddy / 任意 MCP 客户端**
在 `~/.workbuddy/mcp.json` 的 `mcpServers` 中加入：
```json
"medxpert-reg-connector": {
  "command": "python",
  "args": ["<本包解压路径>/reg_connector_server.py"],
  "disabled": false
}
```
> 不同机器把 `<本包解压路径>` 换成实际路径即可；依赖 Python 环境能找到 `fastmcp`。

**方式 B：命令行直接自测（不依赖客户端）**
```bash
python selftest_stdio.py     # 走真实 stdio 协议调 4 个工具
python security_selfcheck.py # 安全自检（只读/零凭据/无外发）
```

### 3. 启用
WorkBuddy：右上「自定义连接器」→ 找到 `medxpert-reg-connector` → 点「信任」。

> 知识库目录可自定义：设置环境变量 `REG_HUB_REFS` 指向你自己的法规 md 目录，即可复用同一套检索。

## 三、使用示例

**问**：「一次性使用输液器在巴西怎么注册？」
**调**：`ask_classification(product="一次性使用输液器")`
**返回**：相关枢纽匹配 + 5 个推荐枢纽 + 官方链接 + 提示「以目标市场官方分类库为准」。

**问**：「UDI 在欧美的合规日期？」
**调**：`search_regulation(query="UDI 唯一标识", top_k=3)`
**返回**：命中枢纽、小节、摘要片段、相关度得分、官方原文链接（FDA/ecfr/GUDID 等）。

## 四、安全边界（设计原则）

- **只读**：仅加载 `references/` 下的 Markdown，不写任何文件
- **零凭据**：无 API key / token / 账号密码；环境变量仅 `REG_HUB_REFS`（可选）
- **无外发**：不发起任何网络请求，纯本地检索；返回的官方链接由知识库整理者预置
- 检索结果为法规知识整理，**以各市场官方原文为准**

## 五、能力边界（FAQ）

- **Q：支持联网查最新法规吗？** 否——本连接器是本地知识库检索，法规更新靠知识库版本升级；返回内容含官方原文链接，可自行点开核实最新状态。
- **Q：能检索多少市场？** 知识库覆盖中/美/欧/日四大市场 + 拉美（巴西/墨西哥/阿根廷）+ 东南亚（印尼/泰国/马来/越南/新加坡/菲律宾）的注册路径与法规要点。
- **Q：换自己的知识库怎么用？** 设 `REG_HUB_REFS` 指向你的 md 目录（须含 .md 文件），重启即用。
- **Q：会收集我的数据吗？** 不会——本地只读，零外发、零凭据、零日志上传。

## 六、安全稳定性实测

实测方法：本地闭环行为化测试（FastMCP 官方 Client 走真实 stdio 协议调 4 工具 + 发布前扫描 34 文件 + 静态审计）。

| 维度 | 实测 | 行业基线 | 企业级标准 |
|------|------|---------|-----------|
| 敏感信息零泄露 | 5.0 | 3.5 | 4.5 |
| 本地闭环无外联 | 5.0 | 3.5 | 4.5 |
| 零凭据最小权限 | 5.0 | 3.5 | 4.5 |
| 无隐藏行为 | 5.0 | 3.5 | 4.5 |
| 协议健壮性 | 5.0 | 3.5 | 4.5 |
| 只读安全边界 | 5.0 | 3.5 | 4.5 |
| 可复跑稳定性 | 5.0 | 3.5 | 4.5 |
| 输入容错 | 4.5 | 3.5 | 4.5 |
| **综合** | **4.94** | 3.5 | 4.5 |

- 多维雷达对比图见包内 `安全稳定性雷达图.svg`（我们 vs 行业基线 vs 企业级标准）
- 明细数据见 `security_results.json`（可复现，测试脚本 `selftest_stdio.py` / `security_selfcheck.py` 随包提供）

## 七、文件导航

| 文件 | 说明 |
|------|------|
| `reg_connector_server.py` | MCP Server 主程序（含 4 工具与检索实现） |
| `selftest_stdio.py` | stdio 协议层自检脚本（可重跑） |
| `security_selfcheck.py` | 安全自检脚本（只读/零凭据/无外发） |
| `references/` | 27 份全球法规枢纽知识库（内容源） |
| `references/README.md` | 知识库文件清单与覆盖说明 |
| `LICENSE.md` | MIT 开源许可 |
| `安全审计报告.md` | 云鼎安全审计报告（P2） |
| `安全稳定性雷达图.svg` | 安全稳定性实测多维雷达对比图 |
| `security_results.json` | 安全稳定性实测明细数据（可复现） |
| `ATTESTATION.md` / `manifest.json` | 权属证明（时间戳 + 作品指纹） |

## 八、版权与许可

**版权与许可**
© 2026 注册老炮。本作品基于 **MIT License** 开源（见 `LICENSE.md`）。

**免责声明**：本作品按「现状」(AS IS) 提供，无任何明示或暗示担保。知识库内容为公开法规的整理汇编，仅供学习与工作参考；**以各市场监管机构官方原文为准**。因使用本作品产生的任何后果由使用者自行承担。

**知识版权声明**：本作品所含知识整理、检索方法论与结构设计归 注册老炮 所有。未经授权不得复制、转售本作品或将其用于任何模型训练。

**零数据收集**：本作品不收集、不传输任何用户数据。
