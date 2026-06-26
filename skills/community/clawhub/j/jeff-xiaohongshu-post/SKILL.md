---
name: xiaohongshu-post
description: |
  小红书图文创作 Skill。根据主题、受众、核心观点进行网络搜索创作，
  生成吸睛标题（≤20字）+ 小红书风格文案（≤1000字，含emoji和hashtag）
  + 3:4竖版封面图（文字突出+简约矢量背景）。
  触发词：发小红书、生成小红书图文、小红书创作、发布小红书。
---

# 小红书图文创作 Skill

## 功能概述

输入主题、受众、核心观点 → 网络搜索调研 → **确认标题和大纲** → 创作文案 → 生成封面图。

## 触发条件

用户说：**"发小红书"、"生成小红书图文"、"小红书创作"、"发布小红书"** 等。

## ⚠️ 核心规则（必须严格遵守）

1. **标题和正文大纲必须与用户确认后才能进入正式创作**
2. **封面图中的文字 = 确认后的标题，不得额外扩展或改写**
3. 封面图 prompt 中只放入确认后的标题，不自行添加副标题或其他文字

---

## 输入参数（必须收集）

| 参数 | 说明 | 示例 |
|------|------|------|
| `theme` | 主题/话题 | "AI时代个人成长" |
| `audience` | 面向受众 | "25-35岁职场人" |
| `core_message` | 核心观点 | "用AI放大个人杠杆，3年内超越同龄人" |

等待用户明确提供以上三个参数后，再进入下一步。

---

## 工作流

### Step 1: 确认输入

向用户确认三个参数，如有缺失请补充。

---

### Step 2: 网络调研

使用 `smart_search.py` 搜索相关内容，收集：
- 热门观点和数据
- 受众痛点和需求
- 平台热门表达方式

```bash
python3 /root/.openclaw/workspace/scripts/smart_search.py "theme + 受众关键词" --max-results 8
python3 /root/.openclaw/workspace/scripts/smart_search.py "theme + 痛点/解决方案" --max-results 5
```

---

### Step 3: 生成标题候选 + 正文大纲 → **用户确认**

**严禁跳过此步骤直接进入文案创作和封面图生成。**

输出格式：

```
📌 标题候选（2-3个，各≤20字）

1. [标题1]
2. [标题2]
3. [标题3]

📌 正文大纲

[给出各段落/各模块的简要描述，3-5个要点]

请老板确认：
- 用哪个标题？
- 大纲是否OK？
- 有无调整意见？
```

等待用户回复确认后，再进入 Step 4。

---

### Step 4: 创作文案（确认后）

标题以用户确认为准，正文按确认大纲创作：

#### 标题（≤20字符）

用户选定的标题直接使用，不得自行改写。

#### 正文（≤1000字符，含emoji）

**文案结构（三段式，必须严格遵守）：**

```
① 【Hook】
   - 具体场景：一个可以想象的具体画面，一句话代入
   - 不要教育口吻，用"我今天遇到一件事"开场
   - 开头3秒必须抓住注意力

② 【痛点共情】
   - "我也有这个问题"——和用户站在一起，不是高高在上
   - 说出用户心里没说出口的抱怨或焦虑
   - 不要列数据讲道理，先让用户觉得"被懂了"

③ 【引出方案 + 实操建议】
   - 不是"帮你解决"，是"我是这样解决的"
   - 分享真实经历或亲眼所见的效果
   - 给出3个以内可直接抄作业的步骤
   - 不要堆砌功能介绍，聚焦"用了之后发生了什么"
```

**写作心态：**
- 我是**分享者**，不是老师，更不是销售
- 不说"你应该""你需要"，说"我发现""我用了""真的管用"
- 禁止：课程介绍话术、催单、制造焦虑再卖货
- 结尾：互动引导或干货延续，不做商业推销

**写作规范：**
- 每段带1-3个emoji（✨💡🚀📊💪🔥🌟⭐📈🔍）
- 句子短小精悍，每段不超过3-4句
- 用"你/你们"称呼读者，不用"大家"
- 禁止：啰嗦开头、自我介绍、堆砌形容词
- 字数统计：正文（不含hashtag）800-1000字

```python
# 验证正文字数
body = "正文内容（不含hashtag）"
char_count = len(body)
assert 800 <= char_count <= 1000, f"正文字数{char_count}，需在800-1000之间"
```

**Hashtag格式：**
```
#职场成长 #AI副业 #个人提升 #效率工具 #科技趋势 #自我提升 #干货分享
```

---

### Step 5: 生成封面图（确认后）

**⚠️ 封面图标题 = 用户确认的标题，不多不少一字不差。**

不得在封面图 prompt 中自行添加副标题、金句或任何额外文字。

**生成方式 A（推荐）：KIE GPT Image-2**

```bash
# 启动回调服务
python3 ${SKILL_DIR}/scripts/kie-callback-server.py &
# 获取 tunnel（每次重启需更新）
cloudflared tunnel --url http://127.0.0.1:8787
# 提交任务
python3 ${SKILL_DIR}/scripts/kie-create-task.py "小红书封面图，[用户确认的标题]，[风格词]，3:4竖版" \
  --model gpt-image-2-text-to-image \
  --aspect 3:4 \
  "<callback-url>"
# 等待下载
python3 ${SKILL_DIR}/scripts/kie-wait-download.py <taskId> /root/.openclaw/workspace/output/xhs_cover.png
```
- 默认模型：`gpt-image-2-text-to-image`，默认分辨率 1K
- 默认比例：3:4（小红书封面标准比例）

**生成方式 B（备选）：Seedream 5.0 API**

```bash
python3 scripts/seedream_cover.py \
  --title "用户确认的标题" \
  --subtitle "" \
  --output /root/.openclaw/workspace/output/xhs_cover.png
```

注意：`--subtitle` 留空，封面图 prompt 严格只包含确认标题 + 基础风格词。

**Prompt 构造规范（严格版）：**
```
"小红书封面图，[用户确认的标题]，[可选基础风格词：扁平矢量/简约几何/暖色调]，3:4竖版构图"
```
禁止：添加任何标题以外的描述性文字、金句、副标题到 prompt 中。

**如封面图出现文字偏差**，责任在 agent（未严格使用确认标题），需重新生成。

---

### Step 6: 输出交付

输出目录：`/root/.openclaw/workspace/output/xhs_YYYY-MM-DD/`

文件结构：
```
xhs_2026-04-10/
├── cover.png              # 封面图
├── cover_compressed.jpg   # 压缩版（用于发布）
└── content.md            # 完整文案
```

---

## 文件位置

- 主脚本：`scripts/generate_post.py`
- Seedream API：`scripts/seedream_cover.py`
- 封面模板：`scripts/xhs_cover_template.html`（HTML模式备选）
- 输出目录：`/root/.openclaw/workspace/output/xhs_YYYY-MM-DD/`

## 注意事项

1. **标题≤20字**：严格计数，超出必须重写
2. **正文≤1000字**：含emoji，实际统计字符数
3. **封面图3:4**：必须为竖版
4. **正文风格**：口语化、有情绪、带emoji，但不做作
5. **Hashtag**：选相关性高的标签，不要堆砌无关标签
6. **标题和大纲必须先确认**：未经确认不得进入创作和生图，这是铁律
