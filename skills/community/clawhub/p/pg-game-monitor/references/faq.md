# 常见问题 FAQ

## Agent 类问题

### Q: game_monitor 服务启动失败
**A**: 按以下顺序排查：
```bash
# 1. 检查服务状态
systemctl status game_monitor

# 2. 查看日志
journalctl -u game_monitor -f

# 3. 检查环境变量配置
cat /opt/game_monitor/env.conf

# 4. 验证 Python 依赖
pip list | grep prometheus_client

# 5. 手动运行看报错
/usr/bin/python3 /opt/game_monitor/game_agent.py
```

### Q: JVM 指标标签 hostname / game_dir 为空
**A**:
1. 检查 `GAME_ROOT_DIR` 环境变量是否与实际路径匹配
2. 确认 `GAME_PROCESS_NAME` 与 Java 进程 cmdline 匹配
3. 检查日志中是否有 "JVM collected for" 字样
4. 手动验证：
```bash
ps aux | grep java
# 找到 game_dir 对应的 arg，验证 GAME_ROOT_DIR 前缀是否匹配
```

### Q: jcmd 命令权限不足
**A**: agent 使用 `jstat` 和 `jcmd` 采集 JVM 指标，确保运行 agent 的用户有权限访问 JDK 工具：
```bash
# 验证 jcmd 可用
jcmd <pid> GC.class_histogram
```

### Q: 如何调整采集间隔？
**A**: 修改 agent 端 `/opt/game_monitor/env.conf` 中的 `PUSH_INTERVAL`，然后：
```bash
systemctl restart game_monitor
```
注意：同时需要更新 Prometheus 端 scrape interval 和告警规则中 GC pressure 的 `gc_time_seconds / 60` 中的 60。

### Q: 类直方图功能如何关闭？
**A**: 设置 `HISTO_INTERVAL=0` 可关闭类直方图采集，降低 agent 资源占用。

## Prometheus 类问题

### Q: Prometheus 页面看不到目标
**A**:
1. 检查 Pushgateway 在线：`curl http://<pushgateway>:9091/-/healthy`
2. 检查 Prometheus target：`http://<prometheus>:9090/targets`
3. 查看 Prometheus 日志：`journalctl -u prometheus -f`

### Q: 告警规则没有触发
**A**:
1. 确认 rule_files 路径正确：`/opt/monitor/prometheus/rules.yml`
2. 重载规则：`curl -X POST http://<prometheus>:9090/-/reload`
3. 在 Prometheus UI 用 PromQL 直接测试表达式

### Q: 告警触发但飞书没收到
**A**:
1. 确认 Alertmanager 配置的 webhook 地址正确
2. 检查 feishu 服务在线：`systemctl status feishu`
3. 确认 `FEISHU_WEBHOOK_URL` 已设置：`cat /opt/monitor/feishu/webhook.env`
4. 手动触发测试：
```bash
curl -X POST "http://<webhook>:5000/webhook?level=warning" \
  -H "Content-Type: application/json" \
  -d '{"alerts":[]}'
```

## Grafana 类问题

### Q: Dashboard 显示 "No data"
**A**:
1. 确认 Prometheus 数据源配置正确
2. 检查时间范围（默认 5 分钟可能太短，尝试 1h）
3. 在 Prometheus UI 确认指标存在： `{__name__=~"heap_used.*"}`
4. 确认 Dashboard JSON 中的数据源 UID 与实际数据源匹配

### Q: 如何导出/导入 Dashboard？
```bash
# 导出
curl -s http://<grafana>:3000/api/dashboards/uid/<uid> \
  | jq '.dashboard' > dashboard.json

# 导入（见 grafana.md）
```
