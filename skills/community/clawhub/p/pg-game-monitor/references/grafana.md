# Grafana 配置指南

## 数据源配置

### 添加 Prometheus 数据源

1. 登录 Grafana（默认 `http://<grafana>:3000`，账号 `admin`）
2. 访问 **Connections → Data Sources → Add data source → Prometheus**
3. 填写配置：
   - **URL**: `http://<prometheus>:9090`
   - **Access**: Proxy
   - **Default**: 勾选
4. 点击 **Save & Test**

### 验证数据源
```bash
curl -s "http://<grafana>:3000/api/datasources" \
  -H "Authorization: Bearer <grafana-api-key>" | jq
```

## Dashboard 导入

### 通过 UI 导入
1. **Dashboards → Import → Upload JSON file**
2. 上传 `references/files/` 下的 Dashboard JSON
3. 选择 Prometheus 数据源
4. 配置 Dashboard 变量：
   - `hostname` — 主机名，多选
   - `game_dir` — 游戏服目录，多选，includeAll
5. 保存

### 通过 API 导入
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <api-key>" \
  "http://<grafana>:3000/api/dashboards/db" \
  -d @references/files/jvm_dashboard.json
```

## Dashboard 目录

建议按以下结构组织 Dashboard 文件夹：

| 目录 | 用途 |
|------|------|
| JVM-Memory/ | 堆内存、新生代、老年代 Dashboard |
| JVM-Class/ | 类内存分析、类实例数 Dashboard |
| MySQL/ | MySQL 存活、Buffer Pool、内存 Dashboard |

## 权限管理

建议按角色划分 Dashboard 访问权限：

| 角色 | 权限 | 范围 |
|------|------|------|
| Admin | 所有 Dashboard CRUD | 运维团队 |
| Editor | Dashboard 编辑 | 开发团队 |
| Viewer | 只读 | 运营团队 |

## 告警配置

Grafana 支持基于 Panel 创建告警规则，但本方案推荐使用 **Alertmanager 统一告警**（rules.yml），优势：
- 告警规则集中管理，与 Prometheus 共部署
- 支持告警抑制、静默、路由
- 统一通过飞书 Webhook 发送通知

如需在 Grafana 中配置面板告警：
1. 打开 Panel → Alert → **Create alert rule**
2. 配置条件表达式（如 `B > 0.85`）
3. 设置评估周期和 For（持续时间）
4. 选择通知渠道

## 变量（Variables）

Dashboard 支持以下变量，便于跨主机/游戏查询：

| 变量名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `hostname` | Query | 主机名，支持正则 | `game-0[1-5]` |
| `game_dir` | Query | 游戏服目录 | `xy_game_1` |
| `class`（仅 Class Dashboard） | Query | 类名 | `java.lang.String` |

## 注意事项

- Dashboard JSON 中的 `uid: "afh281y5lqjuob"` 为测试数据源 UID，**生产环境需替换为实际 Prometheus 数据源 UID**
- Grafana 默认端口 `3000`，建议通过反向代理或安全组限制访问
- 部署后请立即修改 admin 默认密码
