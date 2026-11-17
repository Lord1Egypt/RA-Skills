---
name: framework-overview
title: 方法总体框架
type: pipeline
journal: nature
width: double
font_size_pt: 7
palette: okabe-ito
---

# 图注
图 1  方法总体框架。(a) 双通道输入编码后做跨模态融合，并用一致性约束对齐；(b) 下游任务头输出预测并评估。

## 面板
- a | 输入编码与融合
- b | 下游任务

## 节点
- n1 | 文本编码 | BERT-base | a | rounded
- n2 | 图像编码 | ViT-B/16 | a | rounded
- n3 | 跨模态融合 | cross-attention ×6 | a | rounded
- n4 | 一致性约束 | InfoNCE | a | note
- n5 | 分类头 | linear | b | rounded
- n6 | 预测输出 | top-1 / top-5 | b | rounded
- n7 | 评估指标 | Acc / F1 | b | box

## 边
- n1 -> n3
- n2 -> n3
- n3 -> n4 : 对齐 | dashed
- n4 -> n5 : 特征
- n5 -> n6
- n6 -> n7

## 布局
- direction: left-right
- gap_mm: 6
- node_w_mm: 40
- node_h_mm: 13
