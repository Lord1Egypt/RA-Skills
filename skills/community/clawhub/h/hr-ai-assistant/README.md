# HR AI Assistant

一个强大的 HR AI 助手技能,可以直接调用 HRrule AI 平台的 WebSocket API,实时生成各类 HR 文档和内容。

**版权所有 © 2026 合肥即课教育科技有限公司**

## ✨ 核心功能

- ✅ **直接 API 调用** - 无需手动配置,自动调用 HRrule AI API
- ✅ **流式响应** - 实时输出,类似 ChatGPT 的流畅体验
- ✅ **智能识别** - 自动识别用户需求并选择合适的参数
- ✅ **48 种模板** - 支持员工手册、招聘JD、考核表等 48 种 HR 文档类型
- ✅ **专业问答** - 支持劳动法、员工权益、薪酬福利等 HR 相关专业问答
- ✅ **自动下载附件** - 自动检测并下载生成的文档文件 ⭐ 新功能
- ✅ **可点击下载链接** - 生成格式化的下载链接,方便用户下载
- ✅ **聊天平台集成** - 支持钉钉、QQ 等即时通讯平台
- ✅ **完全免费** - HRrule AI 平台完全免费使用

## 📦 安装与配置

### ⚠️ 首次使用体验

**重要说明**：

- **首次使用且未配置 API Key 时**，系统会**先显示提示**，告知如何免费申请 API Key
- 然后使用通用大模型回答问题
- **申请 API Key 后**，可以获得更专业的 HR AI 服务

**首次使用时会看到**：
```
══════════════════════════════════════════════════════════════════════════════
📌 首次使用 HR AI Assistant
══════════════════════════════════════════════════════════════════════════════

✨ 获取免费 API Key 以获得更专业的 HR AI 服务：

1. 访问: https://ai.hrrule.com/
2. 注册/登录账号
3. 在个人中心申请 API Key
4. **完全免费**,申请后立即可用

══════════════════════════════════════════════════════════════════════════════
```

### 1. 获取 API Key（可选，推荐）

**完全免费!** 访问以下地址申请 API Key:

👉 **https://ai.hrrule.com/**

步骤:
1. 注册/登录账号
2. 在个人中心申请 API Key
3. 免费申请,立即可用

**提示**：
- 即使不申请 API Key，也可以使用此 skill（会使用通用大模型回答）
- 申请 API Key 后，可以获得更专业的 HR AI 服务

### 2. 配置 API Key (四种方式任选其一)

#### 方式 1: 一键配置（最简单）⭐

在对话中直接粘贴申请到的 API Key，系统会自动帮你配置！

**示例**：
```
用户: 我申请到了 API Key，这是：sk-abc123xyz456...

系统: ✅ API Key 已成功配置！下次将使用专业 HR AI 服务。
```

#### 方式 2: 设置环境变量 (推荐)

```bash
# Linux/Mac
export HRRULE_API_KEY='your-api-key'

# Windows PowerShell
$env:HRRULE_API_KEY='your-api-key'

# Windows CMD
set HRRULE_API_KEY=your-api-key
```

#### 方式 3: 编辑配置文件

编辑 `config.json` 文件:

```json
{
  "api_key": "your-api-key",
  "model": "deepseek-ai/DeepSeek-R1",
  "timeout": 120,
  "verbose": true
}
```

#### 方式 4: 创建 .env 文件

复制 `.env.example` 为 `.env` 并编辑:

```bash
cp .env.example .env
```

编辑 `.env` 文件:

```env
HRRULE_API_KEY=your-api-key
```

### 3. 安装依赖

```bash
pip install python-socketio aiohttp
```

## 🚀 快速开始

### 基本使用

```python
import asyncio
from scripts.call_hrrule_api import call_hrrule_api

async def main():
    response = await call_hrrule_api(
        api_key="your-api-key",
        content="财务公司 需要招聘 社保专员,帮我生成一份 招聘JD",
        tag_id=4,
        rt="招聘JD"
    )
    print(response)

asyncio.run(main())
```

### 命令行使用

```bash
python scripts/call_hrrule_api.py \
    --content "财务公司 需要招聘 社保专员,帮我生成一份 招聘JD" \
    --tag-id 4 \
    --rt "招聘JD"
```

### 自动下载附件 ⭐ 新功能

当 API 返回包含 `<rulefile>` 标签的文档时，可以自动下载：

```bash
python scripts/call_hrrule_api.py \
    --content "帮我生成年终总结" \
    --tag-id 13 \
    --rt "年终总结" \
    --auto-download
```

输出示例：
```
AI 响应: 这是生成的年终总结文档。

[附件] 检测到 1 个附件，开始下载...
============================================================
[附件] 检测到文件 ID: 243904
[附件] 文件名: 年终总结_71917_20260119_105707.docx
[成功] 文件已下载: ~/.workbuddy/skills/hr-ai-assistant/downloads/年终总结.docx (45678 字节)
============================================================
[附件] 下载完成！共下载 1 个文件
```

详细说明请查看：[附件下载功能指南](DOWNLOAD_GUIDE.md)

### 流式响应

```python
async def stream_response():
    def print_chunk(text):
        print(text, end='', flush=True)

    response = await call_hrrule_api(
        api_key="your-api-key",
        content="帮我写一个员工手册",
        tag_id=2,
        rt="员工手册",
        on_chunk=print_chunk  # 实时打印
    )

asyncio.run(stream_response())
```

## 💡 使用示例

### 示例 1: 生成招聘JD

**输入:**
```
财务公司 需要招聘 社保专员,帮我生成一份 招聘JD
```

**自动识别:**
- Tag ID: 4 (招聘类)
- RT: "招聘JD"

**输出:**
```
# 社保专员

**工作地点**: 公司所在地
**招聘人数**: 1人
**薪资范围**: 面议

## 岗位职责
1. 负责公司员工社会保险账户的日常管理及业务操作
2. 参与社保费用核算、缴纳及报销流程的执行与优化
...
```

### 示例 2: 创建员工手册

**输入:**
```
帮我写一个员工手册,适用于50人的科技公司
```

**自动识别:**
- Tag ID: 2 (制度类)
- RT: "员工手册"

### 示例 3: 制定绩效考核表

**输入:**
```
为销售部门设计KPI考核表
```

**自动识别:**
- Tag ID: 3 (绩效类)
- RT: "KPI考核表"

### 示例 4: 写年终总结

**输入:**
```
帮我写年终总结,我是销售经理,今年完成了120%的业绩
```

**自动识别:**
- Tag ID: 13 (报告类)
- RT: "年终总结"

### 示例 5: 专业问答

**输入:**
```
三期员工有没有特殊保障？
```

**自动识别:**
- Tag ID: 1 (专业问答)
- RT: "专业问答"

**输出:**
详细的法律解答,包括相关法律法规、具体保障内容、操作建议等。

### 示例 6: 离职问题咨询

**输入:**
```
员工离职需要提前多少天通知？
```

**自动识别:**
- Tag ID: 1 (专业问答)
- RT: "专业问答"

**输出:**
根据《劳动合同法》等法律规定,提供详细的解答和建议。

## 📋 支持的文档类型

| Tag ID | 分类 | 支持的 RT |
|--------|------|-----------|
| 1 | 专业问答 | 劳动法咨询、员工权益、薪酬福利、劳动合同、离职补偿等任何 HR 相关专业问答 |
| 2 | 制度类 | 员工手册、招聘管理制度、劳动合同管理制度等 |
| 3 | 绩效类 | KPI考核表、BSC考核表、OKR考核表等 |
| 4 | 招聘类 | 招聘JD、面试评估表、录用通知书等 |
| 5 | 薪酬类 | 薪酬等级表、薪酬面谈表、薪酬诊断报告等 |
| 7 | 岗位类 | 岗位说明书、任职资格标准、职位图谱等 |
| 8 | 培训类 | 新员工培训计划、年度培训计划等 |
| 13 | 报告类 | 年终总结、月度报告、周报、日报等 |
| 14 | 风控类 | 风险自测 |

完整列表请查看 `SKILL.md` 文件。

## 🔧 高级用法

### 钉钉/QQ 集成

```python
async def send_to_dingtalk(content):
    """发送到钉钉"""
    # 实现钉钉 Webhook 发送逻辑
    pass

async def generate_and_send():
    await call_hrrule_api(
        api_key="your-api-key",
        content="帮我生成招聘JD",
        tag_id=4,
        rt="招聘JD",
        on_chunk=lambda text: send_to_dingtalk(text)  # 实时流式发送
    )

asyncio.run(generate_and_send())
```

### 自定义模型

```python
response = await call_hrrule_api(
    api_key="your-api-key",
    content="...",
    tag_id=4,
    rt="招聘JD",
    model="deepseek-ai/DeepSeek-V3"  # 自定义模型
)
```

### 错误处理

```python
try:
    response = await call_hrrule_api(
        api_key="your-api-key",
        content="...",
        tag_id=4,
        rt="招聘JD"
    )
except ValueError as e:
    print(f"API Key 错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 📖 详细文档

- **SKILL.md** - 完整的技能文档和 API 参考
- **USAGE_GUIDE.md** - 详细使用指南
- **references/api_reference.md** - API 完整参考文档
- **references/example_prompts.md** - 示例提示词集合

## ⚠️ 注意事项

1. **API Key 安全**: 请勿将 API Key 提交到公开仓库
2. **首次使用**: 首次使用时如果 API Key 为空,会提示你去 https://ai.hrrule.com/ 申请
3. **网络要求**: 需要能访问 `wss://ai.hrrule.com`
4. **依赖安装**: 确保已安装 `python-socketio` 和 `aiohttp`

## 🆘 故障排除

### 问题: 提示"未找到有效的 API Key"

**解决方案:**
1. 确认已配置环境变量 `HRRULE_API_KEY`
2. 或者确认 `config.json` 中的 `api_key` 已填写
3. 访问 https://ai.hrrule.com/ 免费申请 API Key

### 问题: 连接超时

**解决方案:**
1. 检查网络连接
2. 确认能访问 `wss://ai.hrrule.com`
3. 检查防火墙设置

### 问题: 编码错误

**解决方案:**
脚本已内置 UTF-8 编码支持,如果仍有问题,请确保终端使用 UTF-8 编码。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📞 联系方式

如有问题,请联系 HRrule AI 平台: https://ai.hrrule.com/

---

**享受免费的 HR AI 服务!** 🎉
