# 完整流程

## 两条路

```
材料齐了      读材料 → preview → create → 下载两份 Word
只有个想法    ideas → 用户挑方向 → create --from-ideas → 下载两份 Word
```

判断走哪条：**用户能不能说清「具体怎么做」**。能说清，走第一条；只说得出「想解决什么问题」，走第二条。

---

## 第一条：材料齐了

### 1. 读材料

见 `materials-guide.md`。`.md` / `.txt` / `.docx` 用 `--file` 交给脚本，其他格式读完后写进 `--supplement`。

### 2. 预览（不花钱）

```bash
python scripts/patentmax_disclosure.py preview --file ./方案.docx --file ./实验.md
```

看 `chars` 和 `level`。`偏薄` 时先问用户两三个问题，把答案写进 `--supplement` 再提交。

### 3. 确认后提交

跟用户说清：这是付费任务，通常 6～15 分钟出结果，排队或材料多时可能到 30 分钟。用户同意后：

```bash
python scripts/patentmax_disclosure.py create \
  --file ./方案.docx --file ./实验.md \
  --supplement "用户补充：……" \
  --title "案件名称" --yes
```

`--title` 可以不给，服务端会自己起名。发明名称不超过 25 个字。

### 4. 下载

```bash
python scripts/patentmax_disclosure.py download --report-id <report_id> --out 技术交底书.docx
python scripts/patentmax_disclosure.py download --report-id <report_id> --kind notes --out 核对说明.docx
```

---

## 第二条：只有个想法

### 1. 出方向

```bash
python scripts/patentmax_disclosure.py ideas --idea "……" --count 3 --yes
```

`--count` 取 1 到 5，默认 3。价格不随个数变，但个数越多等得越久。**用户想多看几个就给 5。**

### 2. 把方向列给用户

每个方向讲清楚：

- **标题和一句话概述**
- **和原始想法比，多了什么**：看 `core_idea` 和 `innovation_points`
- **评分**：`scores.overall` 综合分，`novelty` / `feasibility` / `differentiation` 分项
- **现有技术**：`existing_tech_description`，写「未检索到」就照实说

**让用户挑，不要替他选。** 用户问哪个好时，可以按综合分给建议，但要说出理由。

### 3. 接着写交底书

```bash
python scripts/patentmax_disclosure.py create \
  --from-ideas <ideas 的 report_id> --direction 2 \
  --idea "原始想法原文" \
  --supplement "用户对这个方向的补充：……" \
  --yes
```

`--idea` 把原始想法一起带上，`--supplement` 放用户针对这个方向补充的细节。**方向本身的内容往往偏概括，这时候让用户补一两句具体做法，交底书会扎实很多。**

---

## 结果怎么读

### 交底书正文（disclosure.docx）

| 节 | 内容 |
| --- | --- |
| 1 | 发明创造名称 |
| 2 | 背景技术及现有技术的缺陷和不足 |
| 3 | 具体的技术方案描述 |
| 4 | 本发明创造的优点 |
| 5 | 具体实施方式及附图 |
| 6 | 权利要求结构预览：一张表，独立项、从属项连续编号，引用关系标清 |
| 7 | 说明书摘要（300 字以内） |
| 8 | 附图标号表 |

附图按领域自动画：连接关系图、流程图、模块框图、结构图、电路图等。

### 核对说明（notes.docx）

正文是干净的，**正文中的推导、待补充和需要留意的事项都汇总在这一份里**：

- 系统推导的条目：按通行做法补上的内容，要发明人确认
- 待补充信息：只有发明人能给的事实（实验原始数据、具体型号、实测条件）
- 附图绘图说明：系统没画出来的图，按说明另行绘制
- 发明点对照：每个发明点在专利库里的比对结果
- 替代方案：每个关键特征可以换成什么，用来扩大保护范围

### 结果 JSON

| 字段 | 含义 |
| --- | --- |
| `title` / `domain` / `subject` | 发明名称、判定的领域、保护主题 |
| `pending_count` | 推断条目数。**大于 0 时务必让用户看核对说明** |
| `missing_sections` | 缺的节 |
| `figures[]` | `no` 图号、`name` 图名、`type` 类型、`auto` 是否已画出 |
| `novelty.rows[]` | 每个发明点：`feature` 特征、`hits` 撞上的文献（`present` 完全公开 / `similar` 相近）、`found` 是否撞上 |
| `novelty.candidate_count` | 参与比对的候选文献数 |
| `alternatives[]` | 替代方案 |
| `conflicts[]` | 材料间的数值冲突，`severity` 为 `high` 时必须让用户定 |
| `check_notes[]` | 数值保真、引证校验的提示 |

### 发明点比对怎么讲

`novelty.rows` 里每一行是一个发明点：

- **`found: false`**：在参与比对的文献里没找到公开这个特征的
- **`found: true` + `present`**：有文献完全公开了这个特征，**这个点单独撑不起新颖性**，要靠和其他特征组合
- **`found: true` + `similar`**：有相近的，要看具体区别

注意 `unverified`：圈中了但没能取到全文核对的文献。有这类文献时，「没找到」要打折扣，照实告诉用户。

**这是发明点比对，不是查新结论。** 要判断能不能申请，交底书写完再跑专利查新。

---

## 失败了怎么办

`status` 变成 `failed` 或 `cancelled` 时，**预扣的钱全额退回**。

先把 `message` 原样告诉用户。材料问题就补材料再提交（材料变了，幂等键自动变，不会被当成重复请求）；服务端问题稍后重试。
