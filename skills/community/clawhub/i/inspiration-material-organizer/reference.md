# 参考说明

## 灵感卡片标准结构

每条素材保存为一张卡片：

```json
{
  "id": "uuid",
  "title": "自动或手动标题",
  "content": "正文内容",
  "url": "可选链接",
  "source": "chat|screenshot|link|note|other",
  "created_at": "ISO 时间",
  "updated_at": "ISO 时间",
  "topic": "主题分类",
  "tags": ["标签1", "标签2"],
  "group": "分组名"
}
```

## 主题分类规则（可配置）

默认读取：

` .cursor/skills/inspiration-material-organizer/config/topic_rules.json `

也可通过环境变量覆盖：

`INSPIRATION_TOPIC_RULES_PATH`

示例格式：

```json
{
  "写作": ["写作", "选题", "表达"],
  "产品": ["需求", "用户", "功能"],
  "你自定义的新主题": ["关键词1", "关键词2"]
}
```

内置默认规则：

- 写作：写作、选题、表达、文案、结构、标题
- 产品：需求、用户、功能、原型、体验、增长
- 运营：社群、活动、复盘、留存、转化
- 营销：品牌、传播、投放、渠道、广告
- 技术：代码、架构、接口、自动化、AI、Python
- 个人成长：习惯、效率、学习、目标、认知
- 未分类：未命中关键词

## 检索评分逻辑

总分由三部分组成：

1. 查询词在 `title/content` 的命中次数
2. 查询词与 `tags/topic/group` 的交集加权
3. 归一化后的 token overlap（简易语义近似）

## 灵感反刍建议

- 每日 3~5 条随机回顾
- 每周按主题定向回顾（如写作、产品）
- 对高价值素材补充“可执行下一步”，让收藏变可用
