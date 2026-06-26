## 🩺 心电检测报告

### 📊 核心结论

| 项目       | 结果                   |
|:---------|:---------------------|
| **分析结果** | {{ ecg_result }}     |
| **分析解读** | {{ abnor_analysis }} |
| **平均心率** | **{{ avg_hr }}** bpm |
| **最高心率** | **{{ max_hr }}** bpm |
| **最低心率** | **{{ min_hr }}** bpm |

---

### 📈 核心指标

| 指标名称           | 测量值                 | 参考范围                | 状态                        |
|:---------------|:--------------------|:--------------------|:--------------------------|
| **心率**         | {{ avg_hr }}        | 60-100              | {{ hr_status_icon }}      |
| **5分钟心率变异性指数** | {{ hrv_value }}     | {{ hrv_range }}     | {{ hrv_status_icon }}     |
| **疾病风险**       | {{ hdrisk_value }}  | {{ hdrisk_range }}  | {{ hdrisk_status_icon }}  |
| **精神压力**       | {{ mental_value }}  | {{ mental_range }}  | {{ mental_status_icon }}  |
| **疲劳指数**       | {{ fatigue_value }} | {{ fatigue_range }} | {{ fatigue_status_icon }} |

---

### 🧬 心电指标分析

| 指标名称 | 测量值 | 参考范围 | 状态 | 指标解读 |
| :--- | :--- | :--- | :--- | :--- |
{% for item in normalList %}
| **{{ item.name }}** | {{ item.value }} | {{ item.range }} | {{ item.status_icon }} | {{ item.explain }} |
{% endfor %}

---

### 💡 详细解读

#### 💓 心率分布

- 正常心率 (60-100): **{{ normal_rate }}%**
- 心率偏快 (>100): **{{ fast_rate }}%**
- 心率偏慢 (<60): **{{ slow_rate }}%**

#### 📝 心电分析印象

> {{ result_tz }}

#### 🧠 压力与疲劳

- **精神压力**: {{ mental }}
- **身体疲劳**: {{ fatigue }}

---

### ⚕️ 健康建议与指导

{% if suggestion %}
**建议**:
> {{ suggestion }}
> {% endif %}

{% if health_care_advice %}
**健康管理建议**:
> {{ health_care_advice }}
> {% endif %}

---

### 📥 报告下载

[📄 点击下载完整 PDF 报告]({{ report_pdf_url }})

---

### 💖 友情提示
Apple Watch ECG 不能检测心脏病发作、血液凝块或中风，也不能识别高血压。出现胸痛、胸闷等明显不适，请立即联系医生或急救服务。 