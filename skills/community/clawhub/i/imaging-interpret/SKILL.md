# Diagnostic Imaging Report Interpreter

Interpret common diagnostic imaging findings. Does not replace radiology specialist report or clinical judgment.

## Common Findings Reference

### 胸部 X-ray

| 发现 | 可能含义 | 严重程度 |
| --- | --- | --- |
| 双肺纹理增粗 | 支气管炎、肺水肿 | ⚠️ 需结合症状 |
| 肺叶实变影 | 肺炎、肺不张 | 🔴 需治疗 |
| 团块影 > 3cm | 肿瘤待排除 | 🔴 需进一步检查 |
| 胸腔积液 | 感染/肿瘤/心衰 | 🔴 需处理 |
| 气胸 | 自发性/外伤性气胸 | 🔴 紧急评估 |

### 心电图 (ECG)

| 发现 | 可能含义 | 处理 |
| --- | --- | --- |
| ST段抬高 | 急性心肌梗死(STEMI) | 🚨 立即处理 |
| ST段压低 | 心肌缺血 | 🔴 评估胸痛 |
| 房颤 | R-R不等+f波 | 🔴 评估抗凝 |

### 影像危急值（必须立即提示）

1. **急性脑出血** — 头部CT高密度影
2. **肺栓塞** — CT报告"充盈缺损"
3. **主动脉夹层** — 胸痛+主动脉壁内膜片
4. **肠梗阻伴穿孔** — 膈下游离气体

## Usage

Triggered by: `检查报告解读`, `影像解读`, `CT报告`, `胸片`, `心电图`, `超声`, `磁共振`, `X-ray`, `CT`, `MRI`, `ECG`