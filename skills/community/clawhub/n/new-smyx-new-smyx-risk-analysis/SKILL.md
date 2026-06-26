---
name: "risk-analysis"
description: "Supports identifying high-risk behaviors and health risks through video/images, including elderly falls, precursors to heart attacks and strokes, and abnormal behaviors, issuing timely warning alerts. | 高风险行为识别分析工具，支持通过视频/图片识别高危行为和健康风险，包括老人跌倒、心梗脑梗前兆、异常行为等，及时发出预警提示"
version: "1.0.0"
---

# High-Risk Behavior Identification & Analysis Tool | 高风险行为识别分析工具

Deeply integrating Computer Vision, Pose Estimation, and Multimodal Health Risk Recognition algorithms, this feature
constructs an intelligent early warning system designed for high-risk behaviors and sudden health events. The system
analyzes individual behavior patterns and physiological manifestations in real-time from video or images. It precisely
captures high-risk behaviors such as sudden posture changes during falls or prolonged stillness indicating abnormal
retention. Simultaneously, by analyzing visual cues like facial microcirculation changes, abnormal skin color, and
decreased limb coordination, it assists in identifying precursors to sudden diseases such as heart attacks and
strokes.  
Leveraging temporal behavior modeling and risk assessment models, the system effectively distinguishes between daily
activities and potential dangers. Once an anomaly is detected, it immediately triggers a multi-level warning mechanism,
notifying family members and caregivers via APP push, SMS, and voice broadcasts. It synchronously transmits anomaly
footage, risk type, and location information. This provides 24/7, unobtrusive, and precise safety protection for
high-risk groups like the elderly living alone and chronic disease patients, realizing a closed-loop health management
system that shifts from passive response to active prevention.

本功能深度融合计算机视觉、姿态估计与多模态健康风险识别算法，构建了一套面向高危行为与突发健康事件的智能预警系统。系统可实时解析视频或图片中的个体行为模式与生理表征，精准捕捉老人跌倒时的姿态骤变、异常滞留时的长时间静止等高危行为，同时通过面部微循环变化、肤色异常、肢体协调性下降等视觉线索，辅助识别心梗、脑梗等突发疾病的前兆特征。借助时序行为建模与风险等级评估模型，系统能够有效区分日常活动与潜在危险，一旦检测到异常，立即触发分级预警机制，通过APP推送、短信、语音播报等多渠道通知家属及护理人员，并同步发送异常画面、风险类型与位置信息，为独居老人、慢性病患者等高风险群体提供7×24小时无感化、精准化的安全守护，实现从被动应对到主动预防的健康管理闭环

## 任务目标

- 本 Skill 用于：通过视频或图片分析识别高风险行为和健康风险，及时发出预警
- 能力包含：跌倒识别、异常行为检测、心梗脑梗前兆识别、健康风险评估、实时预警
- 触发条件：**仅当用户明确提及"风险分析"、"跌倒"、"跌倒检测"、"行为识别"、"安全监测"、"老人看护"、"风险识别"、"高危风险识别"
  时才触发本技能**。默认情况下，视频/URL分析应该触发中医面诊分析（face_analysis）技能，不触发本技能(**除非最近一次执行了风险分析或者提及风险分析
  **)。
- 支持输入：本地视频/图片文件、网络视频/图片URL、实时流地址

## 前置准备

- 依赖说明：scripts脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  opencv-python>=4.5.5
  numpy>=1.21.0
  pillow>=9.0.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行风险分析前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：【最高优先级】检查技能所在目录的配置文件（优先）
        路径：skills/smyx_common/scripts/config.yaml（相对于技能根目录）
        完整路径示例：${OPENCLAW_WORKSPACE}/skills/{当前技能目录}/skills/smyx_common/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置/api-key 为空)
第 2 步：检查 workspace 公共目录的配置文件
        路径：${OPENCLAW_WORKSPACE}/skills/smyx_common/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置)
第 3 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 4 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询历史报告记录），并询问是否继续

---

- 标准流程:
    1. **准备输入源**
        - 支持本地视频/图片路径、网络URL、RTSP实时流地址
        - 确保视频/图片清晰，覆盖需要监测的区域
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行风险分析**
        - 调用 `-m scripts.risk_analysis` 处理输入源
        - 参数说明:
            - `--input`: 本地文件路径（与--url二选一）
            - `--url`: 网络URL或实时流地址（与--input二选一）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 列出该 open-id 的历史风险分析报告（与--input/--url互斥）
            - `--page-num`: 分页页码，配合--list使用（默认 1）
            - `--page-size`: 分页大小，配合--list使用（默认 30）
            - `--api-key`: API访问密钥（可选）
            - `--api-url`: API服务地址（可选，使用默认值）
            - `--mode`: 分析模式（all/fall/health/behavior，默认all）
            - `--threshold`: 预警阈值（0.1-1.0，默认0.8）
            - `--output`: 结果输出文件路径（可选）
            - `--alert`: 是否开启自动预警（true/false，默认false）
    4. **获取分析结果**
        - 结构化的风险分析报告
        - 包含：风险类型、置信度、发生时间、位置信息、预警等级、处理建议
        - 高风险事件自动触发预警通知

## 资源索引

- 必要脚本: [scripts/risk_analysis.py](scripts/risk_analysis.py)（调用API进行风险分析，支持多种输入源）
- 配置文件: [scripts/config.py](scripts/config.py)（配置API地址、默认参数、预警阈值）
- 领域参考: [references/risk_categories.md](references/risk_categories.md)（风险分类标准和预警等级说明）

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：mp4/avi/mov/jpg/png/rtsp/http/https
- 最大支持视频大小：200MB
- 分析结果仅供参考，不能替代专业安防和医疗诊断
- 高风险事件会自动记录到日志目录
- 实时流分析支持持续监测，检测到风险立即触发预警

## 使用示例

```bash
# 分析本地视频文件
python -m scripts.risk_analysis --input /path/to/video.mp4 --open-id your-open-id

# 分析网络视频URL
python -m scripts.risk_analysis --url https://example.com/video.mp4 --open-id your-open-id

# 跌倒识别模式（只检测跌倒事件）
python -m scripts.risk_analysis --input video.mp4 --open-id your-open-id --mode fall

# 实时流监测（RTSP摄像头）
python -m scripts.risk_analysis --url rtsp://camera_ip:554/stream --open-id your-open-id --alert true

# 自定义预警阈值
python -m scripts.risk_analysis --input video.mp4 --open-id your-open-id --threshold 0.7

# 保存结果到文件
python -m scripts.risk_analysis --input video.mp4 --open-id your-open-id --output result.json

# 📋 列出指定用户的历史风险分析报告
python -m scripts.risk_analysis --list --open-id your-open-id

# 列出指定用户的历史报告，自定义分页
python -m scripts.risk_analysis --list --open-id your-open-id --page-num 2 --page-size 20
```

## 风险类型说明

1. **跌倒风险（fall）**：识别人员跌倒事件，置信度>0.8触发高等级预警
2. **健康风险（health）**：识别心梗/脑梗前兆、突发疾病症状等
3. **异常行为（behavior）**：识别剧烈运动、长时间静止、闯入等异常行为
4. **综合模式（all）**：同时检测所有类型风险

## 预警等级

- **高风险（红色）**：置信度>0.9，立即触发报警
- **中风险（黄色）**：置信度0.7-0.9，记录并关注
- **低风险（蓝色）**：置信度0.5-0.7，仅记录日志
