本文档描述了核心数据文件的结构及其检索逻辑。

## 1. 核心数据文件预览

| 文件名 | 角色 | 主要用途 |
| :--- | :--- | :--- |
| `tarot.json` | **全量数据库** | 存储 78 张牌的详尽牌意、关键词和中英文名。 |
| `tarot_index.json` | **检索索引表** | 用于处理别名（如：隐者/隐士）和 ID 快速对齐。 |
| `spreads.json` | **牌阵逻辑库** | 定义牌阵名称、抽卡数量、各个位置的含义及 Prompt 模板。 |

---

## 2. 详细结构与检索方法

### 📂 `json/tarot_index.json` (索引层)
**结构示例：**
```json
{
    "total": 78,
    "directory": {
        "9": { "name_cn": "隐者", "name_en": "The Hermit" }
    },
    "lookup": {
        "隐者": 9,
        "隐士": 9,
        "the hermit": 9
    }
}
```
* **检索办法：** 1.  当接收到用户输入（如“帮我查查隐士”）时，先在 `lookup` 字典中进行 **Key 匹配**。
    2.  获取对应的 `index`（如 `9`）。
    3.  使用该 `index` 去 `tarot.json` 中提取完整信息。

---

### 📂 `json/tarot.json` (数据层)
**结构示例：**
```json
{
    "version": "1.0.0",
    "cards": [
        {
            "number": 9,
            "name_en": "The Hermit",
            "name_cn": "隐者",
            "upright_keywords": ["内省", "孤独", "引导"],
            "reversed_keywords": ["孤立", "隐居", "失落"],
            "upright_interpretation": "正位牌意描述...",
            "reversed_interpretation": "逆位牌意描述..."
        }
    ]
}
```
* **检索办法：** * **按 ID 访问：** `data['cards'][9]` (因为数组下标与 `number` 已对齐)。
    * **给 Agent 调用：** 当 Agent 确定了抽卡结果后，从此文件中读取对应的 `upright_interpretation` 喂给 LLM 进行二次感性解读。

---

### 📂 `json/spreads.json` (逻辑层)
**结构示例：**
```json
{
    "shared_prompt_template": "你是一只神秘的猫咪塔罗大师... {cards_info} ...",
    "spreads": {
        "past_present_future": {
            "id": "past_present_future",
            "name": "时间之流",
            "card_count": 3,
            "positions": ["过去的影响", "目前的状况", "未来的发展"],
            "usage": "用于分析事物发展脉络...",
            "interpretation": "请将三张牌串联起来讲解..."
        }
    }
}
```
* **检索办法：** 1.  **确定牌阵：** 通过 `spreads['past_present_future']` 获取配置。
    2.  **执行逻辑：** 读取 `card_count` 决定随机抽取几张牌。
    3.  **位置映射：** 将抽到的第 $i$ 张牌与 `positions[i]` 进行关联。
    4.  **组装 Prompt：** 将牌面信息填入 `shared_prompt_template`。

---

## 3. 典型的业务工作流 (Workflow)

1.  **用户命令：** `draw --spread daily_one`
2.  **程序动作：**
    * 从 `spreads.json` 查到 `daily_one` 需要 1 张牌。
    * 生成随机数 $r \in [0, 77]$，并决定正逆位。
    * 去 `tarot.json` 提取 `cards[r]` 的详细文本。
    * 如果是 Agent 调用，通过 `tarot_index.json` 确认官方称呼。
3.  **输出结果：** 格式化 JSON 或填充好的 Prompt 文本。

---