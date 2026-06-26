# SKILL.md - 九歌完美版音频处理流水线

## 名称
Jiuge Flow Perfect V1 - 九歌音频大师完美版

## 版本
V1.2.0

## 描述
基于2026-05-01 21:47《敬兄弟》no-wash完美处理经验封装的音频处理Skill。执行"01_Sep → 03_Dry → 04_Master"三步流程，跳过洗声节省25%时间，全链路48kHz，输出320kbps MP3预览版。

## 核心特性
- **默认no-wash**：智能跳过洗声，节省约25%处理时间
- **全链路48kHz**：从分离到母带保持统一采样率
- **双版本输出**：320kbps母带 + 128kbps预览版
- **自动归档**：按"项目名+时间戳"自动归档到Jiuge_Audio_Projects
- **断点续处理**：支持从任意步骤中断点继续

## 执行流程

### 第一步：人声分离 (01_Sep)
- **引擎**：Kim_Vocal_2.onnx (MDX-Net)
- **模型路径**：/Applications/Ultimate Vocal Remover.app/Contents/Resources/models/MDX_Net_Models
- **输出格式**：WAV 48kHz
- **输出文件**：(Vocals)_Kim_Vocal_2.wav, (Instrumental)_Kim_Vocal_2.wav

### 第二步：去混响脱水 (03_Dry) 
- **引擎**：UVR-De-Echo-Aggressive.pth (VR Architecture)
- **模型路径**：/Applications/Ultimate Vocal Remover.app/Contents/Resources/models/VR_Models
- **输入**：第一步的Vocals文件
- **输出**：(No Echo)_UVR-De-Echo-Aggressive.wav

### 第三步：母带处理 (04_Master)
- **转换工具**：ffmpeg
- **母带版本**：320kbps MP3, 48kHz, 立体声
- **预览版本**：128kbps MP3, 48kHz, 立体声
- **命名规则**：{项目名}_Master.mp3, {项目名}_Preview.mp3

## 使用方法

### 基本用法（默认no-wash）
```bash
~/Desktop/Jiuge_Flow_Perfect_V1.skill/scripts/jiuge_flow.sh "文件名.mp3" [模式编号]
```

### 强制wash模式
```bash
~/Desktop/Jiuge_Flow_Perfect_V1.skill/scripts/jiuge_flow.sh "文件名.mp3" 1 wash
```

### 参数说明
- $1：输入文件名（必填）
- $2：处理模式（可选，默认1）
  - 1：民歌高亢版（默认）
  - 2：美声共鸣版
  - 3：流行中度脱水
  - 4：会议轻度脱水
  - 5：大教堂重度脱水
- $3：wash开关（可选，默认no-wash）
  - wash：执行完整四步流程（含洗声）
  - no-wash：跳过洗声，三步完成

## 技术规范

### 硬性指标
| 项目 | 规格 |
|------|------|
| 采样率 | 48kHz（全链路统一） |
| 母带码率 | 320kbps MP3 |
| 预览码率 | 128kbps MP3 |
| 声道 | 立体声 |
| 输出格式 | MP3 |

### 模型配置
| 步骤 | 模型 | 架构 | 用途 |
|------|------|------|------|
| 分离 | Kim_Vocal_2.onnx | MDX-Net | 人声/伴奏分离 |
| 脱水 | UVR-De-Echo-Aggressive.pth | VR | 去混响 |

## 环境要求
- Python：3.11+（uvr_auto conda环境）
- audio-separator：0.24.1+
- ffmpeg：4.3.2+
- 模型文件：已安装UVR5模型

## 修复记录
### V29 Bug修复
- **问题**：V29脚本dry_cmd为None导致TypeError
- **原因**：自动化逻辑中变量未正确初始化
- **解决**：按21:47手动成功流程重新编写分步脚本
- **验证**：2026-05-01 21:47《敬兄弟》处理成功

## 作者
九歌传媒 AI助手

## 更新日志
- V1.2.0 (2026-05-01 23:51): 修复03_Dry文件名选择bug，排除Instrumental文件，确保选择主唱人声
- V1.1.0 (2026-05-01 22:47): 修复洗声逻辑，补充完整的背景合唱分离功能
- V1.0.0 (2026-05-01): 基于21:47完美处理经验首次封装
