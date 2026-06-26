---
name: mooc-course-search
description: MOOC 课程搜索与推荐服务。适用于找课、课程对比、按学习目标筛课、关注证书与评价等场景。关键词：MOOC、慕课、课程推荐、课程对比、证书、考研、机器学习、高等数学。
version: 1.0.4
official: false
---

# MOOC Course Search

用于搜索 MOOC 课程，并基于用户目标输出可执行的选课建议。

## When to Use This Skill

### Primary Triggers（优先触发）

- 用户明确要找某主题课程（如高等数学、机器学习、考研相关）
- 用户要求比较多门课程并给出推荐结论
- 用户关心课程详情、学习路径、认证成绩或证书信息
- 用户希望按目标筛选最适合课程（考试、就业、兴趣、转专业）

### Automatic Trigger Keywords

- mooc, 慕课, 中国大学MOOC, 课程推荐, 课程对比
- 证书, 认证成绩, 考核方式, 学习收益
- 高等数学, 机器学习, 人工智能,计算机基础, 考研辅导

### When NOT to Use This Skill

- 用户仅需通用网页信息检索，且不涉及课程选择
- 用户问题与学习课程无关（如商品比价、新闻热点）

## Platform Notes

- 平台：中国大学 MOOC（网易与教育部爱课程网联合推出）
- 特色：名校名师课程丰富，支持免费学习与认证体系
- 学科覆盖：基础科学、人文社科、工程技术、经管法学、农林医药等

## Execution Guidelines

### Request Endpoint

默认使用以下接口进行课程搜索：

```bash
curl --location "https://mcp.study.youdao.com/public/mm-course/course/search" \
  --header "Content-Type: application/json" \
  --data '{
    "queryList": ["高等数学", "微积分", "考研数学"]
  }'
```

课程详情查询接口（仅在用户明确想进一步了解某门课程时调用，入参来自上一步搜索结果中的 `courseId` 和 `termId`）：

```bash
curl --location "https://mcp.study.youdao.com/public/mm-course/course/detail" \
  --header "Content-Type: application/json" \
  --data '{
    "courseId": 1207108809,
    "termId": 1472362510
  }'
```

### Runtime Rules

- API 调用应等待服务端完成并返回结果后再继续处理
- 搜索接口请求体使用 `queryList`
- 根据用户提问自动生成搜索词列表，默认约 3 个，最多不超过 5 个
- `queryList` 内搜索词应去重，并覆盖同义词/近义表达（如“机器学习/机器学习入门”）
- 仅当用户表达“想进一步了解某门课”时调用课程详情接口
- 详情接口请求体固定使用上一步搜索结果：`courseId`、`termId`
- 当搜索结果不足时，需自动改写检索词再检索 1 次
- 结果为空时，明确告知并给出下一轮检索建议

### Timeout & Retry

| Operation                                         | Expected Time | Recommended Timeout | Notes  |
| ------------------------------------------------- | ------------- | ------------------- | ------ |
| Course Search (`/public/mm-course/course/search`) | 5-20s         | 30s                 | 常规课程检索 |
| Course Detail (`/public/mm-course/course/detail`) | 5-15s         | 30s                 | 课程详情补全 |

重试策略（仅瞬时错误）：

1. 第 1 次重试：等待 2 秒
2. 第 2 次重试：等待 4 秒
3. 第 3 次重试：等待 8 秒
4. 最多 3 次，超出后返回失败原因与建议

不重试场景：

- 参数错误或请求体不合法
- 认证失败（访问凭证缺失、无效或已过期）

## Endpoint Configuration

- Course Search: `https://mcp.study.youdao.com/public/mm-course/course/search`
- Course Detail: `https://mcp.study.youdao.com/public/mm-course/course/detail`

## Output Requirements

拿到检索结果后，必须结合用户意图进行二次分析，输出以下内容：

1. 最推荐课程（1-3 门）及推荐理由
2. 每门课程关键信息摘要（课程定位、适合人群、学习收益）
3. 若结果不足，给出更精确的下一轮检索词
4. 若用户关注证书，补充认证与考核相关提示
5. 仅在用户要求进一步了解单门课程时，调用详情接口并补充课程详细信息（如开课院校、授课教师、章节/进度安排、考核与证书说明）
6. 输出时可展示实际使用的 `queryList`（3-5 个）以便用户理解检索覆盖范围

## Interaction Strategy

- 用户目标不清晰时，先澄清学习目标（考试/就业/兴趣）
- 用户强调效率时，优先推荐结构清晰、评价稳定的入门课
- 用户要求进阶时，按“入门 -> 进阶 -> 实战”给出组合建议
- 用户未提出“进一步了解某门课程”时，不主动调用详情接口

## Error Handling

推荐按 HTTP 状态码处理：

- `200`: 正常解析并输出推荐
- `400`: 提示用户优化查询词或参数
- `404`: 提示资源不存在并建议更换关键词
- `500/503/504`: 按重试策略处理，失败后给出降级建议

## Security Constraints

- 不在回复中明文输出长期有效访问凭证
- 不将访问凭证写入仓库文件或日志
- 仅展示与用户问题相关的最小必要信息
