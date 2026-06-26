# 快速测试指南

## 测试 Skill

### 1. 列出打印机
```bash
cd C:\Users\39173\Desktop\printer-control-skill
python scripts/list_printers.py
```

### 2. 打印测试文本
```bash
python scripts/print_text.py --printer "Microsoft Print to PDF" --text "Hello from 月月鸟's printer skill!"
```

### 3. 打印文件
```bash
python scripts/print_file.py --printer "Microsoft Print to PDF" --file "C:\path\to\your\file.txt"
```

### 4. 查看打印机状态
```bash
python scripts/printer_status.py --all
```

## 发布到 ClawHub

### 1. 登录 ClawHub
```bash
clawhub login
```
这会打开浏览器让你登录 GitHub 账号。

### 2. 发布 Skill
```bash
cd C:\Users\39173\Desktop\printer-control-skill
clawhub publish . --slug printer-control --name "Printer Control" --version 1.0.0 --changelog "Initial release - Windows printer control with pywin32 and PowerShell fallback"
```

### 3. 验证发布
```bash
clawhub list
```

## 依赖安装（可选，提升兼容性）

```bash
pip install pywin32
```

不安装也可以，脚本会自动使用 PowerShell fallback。
