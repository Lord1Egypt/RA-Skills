# 预检验证指南

> 本文件为 SKILL.md 步骤0 的详细参考文档，按需加载。

---

## 一、环境检查清单

在开始任何工作流程之前，必须验证以下条件：

| 检查项 | 命令/方法 | 预期结果 |
|--------|----------|----------|
| Python 环境 | `python --version` | Python 3.8+ |
| 依赖安装 | `pip install -r requirements.txt` | 无错误 |
| 数据文件存在 | 检查 `assets/moe_pdfs_final.json` | 文件存在 |
| 职业大典存在 | 检查 `assets/occupation_dictionary_split/` | 目录有6个文件 |
| 输出目录 | 检查/创建 `output/` 和 `temp/` | 目录存在 |
| IMA 凭证 | 检查环境变量 `IMA_OPENAPI_CLIENTID` | 已设置 |

---

## 二、预检脚本

### 2.1 快速检查命令

```bash
# 一行检查核心文件
python -c "from pathlib import Path; print('[OK]' if Path('assets/moe_pdfs_final.json').exists() else '[X]', 'moe_pdfs_final.json')"
```

### 2.2 完整预检脚本

```python
#!/usr/bin/env python3
"""预检验证脚本"""

import os
from pathlib import Path

def check_environment():
    """检查环境配置"""
    checks = []
    
    # Python 版本
    import sys
    checks.append(("Python 版本", sys.version_info >= (3, 8), f"{sys.version_info.major}.{sys.version_info.minor}"))
    
    # 必需文件
    required_files = [
        "assets/moe_pdfs_final.json",
        "assets/moe_pdfs_new.json",
    ]
    for f in required_files:
        path = Path(f)
        checks.append((f, path.exists(), "存在" if path.exists() else "缺失"))
    
    # 职业大典分块目录
    occ_dir = Path("assets/occupation_dictionary_split")
    if occ_dir.exists():
        file_count = len(list(occ_dir.glob("*.md")))
        checks.append(("职业大典分块", file_count == 6, f"{file_count} 个文件"))
    else:
        checks.append(("职业大典分块", False, "目录不存在"))
    
    # 输出目录
    for d in ["output", "temp"]:
        path = Path(d)
        if not path.exists():
            path.mkdir(parents=True)
        checks.append((f"{d}/ 目录", path.exists(), "已创建" if path.exists() else "创建失败"))
    
    # IMA 凭证
    ima_clientid = os.environ.get("IMA_OPENAPI_CLIENTID", "")
    ima_apikey = os.environ.get("IMA_OPENAPI_APIKEY", "")
    checks.append(("IMA Client ID", bool(ima_clientid), "已配置" if ima_clientid else "未配置"))
    checks.append(("IMA API Key", bool(ima_apikey), "已配置" if ima_apikey else "未配置"))
    
    # 打印结果
    print("\n=== 预检验证结果 ===\n")
    all_passed = True
    for name, passed, detail in checks:
        status = "[OK]" if passed else "[X]"
        print(f"  {status} {name}: {detail}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("[OK] 所有检查通过")
    else:
        print("[WARNING] 部分检查未通过，请检查配置")
    
    return all_passed

if __name__ == "__main__":
    check_environment()
```

### 2.3 使用 occupation_dict_loader 内置检查

```bash
python scripts/occupation_dict_loader.py
```

运行时会自动验证文件。

---

## 三、数据源优先级

| 优先级 | 数据源 | 用途 | 备注 |
|--------|--------|------|------|
| 1 | `assets/moe_pdfs_final.json` | 专业教学标准 | 主数据源 |
| 2 | `assets/moe_pdfs_new.json` | 专业简介 | 备选数据源 |
| 1 | IMA知识库 | ESCO/O*NET数据 | 需配置凭证 |
| 2 | 官方API | ESCO/O*NET数据 | 网络访问 |
| 3 | Web搜索 | 补充数据 | 最后备选 |

---

## 四、常见预检问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Python 版本过低 | 系统安装的是 Python 2 或旧版 3.x | 安装 Python 3.8+ |
| 数据文件缺失 | 未下载或路径错误 | 检查 assets/ 目录 |
| IMA 凭证未配置 | .env 文件不存在或未加载 | 创建 .env 文件并配置环境变量 |
| 依赖安装失败 | 网络问题或版本冲突 | 使用国内镜像或更新 pip |

---

## 五、快速启动检查清单

```bash
# 1. 检查 Python
python --version

# 2. 安装依赖
pip install -r requirements.txt

# 3. 检查数据文件
ls assets/moe_pdfs_final.json
ls assets/occupation_dictionary_split/

# 4. 配置环境变量（创建 .env）
echo "IMA_OPENAPI_CLIENTID=your_client_id" > .env
echo "IMA_OPENAPI_APIKEY=your_api_key" >> .env

# 5. 运行测试
python scripts/search_major.py --major "汽车运用与维修" --level "中等职业教育"
```