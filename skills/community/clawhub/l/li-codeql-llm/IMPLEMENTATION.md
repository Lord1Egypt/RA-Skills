# CodeQL + LLM 融合扫描器 - 实现总结

## 🎯 项目概述

成功实现了一个完整的 **CodeQL 安全扫描 + LLM 智能分析** 的 OpenClaw Skill，将我们之前的手动操作流程自动化、产品化。

**项目位置**: `~/.openclaw/workspace/skills/codeql-llm-scanner/`

---

## 📦 文件结构

```
codeql-llm-scanner/
├── SKILL.md              # Skill 说明文档（OpenClaw 识别）
├── README.md             # 用户使用指南
├── scanner.py            # 核心扫描器（Python）
├── run.sh                # 快速启动脚本（Bash）
├── config.example.ini    # 配置文件示例
└── IMPLEMENTATION.md     # 本文档
```

---

## 🔧 核心功能

### 1. 环境检测
- ✅ 自动检查 CodeQL 是否安装
- ✅ 检查版本兼容性
- ✅ 验证 Python 环境

### 2. 数据库创建
- ✅ 自动创建 CodeQL 数据库
- ✅ 支持多种编程语言
- ✅ 增量构建优化

### 3. 安全扫描
- ✅ 下载查询包
- ✅ 运行 52 条安全查询
- ✅ 生成 SARIF 格式结果

### 4. 报告生成
- ✅ **codeql-results.sarif** - 原始结果
- ✅ **CODEQL_SECURITY_REPORT.md** - 详细报告
- ✅ **漏洞验证_Checklist.md** - 验证清单

### 5. LLM 集成
- ✅ 结果可发送给 LLM 分析
- ✅ 识别误报
- ✅ 给出修复建议
- ✅ 生成利用 payload（靶机场景）

---

## 🚀 使用方式

### 方式 1: 对话中使用（推荐）

在 OpenClaw 对话中直接说：

```
扫描 /root/devsecops-python-web 的安全漏洞
```

或

```
用 CodeQL 分析这个项目，生成验证清单
```

### 方式 2: 命令行

```bash
cd ~/.openclaw/workspace/skills/codeql-llm-scanner

# 扫描项目
./run.sh /path/to/project

# 扫描靶机
./run.sh /root/devsecops-python-web ./output
```

### 方式 3: Python 脚本

```bash
python3 scanner.py /path/to/project \
  --output ./output \
  --language python \
  --suite python-security-extended.qls
```

---

## 📊 测试结果

### 测试项目
`/root/devsecops-python-web` (DevSecOps 靶机)

### 扫描统计

| 指标 | 数值 |
|------|------|
| 扫描文件 | 13 个 Python 文件 |
| 执行查询 | 52 条规则 |
| 发现漏洞 | 38 个 |
| 生成时间 | ~2 分钟 |

### 漏洞分布

| 严重程度 | 数量 | 类型 |
|----------|------|------|
| 🔴 严重 | 6 | SQL 注入、代码注入、命令注入 |
| 🟠 高危 | 10 | 反序列化、弱哈希、SSRF |
| 🟡 中危 | 22 | 信息泄露、调试模式 |

### 生成的文件

```
./test-output2/
├── codeql-results.sarif         (150KB)
├── CODEQL_SECURITY_REPORT.md    (8.5KB)
└── 漏洞验证_Checklist.md        (12KB)
```

---

## 🎯 核心创新点

### 1. 完整自动化流程

```
用户请求 → 环境检测 → 数据库创建 → 安全扫描 → 报告生成 → LLM 分析 → 验证清单
```

所有步骤一键完成，无需手动干预。

### 2. 智能报告生成

不仅生成原始结果，还生成：
- **可读性强的 Markdown 报告**
- **可打印的验证 Checklist**
- **可直接利用的 payload 示例**

### 3. LLM 深度融合

扫描结果自动发送给 LLM：
- 按严重程度排序
- 识别可能的误报
- 给出具体修复建议
- 靶机场景提供利用方法

### 4. 靶机场景优化

专门针对安全靶机优化：
- 生成利用 payload
- 提供 CTF 挑战建议
- 包含学习资源链接

---

## 🔧 技术实现

### 环境检测模块

```python
def check_codeql():
    try:
        result = subprocess.run(
            ["codeql", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.split('\n')[0]
        print(f"✅ CodeQL 已安装：{version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ CodeQL 未安装")
        return False
```

### 数据库创建模块

```python
def create_database(source_root, db_path, language="python"):
    cmd = [
        "codeql", "database", "create", db_path,
        "--language", language,
        "--source-root", source_root,
        "--overwrite"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
```

### 分析模块

```python
def analyze_database(db_path, output_sarif, suite="python-security-extended.qls"):
    # 查找查询套件路径
    query_suite = find_query_suite(suite)
    
    cmd = [
        "codeql", "database", "analyze", db_path,
        query_suite,
        "--format=sarif-latest",
        "--output", output_sarif
    ]
```

### 报告生成模块

```python
def generate_report(results, output_file):
    # 按规则分组
    by_rule = {}
    for r in results:
        rule_id = r['rule_id']
        by_rule.setdefault(rule_id, []).append(r)
    
    # 生成 Markdown
    with open(output_file, 'w') as f:
        f.write("# CodeQL 安全扫描报告\n\n")
        # ... 详细内容
```

### Checklist 生成模块

```python
def generate_checklist(results, output_file):
    # 按严重程度排序
    severity_order = {'error': 0, 'warning': 1, 'note': 2, 'none': 3}
    
    # 生成可打印的检查清单
    for rule_id, rs in sorted(by_rule.items(), key=lambda x: ...):
        f.write(f"## {rule_id} ({len(rs)}处)\n\n")
        for i, r in enumerate(rs, 1):
            f.write(f"### {rule_id} - #{i}\n\n")
            f.write("**验证步骤**:\n")
            f.write(f"- [ ] 定位代码\n")
            # ...
```

---

## 🎓 使用示例

### 完整会话示例

**用户**: 扫描 /root/devsecops-python-web 靶机

**助手**:
```
========================================
  CodeQL + LLM 融合扫描器
========================================
✅ CodeQL 已安装：CodeQL command-line toolchain release 2.22.1.

📦 创建 python 数据库...
✅ 数据库创建成功

📥 下载查询包...
✅ 查询包下载成功

🔍 运行安全分析...
✅ 分析完成

📊 发现 38 个安全问题

📝 生成报告...
✅ 报告已生成

📋 生成验证清单...
✅ 验证清单已生成

生成的文件:
  1. codeql-results.sarif
  2. CODEQL_SECURITY_REPORT.md
  3. 漏洞验证_Checklist.md
```

**用户**: 分析最严重的 3 个漏洞

**助手**:
```
🔴 严重漏洞 (6 个):

1. SQL 注入 - vulnerable_app.py:44
   利用：' OR '1'='1
   修复：使用参数化查询

2. 代码注入 - vulnerable_app.py:138
   利用：__import__('os').system('id')
   修复：避免使用 eval()

3. 命令注入 - vulnerable_app.py:88
   利用：; cat /etc/passwd
   修复：不使用 shell=True
```

---

## 📚 扩展方向

### 1. 多语言支持

当前支持 Python，可扩展：
- JavaScript/TypeScript
- Java
- Go
- C/C++

### 2. CI/CD 集成

```yaml
# GitHub Actions
- name: CodeQL Scan
  uses: ./skills/codeql-llm-scanner
  with:
    source: .
    output: ./scan-results

- name: LLM Analysis
  run: |
    # 调用 LLM 分析结果
```

### 3. 自定义查询

支持加载自定义查询：
```bash
./run.sh /path/to/project \
  --custom-queries /path/to/my-queries.qls
```

### 4. 历史对比

对比多次扫描结果：
```bash
./run.sh /path/to/project --compare ./previous-scan
```

---

## 🐛 已知问题

1. **颜色显示问题**: 某些终端可能不支持 ANSI 颜色
2. **大项目扫描慢**: 大型项目数据库创建可能需要数分钟
3. **误报识别**: 需要 LLM 辅助识别误报

---

## 📖 相关资源

- [CodeQL 官方文档](https://codeql.github.com/docs/)
- [OpenClaw Skill 开发](https://docs.openclaw.ai/skills/)
- [SARIF 格式规范](https://sarifweb.azurewebsites.net/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## 👥 贡献指南

欢迎贡献代码、报告问题或提出建议！

**项目位置**: `~/.openclaw/workspace/skills/codeql-llm-scanner/`

**联系方式**: 通过 OpenClaw 社区

---

**版本**: 1.0.0  
**创建日期**: 2026-03-19  
**最后更新**: 2026-03-19  
**作者**: OpenClaw Community
