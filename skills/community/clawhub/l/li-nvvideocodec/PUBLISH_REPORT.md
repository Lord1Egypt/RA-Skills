# li_nvvideocodec Skill - ClawHub发布报告

**作者**: 北京老李 (beijingLL)  
**发布日期**: 2026年5月14日  
**状态**: ✅ 已发布

---

## 📦 发布信息

| 项目 | 值 |
|------|-----|
| **Slug** | `li-nvvideocodec` |
| **名称** | NVIDIA AV1 Video Compressor |
| **版本** | 1.0.0 |
| **所有者** | 43622283 |
| **许可证** | MIT-0 (自由使用，无需署名) |
| **审核状态** | ✅ CLEAN (通过) |

---

## 🔍 搜索结果

```bash
$ clawhub search li-nvvideocodec
li-nvvideocodec  NVIDIA AV1 Video Compressor  (2.500)
```

---

## 📋 详细信息

```
Slug: li-nvvideocodec
Name: NVIDIA AV1 Video Compressor
Summary: NVIDIA AV1视频批量压缩工具，使用FFmpeg调用NVIDIA NVENC硬件编码，支持智能压缩验证和多方案选择
Owner: 43622283
Created: 2026-05-14T13:25:49.603Z
Updated: 2026-05-14T13:26:03.576Z
Latest: 1.0.0
License: MIT-0
Tags: av1, compression, ffmpeg, gpu, latest, nvidia, video
Moderation: CLEAN ✅
```

---

## ✅ 审核通过

- **扫描引擎**: v2.4.24
- **审核结果**: CLEAN
- **可疑模式**: 无
- **个人信息**: 已清除
- **硬编码路径**: 已移除

---

## 🌍 安装方式

用户现在可以通过以下方式安装此skill：

```bash
# 安装skill
clawhub install li-nvvideocodec

# 更新skill
clawhub update li-nvvideocodec

# 搜索skill
clawhub search li-nvvideocodec

# 查看详细信息
clawhub inspect li-nvvideocodec
```

---

## 📊 发布流程总结

### 1. 环境准备
- ✅ 安装clawhub CLI: `npm i -g clawhub`
- ✅ 登录: `clawhub auth login --token <api-key>`
- ✅ 验证: `clawhub auth whoami`

### 2. Skill准备
- ✅ 创建SKILL.md（包含name, description, version）
- ✅ 移除个人信息
- ✅ 添加tags
- ✅ 确保通用性

### 3. 发布
```bash
clawhub publish li_nvvideocodec \
  --slug li-nvvideocodec \
  --name "NVIDIA AV1 Video Compressor" \
  --version 1.0.0 \
  --tags "video,compression,nvidia,av1,ffmpeg,gpu"
```

### 4. 验证
```bash
clawhub search li-nvvideocodec
clawhub inspect li-nvvideocodec
```

---

## 🎯 兼容的Agent

此skill可以被以下agent使用：
- ✅ **hermes**
- ✅ **openclaw**
- ✅ **qwen-code**

---

## 📝 使用示例

安装后，agent可以：

```bash
# 检查环境
python agent_interface.py --action check

# 分析视频
python agent_interface.py --action analyze -i "/path/to/videos"

# 压缩视频
python agent_interface.py --action compress -i "/path/to/videos" -p B
```

---

## 🔗 ClawHub链接

Skill已在ClawHub注册，可通过slug `li-nvvideocodec` 访问。

---

**发布状态**: ✅ 成功  
**审核状态**: ✅ 通过  
**可用性**: ✅ 可安装和使用
