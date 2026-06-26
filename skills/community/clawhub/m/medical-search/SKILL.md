---
name: medical-search
description: "Drug safety and medical information search. Use when user asks about: drug interactions, medication safety, contraindications, side effects, drug-alcohol interactions (吃药能喝酒吗), drug-food interactions, traditional Chinese medicine safety, medication conflicts, dosage concerns. 药物安全、药物交互、用药禁忌、药品不良反应、药物+酒精、药物+食物、中成药安全。HIGHER PRIORITY than searxng-search for any medical/drug question."
metadata: { "openclaw": { "emoji": "💊", "requires": { "bins": ["curl"] } } }
---

# Medical Search - 药物安全与医药信息搜索

专门处理药物安全、用药禁忌、药物交互等医药健康信息搜索的技能。

## 核心原则（强制规则）

**凡是涉及药物安全、药物交互、用药禁忌、不良反应、药物+酒精、药物+食物的问题，必须先搜索再回答，禁止仅凭训练数据回答。** 这是硬性要求，不可跳过。

即使你对答案有信心，也必须搜索验证。药物安全信息错误可能危及生命。

## 查询方式选择

| 场景 | 查询方式 |
|------|---------|
| 两种西药之间的交互 | 先查 DDInter（如可用），再用 web search 补充 |
| 中成药相关问题 | 直接用 web search（DDInter 不收录中成药） |
| 药物+酒精/食物 | 直接用 web search（DDInter 不覆盖） |
| 药品说明书/禁忌/不良反应 | 直接用 web search |
| 孕妇/哺乳期/儿童用药安全 | 直接用 web search |
| 药物副作用/不良反应 | 直接用 web search |

## 搜索方法

### 方式一：SearXNG Web Search（主要方式）

使用自托管 SearXNG 实例搜索医药信息。

```bash
# 基础搜索（中文医药问题推荐加 language=zh）
curl -s "http://43.156.131.167:4000/search?q=QUERY&format=json&language=zh" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for i, r in enumerate(data.get('results', [])[:10], 1):
    print(f'{i}. {r.get(\"title\", \"No title\")}')
    print(f'   URL: {r.get(\"url\", \"\")}')
    print(f'   {r.get(\"content\", \"No description\")[:200]}')
    print()
"
```

**搜索关键词构造建议：**

- 药物交互问题："药名A 药名B 药物相互作用"、"药名A 药名B 能一起吃吗"
- 药物+酒精："药名 喝酒 禁忌"、"药名 酒精 相互作用"
- 药物+食物："药名 食物禁忌"、"药名 饮食注意事项"
- 药物副作用："药名 不良反应"、"药名 副作用"
- 用药安全："药名 禁忌症"、"药名 注意事项"、"药名 说明书"
- 特殊人群："药名 孕妇 能吃吗"、"药名 哺乳期"、"药名 儿童用药"

**推荐搜索示例：**

```bash
# 药物+酒精
curl -s "http://43.156.131.167:4000/search?q=感冒滴丸+喝酒+禁忌&format=json&language=zh"

# 药物交互
curl -s "http://43.156.131.167:4000/search?q=阿司匹林+布洛芬+能一起吃吗&format=json&language=zh"

# 药物副作用
curl -s "http://43.156.131.167:4000/search?q=奥美拉唑+不良反应+副作用&format=json&language=zh"

# 中成药安全
curl -s "http://43.156.131.167:4000/search?q=藿香正气水+禁忌+注意事项&format=json&language=zh"
```

### 方式二：DDInter 药物交互数据库（可选，仅限西药交互）

如果用户已配置 mediwise-health-tracker，可调用其 DDInter 脚本查询结构化的西药交互数据：

```bash
# 查询两种西药之间的交互
python3 /home/ubuntu/github/openclaw-project/mediwise-health-tracker/scripts/drug_interaction.py check-pair --drug-a "阿司匹林" --drug-b "华法林"

# 搜索药品（中英文）
python3 /home/ubuntu/github/openclaw-project/mediwise-health-tracker/scripts/drug_interaction.py search --name "布洛芬"

# 查看药品交互概览
python3 /home/ubuntu/github/openclaw-project/mediwise-health-tracker/scripts/drug_interaction.py lookup --name "奥美拉唑"
```

**注意：** DDInter 仅覆盖西药之间的交互，不覆盖中成药、药物+酒精、药物+食物等场景。即使 DDInter 返回了结果，仍建议用 web search 补充验证。

## 推荐信息源（按优先级）

搜索结果中优先采信以下来源的内容：

1. **百度健康** (`health.baidu.com`) - 药品说明书、禁忌症、不良反应，内容较全
2. **好大夫在线** (`haodf.com`) - 医生科普文章，用药注意事项
3. **用药助手/丁香园** (`drugs.dxy.cn`) - 专业药品信息
4. **百度百科** 医学词条 - 药品基础信息
5. **国家药品监督管理局** (`nmpa.gov.cn`) - 官方药品信息
6. **医脉通** (`medlive.cn`) - 专业医学资讯

搜到感兴趣的结果后，可用 `web_fetch` 工具抓取页面详情。

## 结果呈现（强制要求）

### 回复模板（必须遵循）

回复**必须**包含以下结构，缺一不可：

```
1. 【直接回答】— 一句话回答用户问题（能/不能/需谨慎）
2. 【搜索发现】— 告诉用户你搜索了什么、找到了哪些相关信息，摘要 2-3 条最相关的搜索结果
3. 【详细分析】— 基于搜索结果给出具体的风险分析和建议
4. 【参考来源】— 列出 2-3 个搜索到的具体 URL 链接（从搜索结果中提取）
5. 【免责声明】— 固定文本
```

**示例回复：**

```
**不建议。** 服用感冒滴丸期间不要饮酒。

**搜到以下相关信息：**

- 药智新闻报道：酒精在体内代谢为乙醛，部分感冒药会抑制乙醛代谢，造成蓄积中毒（来源：https://news.yaozh.com/archive/30637.html）
- 39健康网：感冒药含对乙酰氨基酚，与酒精同服会增加肝毒性风险（来源：http://askar.39.net/a/230714/k490n3e.html）
- 健康之路：滴丸类药物服用期间饮酒会刺激加重症状（来源：https://m.jkzl.com/...）

**具体风险分析：**
...（基于以上搜索结果展开）

**参考来源：**
1. 药智新闻 https://news.yaozh.com/archive/30637.html
2. 39健康网 http://askar.39.net/a/230714/k490n3e.html
3. 健康之路 https://m.jkzl.com/...

⚕️ 以上信息来自公开医药数据库和医学百科，仅供参考，不构成医疗建议。具体用药请咨询医生或药师。
```

### 关键要求

- **必须展示搜索到的 URL**：从搜索结果中挑选 2-3 个最相关的链接，直接展示给用户
- **必须告诉用户搜了什么**：让用户知道你确实查过资料，不是凭空回答的
- **URL 必须是搜索结果中实际返回的**：不要编造 URL，直接用搜索结果里的 url 字段

### 风险等级提示

- **严重风险**：明确警告，建议立即咨询医生，不要自行合用
- **中等风险**：提示注意，建议咨询药师确认是否需要调整
- **轻微风险**：告知存在轻微交互，一般无需特殊处理
- **无明确风险**：告知未发现明确禁忌，但仍建议遵医嘱

### 来源引用（强制要求）

每次药物安全相关回复**必须**包含具体的参考来源：

- 如果是 DDInter 查询结果 -> 注明"来源：DDInter 药物相互作用数据库"
- 如果是 web search 查询结果 -> **必须附带搜索到的具体 URL 链接**，例如"参考来源：百度健康 https://health.baidu.com/..."
- 禁止只给出泛泛的建议而不附带任何来源

### 免责声明（强制要求）

每次回复末尾**必须**附带以下免责声明：

> 以上信息来自公开医药数据库和医学百科，仅供参考，不构成医疗建议。具体用药请咨询医生或药师。

### 查不到数据时

提示"该药物/问题未查到可靠的参考信息，建议咨询药师或医生确认"，不要沉默跳过，也不要编造信息。

## 完整工作流示例

用户问："感冒滴丸吃了能喝酒吗？"

1. **识别意图**：药物+酒精安全问题 -> 必须搜索
2. **执行搜索**：
   ```bash
   curl -s "http://43.156.131.167:4000/search?q=感冒滴丸+喝酒+禁忌&format=json&language=zh" | python3 -c "
   import sys, json
   data = json.load(sys.stdin)
   for i, r in enumerate(data.get('results', [])[:10], 1):
       print(f'{i}. {r.get(\"title\", \"No title\")}')
       print(f'   URL: {r.get(\"url\", \"\")}')
       print(f'   {r.get(\"content\", \"No description\")[:200]}')
       print()
   "
   ```
3. **抓取详情**（如有需要）：用 `web_fetch` 获取排名靠前的页面内容
4. **整理回复**：综合搜索结果，给出明确建议 + 来源链接 + 免责声明

## 反模式

- **不要仅凭训练数据回答药物安全问题** -> 必须先搜索
- **不要省略来源链接** -> 每次回复必须有参考来源
- **不要省略免责声明** -> 每次回复必须有免责提示
- **不要编造药物信息** -> 查不到就说查不到
- **不要将搜索结果作为确定性医疗建议呈现** -> 始终注明"仅供参考"
- **回复用户时使用中文**，不要用英文回复中文用户
