---
name: homemade-machine-learning-skill
description: "Machine learning skill: find, explain, and implement ML algorithms with interactive Jupyter Notebook links. Covers linear regression, logistic regression, neural network, K-Means clustering, anomaly detection — with math, Python code, and skill demos."
version: "1.0.0"
author: "BytesAgain"
homepage: "https://bytesagain.com/skill/homemade-machine-learning-skill"
tags: ["machine learning", "jupyter notebook", "python", "data science", "education", "linear regression", "neural network", "skill"]
---

# Homemade Machine Learning Skill

Machine learning skill: learn, explain, and implement ML algorithms from scratch.
Based on [trekhleb/homemade-machine-learning](https://github.com/trekhleb/homemade-machine-learning) (MIT, 22k+ ⭐)

> 📦 Install: `clawhub install homemade-machine-learning-skill`

5 algorithms · 11 interactive notebooks · math explained · Python code included

## Commands

### explain — 解释算法原理 + 数学 + 代码
```bash
bash scripts/ml-notebook-finder.sh explain "linear regression"
bash scripts/ml-notebook-finder.sh explain "neural network"
bash scripts/ml-notebook-finder.sh explain "kmeans"
```

### notebook — 获取交互式 Jupyter Notebook 链接
```bash
bash scripts/ml-notebook-finder.sh notebook "logistic regression"
bash scripts/ml-notebook-finder.sh notebook "anomaly detection"
```

### code — 获取 Python 实现代码片段
```bash
bash scripts/ml-notebook-finder.sh code "linear regression"
bash scripts/ml-notebook-finder.sh code "kmeans"
```

### path — 生成学习路径（按难度排序）
```bash
bash scripts/ml-notebook-finder.sh path beginner
bash scripts/ml-notebook-finder.sh path intermediate
bash scripts/ml-notebook-finder.sh path advanced
```

### list — 列出所有算法
```bash
bash scripts/ml-notebook-finder.sh list
```

## Algorithms

| Algorithm | Type | Notebooks | Use Case |
|-----------|------|-----------|----------|
| linear regression | supervised | 3 | price prediction, forecasting |
| logistic regression | supervised | 4 | classification, MNIST |
| neural network (MLP) | supervised | 2 | image recognition, deep learning |
| k-means | unsupervised | 1 | clustering, segmentation |
| anomaly detection | unsupervised | 1 | fraud detection, monitoring |

## Source
MIT License — Original author: [trekhleb](https://github.com/trekhleb/homemade-machine-learning)
Indexed by [BytesAgain](https://bytesagain.com) — AI skill discovery platform
