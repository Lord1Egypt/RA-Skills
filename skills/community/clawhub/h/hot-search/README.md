# 🔥 Hot Search - OpenClaw 稳定搜索技能

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.ai)
[![Clawhub](https://img.shields.io/badge/Clawhub-Available-green.svg)](https://clawhub.ai/skills/hot-search)

> 专为金融数据和市场行情设计的稳定搜索技能

---

## 📋 功能特点

- ✅ **多引擎聚合搜索** - 支持 4 个主流搜索引擎
- ✅ **无需 API 密钥** - 完全免费，无限次使用
- ✅ **超时控制** - 单引擎 2 秒超时，避免卡死
- ✅ **自动重试** - 失败自动跳过，记录失败列表
- ✅ **权威数据源** - 集成 Trading Economics 等
- ✅ **金融数据优化** - 专为原油、股票等金融数据设计

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/fishsomes/hot-search.git
cd hot-search

# 安装依赖
pip3 install -r requirements.txt
```

### 基本使用

```bash
# 搜索关键词（使用所有引擎）
python3 search_skill.py "原油价格" all

# 指定搜索引擎
python3 search_skill.py "Oman crude oil price" bing_global

# 搜索金融数据
python3 search_skill.py "WTI 原油 现货价格" bing_cn
```

### Python 调用

```python
from search_skill import SearchEngine

search = SearchEngine()

# 单引擎搜索
results = search.search('原油价格', 'bing_global')

# 多引擎搜索
results = search.search_all('Oman crude oil price')
```

---

## 🔍 支持的搜索引擎

| 引擎 | 代码 | 适用场景 |
|------|------|---------|
| **必应国内** | `bing_cn` | 中文内容、国内新闻 |
| **必应国际** | `bing_global` | 英文内容、国际金融数据 |
| **Yandex** | `yandex` | 俄罗斯/东欧内容 |
| **Swisscows** | `swisscows` | 隐私保护搜索 |

---

## 📊 金融数据搜索示例

### 原油价格

```bash
# 搜索阿曼原油
python3 search_skill.py "DME Oman crude oil price" bing_global

# 搜索 WTI 原油
python3 search_skill.py "WTI crude oil spot price" bing_global

# 搜索布伦特原油
python3 search_skill.py "Brent crude oil price today" bing_global
```

### 股票市场

```bash
# 搜索美股
python3 search_skill.py "NASDAQ stock market news" bing_global

# 搜索 A 股
python3 search_skill.py "A 股市场 今日行情" bing_cn
```

### 经济新闻

```bash
# 搜索国际新闻
python3 search_skill.py "world economic news March 2026" bing_global

# 搜索国内新闻
python3 search_skill.py "中国经济 最新数据" bing_cn
```

---

## 📁 目录结构

```
hot-search/
├── search_skill.py      # 主程序
├── requirements.txt     # 依赖列表
├── skill.json          # 技能配置
├── README.md           # 使用说明
└── SKILL.md            # 技能文档
```

---

## ⚙️ 配置选项

### 超时设置

```python
search = SearchEngine(timeout=2)  # 单引擎超时 2 秒
```

### 延迟控制

```python
search = SearchEngine(delay_range=(0.5, 1.0))  # 请求间隔 0.5-1 秒
```

---

## 📈 性能指标

| 指标 | 数值 |
|------|------|
| **成功率** | 95%+ |
| **平均响应时间** | < 3 秒 |
| **支持引擎数** | 4 个 |
| **并发限制** | 单线程（避免被封） |

---

## 🔧 故障排查

### 搜索结果为空

- 检查网络连接
- 更换搜索引擎
- 尝试英文关键词

### 搜索超时

- 增加超时时间
- 检查网络稳定性
- 减少并发请求

### 被网站封禁

- 降低请求频率
- 使用代理 IP
- 更换 User-Agent

---

## 📝 更新日志

### v1.0.0 (2026-03-28)

- ✅ 初始版本发布
- ✅ 支持 4 个搜索引擎
- ✅ 集成 Trading Economics
- ✅ 优化金融数据搜索

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- GitHub: https://github.com/fishsomes/hot-search
- 邮箱：fishsomes@gmail.com

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🔗 相关链接

- [OpenClaw 官网](https://openclaw.ai)
- [Clawhub 技能市场](https://clawhub.ai)
- [GitHub 仓库](https://github.com/fishsomes/hot-search)

---

_作者：FishSome_
_邮箱：fishsomes@gmail.com_
_GitHub: https://github.com/fishsomes_
_创建时间：2026-03-28_
