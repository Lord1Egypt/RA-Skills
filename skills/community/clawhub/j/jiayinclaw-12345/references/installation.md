# 安装指南

## 前提条件

- Python 3.6 或更高版本
- pip 包管理器
- 稳定的网络连接

## 依赖安装

在使用此技能前，需要安装必要的Python库：

```bash
pip install requests beautifulsoup4
```

或者使用 requirements.txt：

```txt
requests>=2.28.0
beautifulsoup4>=4.11.0
```

## 安装步骤

### 方式一：通过ClawHub安装

```bash
clawhub install web-content-extractor
```

### 方式二：手动安装

1. 克隆技能仓库或下载文件
2. 进入技能目录
3. 安装依赖：pip install -r requirements.txt
4. 测试运行：python scripts/extractor.py --help

## 验证安装

运行以下命令验证安装是否成功：

```bash
python scripts/extractor.py https://example.com --format text
```

如果看到类似输出，说明安装成功：

```
正在提取：https://example.com
标题：Example Domain
正文内容：...

提取完成！
```

## 故障排除

### 问题1：ImportError

错误信息：ImportError: No module named 'requests'

解决方案：

```bash
pip install requests beautifulsoup4
```

### 问题2：网络超时

错误信息：HTTPSConnectionPool error

解决方案：

- 检查网络连接
- 尝试使用代理
- 稍后重试

### 问题3：编码错误

错误信息：UnicodeDecodeError

解决方案：

脚本已内置编码处理，如仍有问题，请检查Python版本。

## 与OpenClaw集成

安装后在OpenClaw中可以使用以下命令：

```
/skill activate web-content-extractor
/skill run web-content-extractor --url https://example.com
```

## 更新技能

```bash
clawhub update web-content-extractor
```

## 卸载技能

```bash
clawhub uninstall web-content-extractor
```
