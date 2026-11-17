# Contributing to mu-mbti-job

感谢你对 mu-mbti-job 的兴趣！以下是参与贡献的指南。

## 如何贡献

### 报告 Bug

1. 使用 GitHub Issues 提交 Bug 报告
2. 提供复现步骤、环境信息（Python 版本、操作系统）和错误日志
3. 如果涉及 PDF 生成问题，请说明使用的 PDF 引擎（weasyprint / Chrome / Edge / reportlab）

### 提交功能请求

1. 在提交前搜索现有 Issues，避免重复
2. 清晰描述使用场景和预期行为
3. 如果涉及新题库或新语言，请说明数据来源和版权情况

### 提交代码

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -m "feat: description"`
4. 推送到你的 Fork：`git push origin feature/your-feature-name`
5. 创建 Pull Request

### 代码规范

- Python 代码遵循 PEP 8
- 保持 `./data/` 目录只读，题库修改需单独说明理由
- 新增功能需附带基本测试
- 中英双语内容需同时更新两种语言

## 开发环境

```bash
git clone https://github.com/muippt/mu-mbti-job.git
cd mu-mbti-job
python3 scripts/score.py --regression  # 运行回归测试
```

## 行为准则

参与本项目即表示你同意遵守我们的 [行为准则](CODE_OF_CONDUCT.md)。

## 许可证

通过向本项目提交代码，你同意将你的贡献在 [MIT 许可证](LICENSE) 下发布。
