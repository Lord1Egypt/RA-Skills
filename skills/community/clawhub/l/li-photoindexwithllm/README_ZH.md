# Photo Search Skill - 中文说明

📸 基于 VL 大模型的智能照片索引和语义搜索系统

## 简介

PhotoIndexWithLLM 是一个基于视觉-语言（VL）大模型的智能照片索引和搜索系统。

## 快速开始

```bash
# 安装依赖
pip install requests

# 扫描照片
python skill.py scan --dir D:\Photos

# 搜索照片
python skill.py search "海滩 日落"

# JSON 输出
python skill.py search "海滩" --format json
```

## 支持的平台

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

## 支持的图片格式（17 种）

| 类型 | 格式 |
|------|------|
| 常见格式 | `.jpg` `.jpeg` `.png` `.webp` `.bmp` `.tiff` `.gif` |
| iPhone/Apple | `.heic` `.heif` |
| Canon 单反 | `.cr2` |
| Nikon 单反 | `.nef` |
| Sony 单反 | `.arw` |
| 其他 RAW | `.orf` `.raf` `.dng` `.rw2` `.pef` `.sr2` |

## 隐私保护

- 默认仅使用本地模型
- 照片不会离开您的电脑
- 远程传输需要用户确认

## 完整命令

```bash
# 扫描照片
python skill.py scan --dir D:\Photos

# 搜索照片
python skill.py search "海滩日落"

# 扫描并搜索
python skill.py scan_and_search --dir D:\Photos --query "海边"

# 添加标注
python skill.py annotate --photo D:\Photos\img001.jpg --type person --name 张三

# 训练模型
python skill.py train

# 查看统计
python skill.py stats

# 测试连接
python skill.py test
```

## 联系方式

**作者**: 北京老李（beijingLL）
**ClawHub ID**: 43622283
