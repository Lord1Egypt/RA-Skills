# 长桥智能投资助手

## 简介

这是一个 OpenClaw Skill，用于自动监控长桥证券持仓，提供：
- 📊 实时持仓分析
- 📈 投资组合可视化（港股/美股分开显示）
- 🔔 智能止盈止损提醒
- 💡 投资建议

## 安装

### 前提条件

1. 拥有长桥证券账户
2. 申请长桥 OpenAPI 权限
3. 获取 API Token

### 配置步骤

#### 步骤 1：安装长桥 Python SDK

```bash
pip install longbridge
```

#### 步骤 2：配置 API Token

创建文件 `~/.longbridge/env`，内容如下：

```bash
export LONGBRIDGE_APP_KEY="你的 App Key"
export LONGBRIDGE_APP_SECRET="你的 App Secret"
export LONGBRIDGE_ACCESS_TOKEN="你的 Access Token"
```

#### 步骤 3：安装本 Skill

将本 Skill 复制到 OpenClaw skills 目录：

```bash
cp -r longbridge-assistant ~/.qclaw/workspace/skills/
```

## 使用

### 命令行运行

```bash
cd ~/.qclaw/workspace/skills/longbridge-assistant
./run.sh
```

### 在 OpenClaw 中使用

```
/longbridge          # 获取完整持仓分析
/longbridge holdings # 查看持仓列表
/longbridge chart    # 生成投资组合图表
```

## 功能说明

### 1. 持仓分析
- 自动获取所有持仓股票
- 计算实时市值
- 分析做多/做空比例

### 2. 可视化图表
- 港股持仓饼图
- 美股持仓饼图
- 前15大持仓占比

### 3. 止盈止损监控
默认监控以下股票：

| 股票 | 操作 | 触发价格 |
|------|------|----------|
| SMCI | 卖出 | $35 / $40 |
| 小米 | 买入/卖出 | $32 / $55 |
| 7226.HK | 卖出 | $4.50 |
| Nike | 止损 | $48 |

### 4. 自定义配置

编辑 `longbridge_skill.py` 中的 `ALERTS` 字典，添加你自己的监控股票：

```python
ALERTS = {
    'AAPL.US': [
        {'price': 150.0, 'action': 'buy_more', 'msg': '苹果回调至$150，建议加仓'},
        {'price': 200.0, 'action': 'sell_partial', 'msg': '苹果涨至$200，建议减仓'},
    ],
    # 添加更多...
}
```

## 输出示例

```
🦞 长桥智能投资助手 v2.0.0

📊 获取持仓及市值信息...
✅ 获取成功，共 49 只持仓
💰 总市值: $1,769,599

📈 生成投资组合图表...
   ✅ 图表已保存: ~/longbridge-scripts/portfolio_chart.png

📋 前10大持仓:
 1. 🟢 1810.HK  10700股 @ $33.20 = $355,240
 2. 🟢 7226.HK  60000股 @ $3.86 = $231,600
 ...

🔔 价格提醒检查:
   ✅ 暂无价格提醒触发

📊 组合分析:
   总持仓: 49 只
   做多: 41 只 ($1,715,764)
   做空: 8 只 ($53,835)
   净值: $1,661,929
   💡 持仓过于分散，建议集中优质标的
```

## 注意事项

1. **API 限制**：长桥 API 有调用频率限制，请勿频繁运行
2. **数据安全**：Token 文件请妥善保管，不要分享给他人
3. **投资风险**：本 Skill 仅供参考，不构成投资建议

## 故障排除

### 问题：无法获取持仓
**解决**：检查 `~/.longbridge/env` 文件是否正确配置

### 问题：图表无法生成
**解决**：安装 matplotlib：`pip install matplotlib`

### 问题：权限错误
**解决**：确保 Token 有读取持仓和行情的权限

## 更新日志

### v2.0.0
- 新增港股/美股分开显示
- 优化图表生成
- 改进错误处理

### v1.0.0
- 初始版本
- 基础持仓监控
- 止盈止损提醒

## 作者

OpenClaw Community

## 许可证

MIT License
