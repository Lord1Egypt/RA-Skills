# OpenClaw 记忆插件生态对比

## 作者推荐插件

OpenClaw 作者 Peter Steinberger 推荐：

| 插件 | 解决问题 | 定位 |
|------|---------|------|
| **qmd** | 搜不到 | 换掉原生搜索引擎 |
| **lossless-claw (LCM)** | 压掉丢失 | 无损上下文保留 |

---

## 7 大记忆插件对比

| 插件 | 定位 | 存储方式 | 费用 | 难度 | 核心功能 |
|------|------|---------|------|------|---------|
| **qmd** | 搜索增强 | 本地向量 | 免费 | 低 | 三重检索机制 |
| **lossless-claw** | 无损压缩 | 本地存储 | 免费 | 低 | 永不丢失对话 |
| **memory-lancedb-pro** | 全面增强 | LanceDB | 免费 | 中 | 智能提取+去重 |
| **MemOS Cloud** | 团队共享 | 云端 | 付费 | 低 | Token 降 72% |
| **Total Recall** | 记忆整理 | 多种 | 免费 | 中 | 自动分类整理 |
| **Mem0** | 外部记忆 | 云端 | 付费 | 低 | 托管式记忆 |
| **Cognee** | 知识图谱 | 图数据库 | 免费 | 高 | 知识关联 |

---

## 插件详解

### 1. qmd - 搜索增强

**解决的问题**：原生 SQLite 搜索无语义理解

**核心功能**：
- BM25 关键词检索
- 向量语义检索
- Cross-encoder 重排序

**安装**：
```bash
clawhub install qmd
```

**适用场景**：记忆量大，搜索效率低

---

### 2. lossless-claw (LCM) - 无损压缩

**解决的问题**：Compaction 后丢失关键约束

**核心功能**：
- 完整保留所有对话历史
- 按需检索而非压缩丢弃
- 长任务不再失忆

**安装**：
```bash
clawhub install lossless-claw
```

**适用场景**：长任务、复杂项目

---

### 3. memory-lancedb-pro - 全面增强

**GitHub**: `CortexReach/memory-lancedb-pro` (2.4K+ Star)

**核心功能**：
- 向量 + BM25 混合检索
- Cross-encoder 重排序
- 多 Scope 隔离
- 智能提取（自动筛选重要内容）
- 去重检测
- 噪声拦截

**安装**：参考 GitHub 文档

**适用场景**：对记忆质量要求高

---

### 4. MemOS Cloud - 团队共享

**解决的问题**：多 Agent 协作，重复传递信息

**核心功能**：
- 跨实例共享记忆
- 按需检索，Token 降 72%
- 团队协作场景优化

**适用场景**：多 Agent 团队、企业级部署

---

## 推荐组合

### 个人用户（免费方案）

```
qmd + lossless-claw
```
- 搜得到 + 压不掉
- 完全免费
- 安装简单

### 高级用户（功能完善）

```
memory-lancedb-pro
```
- 一站式解决方案
- 智能提取
- 噪声拦截

### 团队协作（付费方案）

```
MemOS Cloud
```
- 跨实例共享
- Token 大幅降低
- 企业级支持

---

## 插件选择指南

| 需求 | 推荐插件 |
|------|---------|
| 搜索不够准确 | qmd |
| 长任务失忆 | lossless-claw |
| 记忆杂乱无章 | Total Recall |
| 团队多 Agent | MemOS Cloud |
| 一站式解决 | memory-lancedb-pro |