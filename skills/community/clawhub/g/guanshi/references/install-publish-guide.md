# 安装/发布流程 + 关键陷阱

## 安装

### 用户侧安装
```bash
clawhub install guanshi
```

### 专家集群安装
```bash
# 必需专家（自动安装）
clawhub install guanshi-strategy-expert
clawhub install guanshi-industry-expert
clawhub install guanshi-competition-expert
clawhub install guanshi-org-expert

# 可选专家（按需安装）
clawhub install guanshi-finance-expert
clawhub install guanshi-market-expert
clawhub install guanshi-intelligence-expert
clawhub install guanshi-data-expert
```

### 离线自举
网络不可用时，运行：
```bash
python3 ~/.hermes/skills/market/guanshi/scripts/guanshi-init.py --yes
```
自动创建 8 个专家的本地自举版本。

---

## 发布

### 发布前检查清单

- [ ] SKILL.md ≤ 12KB（约 350 行）
- [ ] SKILL.md frontmatter `version` 更新
- [ ] `.clawhubignore` 已配置（排除 `scripts/__pycache__/`）
- [ ] 所有 references 文件路径引用正确
- [ ] 专家集群的 `min_version` 与 ClawHub 最新一致

### 发布命令
```bash
cd ~/.hermes/skills/market/guanshi
clawhub publish --version 1.0.0
```

---

## 五大陷阱

### 陷阱 1：SKILL.md 超 8192 tokens
ClawHub embedding 限制 8192 tokens，SKILL.md 超过会导致发布失败。
**解法**：提取详细内容到 references/，主文件只保留路由表。`.clawhubignore` 排除 `scripts/` 和大 references。

### 陷阱 2：ZIP 嵌套目录
ClawHub 下载的 ZIP 自带同名子目录（`guanshi/guanshi/SKILL.md`），直接解压造成嵌套。
**解法**：guanshi-init.py 内置解压后自动提升一层逻辑。

### 陷阱 3：.clawhubignore 误排除脚本
`scripts/` 不能全排除——guanshi-init.py 必须在包里。
**正确做法**：只排除 `scripts/__pycache__/`。

### 陷阱 4：版本不一致
publish --version 必须与 SKILL.md frontmatter version 一致。
不一致 → ClawHub latest tag 正确但 install 拉到旧版本。

### 陷阱 5：新陈代谢膨胀
持续优化必须一换一。任何新增内容必须替换一个现有内容，否则 Skill 膨胀到无法加载。
- L1 核心路由（SKILL.md）：≤ 300 行
- L2 方法论（references/）：≤ 2000 行总计
- L3 知识库（~/.hermes/strategy-knowledge/）：无限制

---

## 目录结构

```
skills/market/guanshi/
├── SKILL.md                          # 主入口（≤12KB）
├── references/
│   ├── six-steps.md                  # 六步洞察法
│   ├── core-principles.md            # 核心原则
│   ├── strategy-frameworks.md        # 战略框架库
│   ├── scenario-routing.md           # 场景路由
│   ├── expert-registry.md            # 专家注册表
│   ├── audit-checklist.md            # 宪法审计清单
│   ├── output-spec.md                # 输出规范
│   ├── ppt-bridge-protocol.md        # PPT 桥接
│   ├── auto-init-protocol.md         # 初始化协议
│   ├── supplementary.md              # 补充说明+坑点
│   └── install-publish-guide.md      # 本文件
└── scripts/
    ├── guanshi-init.py               # 初始化脚本
    └── __pycache__/                  # (gitignore)
```