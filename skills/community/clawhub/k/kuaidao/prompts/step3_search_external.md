# 子任务3：搜索外网平台

## 任务目标
从用户设置的外网关键词池中随机抽取3个，搜索TikTok/YouTube爆款，最终选定1个外网爆款作为创意参考。

## 输入变量

| 变量名 | 说明 | 来源 | 如何设置 |
|:---|:---|:---|:---|
| `{{platform}}` | 目标平台名称 | 子任务参数 | 执行时传入，如：xiaohongshu |
| `{{external_keywords_pool}}` | 用户设置的外网关键词池 | 用户配置 | `kd config set-external-keywords` 或编辑配置文件 |
| `{{search_count}}` | 每个关键词搜索结果数 | 用户配置 | 默认20，可配置 |
| `{{select_count}}` | 最终选定爆款数 | 用户配置 | 默认1，可配置 |

## 变量设置说明

### 如何设置外网关键词池

**方式1：使用命令行**
```bash
kd config set-external-keywords --keywords "关键词1,关键词2,关键词3"
```

**方式2：直接编辑配置文件**
编辑 `config/platforms.json` 或用户配置文件：
```json
{
  "external_keywords": ["food", "cooking", "life", "vlog", "story"]
}
```

**方式3：在Python脚本中设置**
```python
from config_manager import ConfigManager
config = ConfigManager()
config.set_external_keywords(["food", "cooking", "life", "vlog", "story"])
```

### 外网关键词池为空时的处理

**如果 `{{external_keywords_pool}}` 为空数组 `[]`：**
- ⚠️ 输出提示："外网关键词池为空，跳过外网搜索"
- ⏭️ 直接跳到子任务4（不终止任务）
- 💡 提示用户可配置外网关键词（可选）

**注意：** 外网搜索是可选步骤，即使为空也不影响主流程

**用户配置示例（可选）：**
```bash
# 配置外网关键词池（可选）
kd config set-external-keywords \
  --keywords "food,cooking,life,vlog,story,family,memory"
```

## 执行流程

1. 检查 `{{external_keywords_pool}}` 是否为空
2. 如为空，输出提示并跳到子任务4
3. 从外网关键词池中**随机抽取3个**
4. 用"TikTok/YouTube + 关键词"分别搜索3次
5. 每个关键词取前 `{{search_count}}` 条结果（默认20）
6. 从结果中选取最优的 `{{select_count}}` 个爆款（默认1）
7. 记录最终选中的外网爆款

## 输出格式

```markdown
## 外网搜索结果

### 关键词池状态
- 外网关键词池：{{external_keywords_pool}}
- 状态：[✅ 已配置 / ➖ 为空]

### 抽取的关键词（如已配置）
关键词1、关键词2、关键词3

### 搜索1结果（TikTok - 关键词1）
| 排名 | 标题 | 播放量 | 创意亮点 |
|:---:|:---|:---:|:---|
| 1 | [标题] | [数据] | [亮点] |
| 2 | [标题] | [数据] | |
| ... | ... | ... | |

### 搜索2结果（YouTube - 关键词2）
（同上格式）

### 搜索3结果（TikTok - 关键词3）
（同上格式）

## 最终选定的{{select_count}}个外网爆款（如已配置）
| 平台 | 标题 | 关键词 | 创意亮点 | 可借鉴点 |
|:---|:---|:---|:---|:---|
| TikTok/YouTube | [爆款标题] | [关键词] | [亮点] | [借鉴思路] |

## 创意提取（如已配置）
基于外网爆款，提取以下创意元素：
- 叙事结构: [结构类型]
- 视觉风格: [风格描述]
- 情绪节奏: [节奏特点]
- 可本土化适配: [适配建议]
```

## 选择标准

| 维度 | 权重 | 说明 |
|:---|:---:|:---|
| 创意新颖度 | 40% | 创意独特、有启发性 |
| 制作水准 | 30% | 拍摄、剪辑精良 |
| 情感共鸣 | 20% | 有情感感染力 |
| 可本土化 | 10% | 可适配到国内平台 |

## 注意事项

1. ✅ **随机抽取**关键词，不固定顺序
2. ✅ 重点关注创意和叙事手法，非直接搬运
3. ✅ 记录可本土化的创意点
4. ❌ 如无合适爆款可选，可取消本次外网搜索
5. ❌ 避免选择与目标平台风格差异过大的内容

## 使用示例

**场景1：外网关键词池已配置**

输入：
- platform: xiaohongshu
- external_keywords_pool: ["food", "cooking", "life", "vlog", "story"]
- search_count: 20
- select_count: 1

输出：
```markdown
## 外网搜索结果

### 关键词池状态
- 外网关键词池：["food", "cooking", "life", "vlog", "story"]
- 状态：✅ 已配置（5个关键词）

### 抽取的关键词
life, vlog, story

搜索1结果（TikTok - life）:
...

最终选定1个外网爆款：
- 平台: TikTok
- 标题: 「A day in my countryside life」
- 关键词: life
- 创意亮点: 乡村慢生活vlog风格
- 可借鉴点: 可本土化为嘉泰苑慢生活场景

创意提取：
- 叙事结构: 一天时间线叙事
- 视觉风格: 自然光、暖色调
- 情绪节奏: 舒缓、放松
- 可本土化适配: 嘉泰苑的一天（采摘+就餐+休闲）
```

**场景2：外网关键词池为空**

输出：
```markdown
## 外网搜索结果

### 关键词池状态
- 外网关键词池：[]
- 状态：➖ 为空（跳过此步骤）

### 提示
⏭️ 外网关键词池为空，跳过外网搜索

### 可选配置
如需启用外网搜索，可配置关键词池：
kd config set-external-keywords \
  --keywords "food,cooking,life,vlog,story"

### 后续流程
直接跳转到子任务4：同质化检查
```
