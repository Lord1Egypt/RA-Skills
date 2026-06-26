---
name: pans-tech-profile
description: |
  分析目标公司的技术栈和算力需求，为 AI 算力销售提供客户画像。
  自动采集公司官网、招聘页面、GitHub、新闻等数据源，输出技术栈分析、
  GPU 需求量级估算、推理/训练比例及销售切入建议。
  触发词：技术栈分析、公司技术画像、tech profile、算力需求评估、客户技术调研
---

# pans-tech-profile

## 概述
分析目标公司的技术栈和算力需求，为 AI 算力销售提供客户画像。

## 触发词
技术栈分析、公司技术画像、tech profile、算力需求评估、客户技术调研

## 使用方法

### 基本用法
```bash
python3 scripts/profile.py --company "OpenAI"
python3 scripts/profile.py --domain openai.com
```

### 指定输出格式
```bash
python3 scripts/profile.py --company "字节跳动" --format json
python3 scripts/profile.py --company "Anthropic" --format markdown
```

### 深度分析
```bash
python3 scripts/profile.py --company "Midjourney" --deep
```

## 参数

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `--company` | 公司名称 | 二选一 | - |
| `--domain` | 公司域名 | 二选一 | - |
| `--format` | 输出格式：text/json/markdown | 否 | text |
| `--deep` | 深度分析（更多数据源） | 否 | false |
| `--output` | 输出到文件 | 否 | stdout |

## 输出内容

1. **公司基本信息** — 名称、域名、行业
2. **技术栈分析** — 编程语言、框架、云服务、ML/DL 工具链
3. **算力需求评估** — GPU 需求量级、推理/训练比例、预估月成本
4. **信号来源** — 官网、招聘信息、GitHub、新闻报道
5. **销售建议** — 优先级评级、切入角度

## 数据来源

- 公司官网 meta / tech stack 检测
- 招聘页面（技术岗位关键词）
- GitHub organization（语言分布、star 项目）
- BuiltWith / Wappalyzer 线索
- 公开新闻与融资信息

## 依赖

- Python 3.10+
- requests
- beautifulsoup4

首次运行自动安装依赖。
