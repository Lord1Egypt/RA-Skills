# 管理驾驶舱 Skill

基于 OpenClaw 的管理驾驶舱 AI 教练录音分析日报生成器。

## 功能特性

- ✅ 自动分页获取录音 AI 总结内容（每页 20 条）
- ✅ 使用 OpenClaw LLM 智能分析录音数据
- ✅ 生成美观的 HTML 管理驾驶舱报表
- ✅ 支持自定义时间范围查询
- ✅ 自动保存到 skill 目录下的 `reports/` 子目录
- ✅ **数据为空时也生成空报表**（指标为 0），并返回文件路径

## 触发方式

在 OpenClaw 对话中输入以下关键词触发：

- `系统驾驶舱` - 查询最近 1 天数据
- `系统驾驶舱 2026-06-04` - 查询指定日期
- `系统驾驶舱 2026-06-01 2026-06-04` - 查询时间区间
- `管理驾驶舱` - 同上
- `日报生成` - 同上

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

编辑 `config.py` 文件，配置 API 地址：

```python
# API 配置 - 请根据实际环境修改 API_BASE_URL
API_BASE_URL = 'http://your-api-server:port'
API_ENDPOINT = '/api/recordings/asr-completed/page'

# 分页配置
DEFAULT_PAGE_SIZE = 20
DEFAULT_DAYS = 1  # 默认查询最近 1 天
```

**注意**：API 地址统一在 `config.py` 中配置，请勿在其他文件中硬编码。

## 使用方法

### 1. 命令行测试

```bash
python main.py "系统驾驶舱 2026-06-04" agent123 org456 "杭银消金苏州团队"
```

参数说明：
- `user_input`: 用户输入（包含触发词和时间）
- `agent_id`: 当前会话的 agentId（必填）
- `org_id`: 组织 ID（必填）
- `team_name`: 团队名称（可选）

### 2. 在 OpenClaw 中集成

需要在 OpenClaw 的 Skill 加载器中注册此 Skill：

```javascript
// OpenClaw Skill 加载示例
const skill = require('./management-dashboard-skill/main.py');

// 当用户输入触发词时
if (userInput.includes('系统驾驶舱')) {
    const agentId = getCurrentAgentId();  // 获取当前会话的 agentId
    const orgId = getCurrentOrgId();      // 获取当前组织 ID
    
    // 调用 Python Skill
    const result = await callPythonSkill(
        'main.py',
        [userInput, agentId, orgId, teamName]
    );
    
    // 检查返回结果
    if (result.success) {
        return `报表已生成：${result.file_path}`;
    } else {
        return result.message;  // 返回提示信息
    }
}
```

## 报表内容

生成的报表包含以下板块：

1. **团队资产沉淀大盘** - 历史累积客户、本月新增、今日新增、人均维护深度
2. **每日外勤实地效能监测** - 录音时长、面谈次数、客群分布、产业带轨迹
3. **当日合规与红线监控** - 授权告知率、利率明示率、违规词触发等
4. **当日 RM 业务水平排行** - 沟通技能得分、销冠行为、待提升人员
5. **当日线索转化效率** - A/B/C 级商机分级、跟进建议
6. **管理者跟进与靶向督导建议** - AI 生成的管理建议

## 文件结构

```
management-dashboard-skill/
├── SKILL.md                # Skill 定义文档（OpenClaw 格式）
├── main.py                 # 主逻辑
├── analyzer.py             # AI 分析模块
├── html_generator.py       # HTML 生成器
├── utils.py                # 工具函数
├── config.py               # 配置文件
├── requirements.txt        # Python 依赖
├── reports/                # 报表输出目录（自动创建）
└── README.md               # 说明文档
```

## 输出示例

### 成功生成报表

报表文件保存在：`management-dashboard-skill/reports/系统驾驶舱报告_{日期}.html`

例如：`management-dashboard-skill/reports/系统驾驶舱报告_2026-06-08.html`

返回结果：
```json
{
  "success": true,
  "message": "已根据 2026-06-07 00:00:00 至 2026-06-08 23:59:59 的 45 条录音 AI 总结，生成管理驾驶舱报告。",
  "file_path": "management-dashboard-skill/reports/系统驾驶舱报告_2026-06-08.html",
  "data_count": 45,
  "start_time": "2026-06-07 00:00:00",
  "end_time": "2026-06-08 23:59:59"
}
```

### 数据为空

当查询时间范围内没有数据时，仍生成空报表并返回：

```json
{
  "success": true,
  "message": "已根据 2026-06-07 00:00:00 至 2026-06-08 23:59:59 生成管理驾驶舱报告（当前查询周期暂无录音数据）。",
  "file_path": "management-dashboard-skill/reports/系统驾驶舱报告_2026-06-07.html",
  "data_count": 0,
  "start_time": "2026-06-07 00:00:00",
  "end_time": "2026-06-08 23:59:59"
}
```

## 注意事项

1. **LLM 调用**：需要在 `main.py` 的 `_get_llm_client()` 方法中实现实际的 OpenClaw LLM 调用逻辑
2. **API 地址**：确保 `config.py` 中的 `API_BASE_URL` 配置正确
3. **输出目录**：`reports/` 目录会自动创建，无需手动配置
4. **网络访问**：Skill 需要访问录音查询 API，确保网络连通
5. **分页逻辑**：必须使用相同的 `uuid` 进行分页请求，直到 `completed=true`

## 性能优化

- ✅ 使用分页接口，避免一次性加载大量数据
- ✅ Redis 管理分页状态，支持断点续传
- ✅ 10 分钟过期时间，避免内存占用
- ✅ 数据为空时仍生成空报表，不调用 LLM

## 故障排查

### 问题：接口调用失败

**解决**：检查 `config.py` 中的 `API_BASE_URL` 是否正确，确保 API 服务正常运行。

### 问题：LLM 返回空结果

**解决**：检查 `main.py` 中的 `_get_llm_client()` 实现，确保 OpenClaw LLM 调用正常。

### 问题：数据为空但未生成报表

**解决**：检查 `main.py` 是否在 `contents` 为空时提前返回；空数据应继续生成 HTML。

## 许可证

MIT License

## 联系方式

如有问题，请联系开发团队。
