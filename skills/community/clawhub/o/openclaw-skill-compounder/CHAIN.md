# 调用链设计逻辑（CHAIN.md）

> skill-compounder 的核心：如何判断技能组合 + 生成调用链

---

## 1. 意图分类器

### 标准意图类型

| 意图类型 | 关键词模式 | 描述 |
|----------|-----------|------|
| `content_creation` | 写文章/创作/发公众号 | 内容创作类任务 |
| `research_analysis` | 分析/研究/调研/报告 | 研究分析类任务 |
| `information_gathering` | 抓取/采集/爬取/搜索 | 信息采集类任务 |
| `media_processing` | 视频/音频/图片/提取帧 | 媒体处理类任务 |
| `investment_analysis` | 投资/股票/基金/分析 | 投资分析类任务 |
| `document_processing` | PDF/电子书/摘要/总结 | 文档处理类任务 |
| `skill_improvement` | 优化/改进/修复/自进化 | 技能改进类任务 |
| `knowledge_management` | wiki/知识库/沉淀/结构化 | 知识管理类任务 |

### 意图分类 Prompt

```
你是一个意图分类器。根据用户输入，判断用户意图类型。

用户输入：{user_input}

可选类型：
- content_creation: 内容创作（写文章、发公众号）
- research_analysis: 研究分析（调研、报告）
- information_gathering: 信息采集（抓取、搜索）
- media_processing: 媒体处理（视频、音频）
- investment_analysis: 投资分析（股票、基金）
- document_processing: 文档处理（PDF、电子书）
- skill_improvement: 技能改进（优化、修复、自进化）
- knowledge_management: 知识管理（Wiki、知识库、沉淀）

输出格式：
{{"intent": "类型", "confidence": 0.0-1.0, "keywords": ["识别的关键词"]}}
```

---

## 2. 技能清单索引

### 可用技能库（完整列表见 REGISTRY.md）

```yaml
# 内容创作类
writer: "通用写作"
writing-agent: "写作助手"
content-creator: "内容创建器"
article-writing: "文章写作"
wechat-article-creator: "微信公众号创作"
wechat-mp-upload: "微信上传"

# 信息采集类
web-content-fetcher: "网页内容抓取"
multi-search-engine: "多引擎搜索"
playwright-scraper-skill: "浏览器爬虫"

# 媒体处理类
video-frames: "视频帧提取"
analyze_video: "视频分析"

# 文档处理类
pdf-extractor: "PDF提取"
epub-read: "电子书阅读"
epub-to-markdown: "电子书转Markdown"

# 投资分析类
investment-agent: "投资分析师"
investment-analysis-kit: "投资分析工具包"
investment-portfolio: "投资组合"
crypto-investment-strategist: "加密货币策略"

# 思维工具类
thinking-toolbox: "思维工具箱"
writer: "写作"

# 技能进化类
skill-self-evolution-enhancer: "技能自进化增强器"
skill-builder: "技能构建器"
skill-vetter: "技能审查器"

# 知识管理类
epub-to-markdown: "格式转换（也用于Wiki生成）"
```

### 意图→技能映射表

```yaml
content_creation:
  primary: [writer, writing-agent]
  optional: [content-creator, article-writing]
  dependencies: []

research_analysis:
  primary: [multi-search-engine, writing-agent]
  optional: [content-creator, investment-agent]
  dependencies: []

information_gathering:
  primary: [web-content-fetcher, multi-search-engine]
  optional: [playwright-scraper-skill]
  dependencies: []

media_processing:
  primary: [video-frames, analyze_video]
  optional: [writing-agent]
  dependencies: []

investment_analysis:
  primary: [investment-agent, investment-analysis-kit]
  optional: [investment-portfolio, multi-search-engine]
  dependencies: []

document_processing:
  primary: [pdf-extractor, epub-read]
  optional: [epub-to-markdown, writing-agent]
  dependencies: []

skill_improvement:
  primary: [skill-self-evolution-enhancer]
  optional: [skill-builder, skill-vetter]
  dependencies: []

knowledge_management:
  primary: [web-content-fetcher, writing-agent]
  optional: [epub-to-markdown]
  dependencies: []
```

---

## 3. 调用链生成算法

### Step 1: 意图分类

```python
def classify_intent(user_input):
    """使用 thinking-toolbox 分析用户意图"""
    prompt = f"""分析用户输入，判断意图类型。
    
    用户输入：{user_input}
    
    输出：{{"intent": "类型", "confidence": 0.0-1.0}}"""
    
    result = call_skill("thinking-toolbox", {"prompt": prompt})
    return parse_json(result)
```

### Step 2: 技能匹配

```python
def match_skills(intent_type, user_context):
    """从技能库匹配最合适的技能组合"""
    
    # 加载候选模板
    templates = load_templates_for_intent(intent_type)
    
    # 按相似度排序
    ranked = rank_by_similarity(templates, user_context)
    
    # 选择最佳匹配
    best = ranked[0] if ranked else get_default_chain(intent_type)
    
    return best["skills"], best["confidence"]
```

### Step 3: 链生成

```python
def generate_chain(skills, user_context):
    """生成完整的调用链"""
    
    chain = []
    shared_context = {}
    
    for i, skill in enumerate(skills):
        call = {
            "skill_name": skill,
            "trigger": f"step_{i+1}" if i > 0 else "user_input",
            "input_map": {
                "text": "${prev.result}" if i > 0 else "${user_input}",
                "context": user_context
            },
            "output_field": "result",
            "next": f"step_{i+2}" if i < len(skills) - 1 else "finish"
        }
        chain.append(call)
        shared_context[f"step_{i+1}"] = call
    
    return chain
```

### Step 4: 参数注入

```python
def inject_params(chain, user_params):
    """注入用户定制参数"""
    
    for call in chain:
        # 合并用户参数到 context
        call["input_map"]["context"].update(user_params)
        
        # 解析变量引用
        call["input_map"]["text"] = resolve_variables(
            call["input_map"]["text"], 
            shared_context
        )
    
    return chain
```

### Step 5: 输出验证（新增）

```python
def validate_output(step_result, expected_fields):
    """验证技能输出是否有效"""
    
    # 检查基本结构
    if not isinstance(step_result, dict):
        return {"valid": False, "reason": "Output is not a dict"}
    
    # 检查必要字段
    for field in expected_fields:
        if field not in step_result:
            return {"valid": False, "reason": f"Missing field: {field}"}
    
    # 检查内容有效性
    if "result" in expected_fields:
        if not step_result["result"] or len(str(step_result["result"])) < 10:
            return {"valid": False, "reason": "Result content too short"}
    
    return {"valid": True, "confidence": step_result.get("confidence", 0.8)}


def execute_with_validation(chain):
    """带验证的链执行"""
    
    results = []
    
    for i, step in enumerate(chain):
        # 执行技能
        raw_result = execute_skill(step)
        
        # 验证输出
        validation = validate_output(raw_result, step["expected_fields"])
        
        if not validation["valid"]:
            # 触发 fallback
            fallback_skill = step.get("fallback_skill")
            if fallback_skill:
                print(f"Step {i+1} failed, trying fallback: {fallback_skill}")
                raw_result = execute_skill({"skill": fallback_skill, ...})
            else:
                print(f"Step {i+1} failed with no fallback: {validation['reason']}")
                return {"success": False, "failed_step": i+1, "reason": validation["reason"]}
        
        results.append(raw_result)
    
    return {"success": True, "results": results}
```

---

## 4. 数据流转规则

### 字段映射标准

```yaml
# 通用映射
result_field: "result"           # 核心结果字段
confidence_field: "confidence"    # 置信度字段
metadata_field: "metadata"       # 元数据字段

# 写作类技能输出
writer:
  result: "text"                  # 生成的文本
  word_count: "word_count"        # 字数
  tone: "tone"                    # 语气

# 抓取类技能输出
fetcher:
  result: "content"               # 抓取的内容
  url: "source_url"                # 来源URL
  title: "title"                  # 标题

# 视频类技能输出
video:
  result: "frames"               # 提取的帧
  description: "description"       # 视频描述
  key_moments: "key_moments"      # 关键时刻
```

### 跨技能数据传递

```python
# 示例：文章创作流水线
chain = [
    {
        "skill": "web-content-fetcher",
        "output": {
            "result": "content",      # 抓取的素材
            "title": "来源标题",
            "url": "来源URL"
        }
    },
    {
        "skill": "writing-agent",
        "input": {
            "text": "${step_1.result}",  # 使用上一步的 content
            "context": {
                "source_title": "${step_1.title}",  # 引用上一步的 title
                "writing_style": "专业技术分享"
            }
        },
        "output": {
            "result": "article_text",
            "word_count": 2000
        }
    },
    {
        "skill": "wechat-mp-upload",
        "input": {
            "text": "${step_2.result}",  # 使用上一步的文章
            "context": {
                "title": "${step_1.title}",
                "source_url": "${step_1.url}"
            }
        }
    }
]
```

---

## 5. 异常处理

### 技能失败策略

```yaml
error_handling:
  retry:
    max_attempts: 3
    backoff: "exponential"
    
  fallback:
    # 技能A失败 → 回退到技能B
    web-content-fetcher → playwright-scraper-skill
    writer → article-writing
    investment-agent → multi-search-engine
    
  skip:
    # 跳过可选技能
    optional_skills: [content-creator, epub-to-markdown]
    
  confirm:
    # 关键决策点需要用户确认
    confirm_points:
      - "发布前确认"
      - "投资决策前确认"
      - "删除操作确认"
```

### 置信度阈值

```yaml
confidence_thresholds:
  high: 0.8      # 直接执行
  medium: 0.6    # 提示用户确认
  low: 0.4       # 询问用户选择
  
action:
  high: "直接执行调用链"
  medium: "展示方案 + 询问是否继续"
  low: "提供多个选项让用户选择"
```

### 输出验证规则

```yaml
output_validation:
  required_fields:
    - result
    - confidence
  
  min_content_length: 10
  
  validation_actions:
    - 检查 result 字段存在
    - 检查内容长度 >= min_content_length
    - 检查 confidence 合理 (0.0-1.0)
  
  fallback_trigger:
    - result 字段缺失
    - 内容为空或太短
    - confidence < 0.3
```

---

## 6. 模板格式

### 标准 YAML 模板格式

```yaml
# article-pipeline.yaml 示例
name: article-pipeline
version: 1.0.0
description: 抓取网页素材生成公众号文章
intent_type: content_creation

skills:
  - skill: web-content-fetcher
    trigger: 用户提供URL或搜索关键词
    input:
      source: "${user_input}"
      purpose: "提取素材"
    output:
      result_field: "content"
      confidence_field: "confidence"
      
  - skill: writing-agent
    trigger: step_1 完成
    input:
      text: "${step_1.result}"
      context:
        article_type: "${user.article_type}"
        target_audience: "${user.target_audience}"
    output:
      result_field: "article_text"
      word_count_field: "word_count"
      
  - skill: wechat-mp-upload
    trigger: step_2 完成
    input:
      text: "${step_2.result}"
      context:
        title: "${user.article_title}"
        auto_publish: "${user.auto_publish}"
```

---

## 7. 与 Orchestration 的协作

### 分工边界

| 方面 | Orchestration | Skill Compounder |
|------|--------------|-----------------|
| **定义方式** | 预置 YAML 流程 | 动态按需生成 |
| **触发时机** | 固定流程模板 | 用户自定义需求 |
| **技能组合** | 硬编码步骤 | 算法智能匹配 |
| **异常处理** | 预定义回退 | 动态回退策略 |
| **适用场景** | 标准化场景 | 复杂多变场景 |

### 协作示例

```
用户："看到一个投资视频，想分析内容生成报告"

1. skill-compounder 动态判断：
   intent: investment_analysis
   skills: [video-frames, analyze_video, investment-agent, writing-agent]
   
2. 生成调用链并交给 orchestration 执行

3. orchestration 负责：
   - 执行步骤调度
   - 异常处理
   - 结果聚合
```

---

## 8. 输出质量验证机制

### 验证流程

```
技能执行 → 输出检查 → 有效性判断 → 通过/失败处理
                              ↓
                        无效则触发 fallback
```

### 验证检查点

```yaml
validation_checkpoints:
  step_1_fetch:
    check:
      - result.content 非空
      - result.content 长度 > 50
    fallback: playwright-scraper-skill
    
  step_2_analyze:
    check:
      - result 非空
      - confidence >= 0.6
    fallback: 简化分析维度
    
  step_3_write:
    check:
      - result.article_text 非空
      - result.article_text 长度 > 100
    fallback: article-writing
    
  step_4_format:
    check:
      - result 非空
    fallback: 输出原始 markdown
```

### 示例验证代码

```python
def validate_skill_output(skill_name, result, context):
    """标准化输出验证"""
    
    validators = {
        "web-content-fetcher": lambda r: (
            r.get("result") and 
            len(str(r.get("result", ""))) > 50 and
            r.get("confidence", 0) > 0.3
        ),
        "writing-agent": lambda r: (
            r.get("result") and
            len(str(r.get("result", ""))) > 100 and
            r.get("confidence", 0) > 0.5
        ),
        "wechat-mp-upload": lambda r: (
            r.get("result") is not None
        )
    }
    
    validator = validators.get(skill_name, lambda r: r is not None)
    
    if not validator(result):
        return {
            "valid": False,
            "fallback": get_fallback_skill(skill_name),
            "reason": f"{skill_name} output validation failed"
        }
    
    return {"valid": True}
```

---

## 9. 完整执行示例

### 示例场景：Get笔记转公众号文章

```
用户输入：
"帮我把这个Get笔记转成公众号文章：https://getnote.io/abc123"
```

### Step 1: 意图分类

```python
输入: "帮我把这个Get笔记转成公众号文章"
意图: content_creation
置信度: 0.92
关键词: ["Get笔记", "转", "公众号文章"]
```

### Step 2: 技能匹配

```
匹配模板: getnote-to-article.yaml
技能链: web-content-fetcher → writing-agent × 3 → wechat-mp-upload
置信度: 0.88
```

### Step 3: 生成的调用链

```yaml
chain:
  - step: 1
    skill: web-content-fetcher
    trigger: user_input
    input:
      source: "https://getnote.io/abc123"
      fetch_options:
        extract_main_content: true
        preserve_formatting: true
    expected_fields: [result, confidence]
    validation:
      min_length: 50
      fallback: prompt_for_content

  - step: 2
    skill: writing-agent
    trigger: step_1 完成
    input:
      action: deep_content_analysis
      text: "${step_1.result.content}"
      context:
        analysis_type: "getnote_extraction"
    expected_fields: [result, core_message]
    validation:
      min_length: 100
      fallback: simplified_extraction

  - step: 3
    skill: writing-agent
    trigger: step_2 完成
    input:
      action: design_article_structure
      analysis: "${step_2.result}"
    expected_fields: [result, sections]
    validation:
      min_items: 3
      fallback: use_default_outline

  - step: 4
    skill: writing-agent
    trigger: step_3 完成
    input:
      action: write_article
      outline: "${step_3.result}"
      core_content: "${step_2.result}"
    expected_fields: [result, draft_article]
    validation:
      min_length: 500
      fallback: article-writing

  - step: 5
    skill: wechat-mp-upload
    trigger: step_4 完成
    input:
      text: "${step_4.result.draft_article}"
      context:
        title: "${step_1.result.title}"
        need_cover: true
    expected_fields: [result]
    validation:
      fallback: output_markdown
```

### Step 4: 执行日志

```
[03:58:01] 🚀 开始执行 Get笔记转公众号
[03:58:01] 📌 Step 1/5: web-content-fetcher
[03:58:02] ✅ 输出验证通过 (content长度: 2847, confidence: 0.95)
[03:58:02] 📌 Step 2/5: writing-agent (内容分析)
[03:58:03] ✅ 输出验证通过 (core_message长度: 523, confidence: 0.85)
[03:58:03] 📌 Step 3/5: writing-agent (结构设计)
[03:58:04] ✅ 输出验证通过 (sections: 5, confidence: 0.80)
[03:58:04] 📌 Step 4/5: writing-agent (文章撰写)
[03:58:06] ✅ 输出验证通过 (draft长度: 2156, confidence: 0.85)
[03:58:06] 📌 Step 5/5: wechat-mp-upload
[03:58:07] ✅ 输出验证通过 (formatted_content已生成)
[03:58:07] 🎉 流水线执行完成!
```

### Step 5: 最终输出

```yaml
final_output:
  success: true
  steps_executed: 5
  total_time: "6s"
  
  results:
    step_1_fetch:
      content_length: 2847
      title: "如何用AI提升工作效率"
      confidence: 0.95
      
    step_2_analysis:
      core_message: "AI工具能显著提升知识工作效率"
      key_insights: 4
      confidence: 0.85
      
    step_3_outline:
      sections: 5
      estimated_read_time: "8分钟"
      confidence: 0.80
      
    step_4_draft:
      article_text长度: 2156
      word_count: 2156
      confidence: 0.85
      
    step_5_format:
      formatted_content: "<完整HTML格式的文章>"
      image_count: 3
      estimated_read_time: "8分钟"
  
  artifacts:
    - type: draft_article
      content: "..."
    - type: formatted_article
      content: "<html>..."
    - type: metadata
      content: "{...}"
```

---

## 10. 执行统计

```yaml
metrics:
  total_chains_generated: 156
  avg_chain_length: 3.2
  top_intents:
    - content_creation: 40%
    - investment_analysis: 25%
    - research_analysis: 20%
    - media_processing: 15%
  avg_generation_time: "<2s"
  success_rate: "95%"
  validation_triggered_fallbacks: 12
  avg_fallback_recovery_rate: "91%"
```