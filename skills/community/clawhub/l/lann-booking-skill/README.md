# 蘭泰式按摩预约技能 (Lann Booking Skill)

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 简介

蘭泰式按摩预约技能是一个为 AI 助手设计的智能预约系统，支持查询和预约蘭泰式按摩（Lann Thai Massage）的门店和服务。

**核心功能**：
- 🏪 **门店查询**：覆盖全国 75+ 门店，支持按城市、地区、地铁站筛选
- 💆 **服务查询**：提供 28+ 专业泰式按摩与 SPA 服务项目
- 📅 **在线预约**：通过 MCP 协议或直接 API 调用完成预约

**特色**：
- ✅ 支持三种集成模式（MCP、远程 MCP、直连 API）
- ✅ 智能模糊匹配，容错率高
- ✅ 完善的参数校验和错误处理
- ✅ 详细的文档和测试脚本

---

## 快速开始

### 前置要求

- Python 3.8+ 或 Node.js 16+
- 网络连接（用于调用 API）
- （可选）MCP Client（如需使用 MCP 模式）

### 安装步骤

1. **克隆或下载本项目**
   ```bash
   git clone <repository-url>
   cd lann-booking-skill
   ```

2. **查看数据结构**
   - 门店数据：`org_store.json`（75 家门店）
   - 服务项目：`prod_service.json`（28 项服务）

3. **阅读技能文档**
   - 详细说明：`SKILL.md`
   - API 参考：`references/api_reference.md`

4. **运行测试脚本**（可选）
   ```bash
   # Python 版本
   pip install requests
   python scripts/test_booking.py

   # Shell 版本
   chmod +x scripts/test_booking.sh
   ./scripts/test_booking.sh
   ```

---

## 使用方法

### 方式 1：作为 AI Assistant Skill 使用

将本 Skill 集成到您的 AI 助手中，用户可通过自然语言进行交互：

**典型对话示例**：

```
User: 上海有哪些蘭泰门店？

Assistant: 上海目前有 60+ 家蘭泰式按摩门店，以下是部分门店：

1. 淮海店
   📍 上海市黄浦区进贤路216号（近陕西南路）
   📞 021-62670235
   🚇 地铁1号线陕西南路1号口出

2. 花木店
   📍 上海市浦东新区梅花路1029号（近芳甸路）
   📞 021-50806186
   🚇 地铁7号线花木路站4号口出

...（共 60+ 家）

需要我帮您查询特定区域的门店吗？
```

```
User: 我想预约一个缓解肩颈疲劳的服务

Assistant: 针对肩颈疲劳，我为您推荐以下服务：

1. 泰式按摩（肩颈版）-Back 60
   ⏱ 时长：60分钟
   📝 在泰式全身按摩的基础上针对肩颈进行重点加强

2. 传统古法卸负按摩-90分钟
   ⏱ 时长：90分钟
   📝 着重针对肩、颈、腰、背等易疲劳区

3. 精准泰式古法
   📝 结合国际主流徒手疼痛缓解技术，深度缓解慢性疼痛

您希望预约哪项服务？在哪家门店？
```

```
User: 我要预约淮海店的传统古法全身按摩，2人，明天下午2点，手机号13812345678

Assistant: 好的，让我为您确认预约信息：

━━━━━━━━━━━━━━━━━━━━━━━
👤 手机号：138****5678
🏪 门店：淮海店
   地址：上海市黄浦区进贤路216号（近陕西南路）
💆 服务：传统古法全身按摩-90分钟
👥 人数：2 人
🕐 时间：2024年1月16日 14:00
━━━━━━━━━━━━━━━━━━━━━━━

确认无误吗？请回复"确认"以提交预约。

User: 确认

Assistant: ✅ 预约成功！

📋 预约详情
• 预约 ID：BOOK123456
• 门店：淮海店
• 服务：传统古法全身按摩-90分钟
• 时间：2024-01-16 14:00 - 15:30
• 人数：2 人

🚇 交通指引
地铁1号线陕西南路1号口出，沿陕西南路走到进贤路右转约100m

💡 温馨提示
• 请提前 10 分钟到店
• 如需取消或改期，请至少提前 1 小时联系门店
• 祝您享受愉快的按摩体验！
```

### 方式 2：直接调用 API

使用 curl 或其他 HTTP 客户端直接调用预约接口：

```bash
curl -X POST "https://open.lannlife.com/mcp/book/create" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "13812345678",
    "storeName": "淮海店",
    "serviceName": "传统古法全身按摩-90分钟",
    "count": 2,
    "bookTime": "2024-01-16T14:00:00"
  }'
```

### 方式 3：使用 MCP 协议

配置 MCP Client 连接到 Lann MCP Server：

**本地 stdio 模式**（`mcp-config.json`）：
```json
{
  "mcpServers": {
    "lann-booking": {
      "command": "npx",
      "args": ["lann-mcp-server"]
    }
  }
}
```

**远程 streamableHttp 模式**：
```json
{
  "mcpServers": {
    "lann-booking": {
      "url": "https://open.lannlife.com/mcp",
      "type": "streamableHttp"
    }
  }
}
```

---

## 配置说明

### API Endpoint

默认 API 地址：`https://open.lannlife.com/mcp/book/create`

如需修改，请在以下位置更新：
- 测试脚本：`scripts/test_booking.py` 中的 `API_ENDPOINT` 变量
- MCP 配置：`mcp-config.json` 中的环境变量

### 数据文件

- **门店数据**：`org_store.json`
  - 包含 75 家门店的详细信息
  - 字段：name, address, telephone, traffic, longitude, latitude

- **服务数据**：`prod_service.json`
  - 包含 28 项服务项目
  - 字段：name, desc

**重要**：创建预约时，`storeName` 和 `serviceName` 必须与 JSON 文件中的 `name` 字段完全一致。

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `API_ENDPOINT` | API 请求地址 | `https://open.lannlife.com/mcp/book/create` |
| `PORT` | HTTP 服务端口（MCP 模式） | `3000` |
| `HOST` | HTTP 服务主机（MCP 模式） | `localhost` |

---

## 项目结构

```
lann-booking-skill/
├── SKILL.md                  # 技能核心文档（元数据、能力定义、工作流）
├── README.md                 # 项目说明文档（本文件）
├── _meta.json                # 元数据配置
├── org_store.json            # 门店数据（75 家）
├── prod_service.json         # 服务项目数据（28 项）
├── LICENSE                   # MIT 许可证
├── references/               # 参考文档
│   └── api_reference.md      # API 详细文档
├── scripts/                  # 脚本工具
│   ├── test_booking.py       # Python 测试脚本
│   ├── test_booking.sh       # Shell 测试脚本
│   └── start_mcp.sh          # MCP Server 启动脚本
└── assets/                   # 静态资源
    └── booking_template.md   # 预约消息模板
```

---

## 开发指南

### 添加新测试用例

编辑 `scripts/test_booking.py`，添加新的测试函数：

```python
def test_custom_scenario():
    """自定义测试场景"""
    print_separator("自定义测试")
    create_booking(
        mobile="13812345678",
        store_name="淮海店",
        service_name="传统古法全身按摩-90分钟",
        count=1,
        book_time="2024-01-16T10:00:00",
        test_name="自定义测试"
    )
```

然后在 `main()` 函数中调用：
```python
test_custom_scenario()
```

### 扩展 MCP 工具

如需添加新的 MCP 工具（如取消预约、查询预约状态），请参考：
1. 在 `references/api_reference.md` 中定义工具接口
2. 实现对应的业务逻辑
3. 更新 `SKILL.md` 中的能力定义

### 更新门店或服务数据

1. 编辑 `org_store.json` 或 `prod_service.json`
2. 确保 JSON 格式正确
3. 验证新增数据的 `name` 字段唯一性
4. 提交变更并通知相关人员

---

## 注意事项

### 数据隐私

- **手机号保护**：Skill 仅在预约时临时使用手机号，不会持久化存储
- **日志脱敏**：在日志和调试信息中，手机号中间 4 位会被替换为 `****`
- **最小化原则**：只收集完成预约所必需的信息

### 预约政策

- **提前预约**：建议至少提前 2 小时预约
- **取消政策**：需至少提前 1 小时联系门店取消或改期
- **人数限制**：单次预约最多 20 人
- **营业时间**：各门店可能不同，请以门店实际为准

### 错误处理

遇到错误时，请参考：
1. `SKILL.md` 中的"错误处理规范"章节
2. `references/api_reference.md` 中的"常见错误码"表格
3. 测试脚本的输出结果

---

## 常见问题

### Q: 如何获取准确的门店名称？

A: 运行以下命令查看所有门店：
```bash
python -c "import json; data=json.load(open('org_store.json')); print('\n'.join([s['name'] for s in data]))"
```

或在对话中询问 AI："有哪些门店？"

### Q: 如何获取准确的服务名称？

A: 运行以下命令查看所有服务：
```bash
python -c "import json; data=json.load(open('prod_service.json')); print('\n'.join([s['name'] for s in data]))"
```

或在对话中询问 AI："有哪些服务？"

### Q: 预约时间格式应该如何填写？

A: 使用 ISO 8601 格式，例如：
- `2024-01-16T14:00:00` 表示 2024 年 1 月 16 日 14:00
- 自然语言也可被 AI 解析，如"明天下午 2 点"

### Q: 如何切换到不同的集成模式？

A: 根据您的运行环境选择：
- **有 MCP Client**：配置 MCP 模式（推荐）
- **无 MCP 但有网络**：使用直连 API 模式
- **远程部署**：使用远程 MCP 模式

详见 `SKILL.md` 中的"集成模式"章节。

### Q: API 调用失败怎么办？

A: 检查以下几点：
1. 网络连接是否正常
2. API Endpoint 是否正确
3. 参数是否符合规范（手机号、门店名称、服务名称等）
4. 查看错误响应中的具体提示信息

可运行测试脚本验证 API 连通性：
```bash
python scripts/test_booking.py
```

---

## 贡献指南

欢迎贡献代码、文档或建议！

### 提交问题

如发现 bug 或有改进建议，请：
1. 检查是否已有类似的 issue
2. 创建新的 issue，详细描述问题或建议
3. 附上复现步骤或相关代码片段

### 提交代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范

- 遵循现有的代码风格
- 添加必要的注释和文档
- 确保测试通过
- 更新相关文档

---

## 版本历史

### v2.0.0 (2026-04-09)
- ✨ 重构 Skill 架构，支持三种集成模式
- ✨ 优化意图识别和参数校验逻辑
- ✨ 完善错误处理和重试机制
- 📝 增加详细的工作流指南和最佳实践
- 🧪 新增测试脚本和 API 文档

### v1.0.2 (2026-04-03)
- 🎉 初始版本发布
- 🏪 实现门店查询功能
- 💆 实现服务查询功能
- 📅 实现创建预约功能

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 联系方式

- **官方网站**：https://www.lannlife.com
- **API 文档**：`references/api_reference.md`
- **技能文档**：`SKILL.md`

---

## 致谢

感谢所有为蘭泰式按摩预约技能做出贡献的开发者和用户！

**祝您享受愉快的按摩体验！** 💆✨
