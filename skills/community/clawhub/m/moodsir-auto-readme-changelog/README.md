# AI Doc Generator

通用型开发者效率工具 - 一键生成专业 README、版本日志

## 特性

- 一键生成标准开源 README 文档
- 智能生成 Keep a Changelog 格式版本日志
- 自动解析 Git Commit 记录
- 语义化版本号自动计算
- 纯 Python 实现，无第三方依赖

## 功能

### Changelog 生成

支持三种输入方式：
1. Git Commit 记录（feat:/fix:/docs: 等格式）
2. 纯文本更新描述
3. 旧版本号 + 更新内容

自动分类：
- feat → 新增功能
- fix → 问题修复
- perf/refactor → 优化改进
- docs/test/chore → 其他

版本计算规则：
- 仅 fix/perf → 修订号+1 (v1.0.0 → v1.0.1)
- 含 feat → 次版本号+1 (v1.0.0 → v1.1.0)
- 含 BREAKING CHANGE → 主版本号+1 (v1.0.0 → v2.0.0)

### README 生成

自动生成标准开源项目 README，包含：
- 项目名称和描述
- 功能特性列表
- 技术栈说明
- 使用指南
- 贡献指南
- 许可证

## 开始使用

### 本地运行

```bash
# 克隆项目
git clone https://github.com/your-repo/AI-Doc-Generator.git

# 进入目录
cd AI-Doc-Generator

# 生成 Changelog
python app.py changelog "feat: 新增登录功能\nfix: 修复购物车bug" v1.0.0

# 生成 README
python app.py readme "我的项目" "这是一个很棒的项目" "功能A|功能B|功能C"
```

### Python 模块调用

```python
from app import generate_changelog_from_input, generate_readme

# 生成 Changelog
result = generate_changelog_from_input(
    content="",
    old_version="v1.0.0",
    commits_text="feat: 新增会员系统\nfix: 修复登录bug"
)
print(result["content"])

# 生成 README
readme = generate_readme(
    project_name="我的项目",
    description="项目描述",
    features=["功能1", "功能2"]
)
print(readme)
```

## 项目结构

```
AI-Doc-Generator/
├── .gitignore          # Git忽略文件
├── app.py              # 核心代码（纯Python，无依赖）
├── README.md           # 项目文档
├── CHANGELOG.md        # 版本更新日志
├── LICENSE             # MIT许可证
├── requirements.txt    # 依赖文件（无第三方依赖）
└── PLATFORMS.md        # 平台适配指南
```

## 测试用例

### Changelog 测试

| 输入 | 预期输出 |
|------|----------|
| v1.0.0 + feat:新功能 | v1.1.0 |
| v1.0.0 + fix:修复bug | v1.0.1 |
| v1.0.0 + BREAKING | v2.0.0 |
| 无版本号 | v1.0.0 |

### README 测试

```bash
python app.py readme "AI工具箱" "一款高效的AI辅助工具" "自动生成文档|智能分类|版本管理"
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - see LICENSE file
