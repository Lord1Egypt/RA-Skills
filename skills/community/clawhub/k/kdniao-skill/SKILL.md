# 批量快递查询API-快递鸟 (kdniaoapi-skill)

## 技能元数据

| 属性 | 值 |
|------|-----|
| **名称** | 批量快递查询API-快递鸟 |
| **Slug** | kdniaoapi-skill |
| **版本** | v1.0.0 |
| **来源** | ClawHub.ai (kdniao官方) |
| **功能描述** | 支持通过快递鸟API实时查询运单轨迹信息；当用户需要查询快递物流状态、追踪运单进度或获取包裹配送详情时使用 |

---

## 任务目标

- **技能用途**：查询快递运单的实时物流轨迹信息
- **能力包含**：调用快递鸟API获取物流状态、解析轨迹数据、展示配送进度
- **触发条件**：用户提出查询快递物流、追踪运单、查看配送状态等需求

---

## 前置准备

### 依赖安装

```bash
pip install requests>=2.28.0
```

### 凭证配置

**必需环境变量**：`KUAIDI_BIRD_API_CREDENTIALS`

**格式**：`CUSTOMER_CODE|APP_KEY`（使用竖线分隔）

**获取方式**：
1. 访问快递鸟官网注册账号
2. 登录后进入"API管理"或"开发者中心"
3. 获取商户ID（CUSTOMER_CODE）和API密钥（APP_KEY）

**配置示例**：

```bash
# macOS/Linux
export KUAIDI_BIRD_API_CREDENTIALS="1292092|993d0b97-07fa-478c-bfea-ca3597f2ce0f"

# Windows PowerShell
$env:KUAIDI_BIRD_API_CREDENTIALS="1292092|993d0b97-07fa-478c-bfea-ca3597f2ce0f"
```

---

## 操作步骤

### 标准流程

1. **确认运单信息**
   - 获取用户提供的运单号
   - 验证运单号格式（通常为10-20位数字或字母数字组合）

2. **执行查询**
   ```bash
   python3 ~/.workbuddy/skills/kdniaoapi-skill/scripts/query_tracking.py --logistic-code <运单号>
   ```

3. **解析与展示结果**
   - 物流状态（已揽收、运输中、派送中、已签收等）
   - 轨迹时间线（按时间顺序的物流节点）
   - 当前最新状态

### 错误处理

| 场景 | 处理方式 |
|------|----------|
| 运单号无效 | 提示用户检查运单号是否正确 |
| 缺少API凭证 | 检查环境变量是否已设置 |
| 凭证格式错误 | 确认格式为 `CUSTOMER_CODE\|APP_KEY` |
| API异常 | 检查凭证配置，建议稍后重试 |
| 没有可用套餐 | 需在快递鸟官网开通套餐 |

---

## 使用示例

```bash
# 查询顺丰运单
python3 ~/.workbuddy/skills/kdniaoapi-skill/scripts/query_tracking.py --logistic-code SF1234567890

# 查询圆通运单
python3 ~/.workbuddy/skills/kdniaoapi-skill/scripts/query_tracking.py --logistic-code YT1234567890123
```

---

## 注意事项

- 不同快递公司的查询结果格式可能略有差异
- 建议在查询前提醒用户确认运单号准确性
- API使用默认正式环境地址：`https://api.kdniao.com/api/dist`
