---
name: "face-analysis"
description: "Supports uploading local MP4 videos or network video URLs to call the server-side API for facial diagnosis. It returns structured TCM facial diagnosis results. | 支持通过上传本地 MP4 视频或网络视频 URL，调用服务端 API 进行面部诊断，返回结构化的中医面诊结果"
version: "1.0.0"
---

# TCM Facial Diagnosis Analysis Tool | 中医面诊分析工具

This feature supports users in uploading local MP4 video files or providing network video URLs. By leveraging advanced
server-side AI diagnostic APIs, it performs deep analysis and real-time capture of facial features in the video. Based
on the TCM theory of "Inspection," the system precisely analyzes key indicators such as complexion, luster, and texture.
Ultimately, it returns a structured facial diagnosis report containing physical constitution identification and health
status assessment, providing users with a convenient and professional digital health reference.

本功能支持用户上传本地MP4视频文件或提供网络视频URL，通过调用服务端先进的AI智能诊断API，对视频画面中的人物面部特征进行深度解析与实时捕捉。系统将依据中医“望诊”理论，精准分析面色、光泽及纹理等关键信息，最终返回一份包含体质辨识与健康状态评估的结构化中医面诊结果，为用户提供便捷、专业的数字化健康参考

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过面部视频进行中医面诊分析，获取结构化的健康诊断结果和养生建议
- 能力包含：视频分析、面部特征识别、脏腑状况评估、健康风险提示、养生建议生成
- 触发条件:
    1. **默认触发**：当用户提供视频 URL 或文件需要分析，但**未明确提及"风险分析"、"跌倒检测"、"行为识别"时，默认触发本技能**
       进行中医面诊分析
    2. 当用户明确需要进行中医面诊分析时，提及中医面诊、舌诊，以及上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史面诊报告、历史报告、历史面诊分析清单、面诊清单、面诊报告清单、查询历史报告、查看报告列表、查看报告清单、查看报告表格、查看所有报告、显示所有面诊报告、显示面诊报告
- 自动行为：
    1. 如果用户上传了附件或者图片文件，则自动保存到技能目录下 attachments
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有面诊报告"、"显示所有面诊报告"、"
       查看历史报告"、"显示面诊报告"、"面诊报告清单"、"显示所有报告"、"查看报告列表"等），**必须**：
        - 直接使用 `python -m scripts.face_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行面诊分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备视频输入**
        - 提供本地 MP4 视频路径或网络视频 URL
        - 确保视频清晰展示面部特征，光线充足
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行面诊分析**
        - 调用 `-m scripts.face_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径（使用 multipart/form-data 方式上传）
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示面诊视频历史列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的中医面诊报告
        - 包含：整体体质、脏腑状况、面色分析、健康警示、养生建议

## 资源索引

- 必要脚本：见 [scripts/face_analysis.py](scripts/face_analysis.py)(用途：调用 API 进行中医面诊分析，本地文件使用
  multipart/form-data 方式上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 100MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供参考，不能替代专业医疗诊断
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从数据 json 中提取字段 reportImageUrl 作为超链接地址，使用 Markdown 表格格式输出，包含"
  报告名称"、"分析时间"、"点击查看"三列，其中"报告名称"列使用`中医面诊分析报告-{记录id}`形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析时间 | 点击查看 |
  |----------|----------|----------|
  | 中医面诊分析报告-20260312172200001 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.face_analysis --input /path/to/video.mp4 --open-id openclaw-control-ui

# 分析网络视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.face_analysis --url https://example.com/video.mp4 --open-id openclaw-control-ui

# 显示历史分析报告/显示分析报告清单列表/显示历史面诊报告（自动触发关键词：查看历史面诊报告、历史报告、面诊清单等）
python -m scripts.face_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.face_analysis --input video.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.face_analysis --input video.mp4 --open-id your-open-id --output result.json
```
