# Latte News Fetcher V2

> 📰 新闻获取与RSS订阅工具

## 功能

- **新闻列表获取** - 从主流媒体获取今日新闻
- **Tavily 搜索** - 搜索替代信源
- **RSS 订阅** - 支持 RSS 订阅
- **多格式支持** - 国际、国内、财经、科技等

---

## 安装

### 1. 系统依赖

```bash
brew install node
```

### 2. Node 依赖

```bash
npm install node-fetch
```

### 3. 可选：Tavily API Key

```bash
export TAVILY_API_KEY="tvly-xxx"
```

---

## 使用

### 获取今日新闻

```
你：今天有什么新闻
我：[自动获取并发送新闻列表]
```

### 指定网站

```
你：看看 BBC 今天有什么新闻
我：[获取 BBC 首页新闻]
```

### 深入了解

```
你：详细了解第一条
我：[尝试获取全文]
```

---

## 支持的网站

| 类别 | 网站 |
|------|------|
| 国际 | BBC、Reuters、AP、Al Jazeera |
| 国内 | 人民网、新华网、澎湃新闻 |
| 财经 | Bloomberg、财联社、华尔街见闻 |
| 科技 | 36氪、The Verge、虎嗅 |

---

## 注意事项

- ✅ 优先使用免费公开信源（BBC、Reuters、AP）
- ✅ 无法获取时提供替代信源
- ⚠️ 仅供个人学习研究使用

---

## License

MIT

---

_版本: 1.0.0 | 更新: 2026-03-10_
