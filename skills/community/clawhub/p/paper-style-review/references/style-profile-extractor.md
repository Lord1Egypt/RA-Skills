# style-profile extractor

## 目标

从 refs 中建立**可供 target 风格验证直接消费**的唯一风格画像，输出：

- `style-profile.json`
- `ref-style-basis.md`

该模块只负责**从 refs 归纳 paragraphType 对应的风格机制**，不对 target 做诊断，也不直接改写。

当前正式策略：
- 先对每篇 ref 跑统一的 `paper_structure_anchor.py`
- 从结构图谱里拿到严格的 physical anchor + paragraphType
- 再按 `paragraphType` 聚类，用 LLM 做风格机制提取
- 最终保存完整 `style-profile.json`
- target 阶段只读 `style-profile.json`，不再回读 refs 原文

---

## 当前输入事实源

- 不直接从裸 `refs[].text` 学风格。
- 正式输入是每篇 ref 的结构图谱输出。
- paragraphType 是学习主键，不是 chapter number，也不是旧的 segmentType。
- 同一个 physical paragraph 只能进入一个 paragraphType。

---

## 提炼维度

### 1. 段落职责
- 这个 paragraphType 通常承担什么写作任务
- 在章节展开里通常处于什么位置
- 常见前后邻接关系是什么

### 2. 结构推进
- 如何起句
- 如何展开
- 如何转折/连接
- 如何收束

### 3. 语言机制
- 表达密度
- 句式节奏
- 语气措辞
- 抽象层级
- 论据锚定
- 视角位置

### 4. 可复用规则
- 常见公式
- 可执行写法规则
- 高辨识度特征

### 5. 风格偏离依据
- refs 中明显少见的模板化表达
- refs 常见而 target 易缺失的“条件限定 + 对象锚点 + 结果约束”写法
- 应避免模仿的空泛总结句、过匀段落、套话连接词

---

## 输出结构

标准输出文件：
- `style-profile.json`
- `ref-style-basis.md`

其中：
- `style-profile.json` 是机器消费主文件
- `ref-style-basis.md` 是人类可读摘要

`style-profile.json` 的关键结构：

```json
{
  "meta": {},
  "paragraphTypeProfiles": {
    "<paragraphType>": {
      "paragraphType": "<paragraphType>",
      "analysis": {
        "oneLine": "...",
        "mechanisms": {},
        "formula": "...",
        "rules": [],
        "signatureTraits": []
      },
      "context": {}
    }
  },
  "basisIndex": []
}
```

下游运行时不会直接把整份画像原样喂给 LLM，而是：
- 保留磁盘上的完整 `style-profile.json`
- 在 target 审查阶段，按当前 batch 的 paragraphType 动态切出 compact slice
- 只把必要的 oneLine / formula / top mechanisms / rules / signature traits / minimal context 送给 fused LLM

---

## 下游接口要求

后续所有重要判断必须能回指：
- `paragraphType`
- `basisIndex`
- `claim`
- `basisId`

如果 refs 内部不一致，必须输出“样本冲突”，不得擅自定唯一风格。

---

## 明确禁止

- 不要再输出旧的 `segmentType` 画像。
- 不要让 target 风格验证阶段再回读 refs 原文。
- 不要在 target 阶段临时再做一版本地风格投影。
- 不要在 style-profile 之外再造第二份并行风格知识库。
