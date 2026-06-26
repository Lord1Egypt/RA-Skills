# ict

Claw Skill 质量检验工具 - 多语言安全审计

## 功能

- **多语言支持**: Python, Shell, JavaScript/TypeScript
- **23 项安全检测**: 凭证收集、代码执行、数据外泄、提示词注入等
- **组合威胁检测**: 同时收集凭证又发起网络调用
- **防误报机制**: 自动过滤检测规则定义
- **白名单支持**: 可配置信任的 skill

## 安装

```bash
# CLI 使用
python ict.py /path/to/skill-folder
```

## 使用方法

### 命令行

```bash
# 基本用法
python ict.py /path/to/skill-folder

# 输出 JSON
python ict.py /path/to/skill-folder --json

# 使用白名单
python ict.py /path/to/skill-folder --allowlist allowlist.json
```

### Python API

```python
from ict import audit_skill

result = audit_skill("/path/to/skill-folder")
print(result['overall_score'])
```

## 检测项 (17项)

| # | 检测项 | 严重程度 |
|---|--------|----------|
| 1 | 凭证收集 | critical |
| 2 | 代码执行 | critical |
| 3 | 数据外泄URL | critical |
| 4 | Base64混淆 | medium |
| 5 | 敏感文件系统 | critical |
| 6 | 加密钱包地址 | critical |
| 7 | 依赖混淆 | high |
| 8 | 安装钩子 | medium |
| 9 | Symlink攻击 | critical |
| 10 | 时间炸弹 | medium |
| 11 | 远程脚本执行 | critical |
| 12 | 遥测追踪 | medium |
| 13 | 提示词注入 | critical |
| 14 | 隐蔽数据外发 | critical |
| 15 | C2服务器 | critical |
| 16 | 容器逃逸 | critical |
| 17 | SSH远程连接 | medium |

## 评分标准

- **90-100**: 优秀
- **70-89**: 良好
- **50-69**: 需改进
- **0-49**: 风险高

## 版本

v4.0.8
