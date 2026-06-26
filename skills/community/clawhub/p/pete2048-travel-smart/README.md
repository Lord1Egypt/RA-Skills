# TravelSmart - 智能出行决策助手

> 自驾途中的「第二大脑」——不只告诉你哪里近，而是告诉你**综合最优的决策点在哪里、为什么**。

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✨ 核心功能

| 场景 | 说明 |
|------|------|
| 🚗 **高速出口推荐** | 堵车时，推荐哪个出口下去「有好吃的 + 绕行不远 + 值得停」 |
| 🏨 **途中住宿推荐** | 临时找地方住，综合考虑「停车场 + 价格 + 次日行程顺路」 |
| 🚕 **景点打车点推荐** | 景点太堵，告诉你该在哪里停车打车最省事 |

**一句话定位**：TravelSmart 是「自带决策能力的地图」——把距离、评分、绕行代价放在一起给你打分推荐。

## 🎯 解决的问题

> 开车出去玩，高速上发现前面堵死了，心想不如先下高速找个地方吃饭。结果随便选了个出口下去，离出口 10km 才有镇子，绕了一大圈还找不到好吃的。

导航只给你路线，不给你决策建议。TravelSmart 把「**导航的距离**」+「**点评的评分**」+「**绕行代价**」放在一起，给你一个综合最优解。

## 🛠 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置高德 Key

```bash
cp .env.example .env
# 编辑 .env，填入 AMAP_KEY
```

> 高德地图 Key 免费申请：[https://lbs.amap.com/](https://lbs.amap.com/)

### 3. 运行

```bash
python src/main.py --scene highway --highway G4 --lng 116.397 --lat 39.909 --destination 北京
```

### 4. 打开演示页面

```bash
python server.py
# 访问 http://localhost:5188
```

## 📁 项目结构

```
travel-smart/
├── src/
│   ├── main.py              # CLI 入口
│   ├── agents/              # Agent（路由、格式化）
│   ├── clients/             # 高德 API 客户端
│   ├── config/             # 配置（Key 从环境变量读取）
│   ├── scenes/             # 三大场景实现
│   └── scoring/            # 多因子评分引擎
├── server.py               # Flask API 服务（含演示页面）
├── demo.html               # 演示页面 HTML
├── .env.example            # 环境变量示例
└── requirements.txt
```

## 📊 评分算法

各场景采用多因子加权评分：

| 场景 | 距离 | 评分 | 绕行 | 价格 | 次日顺路 |
|------|:----:|:----:|:----:|:----:|:--------:|
| 高速出口 | 35% | 35% | 30% | — | — |
| 途中住宿 | 20% | 20% | — | 30% | 30% |
| 打车点 | 40% | 20% | 30% | 10% | — |

## 🔑 API Key 申请

| 服务 | 申请地址 | 费用 |
|------|---------|------|
| 高德地图 Web API | https://lbs.amap.com/ | 免费（5000次/日） |
| MiniMax LLM（可选） | https://platform.minimaxi.com | Max-极速版 ¥199/月 |

## 🤝 开源协议

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
