# 各平台爬取策略和 API 文档

## 概述

本文档详细说明了各平台(微博、知乎、B站、抖音、今日头条、腾讯新闻、澎湃新闻)的爬取策略、API 文档和注意事项。

## 1. 微博 (Weibo)

### API 方式
- **推荐 API**: 全网热榜聚合 API (uapis.cn)
- **端点**: `https://uapis.cn/api/get-misc-hotboard`
- **参数**:
  - `name`: weibo
  - `limit`: 返回数量(默认 20)
- **返回格式**:
  ```json
  {
    "code": 200,
    "data": [
      {
        "title": "热搜标题",
        "url": "热搜链接",
        "hot": 1234567
      }
    ]
  }
  ```

### 直接爬取方式
- **热搜页面**: `https://s.weibo.com/top/summary`
- **HTML 结构**:
  - 热搜项: `<a href="/weibo?q=...">标题</a>`
  - 排名: 通过列表顺序获取
- **注意事项**:
  - 微博有较强的反爬虫机制,建议优先使用 API
  - 如果直接爬取,需要添加 User-Agent 和合理的延时
  - 注意遵守微博的使用条款

## 2. 知乎 (Zhihu)

### API 方式
- **推荐 API**: 全网热榜聚合 API (uapis.cn)
- **端点**: `https://uapis.cn/api/get-misc-hotboard`
- **参数**:
  - `name`: zhihu
  - `limit`: 返回数量(默认 20)

### 直接爬取方式
- **热榜页面**: `https://www.zhihu.com/hot`
- **HTML 结构**:
  - 热榜项: `<div class="HotItem">`
  - 标题: `<h2 class="HotItem-title">`
  - 链接: `<a href="...">`
- **注意事项**:
  - 知乎需要登录才能查看完整内容
  - 建议使用 API 获取热榜数据
  - 如果直接爬取,需要添加 Referer 头

## 3. B站 (Bilibili)

### API 方式
- **推荐 API**: 全网热榜聚合 API (uapis.cn)
- **端点**: `https://uapis.cn/api/get-misc-hotboard`
- **参数**:
  - `name`: bilibili
  - `limit`: 返回数量(默认 20)

### 直接爬取方式
- **热门页面**: `https://www.bilibili.com/v/popular/all`
- **HTML 结构**:
  - 视频项: `<a class="video-title">`
  - 标题: `title` 属性
  - 链接: `href` 属性
- **注意事项**:
  - B站的反爬虫相对较弱
  - 可以直接爬取热门视频列表
  - 建议添加 1-2 秒的延时

## 4. 抖音 (Douyin)

### API 方式
- **推荐 API**: 全网热榜聚合 API (uapis.cn)
- **端点**: `https://uapis.cn/api/get-misc-hotboard`
- **参数**:
  - `name`: douyin
  - `limit`: 返回数量(默认 20)

### 直接爬取方式
- **难度**: 高
- **原因**: 抖音使用动态加载和加密的 API,直接爬取非常困难
- **建议**: 优先使用 API,不建议直接爬取

## 5. 今日头条 (Toutiao)

### API 方式
- **推荐 API**: 全网热榜聚合 API (uapis.cn)
- **端点**: `https://uapis.cn/api/get-misc-hotboard`
- **参数**:
  - `name`: toutiao
  - `limit`: 返回数量(默认 20)

### 直接爬取方式
- **首页**: `https://www.toutiao.com/`
- **HTML 结构**: 动态加载,需要分析 API
- **建议**: 优先使用 API,直接爬取复杂度较高

## 6. 腾讯新闻 (Tencent News)

### API 方式
- **推荐 API**: 全网热榜聚合 API (uapis.cn)
- **端点**: `https://uapis.cn/api/get-misc-hotboard`
- **参数**:
  - `name`: tencent
  - `limit`: 返回数量(默认 20)

### 直接爬取方式
- **首页**: `https://news.qq.com/`
- **HTML 结构**:
  - 新闻链接: `<a href="/a/...">`
  - 需要从首页提取新闻链接
- **注意事项**:
  - 腾讯新闻的反爬虫较弱
  - 可以直接爬取首页新闻链接
  - 建议添加合理的延时

## 7. 澎湃新闻 (The Paper)

### API 方式
- **推荐 API**: 全网热榜聚合 API (uapis.cn)
- **端点**: `https://uapis.cn/api/get-misc-hotboard`
- **参数**:
  - `name`: thepaper
  - `limit`: 返回数量(默认 20)

### 直接爬取方式
- **首页**: `https://www.thepaper.cn/`
- **HTML 结构**:
  - 新闻标题: `<h2>` 标签
  - 链接: 内部的 `<a>` 标签
- **注意事项**:
  - 澎湃新闻的反爬虫较弱
  - 可以直接爬取首页标题
  - 建议添加合理的延时

## 全网热榜聚合 API (uapis.cn)

### 基本信息
- **基础 URL**: `https://uapis.cn/api/get-misc-hotboard`
- **方法**: GET
- **免费**: 是,无需注册
- **更新频率**: 约 30 分钟一次

### 参数说明
- `name`: 平台名称
  - 支持的平台: weibo, zhihu, bilibili, douyin, toutiao, tencent, thepaper
- `limit`: 返回数量
  - 默认: 20
  - 最大: 50(部分平台)

### 响应格式
```json
{
  "code": 200,
  "message": "获取成功",
  "title": "平台名称",
  "subtitle": "热榜",
  "total": 20,
  "updateTime": "2026-03-21 12:00:00",
  "data": [
    {
      "title": "新闻标题",
      "url": "新闻链接",
      "hot": 1234567,
      "rank": 1
    }
  ]
}
```

### 使用示例
```python
import requests

url = "https://uapis.cn/api/get-misc-hotboard"
params = {
    'name': 'weibo',
    'limit': 20
}

response = requests.get(url, params=params)
data = response.json()
```

### 优势
- 多平台聚合,一次调用获取多个平台数据
- 免费且无需注册
- 已处理反爬虫问题
- 数据格式统一

### 限制
- 更新频率约 30 分钟,不是实时数据
- 部分平台可能不提供完整的热度值
- 依赖第三方服务的稳定性

## 反爬虫处理建议

### 1. 请求头设置
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.example.com/'
}
```

### 2. 延时设置
```python
import time
# 礼貌性延时 1-3 秒
time.sleep(2)
```

### 3. 使用 Session
```python
session = requests.Session()
session.headers.update(headers)
```

### 4. 代理 IP(如需要大量爬取)
```python
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}
response = session.get(url, proxies=proxies)
```

### 5. 遵守 robots.txt
在爬取前,检查目标网站的 robots.txt 文件,遵守其规则。

## 合规性注意事项

1. **版权问题**: 爬取的数据仅供个人学习或研究使用,不得用于商业目的
2. **服务器压力**: 控制请求频率,避免对目标网站造成压力
3. **使用条款**: 遵守各平台的使用条款和 API 使用协议
4. **数据隐私**: 不爬取和存储用户的个人隐私信息
5. **法律风险**: 确保爬取行为符合相关法律法规

## 推荐的数据获取策略

### 快速获取
优先使用全网热榜聚合 API(uapis.cn):
- 速度快,一次调用获取多平台数据
- 已处理反爬虫问题
- 数据格式统一,易于处理

### 详细内容
使用直接爬取方式:
- 获取更详细的内容
- 自定义爬取逻辑
- 但需要处理反爬虫问题

### 混合使用
结合两种方式:
- 使用 API 快速获取热榜
- 使用直接爬取获取详细内容
- 平衡速度和详细度
