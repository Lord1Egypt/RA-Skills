# jimeng-openclaw-video-v1

[万界方舟](https://www.wjark.com)即梦（Jimeng）文生视频技能，适用于 [OpenClaw](https://github.com/openclaw/openclaw) 智能体平台。

通过即梦 API 将文本提示词转换为短视频，支持异步任务提交与自动轮询。

---

## ✨ 功能特点

- **文生视频** — 输入一段中文描述，即可生成对应短视频
- **异步生成** — 后台提交任务，自动轮询状态，生成完成后即刻返回结果
- **任务锁机制** — 同一时刻仅允许一个生成任务运行，防止并发冲突
- **完整日志** — 所有操作记录写入 `jimeng_log.txt`，便于排查问题
- **结果持久化** — 生成结果写入 `jimeng_result.txt`，格式为 `SUCCESS|<视频URL>`

---

## 📁 目录结构

```
jimeng-openclaw-video-v1/
├── SKILL.md                          # 技能描述文件（OpenClaw 自动识别）
├── manifest.json                     # 技能元数据
├── README.md                         # 本文件
└── model/
    └── scripts/
        ├── video_interface.py        # 入口脚本（提交任务）
        ├── jimeng_worker.py          # 核心工作脚本（提交 + 轮询 + 结果提取）
        ├── jimeng_log.txt            # 运行日志（自动生成）
        ├── jimeng_result.txt         # 生成结果（自动生成）
        └── jimeng.lock               # 任务锁文件（运行时自动创建/清理）
```

---

## 🔧 前置要求

| 项目 | 说明 |
|------|------|
| **Python** | 3.8+ |
| **依赖库** | `requests`（首次运行时自动安装） |
| **API Key** | 需在 OpenClaw 配置文件 `~/.openclaw/openclaw.json` 中配置 models.providers 的 `apiKey` |
| **网络** | 需能访问 `maas-openapi.wanjiedata.com`（万界数据 MaaS 平台） |

---

## 🚀 使用方法

### 方式一：命令行直接调用

```bash
python model/scripts/video_interface.py "猫捉老鼠，卡通风格，动态追逐场景"
```

### 方式二：Python 代码调用

```python
from model.scripts.video_interface import trigger_jimeng_generation

result = trigger_jimeng_generation("一个赛博朋克风格的城市街道")
print(result)
```

### 方式三：在 OpenClaw 中使用

直接在对话中告诉 OpenClaw：

> 使用 jimeng-openclaw-video-v1 技能生成视频：小橘猫在阳光下吃小黄鱼

OpenClaw 会自动调用本技能，提交任务并轮询结果。

---

## ⚙️ 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | （必填） | 视频描述提示词，建议使用中文 |
| `model` | string | `jimeng_t2v_v30` | 即梦模型标识 |

---

## 📖 工作流程

```
用户输入 prompt
       │
       ▼
 video_interface.py
  ├── 检查并安装 requests 依赖
  └── 后台启动 jimeng_worker.py
              │
              ▼
       提交异步任务 → 获取 task_id
              │
              ▼
       轮询任务状态（每 20 秒一次，最多 15 次 ≈ 5 分钟）
              │
         ┌────┴────┐
         ▼         ▼
       done      failed / 超时
         │
         ▼
  提取视频 URL → 写入 jimeng_result.txt
         │
         ▼
  Windows 下自动打开视频链接
```

---

## 📝 结果文件格式

**jimeng_result.txt**

```
SUCCESS|https://v26-aiop.aigc-cloud.com/xxx/video/...
```

可通过读取该文件判断生成状态：
- 文件存在且以 `SUCCESS|` 开头 → 生成成功，`|` 后为视频下载链接
- 文件不存在 → 任务仍在进行中或尚未提交

---

## ⚠️ 注意事项

1. **临时链接**：生成的视频 URL 为即梦平台临时链接，有一定有效期，建议尽快下载保存
2. **并发限制**：同一时刻仅支持一个生成任务；如需强制重启，手动删除 `jimeng.lock` 文件
3. **生成耗时**：通常 40 秒 ~ 2 分钟，取决于服务端负载
4. **API 配额**：请关注万界数据平台的调用额度和计费规则

---

## 🐛 常见问题

### 任务卡住 / 锁文件残留

```bash
# 手动清理锁文件
rm model/scripts/jimeng.lock
```

### 提交失败

检查 `jimeng_log.txt` 中的错误信息，常见原因：
- API Key 无效或过期
- 网络无法连接 `maas-openapi.wanjiedata.com`
- 模型标识不正确

### 视频 URL 为空

部分情况下 `video_url` 字段可能为空，脚本会尝试从 `resp_data.videos` 中回退提取。若仍失败，请查看日志中的完整响应。

---

## 📄 许可证

本技能作为 OpenClaw 社区技能发布，供个人学习和使用。

---

## 🔗 相关链接

- [万界方舟](https://www.wjark.com)
- [小龙虾下载教程](https://docs.wjark.com/maas/scenarios/Development/openclaw.html)
- [模型选择](https://www.wjark.com/center/model)

## 🔥 联系我们

**开发者邮箱**：liangshenghzj888@gmail.com