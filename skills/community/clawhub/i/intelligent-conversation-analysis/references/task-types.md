# 分析类型参考

## 8 种分析类型说明

> 以下类型均为官方 API 文档（CreateTask.resultTypes）明确支持的值。

| 类型 | resultTypes 值 | 说明 | 典型场景 |
|------|---------------|------|---------|
| 对话摘要 | `summary` | 提炼对话核心内容，生成结构化摘要 | 快速了解通话内容 |
| 标题生成 | `title` | 为对话生成简短标题 | 对话归档、检索 |
| 关键词抽取 | `keywords` | 提取对话中的关键词 | 内容标注、搜索 |
| 字段信息抽取 | `fields` | 按自定义字段结构提取信息 | CRM 数据录入、结构化存档 |
| 服务质检 | `service_inspection` | 按质检维度检查客服服务是否合规 | 客服质量管理 |
| 问题与解决方案 | `question_solution` | 提取用户问题及对应处理方案 | 工单归档、知识库建设 |
| QA 抽取 | `questions_and_answer` | 生成问答对 | FAQ 构建、知识库 |
| 标签分类 | `category_tag` | 按自定义标签体系对对话分类 | 对话分类、数据统计 |
| 自定义指令 | `custom_prompt` | 使用自定义 prompt 进行分析 | 灵活定制分析逻辑 |

---

## 需要额外配置的类型

### service_inspection（服务质检）

必须提供 `serviceInspection` 配置：

```json
{
  "resultTypes": ["service_inspection"],
  "serviceInspection": {
    "sceneIntroduction": "保险销售场景",
    "inspectionIntroduction": "检测客服是否存在服务不当行为，包括：过度承诺、套取隐私等",
    "inspectionContents": [
      {
        "title": "是否过度承诺",
        "content": "客服在服务过程中，是否存在超出服务标准的承诺行为"
      },
      {
        "title": "是否套取隐私",
        "content": "客服是否故意诱导客户提供非必要的个人隐私信息"
      }
    ]
  }
}
```

### fields（字段信息抽取）

需要提供 `fields` 配置，定义要提取的字段：

```json
{
  "resultTypes": ["fields"],
  "fields": [
    {
      "name": "来电原因",
      "desc": "用户来电咨询的原因分类",
      "code": "callReason",
      "enumValues": [
        { "enumValue": "投诉", "desc": "用户对服务或产品不满" },
        { "enumValue": "咨询", "desc": "用户寻求信息或帮助" },
        { "enumValue": "退款", "desc": "用户申请退款" }
      ]
    },
    {
      "name": "用户联系方式",
      "desc": "对话中提到的用户电话或邮箱",
      "code": "contactInfo"
    }
  ]
}
```

### category_tag（标签分类）

需要提供 `categoryTags` 配置：

```json
{
  "resultTypes": ["category_tag"],
  "categoryTags": [
    {
      "tagName": "高价值客户",
      "tagDesc": "对话中表现出强烈购买意向或高消费能力的客户"
    },
    {
      "tagName": "投诉风险",
      "tagDesc": "对话中表现出明显不满、有投诉倾向的客户"
    }
  ]
}
```

### custom_prompt（自定义指令）

需要提供 `customPrompt` 字段：

```json
{
  "resultTypes": ["custom_prompt"],
  "customPrompt": "请分析这段对话中客服的专业度，并给出 1-10 分的评分及理由"
}
```

---

## 常用组合推荐

| 场景 | 推荐组合 |
|------|---------|
| 快速了解对话 | `["summary", "title", "keywords"]` |
| 客服质检 | `["service_inspection", "question_solution"]` |
| 数据归档 | `["summary", "fields", "category_tag"]` |
| 知识库建设 | `["questions_and_answer", "question_solution"]` |
