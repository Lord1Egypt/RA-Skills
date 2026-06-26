---
name: meixin-meeting-assistant
description: 镁信健康内部会议纪要生成技能。接收会议录音 → Fun-ASR全量转录 → 结合镁信/健康险行业术语 → 输出结构化会议纪要。
metadata:
  openclaw:
    requires:
      env:
        - DASHSCOPE_API_KEY
      skills:
        - meeting-assistant
      files:
        - /workspace/memory/meetings/
        - /workspace/memory/knowledge_index.json
        - /workspace/MEMORY.md
    optional:
      tools: [audios_understand, exec, write]
---

# 镁信健康会议纪要技能
## MeiXin Meeting Minutes Assistant

---

## 核心能力

1. **全自动转录**：直接接收MP3/WAV/M4A文件，调用阿里云百炼Fun-ASR，完整转录不截断（支持100MB+ / 5小时）
2. **术语自动替换**：将口语化的业务描述替换为标准术语
3. **发言人归因**：根据会议背景和声音特征，将发言归因到具体人员
4. **结构化输出**：按会议纪要标准格式输出（不含表格）
5. **知识库联动**：自动关联历史会议、相关文档、待办事项

---

## 转录流程（Fun-ASR）

### Step 1：提交任务

```python
import urllib.request, json, os, time

API_KEY = os.getenv("DASHSCOPE_API_KEY", "sk-46dec88b0761409dbd416405d53f73a5")

def transcribe_meeting(file_path: str) -> dict:
    # Step 1: 上传CDN获取公开URL（通过upload_to_cdn工具）
    # 或直接用文件绝对路径（需公网可访问）
    
    # Step 2: 提交Fun-ASR任务
    url = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"
    payload = {
        "model": "fun-asr",
        "input": {"file_urls": [file_path]},  # 公网URL或CDN URL
        "parameters": {
            "language_hints": ["zh"],
            "diarization_enabled": True,
            "speaker_count": 8
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read())
    return result["output"]["task_id"]
```

### Step 2：轮询结果

```python
def wait_for_result(task_id: str, poll_interval=5, max_wait=1800):
    query_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    start = time.time()
    while True:
        req = urllib.request.Request(query_url, headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        status = data["output"]["task_status"]
        elapsed = time.time() - start
        print(f"[{elapsed:.0f}s] {status}")
        if status == "SUCCEEDED":
            return data["output"]["results"][0]
        elif status in ("RUNNING", "PENDING"):
            time.sleep(poll_interval)
        else:
            raise Exception(f"失败: {status}")
```

---

## 镁信健康行业术语词典

### 产品/平台名称（标准写法）

| 口语写法 | 标准术语 |
|---------|---------|
| BluePass / blue pass / 不pass | BluePass（统一品牌名） |
| 瑞金专区 | 瑞金医院专区 |
| CAR-T / car t / 细胞治疗 | CAR-T（嵌合抗原受体T细胞疗法） |
| vibe-coding | Vibe Coding（快速原型开发模式） |
| TPA | TPA（第三方健康管理机构） |
| MSH | MSH International（国际健康险TPA） |
| Bupa / 保柏 | Bupa（保柏集团，高端医疗险供应商） |
| 汇丰 | HSBC（汇丰银行/汇丰人寿） |
| 保诚 / Prudential | 保诚（Prudential plc，保险公司） |
| 友邦 / AIA | 友邦保险（ AIA，全称友邦人寿保险有限公司） |
| 有邦 / 有邦的 | 友邦（AIA） |
| 和睦家 | 和睦家医疗（UFH，私立高端医疗机构） |
| 慕在 / 睦邻 / 木在 | 慕在（汇丰合作方APP演示方） |
| Fisher | Fisher（外部合作伙伴） |
| 王英 | 王英（港人北上业务接口人） |

### 业务术语

| 口语 | 标准术语 |
|------|---------|
| 北上 / 港人北上 | 港人北上（中国香港居民赴内地就医） |
| 来华就医 / 海外来华 | 国际患者赴华就医（Medical Tourism to China） |
| 保单校验 | 保单真实性核验与理赔资格校验 |
| 履约 / 履约服务 | 医疗服务履约（Service Fulfillment） |
| 系统对接 | 与保司核心系统API对接 |
| 体检 / 齿科 | 体检服务（Health Check）/ 齿科服务（Dental Service） |
| 大湾区 | 粤港澳大湾区（Greater Bay Area） |
| 2C / ToC | 直接面向消费者（Direct-to-Consumer） |
| 2B / ToB | 直接面向企业（Business-to-Business） |
| 投流 | 付费广告投放（Paid Traffic Acquisition） |
| 转化 | 转化率优化（Conversion Optimization） |
| 排期 | 预约等待周期 |
| MDT | 多学科会诊（Multi-Disciplinary Treatment） |
| 质子刀 | 质子重离子治疗（Proton Therapy） |
| 免疫治疗 | 肿瘤免疫治疗（Immuno-Oncology） |

### 公司/团队内部术语

| 口语 | 标准术语 |
|------|---------|
| 明哲 / 明泽 / 李明哲 | 李明哲（产品技术负责人） |
| 瑞恩 / 瑞英 / 瑞盈 | CRA团队，港行业务负责人 |
| 瑞英（女）| CRA团队管理层 |
| Vincent / 文森 | CRA团队成员，香港业务 |
| Judy / 朱丽 / Lisa | 管理层，产品经理 |
| 徐老师 / 徐昂 | 瑞金BD对接负责人 |
| 老板 | 公司管理层（会议主持） |
| 瑞盈 | 同"瑞英"，CRA团队管理层 |
| CRA | Clinical Research Associate / 港行业务团队 |
| MediTrust / 美信 | 上海镁信健康科技集团股份有限公司 |
| BluePass | 镁信健康旗下海外就医服务平台 |
| 镁数科技 | 镁信健康旗下科技子公司 |
| 一码直付 | 镁信健康电子理赔直付平台 |
| ClaimMaster | 镁信健康理赔大师产品 |
| 镁信 | 镁信健康（MediTrust） |

---

## 发言人识别规则

### 会议前已知发言人（可直接归因）

| 声音特征 | 身份 | 常用表达 |
|---------|------|---------|
| 沉稳有力，主持会议 | 老板（公司管理层） | "我觉得……"、"第一个……"、"你们……" |
| 语速快，思路清晰，介绍产品 | 李明哲（产品技术） | "功能就是……"、"后台也能看到……" |
| 声音柔和，女性，积极提问 | 瑞恩/CRA团队 | "能不能……"、"我们能不能……" |
| 女性，逻辑清晰，讨论业务 | Judy/Lisa/管理层 | "我觉得……"、"业务需求……" |
| 男性，讨论港行业务 | Vincent/文森 | "我跟明哲在讨论……" |
| 男性，讨论BD/医院对接 | 徐昂/徐老师 | "我们正在跟瑞金……" |

### 未知发言人的归因流程

1. 读取 `/workspace/memory/knowledge_index.json` 查找历史会议记录
2. 提取 `/workspace/memory/meetings/` 下近期会议，比对声音特征
3. 无法确认时，标注为 [发言者N]，在纪要中注明"身份待确认"

---

## 输出格式标准

### 文件命名

```
/workspace/memory/meetings/{YYYY-MM-DD}-{会议主题简称}_会议纪要.md
/workspace/memory/meetings/{YYYY-MM-DD}-{会议主题简称}_原始转录.md
```

### 会议纪要格式模板

```markdown
# {YYYY-MM-DD} {会议名称} 会议纪要

> **时间：** {YYYY-MM-DD HH:MM}
> **参会人员：** {人员名单}
> **会议主持：** {主持人}
> **纪要整理：** 许霸天 @ OpenClaw

---

## 议题一：{议题名称}

### 讨论要点

- {发言人}：{核心观点，客观陈述，不含个人评价}
- {发言人}：{补充观点}

### 共识

- {已达成一致的结论}

### 待办

- [TODO] {事项}（负责人：{人} | 截止：{时间}）

---

## 议题二：{议题名称}

### 讨论要点

- ...

### 分歧/待确认

- {尚未达成一致的事项}

---

## 附录：关键术语解释

| 术语 | 解释 |
|------|------|
| BluePass | 镁信健康旗下海外就医服务平台，为海外患者提供中国就医预约、翻译、陪诊等一站式服务 |
| ... | ... |

---

*纪要整理完毕 | {时间戳}*
```

---

## 质量标准

1. **客观陈述**：纪要内容为客观事实陈述，不加入分析评价
2. **全量记录**：所有发言均需记录，不选择性省略
3. **术语统一**：口语表达替换为标准行业术语（见术语词典）
4. **行动明确**：每项共识/待办须标注负责人和截止时间
5. **格式规范**：不使用表格，使用层级标题结构

---

## 快速使用

用户只需说：
> "帮我整理这个会议的纪要：[上传音频文件]"

许霸天自动执行：
1. Fun-ASR 全量转录（无截断）
2. 口语词汇标准化
3. 发言人归因
4. 结构化纪要输出
5. 存档至 `/workspace/memory/meetings/`
