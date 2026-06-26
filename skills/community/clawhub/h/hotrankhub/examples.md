# 使用示例

本文档提供 HotRank Hub API 的详细使用示例，帮助您快速集成和使用热榜数据。

## 目录

1. [基础示例](#基础示例)
2. [高级示例](#高级示例)
3. [特定领域监控](#特定领域监控)
4. [错误处理](#错误处理)
5. [性能优化](#性能优化)

---

## 基础示例

### 获取单一平台热榜

#### JavaScript/TypeScript

```javascript
// 获取微博热搜
async function getWeiboHot() {
  const response = await fetch('https://airouter.tech/api/weibo');
  const data = await response.json();

  console.log('微博热搜前10条：');
  data.data.slice(0, 10).forEach((item, index) => {
    console.log(`${index + 1}. ${item.title} - 热度: ${item.hot}`);
  });
}

getWeiboHot();
```

#### Python

```python
import requests

def get_zhihu_hot():
    """获取知乎热榜"""
    response = requests.get('https://airouter.tech/api/zhihu')
    data = response.json()

    print('知乎热榜前10条：')
    for i, item in enumerate(data['data'][:10], 1):
        print(f"{i}. {item['title']} - 热度: {item.get('hot', 'N/A')}")

get_zhihu_hot()
```

#### cURL

```bash
# 获取 GitHub 趋势
curl https://airouter.tech/api/github-trending

# 获取 B站热门
curl https://airouter.tech/api/bilibili

# 获取抖音热点
curl https://airouter.tech/api/douyin
```

---

## 高级示例

### 跨平台对比分析

对比多个平台的热榜，找出共同热点或差异。

```javascript
async function comparePlatforms(sources) {
  // 并发获取多个平台数据
  const results = await Promise.all(
    sources.map(async (source) => {
      const response = await fetch(`https://airouter.tech/api/${source}`);
      return response.json();
    })
  );

  // 创建标题到平台的映射
  const titleMap = new Map();
  results.forEach((result, index) => {
    const source = sources[index];
    result.data.forEach((item) => {
      if (!titleMap.has(item.title)) {
        titleMap.set(item.title, []);
      }
      titleMap.get(item.title).push(source);
    });
  });

  // 找出跨平台共同热点
  const commonTopics = [];
  titleMap.forEach((platforms, title) => {
    if (platforms.length > 1) {
      commonTopics.push({
        title,
        platforms,
        count: platforms.length
      });
    }
  });

  // 按出现次数排序
  commonTopics.sort((a, b) => b.count - a.count);

  console.log('跨平台共同热点：');
  commonTopics.slice(0, 10).forEach((topic, i) => {
    console.log(`${i + 1}. ${topic.title}`);
    console.log(`   出现平台: ${topic.platforms.join(', ')}`);
  });

  return commonTopics;
}

// 对比微博、知乎、今日头条
comparePlatforms(['weibo', 'zhihu', 'toutiao']);
```

### 生成热点日报

```javascript
async function generateDailyReport() {
  const sources = [
    { id: 'weibo', name: '微博' },
    { id: 'zhihu', name: '知乎' },
    { id: 'douyin', name: '抖音' },
    { id: 'bilibili', name: 'B站' }
  ];

  const reports = await Promise.all(
    sources.map(async ({ id, name }) => {
      const response = await fetch(`https://airouter.tech/api/${id}`);
      const data = await response.json();
      return {
        platform: name,
        topItems: data.data.slice(0, 5)
      };
    })
  );

  // 生成报告
  console.log('=== 今日热点日报 ===\n');

  reports.forEach((report) => {
    console.log(`【${report.platform}热榜 TOP 5】`);
    report.topItems.forEach((item, i) => {
      console.log(`${i + 1}. ${item.title}`);
      if (item.hot) console.log(`   热度: ${item.hot}`);
    });
    console.log('');
  });

  return reports;
}

generateDailyReport();
```

### 热度趋势追踪

```javascript
class TrendTracker {
  constructor() {
    this.history = new Map();
  }

  async fetchAndTrack(source) {
    const response = await fetch(`https://airouter.tech/api/${source}`);
    const data = await response.json();
    const timestamp = Date.now();

    data.data.forEach((item) => {
      if (!this.history.has(item.title)) {
        this.history.set(item.title, []);
      }
      this.history.get(item.title).push({
        timestamp,
        rank: item.id,
        hot: item.hot
      });
    });

    return data;
  }

  getTrend(title) {
    return this.history.get(title) || [];
  }
}

// 使用示例
const tracker = new TrendTracker();
setInterval(() => {
  tracker.fetchAndTrack('weibo');
}, 5 * 60 * 1000); // 每5分钟追踪一次
```

---

## 特定领域监控

### 财经热点监控

监控财经类平台热榜，获取最新财经资讯。

```javascript
async function monitorFinanceNews() {
  const financeSources = ['xueqiu', 'wallstreetcn', 'jin10', 'cls'];

  const allNews = await Promise.all(
    financeSources.map(async (source) => {
      const response = await fetch(`https://airouter.tech/api/${source}`);
      const data = await response.json();
      return {
        source,
        items: data.data.slice(0, 10)
      };
    })
  );

  // 提取关键词（示例）
  const keywords = new Map();
  allNews.forEach(({ source, items }) => {
    items.forEach((item) => {
      // 简单的关键词提取（实际应用中可使用 NLP）
      const words = item.title.split(/\s+/);
      words.forEach((word) => {
        if (word.length > 2) {
          if (!keywords.has(word)) {
            keywords.set(word, []);
          }
          keywords.get(word).push(source);
        }
      });
    });
  });

  console.log('财经热点关键词：');
  const sortedKeywords = Array.from(keywords.entries())
    .filter(([_, sources]) => sources.length > 1)
    .sort((a, b) => b[1].length - a[1].length)
    .slice(0, 20);

  sortedKeywords.forEach(([keyword, sources]) => {
    console.log(`${keyword}: ${sources.length} 次提及`);
  });

  return allNews;
}

monitorFinanceNews();
```

### 科技资讯聚合

```javascript
async function aggregateTechNews() {
  const techSources = [
    'github-trending',
    'hackernews',
    'ithome',
    '36kr',
    'juejin'
  ];

  const techNews = await Promise.all(
    techSources.map(async (source) => {
      const response = await fetch(`https://airouter.tech/api/${source}`);
      const data = await response.json();
      return {
        source,
        items: data.data.slice(0, 10)
      };
    })
  );

  // 分类整理
  const categories = {
    programming: [],
    products: [],
    news: []
  };

  techNews.forEach(({ source, items }) => {
    items.forEach((item) => {
      if (source === 'github-trending' || source === 'juejin') {
        categories.programming.push(item);
      } else if (source === '36kr' || source === 'ithome') {
        categories.products.push(item);
      } else {
        categories.news.push(item);
      }
    });
  });

  console.log('=== 科技资讯聚合 ===\n');

  Object.entries(categories).forEach(([category, items]) => {
    console.log(`【${category}】`);
    items.slice(0, 5).forEach((item, i) => {
      console.log(`${i + 1}. ${item.title}`);
    });
    console.log('');
  });

  return categories;
}

aggregateTechNews();
```

### 娱乐热点追踪

```javascript
async function trackEntertainmentTrends() {
  const entertainmentSources = ['weibo', 'douyin', 'bilibili', 'douban-movic'];

  const trends = await Promise.all(
    entertainmentSources.map(async (source) => {
      const response = await fetch(`https://airouter.tech/api/${source}`);
      const data = await response.json();
      return {
        source,
        topTrend: data.data[0]
      };
    })
  );

  console.log('=== 娱乐热点追踪 ===\n');
  trends.forEach(({ source, topTrend }) => {
    console.log(`${source}: ${topTrend.title}`);
    if (topTrend.hot) {
      console.log(`  热度: ${topTrend.hot}`);
    }
    if (topTrend.url) {
      console.log(`  链接: ${topTrend.url}`);
    }
    console.log('');
  });

  return trends;
}

trackEntertainmentTrends();
```

---

## 错误处理

### 基础错误处理

```javascript
async function getHotListWithErrorHandling(source) {
  try {
    const response = await fetch(`https://airouter.tech/api/${source}`);

    // 检查 HTTP 状态码
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    // 检查 API 响应状态
    if (data.code !== 200) {
      throw new Error(`API Error: ${data.msg}`);
    }

    return data.data;
  } catch (error) {
    console.error(`获取 ${source} 热榜失败:`, error.message);

    // 返回空数组或默认值
    return [];
  }
}
```

### 使用 Promise.allSettled

```javascript
async function fetchMultipleSafely(sources) {
  const results = await Promise.allSettled(
    sources.map((source) =>
      fetch(`https://airouter.tech/api/${source}`).then((r) => r.json())
    )
  );

  const successful = [];
  const failed = [];

  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      successful.push({
        source: sources[index],
        data: result.value
      });
    } else {
      failed.push({
        source: sources[index],
        error: result.reason.message
      });
    }
  });

  console.log('成功的请求:', successful.length);
  console.log('失败的请求:', failed.length);

  failed.forEach(({ source, error }) => {
    console.error(`${source}: ${error}`);
  });

  return { successful, failed };
}
```

---

## 性能优化

### 实现本地缓存

```javascript
class HotListCache {
  constructor(cacheTime = 5 * 60 * 1000) {
    this.cache = new Map();
    this.cacheTime = cacheTime;
  }

  async get(source) {
    const cached = this.cache.get(source);

    // 检查缓存是否有效
    if (cached && Date.now() - cached.timestamp < this.cacheTime) {
      console.log(`使用缓存: ${source}`);
      return cached.data;
    }

    // 获取新数据
    console.log(`获取新数据: ${source}`);
    const response = await fetch(`https://airouter.tech/api/${source}`);
    const data = await response.json();

    // 更新缓存
    this.cache.set(source, {
      data: data.data,
      timestamp: Date.now()
    });

    return data.data;
  }

  clear(source) {
    if (source) {
      this.cache.delete(source);
    } else {
      this.cache.clear();
    }
  }
}

// 使用示例
const cache = new HotListCache();
await cache.get('weibo'); // 第一次会请求
await cache.get('weibo'); // 5分钟内会使用缓存
```

### 请求去重

```javascript
class RequestDeduper {
  constructor() {
    this.pendingRequests = new Map();
  }

  async fetch(source) {
    // 如果已有相同请求正在进行，返回同一个 Promise
    if (this.pendingRequests.has(source)) {
      return this.pendingRequests.get(source);
    }

    // 创建新请求
    const promise = fetch(`https://airouter.tech/api/${source}`)
      .then((r) => r.json())
      .finally(() => {
        // 请求完成后移除
        this.pendingRequests.delete(source);
      });

    this.pendingRequests.set(source, promise);
    return promise;
  }
}

// 使用示例
const deduper = new RequestDeduper();

// 即使并发调用，也只会发送一次请求
Promise.all([
  deduper.fetch('weibo'),
  deduper.fetch('weibo'),
  deduper.fetch('weibo')
]);
```

### 批量请求优化

```javascript
async function batchFetch(sources, batchSize = 5) {
  const results = [];

  for (let i = 0; i < sources.length; i += batchSize) {
    const batch = sources.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map((source) =>
        fetch(`https://airouter.tech/api/${source}`).then((r) => r.json())
      )
    );
    results.push(...batchResults);

    // 避免请求过快
    if (i + batchSize < sources.length) {
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }

  return results;
}

// 使用示例
const sources = ['weibo', 'zhihu', 'douyin', 'bilibili', 'toutiao'];
const results = await batchFetch(sources, 2);
```

---

## 更多示例

更多高级用法和最佳实践，请参考：
- [API 完整文档](./api-reference.md)
- [SKILL 主文档](./SKILL.md)