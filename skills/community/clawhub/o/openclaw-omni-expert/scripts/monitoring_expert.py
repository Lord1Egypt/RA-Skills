#!/usr/bin/env python3
"""
OpenClaw 监控运维专家
THE MONITORING EXPERT - 专业的监控运维与故障告警

作者：ProClaw
网站：www.ProClaw.top
联系方式：wechat:Mr-zifang

功能：
1. 日志配置与分析
2. 性能指标监控
3. 健康检查配置
4. 故障告警系统
5. 备份恢复策略
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta


# =============================================================================
# 日志配置
# =============================================================================

class LogConfig:
    """日志配置模板"""

    @staticmethod
    def standard_config(
        log_dir: str = "~/.openclaw/logs",
        level: str = "INFO",
        rotation: str = "daily",
        max_size: str = "100MB",
        backup_count: int = 30
    ) -> Dict:
        """
        标准日志配置
        
        适用场景：开发/测试环境
        """
        return {
            "logging": {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                        "datefmt": "%Y-%m-%d %H:%M:%S"
                    },
                    "detailed": {
                        "format": "%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d] - %(message)s",
                        "datefmt": "%Y-%m-%d %H:%M:%S"
                    }
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": level,
                        "formatter": "standard",
                        "stream": "ext://sys.stdout"
                    },
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": level,
                        "formatter": "detailed",
                        "filename": f"{log_dir}/openclaw.log",
                        "maxBytes": 104857600,  # 100MB
                        "backupCount": backup_count,
                        "encoding": "utf-8"
                    },
                    "error_file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "ERROR",
                        "formatter": "detailed",
                        "filename": f"{log_dir}/openclaw_error.log",
                        "maxBytes": 52428800,  # 50MB
                        "backupCount": 10,
                        "encoding": "utf-8"
                    }
                },
                "loggers": {
                    "openclaw": {
                        "level": level,
                        "handlers": ["console", "file", "error_file"],
                        "propagate": False
                    }
                },
                "root": {
                    "level": level,
                    "handlers": ["console", "file"]
                }
            }
        }

    @staticmethod
    def production_config(
        log_dir: str = "/var/log/openclaw"
    ) -> Dict:
        """
        生产环境日志配置
        
        适用场景：生产环境
        """
        return {
            "logging": {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "json": {
                        "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                        "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
                    }
                },
                "handlers": {
                    "syslog": {
                        "class": "logging.handlers.SysLogHandler",
                        "level": "INFO",
                        "formatter": "json",
                        "address": ["/dev/log"]
                    },
                    "json_file": {
                        "class": "logging.handlers.TimedRotatingFileHandler",
                        "level": "INFO",
                        "formatter": "json",
                        "filename": f"{log_dir}/openclaw.json",
                        "when": "midnight",
                        "interval": 1,
                        "backupCount": 90,
                        "encoding": "utf-8"
                    }
                },
                "loggers": {
                    "openclaw": {
                        "level": "INFO",
                        "handlers": ["syslog", "json_file"],
                        "propagate": False
                    }
                }
            }
        }

    @staticmethod
    def debug_config() -> Dict:
        """调试日志配置"""
        return LogConfig.standard_config(
            level="DEBUG",
            backup_count=5
        )


# =============================================================================
# 性能指标
# =============================================================================

class MetricsConfig:
    """性能指标配置"""

    # 系统级指标
    SYSTEM_METRICS = {
        "cpu_usage": {
            "name": "CPU 使用率",
            "type": "gauge",
            "unit": "percent",
            "interval": 10,
            "thresholds": {"warning": 70, "critical": 90}
        },
        "memory_usage": {
            "name": "内存使用率",
            "type": "gauge",
            "unit": "percent",
            "interval": 10,
            "thresholds": {"warning": 70, "critical": 85}
        },
        "disk_usage": {
            "name": "磁盘使用率",
            "type": "gauge",
            "unit": "percent",
            "interval": 60,
            "thresholds": {"warning": 75, "critical": 90}
        },
        "network_io": {
            "name": "网络 IO",
            "type": "counter",
            "unit": "bytes/s",
            "interval": 10
        }
    }

    # 应用级指标
    APPLICATION_METRICS = {
        "request_count": {
            "name": "请求数",
            "type": "counter",
            "description": "总请求数"
        },
        "request_duration": {
            "name": "请求耗时",
            "type": "histogram",
            "unit": "ms",
            "buckets": [10, 50, 100, 200, 500, 1000, 2000, 5000],
            "thresholds": {"p95": 500, "p99": 1000}
        },
        "active_connections": {
            "name": "活跃连接数",
            "type": "gauge",
            "thresholds": {"warning": 100, "critical": 200}
        },
        "error_rate": {
            "name": "错误率",
            "type": "gauge",
            "unit": "percent",
            "thresholds": {"warning": 1, "critical": 5}
        },
        "queue_depth": {
            "name": "队列深度",
            "type": "gauge",
            "thresholds": {"warning": 100, "critical": 500}
        }
    }

    # OpenClaw 特有指标
    OPENCLAW_METRICS = {
        "agent_execution_time": {
            "name": "Agent 执行时间",
            "type": "histogram",
            "unit": "ms",
            "description": "Agent 任务执行耗时"
        },
        "tool_call_count": {
            "name": "工具调用次数",
            "type": "counter",
            "description": "各工具调用统计"
        },
        "tool_call_duration": {
            "name": "工具调用耗时",
            "type": "histogram",
            "unit": "ms",
            "description": "各工具执行耗时"
        },
        "memory_usage_bytes": {
            "name": "记忆存储大小",
            "type": "gauge",
            "unit": "bytes",
            "description": "向量数据库存储使用量"
        },
        "active_agents": {
            "name": "活跃 Agent 数",
            "type": "gauge",
            "description": "当前运行的 Agent 数量"
        }
    }

    @staticmethod
    def prometheus_config() -> Dict:
        """Prometheus 监控配置"""
        return {
            "metrics": {
                "enabled": True,
                "port": 9090,
                "path": "/metrics",
                "collectors": [
                    "system",
                    "application",
                    "openclaw"
                ]
            },
            "scrape_configs": [
                {
                    "job_name": "openclaw",
                    "scrape_interval": "15s",
                    "static_configs": [{
                        "targets": ["localhost:9090"]
                    }]
                }
            ]
        }

    @staticmethod
    def grafana_dashboard() -> Dict:
        """Grafana 仪表盘配置"""
        return {
            "dashboard": {
                "title": "OpenClaw 监控",
                "panels": [
                    {
                        "title": "系统资源",
                        "type": "graph",
                        "targets": [
                            {"expr": "cpu_usage", "legendFormat": "CPU"},
                            {"expr": "memory_usage", "legendFormat": "Memory"}
                        ]
                    },
                    {
                        "title": "请求延迟",
                        "type": "graph",
                        "targets": [
                            {"expr": "request_duration_p95", "legendFormat": "P95"},
                            {"expr": "request_duration_p99", "legendFormat": "P99"}
                        ]
                    },
                    {
                        "title": "错误率",
                        "type": "gauge",
                        "targets": [
                            {"expr": "error_rate"}
                        ],
                        "fieldConfig": {
                            "thresholds": {
                                "steps": [
                                    {"value": 0, "color": "green"},
                                    {"value": 1, "color": "yellow"},
                                    {"value": 5, "color": "red"}
                                ]
                            }
                        }
                    }
                ]
            }
        }


# =============================================================================
# 健康检查
# =============================================================================

class HealthCheck:
    """健康检查配置"""

    @staticmethod
    def basic_check() -> Dict:
        """基础健康检查"""
        return {
            "health_check": {
                "enabled": True,
                "endpoint": "/health",
                "interval": 30,
                "timeout": 5,
                "checks": [
                    {
                        "name": "process",
                        "type": "process",
                        "config": {
                            "pid_file": "~/.openclaw/openclaw.pid"
                        }
                    },
                    {
                        "name": "disk",
                        "type": "disk",
                        "config": {
                            "path": "~/.openclaw",
                            "threshold": 90
                        }
                    }
                ]
            }
        }

    @staticmethod
    def comprehensive_check() -> Dict:
        """全面健康检查"""
        return {
            "health_check": {
                "enabled": True,
                "endpoint": "/health",
                "interval": 10,
                "timeout": 5,
                "checks": [
                    {
                        "name": "gateway",
                        "type": "http",
                        "config": {
                            "url": "http://localhost:18789/health",
                            "expected_status": 200
                        }
                    },
                    {
                        "name": "database",
                        "type": "database",
                        "config": {
                            "type": "chroma",
                            "connection_check": True
                        }
                    },
                    {
                        "name": "memory",
                        "type": "memory",
                        "config": {
                            "usage_threshold": 80
                        }
                    },
                    {
                        "name": "disk",
                        "type": "disk",
                        "config": {
                            "paths": ["~/.openclaw", "/var/log/openclaw"],
                            "threshold": 85
                        }
                    },
                    {
                        "name": "network",
                        "type": "network",
                        "config": {
                            "ports": [18789],
                            "check_connectivity": True
                        }
                    }
                ]
            }
        }


# =============================================================================
# 告警配置
# =============================================================================

class AlertConfig:
    """告警配置模板"""

    # 告警规则
    ALERT_RULES = {
        "high_cpu": {
            "name": "CPU 使用率过高",
            "condition": "cpu_usage > 90",
            "duration": "5m",
            "severity": "critical",
            "channels": ["email", "slack"],
            "message": "CPU 使用率持续超过 90%"
        },
        "high_memory": {
            "name": "内存使用率过高",
            "condition": "memory_usage > 85",
            "duration": "5m",
            "severity": "critical",
            "channels": ["email", "slack"],
            "message": "内存使用率持续超过 85%"
        },
        "high_error_rate": {
            "name": "错误率过高",
            "condition": "error_rate > 5",
            "duration": "2m",
            "severity": "critical",
            "channels": ["email", "slack", "sms"],
            "message": "错误率持续超过 5%"
        },
        "slow_response": {
            "name": "响应超时",
            "condition": "request_duration_p99 > 5000",
            "duration": "5m",
            "severity": "warning",
            "channels": ["slack"],
            "message": "P99 响应时间超过 5 秒"
        },
        "gateway_down": {
            "name": "网关不可用",
            "condition": "gateway_health == 0",
            "duration": "1m",
            "severity": "critical",
            "channels": ["email", "slack", "sms"],
            "message": "Gateway 服务不可用"
        }
    }

    # 告警渠道配置
    ALERT_CHANNELS = {
        "email": {
            "enabled": True,
            "type": "smtp",
            "config": {
                "smtp_host": "smtp.example.com",
                "smtp_port": 587,
                "from": "openclaw-alert@example.com",
                "to": ["admin@example.com"],
                "use_tls": True
            }
        },
        "slack": {
            "enabled": True,
            "type": "webhook",
            "config": {
                "webhook_url": "https://hooks.slack.com/services/xxx",
                "channel": "#alerts",
                "username": "OpenClaw Alert"
            }
        },
        "sms": {
            "enabled": False,
            "type": "sms",
            "config": {
                "provider": "twilio",
                "to": ["+1234567890"]
            }
        },
        "webhook": {
            "enabled": True,
            "type": "webhook",
            "config": {
                "url": "https://your-webhook-endpoint.com/alerts",
                "headers": {"Authorization": "Bearer xxx"}
            }
        }
    }

    @staticmethod
    def create_alert_rule(
        name: str,
        condition: str,
        severity: str = "warning",
        channels: List[str] = None
    ) -> Dict:
        """创建告警规则"""
        return {
            "name": name,
            "condition": condition,
            "duration": "5m",
            "severity": severity,
            "channels": channels or ["slack"],
            "message": f"告警: {name}",
            "actions": {
                "auto_resolve": True,
                "auto_retry": False
            }
        }


# =============================================================================
# 备份恢复
# =============================================================================

class BackupConfig:
    """备份恢复配置"""

    @staticmethod
    def standard_backup(
        backup_dir: str = "~/.openclaw/backups"
    ) -> Dict:
        """标准备份配置"""
        return {
            "backup": {
                "enabled": True,
                "schedule": "0 2 * * *",  # 每天凌晨2点
                "retention": {
                    "daily": 7,
                    "weekly": 4,
                    "monthly": 12
                },
                "targets": [
                    {
                        "name": "config",
                        "path": "~/.openclaw/config",
                        "compression": "gzip"
                    },
                    {
                        "name": "memory",
                        "path": "~/.openclaw/chroma",
                        "compression": "gzip",
                        "exclude": ["*.lock"]
                    },
                    {
                        "name": "plugins",
                        "path": "~/.openclaw/plugins",
                        "compression": "gzip"
                    },
                    {
                        "name": "logs",
                        "path": "~/.openclaw/logs",
                        "compression": "gzip",
                        "max_age": "7d"
                    }
                ],
                "destination": {
                    "type": "local",
                    "path": backup_dir
                }
            }
        }

    @staticmethod
    def cloud_backup(
        backup_dir: str = "~/.openclaw/backups"
    ) -> Dict:
        """云端备份配置"""
        return {
            "backup": {
                "enabled": True,
                "schedule": "0 2 * * *",
                "retention": {
                    "daily": 7,
                    "weekly": 4,
                    "monthly": 12
                },
                "targets": [
                    {"name": "config", "path": "~/.openclaw/config"},
                    {"name": "memory", "path": "~/.openclaw/chroma"},
                    {"name": "plugins", "path": "~/.openclaw/plugins"}
                ],
                "destination": {
                    "type": "s3",
                    "bucket": "openclaw-backups",
                    "prefix": "openclaw/",
                    "region": "us-east-1",
                    "encryption": True
                }
            }
        }

    @staticmethod
    def recovery_config() -> Dict:
        """恢复配置"""
        return {
            "recovery": {
                "verify_before_restore": True,
                "stop_services": True,
                "backup_before_restore": True,
                "notification": {
                    "enabled": True,
                    "channels": ["email", "slack"]
                }
            }
        }


# =============================================================================
# 监控运维专家系统
# =============================================================================

class MonitoringExpert:
    """
    监控运维专家
    
    提供专业级的监控运维和告警配置服务
    """

    def __init__(self):
        self.log_config = LogConfig()
        self.metrics_config = MetricsConfig()
        self.health_check = HealthCheck()
        self.alert_config = AlertConfig()
        self.backup_config = BackupConfig()

    def create_logging_config(
        self,
        environment: str = "development"
    ) -> Dict:
        """创建日志配置"""
        configs = {
            "development": self.log_config.debug_config,
            "production": self.log_config.production_config
        }
        
        config_func = configs.get(environment, self.log_config.standard_config)
        return config_func()

    def create_monitoring_config(
        self,
        backend: str = "prometheus"
    ) -> Dict:
        """创建监控配置"""
        if backend == "prometheus":
            return self.metrics_config.prometheus_config()
        elif backend == "grafana":
            return self.metrics_config.grafana_dashboard()
        else:
            return {}

    def create_health_check(
        self,
        level: str = "basic"
    ) -> Dict:
        """创建健康检查配置"""
        checks = {
            "basic": self.health_check.basic_check,
            "comprehensive": self.health_check.comprehensive_check
        }
        
        return checks.get(level, self.health_check.basic_check)()

    def create_alert_config(
        self,
        channels: List[str] = None
    ) -> Dict:
        """创建告警配置"""
        # 配置告警渠道
        alert_channels = {
            ch: self.alert_config.ALERT_CHANNELS[ch]
            for ch in (channels or ["slack"])
            if ch in self.alert_config.ALERT_CHANNELS
        }
        
        return {
            "alerts": {
                "enabled": True,
                "rules": self.alert_config.ALERT_RULES,
                "channels": alert_channels
            }
        }

    def create_backup_config(
        self,
        destination: str = "local"
    ) -> Dict:
        """创建备份配置"""
        configs = {
            "local": self.backup_config.standard_backup,
            "cloud": self.backup_config.cloud_backup
        }
        
        backup = configs.get(destination, self.backup_config.standard_backup)()
        recovery = self.backup_config.recovery_config()
        
        return {**backup, **recovery}

    def generate_dashboard_json(
        self,
        dashboard_type: str = "overview"
    ) -> str:
        """生成 Grafana 仪表盘 JSON"""
        if dashboard_type == "overview":
            return json.dumps({
                "dashboard": {
                    "title": "OpenClaw Overview",
                    "tags": ["openclaw", "overview"],
                    "timezone": "browser",
                    "panels": [
                        {
                            "id": 1,
                            "title": "System Resources",
                            "type": "graph",
                            "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
                            "targets": [
                                {"expr": "cpu_usage", "legendFormat": "CPU %"},
                                {"expr": "memory_usage", "legendFormat": "Memory %"}
                            ]
                        },
                        {
                            "id": 2,
                            "title": "Request Rate", 
                            "type": "graph",
                            "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
                            "targets": [
                                {"expr": "rate(request_count[5m])", "legendFormat": "Req/s"}
                            ]
                        }
                    ]
                }
            }, indent=2)
        return "{}"

    def analyze_logs(
        self,
        log_file: str,
        timeframe: str = "1h",
        level: str = None
    ) -> Dict:
        """
        分析日志
        
        Returns:
            分析报告
        """
        # 模拟分析结果
        return {
            "summary": {
                "total_lines": 1000,
                "error_count": 5,
                "warning_count": 20,
                "info_count": 975
            },
            "errors": [
                {
                    "message": "Connection timeout",
                    "count": 3,
                    "last_occurrence": "2024-01-15T10:30:00"
                }
            ],
            "patterns": [
                {"pattern": "slow query", "count": 15}
            ]
        }


# =============================================================================
# 主函数
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw 监控运维专家 v5.0"
    )

    # 日志配置
    parser.add_argument("--logging-config", choices=["development", "production"],
                       help="生成日志配置")
    parser.add_argument("--output", "-o", help="输出文件路径")

    # 监控配置
    parser.add_argument("--monitoring-config", choices=["prometheus", "grafana"],
                       help="生成监控配置")

    # 健康检查
    parser.add_argument("--health-check", choices=["basic", "comprehensive"],
                       help="生成健康检查配置")

    # 告警配置
    parser.add_argument("--alert-config", nargs="+",
                       choices=["email", "slack", "sms", "webhook"],
                       help="生成告警配置")

    # 备份配置
    parser.add_argument("--backup-config", choices=["local", "cloud"],
                       default="local", help="生成备份配置")

    # 分析日志
    parser.add_argument("--analyze-logs", help="分析日志文件")

    # 仪表盘
    parser.add_argument("--dashboard", choices=["overview"],
                       help="生成仪表盘 JSON")

    args = parser.parse_args()

    expert = MonitoringExpert()

    if args.logging_config:
        config = expert.create_logging_config(args.logging_config)
        output = json.dumps(config, indent=2, ensure_ascii=False)
        
        if args.output:
            Path(args.output).write_text(output)
            print(f"日志配置已保存: {args.output}")
        else:
            print(output)

    elif args.monitoring_config:
        config = expert.create_monitoring_config(args.monitoring_config)
        print(json.dumps(config, indent=2, ensure_ascii=False))

    elif args.health_check:
        config = expert.create_health_check(args.health_check)
        print(json.dumps(config, indent=2, ensure_ascii=False))

    elif args.alert_config:
        config = expert.create_alert_config(args.alert_config)
        print(json.dumps(config, indent=2, ensure_ascii=False))

    elif args.backup_config:
        config = expert.create_backup_config(args.backup_config)
        print(json.dumps(config, indent=2, ensure_ascii=False))

    elif args.analyze_logs:
        result = expert.analyze_logs(args.analyze_logs)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.dashboard:
        dashboard = expert.generate_dashboard_json(args.dashboard)
        print(dashboard)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
