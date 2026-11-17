# 验证说明 · kb-keyword-graph Skill

> 作业：把第二大脑的「关键词图谱」能力封装成一个可复用 Skill。
> 结构：`SKILL.md` 负责触发条件 / 任务判断 / 路由规则 / 公共约束；`references/` 负责执行步骤。与作业要求分工一致。
> 一个 Skill 内路由四类任务：知识结构 / 关键词图谱 / 主题分布 / 解释资料关系——覆盖作业列出的全部四个用户请求场景。

## 一、安装（他人拿到即用）

```bash
# 1. 把 kb-keyword-graph/ 放进 Agent 的 skills 目录
#    OpenClaw: ~/.openclaw/<workspace>/skills/kb-keyword-graph/
# 2. 配置凭证（二选一）
mkdir -p ~/.config/2brain-keyword-map
printf '{ "token": "2B-你的图谱Key", "base_id": 700 }' > ~/.config/2brain-keyword-map/config.json
chmod 700 ~/.config/2brain-keyword-map && chmod 600 ~/.config/2brain-keyword-map/config.json
#    或： export TWOBRAIN_GRAPH_KEY=2B-... ; export TWOBRAIN_BASE_ID=700
#    课程环境： export TWOBRAIN_API_BASE=https://test.2brain.ai/api
# 3. 自检
python3 skills/kb-keyword-graph/scripts/kw_graph.py fetch --base-id 700
# 4. 重启 Agent 进程使其重扫 skills（OpenClaw: openclaw gateway restart）
```

依赖：仅 `python3`（标准库，无第三方包）。宿主机需能访问 2brain API_BASE。

## 二、触发方式

用户对 Agent 说出以下任一类请求即触发（详见 SKILL.md description 与路由表）：

1. **知识结构** —— "这个库里有什么 / 知识结构是怎样的 / 有哪些方面"
2. **关键词图谱** —— "帮我看下 XX 库的关键词图谱 / 画个知识图谱"
3. **主题分布** —— "这个库主要讲哪些主题 / 哪块内容最多"
4. **解释关系** —— "库里 X 和 Y 有什么联系"

即使没说"图谱"二字（如只问"这个库都有什么"），description 的 push 式触发词也覆盖，默认走 structure。排歧：本 Skill 的「知识库」特指 2brain 平台的库，不路由到飞书 Wiki / 云文档 / 本地文件。

## 三、输入要求

| 输入 | 必填 | 说明 |
|---|---|---|
| 目标库 base_id | 是 | 整数；`--base-id` 或配置默认；不硬编码、不替用户猜 |
| `TWOBRAIN_GRAPH_KEY` | 是（环境或配置文件） | 2brain 平台生成的「关键词图谱」API Key，Bearer 鉴权，与上传/问答 Key 不同 |
| `TWOBRAIN_API_BASE` | 否 | 默认 `https://test.2brain.ai/api`；课程 test 环境用这个 |
| relate 的 `--a` / `--b` | relate 任务必填 | 两个要比较的关键词（大小写不敏感） |

## 四、执行步骤

1. 判断意图 → 选任务（structure/graph/topics/relate），向用户复述「对库 <id> 做 <任务>」。
2. 跑对应子命令：`python3 scripts/kw_graph.py <子命令> --base-id <id> [...]`。
3. 引擎拉取 `POST <API_BASE>/kbase/keywords/keyword_api {base_id}`（Bearer graph key），返回三层 `keywords_tree`，缓存到 `~/.local/state/2brain-keyword-map/graphs/<base_id>.json`。
4. 读引擎 stdout 的 JSON，按 `references/workflows.md` 对应任务的模板转述给用户（graph 任务另给 HTML 路径）。

## 五、异常处理

| 异常 | 引擎行为 / Agent 应对 |
|---|---|
| 缺图谱 Key | 明确指引去平台生成，不硬试 |
| 缺 base_id | 向用户要整数 base_id，不猜 |
| 401 / 403 | 提示 Key 无效或过期，请重新生成 |
| 无法连接 2brain | 提示检查网络 / API_BASE |
| keywords_tree 为空或极少 | 如实报「资料不足以成图」，不编造 |
| relate 的词不在图中 | 返回 `related:null` + 提示，不硬编关系 |
| 资料刚入库 | 提示可能未解析完成，可 `--fresh` 重拉 |

## 六、输出格式

- **structure**：`levels`（l1/l2/l3 计数）+ `outline`（一级→二级→三级 + 一级占比）。
- **graph**：`levels` + `metric: sibling_count_percentage` + `html`（自包含交互文件路径）。
- **topics**：一级主题按 count 降序，每项 `count` / `share_pct`（全库一级占比）/ `platform_weight`（2brain 权重 0-100）/ `subtopic_count`。
- **relate**：`relation`（ancestor-descendant / shared-parent / cousin / unrelated-in-graph）+ `explanation` + `lowest_common_topic` + `caveat`。

**硬性纪律**：所有数字只来自引擎 stdout；图谱只显示同级占比百分比（不显示 count，每组同级合计 100%，非全库绝对占比）；token 绝不出现在任何产物或对话；关系解读只表示层级同现，不代表因果/语义等价/文档级来源。

## 七、演示（真实库 base 700）

以真实知识库 **base_id 700（求职库，256 篇资料，来自 W5 的 jobwatcher 入库）** 实测，四类任务各一次，全部基于 `keyword_api` 实时返回的三层关键词树（**10 个一级主题 / 21 个二级 / 45 个三级**）：

- **structure**：10 个一级主题 = Ai systems / Compensation / Fellows / Candidates / Logistics / Technical / Project / Collaboration / Research / Operations。
- **graph**：生成 `demo_outputs/keyword-graph-700.html`，渐进环形交互图，一级最重的是 Research(36.8%)、Technical(13.8%)、Compensation(13.4%)。
- **topics**：按资料量 Research(36.8%) > Technical(13.8%) > Compensation(13.4%) > Ai systems(11.5%) > Candidates(11.0%) …
- **relate**：`Visa × Sponsorship` → ancestor-descendant（同一主题链，Sponsorship 是 Visa 下的三级）；`Python × Safety` → unrelated-in-graph（分属 Technical 与 Ai systems 两个一级主题）。

演示输出见 `demo_outputs/`（structure_700.json / topics_700.json / relate_*.json / keyword-graph-700.html）+ 图谱截图。

## 八、安全边界自检

- 只读：不入库、不建库、不删改、不问答；关键词/数字不编造。
- token 只作 Authorization 头发给固定 2brain 端点；grep 产物无 token（已验证 keyword-graph HTML 中 0 命中 Key）。
- base_id 不硬编码：运行时由参数/配置解析。
