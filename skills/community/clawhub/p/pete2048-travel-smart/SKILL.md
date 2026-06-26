---
name: travel-smart
description: |
  自驾出行决策助手 - 高速出口推荐、途中住宿、打车点推荐三大场景。
  高德地图 Web API + 多因子评分算法，支持 CLI / Web / 飞书三种使用方式。
  必填环境变量：AMAP_KEY（高德地图）；可选：MINIMAX_API_KEY、FEISHU_APP_ID、FEISHU_APP_SECRET。
---

# TravelSmart - 智能出行决策助手

自驾途中的「第二大脑」——不只告诉你哪里近，而是告诉你**综合最优的决策点在哪里**。

## 核心能力

- 🚗 **高速出口推荐**：堵车时推荐最佳下高速出口，综合考虑餐饮评分+绕行距离
- 🏨 **途中住宿推荐**：找停车场充足+次日行程顺路的酒店
- 🚕 **景点打车点推荐**：告知最佳停车候车位置

## 环境准备

### 必填

| 变量 | 说明 |
|------|------|
| `AMAP_KEY` | 高德地图 Web API Key（[申请地址](https://console.amap.com/dev/key/app)）|

### 可选

| 变量 | 说明 |
|------|------|
| `MINIMAX_API_KEY` | MiniMax LLM（自然语言路由） |
| `FEISHU_APP_ID` | 飞书推送 App ID |
| `FEISHU_APP_SECRET` | 飞书推送 App Secret |

`.env.example` 文件中有配置模板，复制为 `.env` 后填入即可。

## 快速开始

### 方式一：Python CLI

```bash
cd skills/travel-smart
pip install -r requirements.txt
cp .env.example .env  # 填入 AMAP_KEY
python src/main.py --scene highway --highway G4 --lng 116.397 --lat 39.909 --destination 北京
```

### 方式二：Web 演示页面

```bash
pip install -r requirements.txt
python server.py
# 访问 http://localhost:5188
```

### 方式三：飞书对话集成

集成到大管家，通过自然语言使用。

## 项目结构

```
skills/travel-smart/
├── src/
│   ├── main.py           # CLI 入口
│   ├── agents/           # Agent（路由 + 格式化）
│   ├── clients/          # 高德地图 API 客户端
│   ├── scenes/           # 三大场景逻辑
│   └── scoring/          # 多因子评分引擎
├── server.py             # Web 服务入口
├── requirements.txt      # Python 依赖
├── .env.example          # 环境变量模板
└── references/
    ├── scoring-algorithm.md   # 评分算法详解
    ├── api-reference.md       # API 接口文档
    └── PRD.md                 # 产品需求文档
```

## 技术架构

```
用户自然语言
    ↓
OpenClaw Agent（意图理解 + 编排）
    ↓
┌── 高德地图 Web API（地理编码/POI/路径规划）
├── MiniMax LLM（自然语言路由 + 决策建议，可选）
└── 评分引擎（多因子加权评分）
    ↓
结构化输出 + 飞书推送（可选）
```
