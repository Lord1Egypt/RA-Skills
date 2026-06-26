# mooc-course-search

MOOC 课程搜索与推荐 Skill。用于根据用户提问生成多检索词搜索课程，并在需要时补充课程详情，最终输出可执行的选课建议。

## 版本信息

- name: `mooc-course-search`
- version: `1.0.4`
- official: `false`

## 适用场景

- 查找某一主题课程（如高等数学、机器学习、考研辅导）
- 对比多门课程并给出推荐结论
- 按学习目标筛选最适合课程（考试/就业/兴趣/转专业）
- 用户要求进一步了解某一门课程详情

## 核心能力

- 自动生成 `queryList` 搜索词（默认约 3 个，最多 5 个）
- 检索词去重并覆盖同义词/近义表达
- 对检索结果进行二次分析并给出推荐理由
- 仅在用户明确需要时调用课程详情接口

## 接口说明

### 1) 课程搜索接口

- URL: `https://mcp.study.youdao.com/public/mm-course/course/search`
- 方法：HTTP POST
- 请求体关键字段：`queryList: string[]`

示例：

```bash
curl --location "https://mcp.study.youdao.com/public/mm-course/course/search" \
  --header "Content-Type: application/json" \
  --data '{
    "queryList": ["高等数学", "微积分", "考研数学"]
  }'
```

### 2) 课程详情接口

- URL: `https://mcp.study.youdao.com/public/mm-course/course/detail`
- 方法：HTTP POST
- 调用条件：仅当用户明确表示“想进一步了解某门课程”时调用
- 请求体字段：`courseId`、`termId`（来自上一步搜索结果）

示例：

```bash
curl --location "https://mcp.study.youdao.com/public/mm-course/course/detail" \
  --header "Content-Type: application/json" \
  --data '{
    "courseId": 1207108809,
    "termId": 1472362510
  }'
```

## 处理流程

1. 解析用户意图，自动生成 `queryList`（3-5 个）
2. 调用课程搜索接口，获取候选课程
3. 结合用户目标做课程推荐与对比
4. 若用户明确要求深入了解单门课程，再调用详情接口补全信息
5. 输出推荐结果、摘要与下一轮检索建议

## 输出规范

- 推荐课程 1-3 门及推荐理由
- 每门课程关键信息摘要（课程定位、适合人群、学习收益）
- 结果不足时给出更精确的下一轮检索词
- 用户关注证书时补充认证与考核提示
- 调用详情接口后补充开课院校、授课教师、章节/进度、考核与证书说明
- 可展示实际使用的 `queryList`（3-5 个）

## 超时与重试

| Operation                                         | Expected Time | Recommended Timeout | Notes  |
| ------------------------------------------------- | ------------- | ------------------- | ------ |
| Course Search (`/public/mm-course/course/search`) | 5-20s         | 30s                 | 常规课程检索 |
| Course Detail (`/public/mm-course/course/detail`) | 5-15s         | 30s                 | 课程详情补全 |

重试策略（仅瞬时错误）：

1. 第 1 次重试：等待 2 秒
2. 第 2 次重试：等待 4 秒
3. 第 3 次重试：等待 8 秒
4. 最多 3 次

不重试场景：

- 参数错误或请求体不合法
- 认证失败（访问凭证缺失、无效或已过期）

## 接口地址

- 课程搜索接口：`https://mcp.study.youdao.com/public/mm-course/course/search`
- 课程详情接口：`https://mcp.study.youdao.com/public/mm-course/course/detail`

## 错误处理建议

- `200`：正常解析并输出推荐
- `400`：提示优化检索词或参数
- `404`：提示资源不存在并建议更换关键词
- `500/503/504`：按重试策略处理，失败后给出降级建议

## 安全约束

- 不在回复中明文输出长期有效访问凭证
- 不将访问凭证写入仓库文件或日志
- 仅展示与用户问题相关的最小必要信息

