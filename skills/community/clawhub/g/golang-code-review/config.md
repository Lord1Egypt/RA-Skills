# ⚙️ 配置

## 检测工具链
- **格式化工具**: `gofmt`, `goimports`
- **静态分析器**: `staticcheck` (honnef.co/go/tools)
- **错误检查**: `errcheck`
- **未使用变量**: `unused` (来自 go vet)

## 推荐安装命令
```bash
go install honnef.co/go/tools/cmd/staticcheck@latest
go install golang.org/x/lint/golint@latest
```

## 检测模式
### 1. **快速检查**（格式+基本错误）
```bash
go vet -printf=false ./...
gofmt -l ./... | xargs gofmt -w
```

### 2. **完整分析**（所有规则）
```bash
staticcheck ./...
errcheck ./...
golint ./...
```

### 3. **提交前自动化检测脚本**
可配置为 Git hook：
```bash
#!/bin/bash
go vet ./... | tee /dev/tty
gofmt -l . | xargs gofmt -w
if [ $? -eq 0 ]; then
  echo "✅ 代码检查通过"
else
  echo "❌ 存在以下问题："
  cat errors.txt
fi
```
