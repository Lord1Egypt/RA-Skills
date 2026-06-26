# Anki 卡片领域示例

各领域的高质量 Anki 卡片示例，遵循原子化原则和 simple-anki-sync 格式。

## 目录

- [Anki 卡片领域示例](#anki-卡片领域示例)
  - [目录](#目录)
  - [历史学习](#历史学习)
  - [编程概念](#编程概念)
  - [语言学习](#语言学习)
  - [学术概念](#学术概念)
  - [复杂主题处理](#复杂主题处理)
    - [信息丛林法（4步法）](#信息丛林法4步法)
    - [量子力学示例](#量子力学示例)
  - [错误示例与纠正](#错误示例与纠正)
    - [错误1：太冗长](#错误1太冗长)
    - [错误2：关键信息在问题中](#错误2关键信息在问题中)
  - [高级技巧](#高级技巧)
    - [渐进式白空间](#渐进式白空间)
    - [可逆卡片设计](#可逆卡片设计)
    - [冗余设计](#冗余设计)
    - ["把手"系统](#把手系统)
  - [标签命名规范](#标签命名规范)

## 历史学习

```markdown
#anki/history/ancient_china

| 唐朝建立时间 |
| ---------- |
| 618年，李渊建立<br><br><small>💡 李世民玄武门之变后成为实际创建者</small> |

| 贞观之治皇帝 |
| ----------- |
| 唐太宗李世民（626-649年在位）<br><br><small>💡 被尊称"天可汗"</small> |

| 唐朝疆域特点 |
| ---------- |
| 东至朝鲜，西达中亚，北抵蒙古，南到越南<br><br><small>📝 1237万km²，历史第二大</small> |
```

## 编程概念

```markdown
#anki/programming/python

| Python列表推导式语法 |
| ------------------- |
| [expression for item in iterable if condition]<br><br><small>⚡ 比for循环快35%</small> |

| Python函数定义关键字 |
| ------------------ |
| def function_name(parameters):<br><br><small>💡 def是define的缩写</small> |

| Python创造者 |
| ----------- |
| Guido van Rossum（1991年发布）<br><br><small>💡 绰号"仁慈的独裁者"</small> |
```

## 语言学习

```markdown
#anki/language/english

| algorithm 发音 |
| ------------- |
| /ˈælɡərɪðəm/ 算-格-瑞-泽姆<br><br><small>⚡ 重音在第一音节</small> |

| 算法的英文单词 |
| ------------ |
| algorithm (n.)<br><br><small>🔗 algorithmic (adj.)</small> |

| algorithm 词源 |
| -------------- |
| 来自9世纪波斯数学家 Al-Khwarizmi<br><br><small>💡 拉丁语转写为Algoritmi</small> |
```

## 学术概念

```markdown
#anki/psychology/cognitive

| 短期记忆容量 |
| ---------- |
| 7±2个组块（Miller, 1956）<br><br><small>💡 电话号码因此设计为7位</small> |

| 神奇数字7提出者 |
| ------------- |
| George Miller（认知心理学家）<br><br><small>📝 心理学最高引用文献之一</small> |

| 工作记忆三大系统 |
| -------------- |
| 中央执行系统、语音环路、视觉空间画板<br><br><small>🔗 2000年增加情景缓冲器</small> |
```

## 复杂主题处理

### 信息丛林法（4步法）

1. **创建树状结构**：主题→分支→子分支
2. **制作上下级卡片**：父子关系卡片
3. **添加横向链接**：交叉引用和替代分类
4. **制作语境卡片**：从子到父的连接

### 量子力学示例

```markdown
#anki/physics/quantum_mechanics

| 量子力学三大基本原理 |
| ------------------ |
| 波粒二象性、不确定性原理、量子叠加<br><br><small>💡 彻底改变物质世界认知</small> |

| 海森堡不确定性原理内容 |
| -------------------- |
| 位置和动量不能同时被精确测量<br><br><small>📝 ΔxΔp ≥ ℏ/2</small> |

| 不确定性原理提出者 |
| ---------------- |
| Werner Heisenberg（1927年）<br><br><small>💡 31岁获诺贝尔奖</small> |

| 量子叠加态定义 |
| ------------- |
| 粒子可同时处于多个状态的线性组合<br><br><small>🔗 薛定谔的猫思想实验</small> |
```

## 错误示例与纠正

### 错误1：太冗长

❌ **错误**：

```markdown
| 第二次世界大战中德国入侵波兰的具体日期以及这一事件对欧洲战争格局的影响？ |
| ---------------------------------------------------------------- |
| 1939年9月1日，标志着二战欧洲战场正式开始，英法随即对德宣战 |
```

✅ **正确**：

```markdown
| 二战爆发日期 |
| ---------- |
| 1939年9月1日（德国入侵波兰）<br><br><small>💡 凌晨4:45分开始炮击</small> |

| 德国入侵波兰的后果 |
| ---------------- |
| 英法对德宣战，二战全面爆发<br><br><small>📝 9月3日正式宣战</small> |

| 二战欧洲战场开端事件 |
| ----------------- |
| 德国闪击波兰（1939.9.1）<br><br><small>⚡ 5周内波兰沦陷</small> |
```

### 错误2：关键信息在问题中

❌ **错误**：

```markdown
| 1950年德国农业劳动力占总劳动力的百分比是多少？ |
| ---------------------------------------- |
| 24% |
```

✅ **正确**：

```markdown
| 德国农业劳动力历史数据 |
| -------------------- |
| 1950年：24%的劳动力从事农业<br><br><small>📝 2020年仅1.3%</small> |
```

## 高级技巧

### 渐进式白空间

对于3要点卡片，使用 `<br>` 标签分行：

```markdown
| X的三个特征 |
| ---------- |
| 特征1<br><br>特征2<br><br>特征3 |
```

### 可逆卡片设计

当语义合理时，创建反向卡片：

```markdown
| 1969年历史事件 |
| ------------- |
| 阿波罗11号登月 |

| who 首次登月 |
| ----------- |
| 阿波罗11号, 1969年 |
```

### 冗余设计

为重要概念创建多个角度的卡片：

```markdown
| DNA结构发现者 |
| ------------ |
| Watson和Crick |

| 1953年生物学突破 |
| --------------- |
| DNA双螺旋结构发现 |

| 诺贝尔奖DNA研究 |
| -------------- |
| Watson, Crick, Wilkins (1962) |
```

### "把手"系统

用 `>` 符号引用其他相关卡片：

```markdown
| 牛顿贡献 |
| ------- |
| >运动定律 >万有引力 >微积分发展 |
```

## 标签命名规范

使用全英文标签 `#anki/[domain]/[topic]`：

| 领域 | 标签 | 子分类示例 |
|------|------|-----------|
| 历史 | history | ancient_china, world_war, modern_history |
| 编程 | programming | python, javascript, algorithms |
| 语言 | language | english, spanish, grammar |
| 科学 | science | physics, chemistry, biology |
| 数学 | mathematics | calculus, algebra, statistics |
| 心理学 | psychology | cognitive, behavioral, clinical |
| 经济 | economics | macro, micro, finance |
| 哲学 | philosophy | ethics, logic, metaphysics |
| 医学 | medicine | anatomy, pathology, pharmacology |
| 艺术 | art | painting, music_theory, architecture |
