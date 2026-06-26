# 支持的网盘类型

PanSou 支持 12 种网盘类型和 70+ 插件。

## 网盘类型

| 类型 | 名称 | 常用插件 | 说明 |
|------|------|----------|------|
| `baidu` | 百度网盘 | baidu, labi | 国内最大网盘 |
| `aliyun` | 阿里云盘 | aliyun, labi | 阿里云盘 |
| `quark` | 夸克网盘 | quark, labi | 夸克浏览器配套网盘 |
| `tianyi` | 天翼云盘 | tianyi | 中国电信网盘 |
| `uc` | UC网盘 | uc, wanou | UC浏览器配套网盘 |
| `mobile` | 移动云盘 | mobile | 中国移动网盘 |
| `115` | 115网盘 | 115 | 115网盘 |
| `pikpak` | PikPak | pikpak | 海外网盘 |
| `xunlei` | 迅雷网盘 | xunlei | 迅雷网盘 |
| `123` | 123网盘 | 123 | 123网盘 |
| `magnet` | 磁力链接 | magnet | 磁力链接 |
| `ed2k` | 电驴 | ed2k | 电驴链接 |
| `others` | 其他 | - | 其他网盘类型 |

## 搜索命令

```bash
uv run {baseDir}/scripts/pansou.py search "关键词" --cloud-types quark,aliyun,baidu
```
