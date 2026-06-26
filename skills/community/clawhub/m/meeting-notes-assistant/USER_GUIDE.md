# Meeting Notes Assistant 使用规范

> **版本**: v1.1  
> **更新时间**: 2026-04-07  
> **适用对象**: 所有需要会议转写和摘要的用户

## 📌 快速开始

### 安装与环境配置

```bash
# 1. 进入项目目录
cd C:\Users\Jin ZX\WorkBuddy\20260404122405\.workbuddy\skills\meeting-notes-assistant

# 2. 激活虚拟环境
.venv-py311\Scripts\activate

# 3. 安装依赖（首次使用）
pip install -r requirements.txt
```

### 基础使用

#### 方式1：命令行直接转写

```bash
# 快速转写（small 模型，5分钟完成）
python scripts/transcribe_audio.py <音频文件路径>

# 高质量转写（large-v3 模型，约1小时/1小时音频）
python scripts/transcribe_audio.py <音频文件路径> --model large-v3 --language zh
```

#### 方式2：交互式转写（推荐飞书用户）

```bash
# 完全交互式流程（所有选项都有数字编号）
python scripts/interactive_meeting_notes.py

# 指定音频目录
python scripts/interactive_meeting_notes.py --audio-dir "F:\Users\Jin ZX\Desktop\会议录音素材"

# 跳过转写方案选择，直接使用指定方案
python scripts/interactive_meeting_notes.py --provider local-small
```

**飞书环境使用说明**：
- 所有交互选项都使用数字编号格式（如 `1 - 选项A`）
- 回复数字即可选择（如回复 `1` 选择选项A）
- 每个交互问题都有明确的选项，不支持自由输入

---

## 🎯 使用场景与推荐配置

### 场景 1: 日常会议快速预览

**推荐配置**: `local-small`

```bash
python scripts/transcribe_audio.py meeting_20260406.m4a
```

**适用情况**:
- ✅ 快速了解会议内容
- ✅ 非正式会议、内部讨论
- ✅ 不需要精确专业术语
- ✅ 时间紧迫

**性能指标**:
- ⚡ 转写速度: ~5 分钟（59 分钟音频）
- 📊 术语识别率: 64.6%（金融领域）
- 💡 建议: 用于预览，正式记录使用 large-v3

### 场景 2: 专业会议正式记录

**推荐配置**: `large-v3 + 中文`

```bash
python scripts/transcribe_audio.py meeting_20260406.m4a --model large-v3 --language zh
```

**适用情况**:
- ✅ 正式会议、客户会议、监管会议
- ✅ 需要准确的专业术语识别
- ✅ 用于报告撰写、法律存档
- ✅ 有充足的转写时间

**性能指标**:
- ⚡ 转写速度: ~59 分钟（59 分钟音频）
- 📊 术语识别率: 70.8%（金融领域）
- 💡 建议: 提前规划时间，建议转写时间与音频时长 1:1

### 场景 3: 英文/多语言会议

**推荐配置**: `large-v3 + 自动检测语言`

```bash
python scripts/transcribe_audio.py meeting_english.m4a --model large-v3
```

**适用情况**:
- ✅ 英文会议
- ✅ 中英混合会议
- ✅ 其他语言会议（支持 99 种语言）

---

## 📊 模型对比与选择

| 模型 | 术语识别率 | 转写速度 | 适用场景 | 推荐度 |
|------|-----------|----------|----------|--------|
| **base** | 4.2% | ~2 分钟 | ❌ 不推荐 | ⭐ |
| **small** | 64.6% | ~5 分钟 | 快速预览 | ⭐⭐⭐⭐ |
| **large-v3** | 70.8% | ~59 分钟 | 正式记录 | ⭐⭐⭐⭐⭐ |

### 详细对比

**base 模型（不推荐）**:
- ❌ 几乎无法识别专业术语
- ❌ 严重同音字错误
- ❌ 数字识别错误
- ✅ 速度快（但质量太差）

**small 模型**:
- ✅ 速度快（12 倍于 large-v3）
- ✅ 术语识别率可接受（64.6%）
- ❌ 部分专业术语仍有错误
- 💡 适合快速预览

**large-v3 模型（推荐）**:
- ✅ 专业术语识别准确
- ✅ 长句理解更好
- ✅ 数字识别准确
- ✅ 股票名称识别好
- ⚠️ 转写时间较长
- 💡 适合正式记录

---

## 🔧 高级配置

### 指定输出路径

```bash
python scripts/transcribe_audio.py input.m4a --output output/transcript.txt
```

### 自定义 ASR 提供商

```bash
# 使用腾讯云 ASR（需配置）
python scripts/transcribe_audio.py input.m4a --asr-provider tencent

# 使用阿里云 ASR（需配置）
python scripts/transcribe_audio.py input.m4a --asr-provider aliyun
```

### 配置 ASR 提供商

```bash
# 交互式配置向导
python scripts/config_asr.py --wizard

# 直接配置（示例）
python scripts/config_asr.py --provider tencent --secret-id YOUR_ID --secret-key YOUR_KEY
```

---

## 📂 输出文件说明

转写完成后会生成以下文件：

```
output/
├── transcript.txt          # 完整转写文本
├── summary.md               # 会议摘要
├── key_terms.json          # 关键术语
├── action_items.json        # 行动项
└── meeting_notes.docx       # 格式化会议记录（可选）
```

### 文件内容说明

**transcript.txt**:
- 完整的音频转写文本
- 包含所有对话内容
- 原始格式，未进行润色

**summary.md**:
- 会议摘要
- 核心观点
- 关键决策
- 后续行动

**key_terms.json**:
- 识别到的专业术语
- 术语解释
- 出现频率

**action_items.json**:
- 行动项
- 责任人
- 截止时间
- 优先级

---

## ⚠️ 注意事项

### 1. 转写时间规划

| 音频时长 | small 模型 | large-v3 模型 |
|----------|-----------|---------------|
| 10 分钟 | ~1 分钟 | ~10 分钟 |
| 30 分钟 | ~3 分钟 | ~30 分钟 |
| 60 分钟 | ~5 分钟 | ~60 分钟 |

**建议**:
- large-v3 转写时，预留与音频等长的时间
- 避免在转写过程中关闭终端
- 确保计算机不会休眠

### 2. 硬件要求

**最低配置**:
- CPU: 4 核及以上
- RAM: 8GB 及以上
- 硬盘: 10GB 可用空间

**推荐配置（large-v3）**:
- GPU: NVIDIA RTX 3060 及以上（支持 CUDA）
- RAM: 16GB 及以上
- 硬盘: 20GB 可用空间

### 3. 音频质量要求

**推荐格式**:
- WAV（无损）
- MP3（320kbps）
- M4A（AAC）

**采样率**:
- 推荐: 16kHz 或以上
- 最低: 8kHz

**注意事项**:
- ❌ 避免背景噪音过大
- ❌ 避免多人同时说话
- ❌ 避免音量过小
- ✅ 推荐使用专业录音设备

---

## 🔍 质量评估

### 如何判断转写质量？

**优秀标准**:
- ✅ 专业术语识别率 > 90%
- ✅ 长句完整，无明显断句错误
- ✅ 数字准确无误
- ✅ 人名、公司名、产品名正确

**良好标准**:
- ✅ 专业术语识别率 70-90%
- ⚠️ 少量术语错误
- ⚠️ 少量标点/断句错误

**需改进标准**:
- ❌ 专业术语识别率 < 70%
- ❌ 大量同音字错误
- ❌ 数字识别错误

### 质量不佳的处理方法

1. **重新使用 large-v3 转写**
   ```bash
   python scripts/transcribe_audio.py input.m4a --model large-v3 --language zh
   ```

2. **检查音频质量**
   - 是否有过多背景噪音
   - 是否有多个说话人重叠
   - 音量是否过小

3. **手动修正**
   - 打开转写结果文件
   - 修正明显的错误
   - 添加缺失的标点

---

## 🆘 常见问题

### Q1: 转写速度太慢怎么办？

**A**: 
- 使用 small 模型快速预览
- 确保使用 GPU 加速
- 检查系统资源占用

### Q2: 专业术语识别不准确？

**A**:
- 使用 large-v3 模型
- 添加领域词典（即将推出）
- 手动修正后处理

### Q3: 转写中断了怎么办？

**A**:
- 重新运行转写命令
- 检查磁盘空间是否充足
- 检查内存是否足够

### Q4: 如何提高准确率？

**A**:
- 使用 large-v3 模型
- 确保音频质量良好
- 减少背景噪音
- 使用专业录音设备

### Q5: 支持哪些语言？

**A**:
- 支持 99 种语言
- 包括中文、英文、日文、韩文等
- 支持多语言混合会议

---

## 📚 参考资料

### 技术文档
- [Whisper 模型对比报告](./smoke-test/whisper-model-comparison-report.md)
- [ASR 快速开始](./ASR_QUICK_START.md)
- [ASR 提供商对比](./ASR_API_COMPARISON.md)

### 优化计划
- [改进计划](./IMPROVEMENT_PLAN.md)
- [通用领域识别架构](./docs/universal-domain-recognition-plan.md)

---

## 📞 支持与反馈

遇到问题或有建议？
- 提交 Issue
- 联系维护者
- 参与社区讨论

---

**最后更新**: 2026-04-06  
**维护者**: Meeting Notes Assistant Team
