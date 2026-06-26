# HexaLotto 发布到 ClawHub 指南

## 前置条件

1. 安装 ClawHub CLI: `npm i -g clawhub`
2. 登录（需 GitHub 账号，注册满一周）: `clawhub login`

## 一键发布

```bash
# 解压 skill 包（如果还没解压）
# unzip hexalotto.skill -d hexalotto

# 发布到 ClawHub
clawhub publish ./hexalotto \
  --slug hexalotto \
  --name "HexaLotto 六爻奇门测彩" \
  --version 2.0.0 \
  --changelog "V2.0: 支持双色球/大乐透/六合彩三彩种，同时推算主号+特殊球，web_search+web_fetch自动获取号码，回头生克检测，病药应期7条规则" \
  --tags latest
```

## 发布后验证

```bash
# 搜索确认
clawhub search hexalotto

# 查看详情
clawhub info hexalotto

# 其他人安装
clawhub install hexalotto
```

## 后续更新

```bash
# 修改代码后发布新版本
clawhub publish ./hexalotto \
  --slug hexalotto \
  --version 2.1.0 \
  --changelog "修复xxx，新增xxx" \
  --tags latest
```

## 文件结构

```
hexalotto/
├── SKILL.md                        # Skill 主文件（含 YAML frontmatter + 执行流程）
├── README.md                       # ClawHub 展示页说明
├── scripts/
│   └── hexalotto.py                # 六爻推演核心引擎（~880行）
└── references/
    └── liuyao_guide.md             # 六爻理论速查手册
```
