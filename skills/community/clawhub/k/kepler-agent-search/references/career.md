# 招聘与职位搜索

## 概述

招聘平台和职位信息的搜索能力，适用于求职调研和人才市场分析。

## 支持平台

### 智联招聘 (Zhaopin)
- **引擎标识**: `"zhaopin"`
- **适用场景**: 国内综合招聘、各行业职位搜索、简历投递
- **特点**: 国内领先招聘平台，职位覆盖全面

```yaml
query: "Java 开发工程师 上海"
engines: ["zhaopin"]
max_results: 10
```

### 前程无忧 (51job)
- **引擎标识**: `"51job"`
- **适用场景**: 综合招聘、外企职位、中高端岗位
- **特点**: 老牌招聘网站，外企资源丰富

```yaml
query: "产品经理 北京"
engines: ["51job"]
max_results: 10
```

## 平台特点对比

| 平台 | 职位类型 | 优势领域 | 适用人群 |
|------|----------|----------|----------|
| 智联招聘 | 综合类 | 互联网、金融、传统行业 | 各层级求职者 |
| 前程无忧 | 综合类 | 外企、中高端岗位 | 有经验的求职者 |

## 使用方式

### 智联招聘定向搜索

```yaml
# 搜索技术职位
query: "Python 工程师"
engines: ["zhaopin"]

# 按地点搜索
query: "前端开发 深圳"
engines: ["zhaopin"]

# 按经验搜索
query: "资深 Java 开发 3-5年"
engines: ["zhaopin"]
```

### 前程无忧定向搜索

```yaml
# 搜索管理岗位
query: "技术经理"
engines: ["51job"]

# 外企职位搜索
query: "外企 产品经理"
engines: ["51job"]

# 按薪资搜索
query: "年薪 30万以上"
engines: ["51job"]
```

### 多平台对比搜索

```yaml
# 同一职位在多个平台对比
query: "算法工程师 北京"
engines: ["zhaopin"]  # 然后执行 engines: ["51job"]
```

### 通过 web_reader 读取详情

```yaml
# 读取智联招聘职位详情
tool: mcp__kepler__web_reader
url: "https://jobs.zhaopin.com/xxxxx"
format: "markdown"

# 读取前程无忧职位详情
tool: mcp__kepler__web_reader
url: "https://jobs.51job.com/xxxxx"
format: "markdown"
```

## 搜索技巧

### 职位搜索优化
1. **职位名称**: 使用标准职位名，如 "Java 后端工程师"、"产品经理"
2. **技能关键词**: 如 "Python"、"React"、"数据分析"
3. **地点筛选**: 城市名，如 "上海"、"北京"、"深圳"
4. **经验要求**: 如 "3-5年"、"应届生"、"5-10年"
5. **薪资范围**: 如 "15-25K"、"年薪30万"

### 公司调研
1. **公司评价**: 搜索 "公司名 + 面试" 或 "公司名 + 评价"
2. **薪资水平**: 搜索 "公司名 + 薪资" 或 "岗位 + 薪资"
3. **团队信息**: 搜索 "公司名 + 团队" 或 "公司名 + 技术栈"

### 不同平台搜索策略
- **智联招聘**: 职位数量多，适合广撒网
- **前程无忧**: 外企资源丰富，适合有经验的求职者
- **多平台对比**: 同一职位在不同平台可能有不同的薪资描述

## 信息提取

招聘页面可提取的信息：
- 职位描述和要求
- 公司介绍和规模
- 薪资范围和福利待遇
- 工作地点和交通信息
- 团队信息和工作内容
- 联系方式和投递方式

## URL 格式

### 智联招聘
- **职位详情**: `jobs.zhaopin.com/xxxxx` 或 `www.zhaopin.com/jobs/xxxxx`
- **搜索结果**: `sou.zhaopin.com/?...`
- **公司主页**: `company.zhaopin.com/xxxxx`

### 前程无忧
- **职位详情**: `jobs.51job.com/xxxxx`
- **搜索结果**: `search.51job.com/jobsearch/...`
- **公司主页**: `company.51job.com/xxxxx`

## 示例

```yaml
# 搜索技术职位
query: "Golang 后端工程师 上海"
engines: ["zhaopin"]

# 搜索互联网大厂
query: "字节跳动 产品经理"
engines: ["zhaopin"]

# 搜索外企职位
query: "外企 软件工程师"
engines: ["51job"]

# 搜索高薪职位
query: "年薪 50万 技术总监"
engines: ["51job"]

# 多平台对比
query: "数据分析师 杭州"
engines: ["zhaopin"]  # 然后执行 engines: ["51job"]
```

## 注意事项
- 职位信息有时效性，注意查看发布日期
- 薪资数据仅供参考，实际以面试沟通为准
- 注意识别虚假招聘信息，谨慎对待要求付费的职位
- 求职时请通过官方渠道投递简历
- 建议使用多个平台对比，获取更全面的职位信息
