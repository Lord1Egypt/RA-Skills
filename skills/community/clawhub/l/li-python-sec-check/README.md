# Li_python_sec_check

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Security](https://img.shields.io/badge/security-enabled-green.svg)](https://github.com/your-repo/Li_python_sec_check)

Python 安全规范检查工具，基于 **CloudBase 开发规范** 和 **腾讯 Python 安全指南**，提供 12 项全面的安全检查。

## ✨ 特性

- 🔍 **12 项安全检查** - 涵盖项目结构、代码安全、配置安全
- 📊 **详细报告** - Markdown/JSON/HTML 多种格式
- 🚀 **快速扫描** - 1-5 分钟完成项目扫描
- 🔧 **灵活配置** - 支持命令行参数和配置文件
- 🎯 **CI/CD 集成** - 轻松集成到 Jenkins/GitHub Actions
- 📚 **中文文档** - 完整的使用指南和示例

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/your-repo/Li_python_sec_check.git
cd Li_python_sec_check

# 安装依赖
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 使用

```bash
# 扫描项目
python scripts/python_sec_check.py /path/to/your/project

# 查看报告
cat reports/*_python_sec_report.md
```

## 📋 检查内容

| # | 检查项 | 严重性 | 来源 |
|---|--------|--------|------|
| 1 | 项目结构 | 🔴 必需 | CloudBase |
| 2 | Dockerfile 规范 | 🔴 必需 | CloudBase |
| 3 | requirements.txt | 🔴 必需 | CloudBase |
| 4 | Python 版本 | 🔴 必需 | 腾讯 |
| 5 | 不安全加密算法 | 🔴 高危 | 腾讯 |
| 6 | SQL 注入风险 | 🔴 高危 | 腾讯 |
| 7 | 命令注入风险 | 🔴 高危 | 腾讯 |
| 8 | 敏感信息硬编码 | 🔴 高危 | 腾讯 |
| 9 | 调试模式 | 🔴 必需 | 腾讯 |
| 10 | 代码质量 (flake8) | 🟡 可选 | - |
| 11 | 安全扫描 (bandit) | 🟡 可选 | - |
| 12 | 依赖漏洞扫描 | 🟡 可选 | - |

## 📖 文档

- [使用指南](docs/USAGE.md) - 详细使用说明
- [SKILL.md](SKILL.md) - Skill 完整文档
- [示例项目](examples/) - 安全/不安全代码示例

## 🎯 使用场景

- ✅ 代码开发完成后进行安全检查
- ✅ CI/CD 流水线集成
- ✅ 代码审计和合规检查
- ✅ 团队安全培训
- ✅ 开源项目安全检测

## 🔧 CI/CD 集成

### Jenkins

```groovy
stage('Python Security Check') {
    steps {
        sh '''
            python scripts/python_sec_check.py ${WORKSPACE}
        '''
    }
}
```

### GitHub Actions

```yaml
- name: Python Security Check
  run: |
    python scripts/python_sec_check.py .
```

## 📊 示例报告

```markdown
# Python 安全规范检查报告

**生成时间**: 2026-03-21 17:45:00
**扫描目录**: /path/to/project

## 📊 检查摘要

| 检查项 | 状态 | 问题数 |
|--------|------|--------|
| 项目结构 | ✅ | 0 |
| 不安全加密算法 | ❌ | 1 |
| SQL 注入风险 | ❌ | 2 |
| 敏感信息硬编码 | ❌ | 1 |

## 🔍 详细结果

### 不安全加密算法
**状态**: ❌ 失败

**问题列表**:
- app.py: 使用不安全的 DES 加密算法 (应使用 AES)
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

```bash
# Fork 项目
git clone https://github.com/your-repo/Li_python_sec_check.git

# 创建分支
git checkout -b feature/your-feature

# 提交更改
git commit -m 'Add some feature'

# 推送分支
git push origin feature/your-feature
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 👥 作者

- **北京老李** - [GitHub](https://github.com/your-repo)

## 🙏 致谢

- [CloudBase](https://docs.cloudbase.net/) - 开发规范
- [腾讯安全指南](https://github.com/Tencent/secguide) - Python 安全指南
- [Bandit](https://bandit.readthedocs.io/) - Python 安全扫描工具
- [flake8](https://flake8.pycqa.org/) - Python 代码质量工具

---

**Li_python_sec_check** - 让 Python 代码更安全！ 🔒🐍
