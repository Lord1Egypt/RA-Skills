# Mem0 Tech Tree Memory System v5

科技树架构：知识节点有依赖关系、解锁路径、协同加成

## 核心概念

| 概念 | 说明 |
|------|------|
| 🌳 节点 (Node) | 一条知识/技能/经验，有唯一ID |
| 🔗 边 (Edge) | 节点间关系：dependency(前置依赖)、synergy(协同加成)、related(关联) |
| 🌿 分支 (Branch) | 领域方向：技术/内容创作/学习/工作/生活 |
| 📊 层级 (Tier) | T1(了解)→T5(创新)，自动检测 |
| 🎯 状态 (State) | ⬜new → 🔘available → ✅unlocked → ⭐mastered |

## 科技树如何工作

```
⬜ T1 [n0001] 了解Python基础语法
⬜ T2 [n0003] 熟悉playwright浏览器自动化
│  ⬜ T4 [n0005] 精通即梦AI自动化流程
⬜ T2 [n0006] 配置ffmpeg合成视频和音频
```

- n0003(n0005的前置): 不会playwright就不可能做即梦自动化
- T1→T4: 从入门到精通的进阶路径
- 跨分支节点自动发现协同关系

## 用法

```bash
# 存储（自动检测分支、层级、类型）
python3 mem0_skill.py store "精通ComfyUI部署和模型训练"

# 检索（目录定位→范围搜索+依赖路径）
python3 mem0_skill.py retrieve "自动化发布视频"

# 查看科技树地图
python3 mem0_skill.py tree              # 全局
python3 mem0_skill.py tree 技术         # 指定分支

# 查看节点详情（依赖+解锁+协同）
python3 mem0_skill.py info n0005

# 查目录（O(1)关键词查找）
python3 mem0_skill.py catalog CDP

# 概览
python3 mem0_skill.py list

# 清除
python3 mem0_skill.py clear
```

## 检索流程

```
查询 → 查目录(关键词O(1)) → 定位节点 → 范围内评分 → 返回知识+依赖路径+协同
```

## AI优势

- **自动依赖发现**: "学会playwright"自动成为"精通即梦自动化"的前置
- **自动层级检测**: "了解/学会/掌握/精通/创新" → T1-T5
- **协同加成**: 技术+内容创作交叉节点自动标记synergy
- **进度系统**: new→available→unlocked→mastered，高频访问节点自动升级
- **完美回忆**: 原始内容不篡改，每次检索强化但不修改
