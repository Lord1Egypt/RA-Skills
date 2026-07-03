<!-- @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08 -->

# OPC智脑 - Dify平台集成指南

## 概述

[Dify](https://dify.ai) 是一款开源的LLM应用开发平台，支持可视化编排AI工作流。opc-skills可以集成到Dify中，构建OPC智脑应用。

## 集成方式

### 方式1：作为Chatflow应用

#### Step 1：创建Chatflow

1. 登录Dify，点击"创建应用"→"Chatflow"
2. 应用名称：`OPC智脑`

#### Step 2：配置LLM节点

添加一个LLM节点，配置如下：

- **模型**：GPT-4o / Claude 3.5 Sonnet（推荐）
- **System Prompt**：拼接以下内容
  ```
  [system-persona.md内容]
  
  [core-hub.md内容]
  ```

#### Step 3：添加变量收集节点

在Chatflow中添加"问题分类器"节点，根据用户输入自动路由到对应Skill：

```
分类规则：
- 包含"idea"/"可行性"/"验证" → Skill1路由
- 包含"MVP"/"产品"/"设计" → Skill2路由
- 包含"注册"/"合规"/"公司" → Skill3路由
- 包含"获客"/"种子"/"冷启动" → Skill4路由
- 包含"增长"/"规模化" → Skill5路由
- 其他 → 核心中枢处理
```

#### Step 4：配置5个Skill分支

每个Skill分支包含：
1. 一个LLM节点（使用对应Skill的Prompt）
2. 一个输出节点（格式化为三维输出模板）

### 方式2：作为Workflow应用

如果需要更精细的控制，可以创建Workflow应用：

#### 节点编排

```
开始 → 信息采集(LLM) → 阶段判定(代码节点) → 路由(条件分支)
  → Skill1分支(LLM+输出)
  → Skill2分支(LLM+输出)
  → Skill3分支(LLM+输出)
  → Skill4分支(LLM+输出)
  → Skill5分支(LLM+输出)
→ 结束
```

#### 阶段判定代码节点

使用Dify的"代码执行"节点，嵌入opc-skills的阶段判定逻辑：

```python
def main(demand_validation, solution_maturity, compliance_readiness, user_acquisition, scalability_level):
    # 五维度加权评分
    weights = {
        'demand': 0.30,
        'solution': 0.25,
        'compliance': 0.15,
        'user': 0.15,
        'scale': 0.15,
    }
    
    score = (
        demand_validation * weights['demand'] +
        solution_maturity * weights['solution'] +
        compliance_readiness * weights['compliance'] +
        user_acquisition * weights['user'] +
        scalability_level * weights['scale']
    )
    
    # 阶段判定
    if score <= 20:
        stage = 'IDEA'
        skill = 'skill1-idea-feasibility'
    elif score <= 40:
        stage = 'MVP'
        skill = 'skill2-mvp-design'
    elif score <= 60:
        stage = 'ENTITY'
        skill = 'skill3-opc-compliance'
    elif score <= 80:
        stage = 'VALIDATION'
        skill = 'skill4-seed-coldstart'
    else:
        stage = 'SCALE'
        skill = 'skill5-scale-growth'
    
    return {
        'stage': stage,
        'skill': skill,
        'score': score,
    }
```

### 方式3：使用Dify知识库

将opc-skills的Prompt文件上传到Dify知识库：

1. 创建知识库：`OPC智脑知识库`
2. 上传文件：
   - `src/prompts/system-persona.md`
   - `src/prompts/core-hub.md`
   - `src/prompts/skill1.md` ~ `skill5.md`
   - `docs/stage-model.md`
   - `docs/skill-reference.md`
3. 在LLM节点中引用知识库
4. 配置检索策略：根据用户问题自动检索相关Prompt

## 输出变量配置

在Dify中配置结构化输出变量：

| 变量名 | 类型 | 说明 |
|--------|------|------|
| stage | string | 当前阶段（IDEA/MVP/ENTITY/VALIDATION/SCALE） |
| stageLabel | string | 阶段中文名 |
| diagnosis | string | 当前阶段诊断 |
| actionPlan | array[string] | 整改方案动作清单 |
| layout | string | 下一阶段前置布局 |
| confidence | number | 判定置信度 |

## 测试用例

| 用户输入 | 预期路由 | 预期阶段 |
|---------|---------|---------|
| "我想做一个SaaS工具" | Skill1 | IDEA |
| "需求验证通过了，帮我设计MVP" | Skill2 | MVP |
| "我要注册一人有限公司" | Skill3 | ENTITY |
| "产品做好了，怎么找第一批用户" | Skill4 | VALIDATION |
| "有10个付费用户了，怎么增长" | Skill5 | SCALE |

## 注意事项

1. Dify的LLM节点有Token限制，长Prompt可能需要拆分为多个节点
2. 建议使用Dify的"对话变量"功能，跨轮次保持用户阶段信息
3. 代码执行节点支持Python，可以嵌入opc-skills的核心逻辑
4. Dify Cloud有API调用限制，自部署版无此限制