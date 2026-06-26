# 🐛 golang-code-review - Golang 代码审查技能

## 功能描述
此技能对 Git merge 提交的 Golang 代码进行全面的代码审查，包括：
- **格式检测**：遵循 `gofmt`、`goimports` 等 Go 语言标准格式规范
- **合理性和质量检测**：使用静态分析工具（如 `staticcheck`, `unused`, `errcheck`）
- **最佳实践检查**：参考 Go Code Review Comments (`https://github.com/golang/go/wiki/CodeReviewComments`)
- **安全漏洞扫描**：检测常见安全问题（SQL 注入、XSS、不安全的反序列化等）

## 输出报告
生成详细的 Markdown 报告，包含：
- 📋 总体评分
- ⚠️ 问题分类和严重等级
- 🔧 修复建议
- 📊 代码度量（复杂度、行数、空白检测）

## 规范参考
- Go Code Review Comments: https://github.com/golang/go/wiki/CodeReviewComments
- Go Error Handling: https://github.com/golang/go/wiki/ErrorHandlingBestPractices
- Effective Go: https://golang.org/doc/effective_go.html
- GO linting rules (https://staticcheck.io)

---
