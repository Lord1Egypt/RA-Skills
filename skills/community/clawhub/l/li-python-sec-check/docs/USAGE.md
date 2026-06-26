# Li_python_sec_check 使用文档

详细使用文档请参考 SKILL.md

## 快速开始

### 1. 安装依赖

```bash
cd Li_python_sec_check

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\Activate.ps1  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行检查

```bash
# 扫描指定目录
python scripts/python_sec_check.py /path/to/your/project

# 扫描当前目录
python scripts/python_sec_check.py .

# 自定义报告输出
python scripts/python_sec_check.py /path/to/project --output ./my-reports
```

### 3. 查看报告

报告保存在 `reports/` 目录：
- `YYYYMMDD_HHMMSS_python_sec_report.md` - 综合报告
- `bandit-report.html` - Bandit 详细报告（如启用）
- `pip-audit-report.json` - 依赖漏洞报告（如启用）

## 检查项说明

### CloudBase 规范 (3 项)
1. 项目结构 - Dockerfile、manage.py、requirements.txt
2. Dockerfile 规范 - 基础镜像、时区、镜像源
3. requirements.txt - 依赖管理

### 腾讯安全指南 (6 项)
4. Python 版本 - 必须 3.6+
5. 不安全加密算法 - DES/3DES/MD5
6. SQL 注入风险 - 字符串拼接 SQL
7. 命令注入风险 - os.system/eval/exec
8. 敏感信息硬编码 - 密码/密钥
9. 调试模式 - Flask/Django debug

### 可选工具 (3 项)
10. flake8 - 代码质量
11. bandit - 安全扫描
12. pip-audit - 依赖漏洞

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| target_dir | 扫描目录 | 当前目录 |
| --output, -o | 报告输出 | ./reports |
| --no-flake8 | 禁用 flake8 | false |
| --no-bandit | 禁用 bandit | false |
| --pip-audit | 启用 pip-audit | false |
| --verbose, -v | 详细输出 | false |

## CI/CD 集成

### Jenkins Pipeline

```groovy
stage('Python Security Check') {
    steps {
        sh '''
            cd Li_python_sec_check
            python scripts/python_sec_check.py ${WORKSPACE} --output ./reports
        '''
        archiveArtifacts artifacts: 'reports/**/*'
    }
}
```

### GitHub Actions

```yaml
- name: Python Security Check
  run: |
    cd Li_python_sec_check
    python scripts/python_sec_check.py . --no-bandit --format json
```

## 常见问题

### Q: 扫描速度慢？
A: 使用 `--no-bandit` 或 `--no-flake8` 禁用部分检查

### Q: 误报怎么办？
A: 在代码中添加 `# nosec` 注释标记

### Q: 如何自定义检查规则？
A: 修改 `scripts/checks/` 目录下的检查脚本

---

**作者**: 北京老李  
**版本**: 2.0.0  
**文档**: SKILL.md
