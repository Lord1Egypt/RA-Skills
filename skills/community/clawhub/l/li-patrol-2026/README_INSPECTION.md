# 智能运维巡检系统使用指南

## 快速开始

### 1. 执行完整巡检
```bash
python3 intelligent_inspection.py
```

### 2. 导出JSON报告
```bash
python3 intelligent_inspection.py --export
```

### 3. 指定巡检层级
```bash
# 仅执行基础资源巡检
python3 intelligent_inspection.py --layers resource

# 执行基础资源和中间件巡检
python3 intelligent_inspection.py --layers resource middleware

# 执行所有层级巡检（默认）
python3 intelligent_inspection.py --layers all
```

## 巡检层级说明

| 层级 | 名称 | 说明 | 实现方式 |
|------|------|------|----------|
| 1 | 基础资源巡检 | CPU、内存、磁盘、网络、Inode、负载 | 真实巡检 |
| 2 | 中间件巡检 | Redis、MySQL、Kafka、MongoDB、ES等 | 真实巡检（自动检测） |
| 3 | K8S巡检 | Node、Pod、Deployment状态 | 真实/模拟 |
| 4 | 日志巡检 | ERROR、WARN、异常分析 | 真实/模拟 |
| 5 | 业务巡检 | 订单成功率、接口响应时间等 | 模拟 |

## 输出示例

```
================================================================================
智能运维巡检报告
巡检时间: 2026-06-04 09:49:19
主机名: your-hostname
操作系统: Linux 6.8.0-117-generic
================================================================================

执行: 基础资源巡检
健康评分: 100/100
摘要: 系统资源状态良好

✓ CPU使用率
  当前值: 2.3%
  阈值: P1: >95% | P2: >85%
  状态: 正常 | 风险等级: 正常

✓ 内存使用率
  当前值: 67.4% (2.55GB/3.78GB)
  阈值: P1: >95% | P2: >85%
  状态: 正常 | 风险等级: 正常

================================================================================
巡检总结
================================================================================
总体健康评分: 98/100
P1级别问题: 0个
P2级别问题: 1个
系统状态: 优秀 ✓
```

## 风险等级说明

- **P1（严重）**: 核心功能不可用，需要立即处理
- **P2（警告）**: 功能受损或存在风险，需要尽快处理
- **P3（提示）**: 存在潜在问题，建议处理
- **正常**: 系统运行正常，无需处理

## 智能特性

### 自动检测
系统会自动检测已安装的软件和服务，仅对存在的组件进行巡检：
- ✓ Redis: 检测redis-cli命令
- ✓ MySQL: 检测mysql命令和systemctl服务
- ✓ Kafka: 检测kafka-topics.sh命令
- ✓ MongoDB: 检测mongo/mongosh命令
- ✓ PostgreSQL: 检测psql命令
- ✓ Elasticsearch: 检测端口9200
- ✓ RabbitMQ: 检测rabbitmqctl命令
- ✓ Nginx: 检测nginx命令
- ✓ Tomcat: 检测端口8080/8443/8005/8009

### 健康评分算法
```
基础分: 100分
每个P1问题: -20分
每个P2问题: -10分
每个P3问题: -5分
最低分: 0分
```

评分等级：
- 90-100分: 优秀 ✓
- 70-89分: 良好
- 50-69分: 需关注
- 0-49分: 需立即处理 ✗

## 依赖要求

### 核心依赖（必需）
```bash
pip install psutil
```

### 可选依赖
```bash
pip install requests  # 用于Elasticsearch检查
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `intelligent_inspection.py` | 主巡检脚本 |
| `.skills/ops-inspection.md` | 运维巡检技能文档 |
| `.env` | 环境配置文件 |
| `inspection_report_*.json` | 导出的巡检报告 |

## 扩展开发

### 添加新的巡检项
```python
class CustomInspection(BaseInspection):
    def __init__(self):
        super().__init__()
        self.layer_name = "自定义巡检"
    
    def inspect(self) -> InspectionResult:
        # 检查组件是否存在
        if not self.check_command_exists('your-command'):
            return self._create_skip_result()
        
        # 实现巡检逻辑
        self.add_item(InspectionItem(
            resource_name="巡检项名称",
            current_value="当前值",
            threshold="异常阈值",
            status="状态",
            risk_level="风险等级",
            analysis="问题分析",
            suggestion="处理建议"
        ))
        
        return InspectionResult(
            layer=self.layer_name,
            items=self.results,
            health_score=self.calculate_health_score(),
            summary=self._generate_summary(),
            timestamp=self.timestamp
        )
```

### 集成到巡检系统
```python
# 在 IntelligentInspection.__init__ 中添加
self.inspectors = [
    ResourceInspection(),
    MiddlewareInspection(),
    K8SInspection(),
    LogInspection(),
    BusinessInspection(),
    CustomInspection()  # 添加自定义巡检
]
```

## 最佳实践

### 定时巡检
使用crontab配置定时巡检：
```bash
# 每15分钟执行一次基础资源巡检
*/15 * * * * /usr/bin/python3 /path/to/intelligent_inspection.py --layers resource --export

# 每小时执行一次完整巡检
0 * * * * /usr/bin/python3 /path/to/intelligent_inspection.py --export
```

### 告警集成
根据巡检结果配置告警：
- P1级别：电话、短信告警
- P2级别：企业微信、钉钉告警
- P3级别：邮件、工单通知

### 报告归档
定期清理历史报告：
```bash
# 保留最近30天的报告
find . -name "inspection_report_*.json" -mtime +30 -delete
```

## 故障排查

### psutil导入失败
```bash
pip install psutil
```

### 权限不足
部分巡检需要root权限：
```bash
sudo python3 intelligent_inspection.py
```

### 网络连接失败
检查防火墙和网络配置，确保可以访问目标服务的端口。

## 技术支持

详细文档请查看：`.skills/ops-inspection.md`
