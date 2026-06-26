# Process Flow Navigator - 业务流程导航助手

🧭 帮助你在复杂的多分支流程中导航、规划路径、查询技能编码

<p align="center">
  <strong>⚡ Powered by Instant</strong>
</p>

---

## 📦 安装

```bash
clawhub install process-flow-navigator
```

或手动安装：

```bash
git clone <repo-url>
cd process-flow-navigator
```

---

## 🚀 快速开始

### CLI 使用

```bash
# 查看帮助
./scripts/navigate.sh help

# 查询下一步
./scripts/navigate.sh next B

# 查询技能编码
./scripts/navigate.sh code C

# 列出所有节点
./scripts/navigate.sh list

# 查看分支结构
./scripts/navigate.sh tree C
```

### AI 助手对话

直接向 AI 助手提问：

```
- 我在流程 B，下一步怎么走？
- 从流程 B 到结束，有几种路线？
- 流程 C 的技能编码是什么？
- 显示 C 分支的完整流程
```

---

## 📊 支持的流程节点

### 主流程
```
A → B → C → D → E → F → G → H → I → J → K → 收尾
```

### 子流程节点
- **A 分支**: A-1
- **B 分支**: B-1, B-2
- **C 分支**: C-1, C-2, C-3, C-4, C-5
- **D 分支**: D-1

### 判断节点
判断 2, 判断 3, 判断 4, 判断 5, 判断 6, 判断 7, 判断 8, 判断 9, 最终判断

### 终点
- **结束** - 正常终止
- **售后** - 异常处理

---

## 🏷️ 技能编码规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 校验技能 | `PROC-X-CHECK-XXX` | PROC-A-CHECK-001 |
| 执行技能 | `PROC-X-EXEC-XXX` | PROC-A-EXEC-001 |
| 判定技能 | `PROC-X-Y-JUDGE-XXX` | PROC-A-B-JUDGE-001 |

完整编码表见 `SKILL.md`

---

## 🗺️ 流程规则

### 核心枢纽：最终判断
- **[是]** → 结束
- **[否]** → 继续流转（根据来源节点决定去向）

### 常见路径示例

**从 B 到结束（最短路径）**
```
B → 判断 2 [否] → B-1 → B-2 → 最终判断 [是] → 结束
```

**从 C 到结束（通过 C-1）**
```
C → 判断 3 [是] → C-1 → 最终判断 [是] → 结束
```

**从 C 到结束（通过 C-4）**
```
C → 判断 3 [否] → C-3 → C-4 → 最终判断 [是] → 结束
```

---

## 📁 文件结构

```
process-flow-navigator/
├── SKILL.md              # 技能元数据
├── README.md             # 使用说明
├── scripts/
│   └── navigate.sh       # CLI 导航工具
├── data/
│   └── flow-rules.json   # 流程规则数据
└── assets/               # (可选) 流程图图片
```

---

## 🔄 更新日志

### v1.0.0 (2026-03-11)
- ✨ 初始版本
- 🧭 完整的 A-K 流程导航
- 🏷️ 技能编码查询
- 📊 分支结构可视化

---

## 📝 许可证

MIT License

---

## 🏢 公司信息

**Instant** © 2026 - 保留所有权利

---

## 🙏 致谢

本 skill 基于用户提供的业务流程图创建。
