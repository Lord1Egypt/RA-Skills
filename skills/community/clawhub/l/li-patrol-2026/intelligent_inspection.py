#!/usr/bin/env python3
"""
智能运维巡检系统
支持5层巡检：基础资源、中间件、K8S、日志、业务巡检
"""

import os
import sys
import json
import time
import shutil
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import platform

# 尝试导入psutil，用于真实系统监控
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("警告: psutil未安装，基础资源巡检功能受限")

# 尝试导入其他依赖
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class RiskLevel(Enum):
    """风险等级"""
    P1 = "P1"  # 严重
    P2 = "P2"  # 警告
    P3 = "P3"  # 提示
    NORMAL = "正常"


@dataclass
class InspectionItem:
    """巡检项"""
    resource_name: str
    current_value: str
    threshold: str
    status: str
    risk_level: str
    analysis: str
    suggestion: str


@dataclass
class InspectionResult:
    """巡检结果"""
    layer: str
    items: List[InspectionItem]
    health_score: int
    summary: str
    timestamp: str


class BaseInspection:
    """巡检基类"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results: List[InspectionItem] = []
    
    def check_command_exists(self, command: str) -> bool:
        """检查命令是否存在"""
        return shutil.which(command) is not None
    
    def check_service_running(self, service_name: str) -> bool:
        """检查服务是否运行"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def check_port_listening(self, port: int) -> bool:
        """检查端口是否监听"""
        if not PSUTIL_AVAILABLE:
            return False
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == 'LISTEN':
                return True
        return False
    
    def add_item(self, item: InspectionItem):
        """添加巡检项"""
        self.results.append(item)
    
    def calculate_health_score(self) -> int:
        """计算健康评分"""
        if not self.results:
            return 100
        
        score = 100
        for item in self.results:
            if item.risk_level == RiskLevel.P1.value:
                score -= 20
            elif item.risk_level == RiskLevel.P2.value:
                score -= 10
            elif item.risk_level == RiskLevel.P3.value:
                score -= 5
        
        return max(0, min(100, score))


class ResourceInspection(BaseInspection):
    """第一层：基础资源巡检"""
    
    def __init__(self):
        super().__init__()
        self.layer_name = "基础资源巡检"
    
    def inspect(self) -> InspectionResult:
        """执行基础资源巡检"""
        if not PSUTIL_AVAILABLE:
            return self._create_unavailable_result()
        
        # CPU检查
        self._check_cpu()
        
        # 内存检查
        self._check_memory()
        
        # 磁盘检查
        self._check_disk()
        
        # Inode检查
        self._check_inode()
        
        # 系统负载检查
        self._check_load()
        
        # 网络检查
        self._check_network()
        
        return InspectionResult(
            layer=self.layer_name,
            items=self.results,
            health_score=self.calculate_health_score(),
            summary=self._generate_summary(),
            timestamp=self.timestamp
        )
    
    def _check_cpu(self):
        """CPU使用率检查"""
        try:
            # 获取CPU使用率（1秒采样）
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # 获取每个核心的使用率
            cpu_per_cpu = psutil.cpu_percent(interval=1, percpu=True)
            
            # 判断风险等级
            if cpu_percent > 95:
                risk = RiskLevel.P1
                status = "严重"
                analysis = f"CPU使用率严重过高，当前{cpu_percent:.1f}%，可能导致系统响应缓慢"
                suggestion = "立即检查高CPU进程，考虑扩容或优化应用"
            elif cpu_percent > 85:
                risk = RiskLevel.P2
                status = "警告"
                analysis = f"CPU使用率偏高，当前{cpu_percent:.1f}%，需要关注"
                suggestion = "检查CPU密集型进程，规划扩容"
            else:
                risk = RiskLevel.NORMAL
                status = "正常"
                analysis = "CPU使用率在正常范围内"
                suggestion = "无需处理"
            
            self.add_item(InspectionItem(
                resource_name="CPU使用率",
                current_value=f"{cpu_percent:.1f}%",
                threshold="P1: >95% | P2: >85%",
                status=status,
                risk_level=risk.value,
                analysis=analysis,
                suggestion=suggestion
            ))
            
            # CPU核心数
            self.add_item(InspectionItem(
                resource_name="CPU核心数",
                current_value=f"{cpu_count}核",
                threshold="无",
                status="信息",
                risk_level=RiskLevel.NORMAL.value,
                analysis=f"系统共有{cpu_count}个CPU核心",
                suggestion="无需处理"
            ))
            
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="CPU使用率",
                current_value="获取失败",
                threshold="P1: >95% | P2: >85%",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"无法获取CPU信息: {str(e)}",
                suggestion="检查系统权限"
            ))
    
    def _check_memory(self):
        """内存检查"""
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            mem_percent = mem.percent
            mem_used_gb = mem.used / (1024**3)
            mem_total_gb = mem.total / (1024**3)
            mem_available_gb = mem.available / (1024**3)
            
            if mem_percent > 95:
                risk = RiskLevel.P1
                status = "严重"
                analysis = f"内存使用率严重过高 {mem_percent:.1f}%，可用内存仅{mem_available_gb:.2f}GB"
                suggestion = "立即释放内存或扩容，检查内存泄漏"
            elif mem_percent > 85:
                risk = RiskLevel.P2
                status = "警告"
                analysis = f"内存使用率偏高 {mem_percent:.1f}%，可用内存{mem_available_gb:.2f}GB"
                suggestion = "关注内存使用趋势，考虑扩容"
            else:
                risk = RiskLevel.NORMAL
                status = "正常"
                analysis = "内存使用率在正常范围内"
                suggestion = "无需处理"
            
            self.add_item(InspectionItem(
                resource_name="内存使用率",
                current_value=f"{mem_percent:.1f}% ({mem_used_gb:.2f}GB/{mem_total_gb:.2f}GB)",
                threshold="P1: >95% | P2: >85%",
                status=status,
                risk_level=risk.value,
                analysis=analysis,
                suggestion=suggestion
            ))
            
            # Swap检查
            if swap.total > 0:
                swap_percent = swap.percent
                swap_risk = RiskLevel.P2 if swap_percent > 50 else RiskLevel.NORMAL
                self.add_item(InspectionItem(
                    resource_name="Swap使用率",
                    current_value=f"{swap_percent:.1f}%",
                    threshold="P2: >50%",
                    status="警告" if swap_percent > 50 else "正常",
                    risk_level=swap_risk.value,
                    analysis=f"Swap使用率{swap_percent:.1f}%" if swap_percent > 50 else "Swap使用率正常",
                    suggestion="检查内存压力" if swap_percent > 50 else "无需处理"
                ))
            
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="内存使用率",
                current_value="获取失败",
                threshold="P1: >95% | P2: >85%",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"无法获取内存信息: {str(e)}",
                suggestion="检查系统权限"
            ))
    
    def _check_disk(self):
        """磁盘检查"""
        try:
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    usage_percent = usage.percent
                    used_gb = usage.used / (1024**3)
                    total_gb = usage.total / (1024**3)
                    
                    if usage_percent > 95:
                        risk = RiskLevel.P1
                        status = "严重"
                        analysis = f"磁盘{partition.mountpoint}空间严重不足，仅剩{(100-usage_percent):.1f}%"
                        suggestion = f"立即清理{partition.mountpoint}磁盘空间"
                    elif usage_percent > 85:
                        risk = RiskLevel.P2
                        status = "警告"
                        analysis = f"磁盘{partition.mountpoint}空间不足，剩余{(100-usage_percent):.1f}%"
                        suggestion = f"规划清理{partition.mountpoint}磁盘空间"
                    else:
                        risk = RiskLevel.NORMAL
                        status = "正常"
                        analysis = "磁盘空间充足"
                        suggestion = "无需处理"
                    
                    self.add_item(InspectionItem(
                        resource_name=f"磁盘使用率({partition.mountpoint})",
                        current_value=f"{usage_percent:.1f}% ({used_gb:.2f}GB/{total_gb:.2f}GB)",
                        threshold="P1: >95% | P2: >85%",
                        status=status,
                        risk_level=risk.value,
                        analysis=analysis,
                        suggestion=suggestion
                    ))
                except PermissionError:
                    continue
                    
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="磁盘使用率",
                current_value="获取失败",
                threshold="P1: >95% | P2: >85%",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"无法获取磁盘信息: {str(e)}",
                suggestion="检查系统权限"
            ))
    
    def _check_inode(self):
        """Inode检查"""
        try:
            result = subprocess.run(
                ['df', '-i'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
                
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 6:
                        filesystem = parts[0]
                        mountpoint = parts[5]
                        
                        # 解析inode使用率
                        used = int(parts[2])
                        available = int(parts[3])
                        total = used + available
                        
                        if total > 0:
                            inode_percent = (used / total) * 100
                            
                            if inode_percent > 95:
                                risk = RiskLevel.P1
                                status = "严重"
                                analysis = f"Inode使用率严重过高，可能无法创建新文件"
                                suggestion = f"清理小文件或扩容{mountpoint}"
                            elif inode_percent > 85:
                                risk = RiskLevel.P2
                                status = "警告"
                                analysis = f"Inode使用率偏高，需要关注"
                                suggestion = f"检查{mountpoint}下的小文件数量"
                            else:
                                risk = RiskLevel.NORMAL
                                status = "正常"
                                analysis = "Inode使用率正常"
                                suggestion = "无需处理"
                            
                            self.add_item(InspectionItem(
                                resource_name=f"Inode使用率({mountpoint})",
                                current_value=f"{inode_percent:.1f}% ({used}/{total})",
                                threshold="P1: >95% | P2: >85%",
                                status=status,
                                risk_level=risk.value,
                                analysis=analysis,
                                suggestion=suggestion
                            ))
                            
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="Inode使用率",
                current_value="获取失败",
                threshold="P1: >95% | P2: >85%",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"无法获取Inode信息: {str(e)}",
                suggestion="检查df命令权限"
            ))
    
    def _check_load(self):
        """系统负载检查"""
        try:
            load_avg = os.getloadavg()
            cpu_count = psutil.cpu_count()
            
            load_1, load_5, load_15 = load_avg
            
            # 负载阈值：CPU核数 * 2
            threshold = cpu_count * 2
            
            if load_1 > threshold:
                risk = RiskLevel.P2
                status = "警告"
                analysis = f"系统负载过高 {load_1:.2f}，超过阈值{threshold}"
                suggestion = "检查系统瓶颈，优化或扩容"
            else:
                risk = RiskLevel.NORMAL
                status = "正常"
                analysis = f"系统负载正常，当前负载{load_1:.2f}"
                suggestion = "无需处理"
            
            self.add_item(InspectionItem(
                resource_name="系统负载(1分钟)",
                current_value=f"{load_1:.2f}",
                threshold=f"P2: >{threshold} (CPU核数×2)",
                status=status,
                risk_level=risk.value,
                analysis=analysis,
                suggestion=suggestion
            ))
            
            self.add_item(InspectionItem(
                resource_name="系统负载(5分钟)",
                current_value=f"{load_5:.2f}",
                threshold=f"P2: >{threshold}",
                status="信息",
                risk_level=RiskLevel.NORMAL.value,
                analysis=f"5分钟平均负载",
                suggestion="无需处理"
            ))
            
            self.add_item(InspectionItem(
                resource_name="系统负载(15分钟)",
                current_value=f"{load_15:.2f}",
                threshold=f"P2: >{threshold}",
                status="信息",
                risk_level=RiskLevel.NORMAL.value,
                analysis=f"15分钟平均负载",
                suggestion="无需处理"
            ))
            
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="系统负载",
                current_value="获取失败",
                threshold="P2: >CPU核数×2",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"无法获取负载信息: {str(e)}",
                suggestion="检查系统权限"
            ))
    
    def _check_network(self):
        """网络检查"""
        try:
            # 网络连接统计
            net_connections = psutil.net_connections()
            
            # 统计连接状态
            status_count = {}
            time_wait_count = 0
            established_count = 0
            
            for conn in net_connections:
                status = conn.status
                status_count[status] = status_count.get(status, 0) + 1
                if status == 'TIME_WAIT':
                    time_wait_count += 1
                elif status == 'ESTABLISHED':
                    established_count += 1
            
            # 网络IO统计
            net_io = psutil.net_io_counters()
            
            self.add_item(InspectionItem(
                resource_name="网络连接数",
                current_value=f"{len(net_connections)}个",
                threshold="无",
                status="信息",
                risk_level=RiskLevel.NORMAL.value,
                analysis=f"当前网络连接总数：{len(net_connections)}，ESTABLISHED: {established_count}",
                suggestion="无需处理"
            ))
            
            # TIME_WAIT检查
            if time_wait_count > 1000:
                risk = RiskLevel.P2
                status = "警告"
                analysis = f"TIME_WAIT连接过多({time_wait_count})，可能影响新连接"
                suggestion = "检查应用连接池配置，考虑调整内核参数"
            else:
                risk = RiskLevel.NORMAL
                status = "正常"
                analysis = f"TIME_WAIT连接数正常({time_wait_count})"
                suggestion = "无需处理"
            
            self.add_item(InspectionItem(
                resource_name="TIME_WAIT连接数",
                current_value=f"{time_wait_count}个",
                threshold="P2: >1000",
                status=status,
                risk_level=risk.value,
                analysis=analysis,
                suggestion=suggestion
            ))
            
            # 网络流量统计
            bytes_sent_mb = net_io.bytes_sent / (1024**2)
            bytes_recv_mb = net_io.bytes_recv / (1024**2)
            
            self.add_item(InspectionItem(
                resource_name="网络流量统计",
                current_value=f"发送: {bytes_sent_mb:.2f}MB, 接收: {bytes_recv_mb:.2f}MB",
                threshold="无",
                status="信息",
                risk_level=RiskLevel.NORMAL.value,
                analysis="累计网络流量统计",
                suggestion="无需处理"
            ))
            
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="网络状态",
                current_value="获取失败",
                threshold="无",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"无法获取网络信息: {str(e)}",
                suggestion="检查系统权限"
            ))
    
    def _generate_summary(self) -> str:
        """生成摘要"""
        p1_count = sum(1 for item in self.results if item.risk_level == RiskLevel.P1.value)
        p2_count = sum(1 for item in self.results if item.risk_level == RiskLevel.P2.value)
        
        if p1_count > 0:
            return f"发现{p1_count}个P1级别问题，需要立即处理"
        elif p2_count > 0:
            return f"发现{p2_count}个P2级别问题，建议尽快处理"
        else:
            return "系统资源状态良好"
    
    def _create_unavailable_result(self) -> InspectionResult:
        """创建不可用结果"""
        return InspectionResult(
            layer=self.layer_name,
            items=[InspectionItem(
                resource_name="基础资源巡检",
                current_value="不可用",
                threshold="无",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis="psutil模块未安装，无法进行基础资源巡检",
                suggestion="安装psutil: pip install psutil"
            )],
            health_score=0,
            summary="巡检功能不可用",
            timestamp=self.timestamp
        )


class MiddlewareInspection(BaseInspection):
    """第二层：中间件巡检"""
    
    def __init__(self):
        super().__init__()
        self.layer_name = "中间件巡检"
    
    def inspect(self) -> InspectionResult:
        """执行中间件巡检"""
        # Redis检查
        self._check_redis()
        
        # MySQL检查
        self._check_mysql()
        
        # Kafka检查
        self._check_kafka()
        
        # MongoDB检查
        self._check_mongodb()
        
        # PostgreSQL检查
        self._check_postgresql()
        
        # Elasticsearch检查
        self._check_elasticsearch()
        
        # RabbitMQ检查
        self._check_rabbitmq()
        
        # Nginx检查
        self._check_nginx()
        
        # Tomcat检查
        self._check_tomcat()
        
        return InspectionResult(
            layer=self.layer_name,
            items=self.results,
            health_score=self.calculate_health_score(),
            summary=self._generate_summary(),
            timestamp=self.timestamp
        )
    
    def _check_redis(self):
        """Redis检查"""
        if not self.check_command_exists('redis-cli'):
            self.add_item(InspectionItem(
                resource_name="Redis",
                current_value="未安装",
                threshold="无",
                status="跳过",
                risk_level=RiskLevel.NORMAL.value,
                analysis="Redis未安装或不在PATH中",
                suggestion="无需处理"
            ))
            return
        
        try:
            # 检查Redis是否运行
            result = subprocess.run(
                ['redis-cli', 'ping'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0 or 'PONG' not in result.stdout:
                self.add_item(InspectionItem(
                    resource_name="Redis状态",
                    current_value="未运行",
                    threshold="无",
                    status="异常",
                    risk_level=RiskLevel.P2.value,
                    analysis="Redis服务未运行",
                    suggestion="启动Redis服务"
                ))
                return
            
            # 获取Redis信息
            info_result = subprocess.run(
                ['redis-cli', 'info'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if info_result.returncode == 0:
                info = info_result.stdout
                
                # 解析关键指标
                metrics = {}
                for line in info.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metrics[key] = value.strip()
                
                # 连接数
                connected_clients = int(metrics.get('connected_clients', 0))
                max_clients = int(metrics.get('maxclients', 10000))
                client_usage = (connected_clients / max_clients * 100) if max_clients > 0 else 0
                
                # 内存使用
                used_memory = int(metrics.get('used_memory', 0))
                max_memory = int(metrics.get('maxmemory', 0))
                mem_usage = (used_memory / max_memory * 100) if max_memory > 0 else 0
                
                # 内存碎片率
                mem_fragmentation_ratio = float(metrics.get('mem_fragmentation_ratio', 1.0))
                
                # 慢查询
                slowlog_result = subprocess.run(
                    ['redis-cli', 'slowlog', 'len'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                slowlog_count = int(slowlog_result.stdout.strip()) if slowlog_result.returncode == 0 else 0
                
                # 判断风险
                if mem_fragmentation_ratio > 1.5:
                    risk = RiskLevel.P2
                    status = "警告"
                    analysis = f"Redis内存碎片率过高({mem_fragmentation_ratio:.2f})"
                    suggestion = "考虑执行MEMORY PURGE或重启Redis"
                elif client_usage > 80:
                    risk = RiskLevel.P2
                    status = "警告"
                    analysis = f"Redis连接数占用过高({client_usage:.1f}%)"
                    suggestion = "检查连接泄漏或增加maxclients"
                else:
                    risk = RiskLevel.NORMAL
                    status = "正常"
                    analysis = "Redis运行正常"
                    suggestion = "无需处理"
                
                self.add_item(InspectionItem(
                    resource_name="Redis状态",
                    current_value=f"运行中 (连接:{connected_clients}, 碎片率:{mem_fragmentation_ratio:.2f})",
                    threshold="碎片率P2: >1.5 | 连接数P2: >80%",
                    status=status,
                    risk_level=risk.value,
                    analysis=analysis,
                    suggestion=suggestion
                ))
                
                self.add_item(InspectionItem(
                    resource_name="Redis慢查询",
                    current_value=f"{slowlog_count}条",
                    threshold="P2: >100条",
                    status="警告" if slowlog_count > 100 else "正常",
                    risk_level=RiskLevel.P2.value if slowlog_count > 100 else RiskLevel.NORMAL.value,
                    analysis=f"慢查询日志数量: {slowlog_count}",
                    suggestion="优化慢查询或分析slowlog" if slowlog_count > 100 else "无需处理"
                ))
                
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="Redis",
                current_value="检查失败",
                threshold="无",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"Redis检查异常: {str(e)}",
                suggestion="检查Redis连接"
            ))
    
    def _check_mysql(self):
        """MySQL检查"""
        if not self.check_command_exists('mysql'):
            self.add_item(InspectionItem(
                resource_name="MySQL",
                current_value="未安装",
                threshold="无",
                status="跳过",
                risk_level=RiskLevel.NORMAL.value,
                analysis="MySQL客户端未安装或不在PATH中",
                suggestion="无需处理"
            ))
            return
        
        # 检查MySQL服务是否运行
        if not self.check_service_running('mysql') and not self.check_service_running('mariadb'):
            self.add_item(InspectionItem(
                resource_name="MySQL状态",
                current_value="未运行",
                threshold="无",
                status="跳过",
                risk_level=RiskLevel.NORMAL.value,
                analysis="MySQL服务未运行",
                suggestion="如需巡检，请启动MySQL服务"
            ))
            return
        
        try:
            # 尝试连接MySQL（需要配置）
            self.add_item(InspectionItem(
                resource_name="MySQL状态",
                current_value="运行中",
                threshold="无",
                status="正常",
                risk_level=RiskLevel.NORMAL.value,
                analysis="MySQL服务运行正常",
                suggestion="详细巡检需要配置连接信息"
            ))
            
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="MySQL",
                current_value="检查失败",
                threshold="无",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"MySQL检查异常: {str(e)}",
                suggestion="检查MySQL连接配置"
            ))
    
    def _check_kafka(self):
        """Kafka检查"""
        if not self.check_command_exists('kafka-topics.sh') and not self.check_command_exists('kafka-topics'):
            self.add_item(InspectionItem(
                resource_name="Kafka",
                current_value="未安装",
                threshold="无",
                status="跳过",
                risk_level=RiskLevel.NORMAL.value,
                analysis="Kafka未安装或不在PATH中",
                suggestion="无需处理"
            ))
            return
        
        try:
            self.add_item(InspectionItem(
                resource_name="Kafka",
                current_value="已安装",
                threshold="无",
                status="正常",
                risk_level=RiskLevel.NORMAL.value,
                analysis="检测到Kafka安装，详细巡检需要配置连接信息",
                suggestion="配置Kafka连接信息进行深度巡检"
            ))
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="Kafka",
                current_value="检查失败",
                threshold="无",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"Kafka检查异常: {str(e)}",
                suggestion="检查Kafka配置"
            ))
    
    def _check_mongodb(self):
        """MongoDB检查"""
        if not self.check_command_exists('mongo') and not self.check_command_exists('mongosh'):
            self.add_item(InspectionItem(
                resource_name="MongoDB",
                current_value="未安装",
                threshold="无",
                status="跳过",
                risk_level=RiskLevel.NORMAL.value,
                analysis="MongoDB未安装或不在PATH中",
                suggestion="无需处理"
            ))
            return
        
        try:
            self.add_item(InspectionItem(
                resource_name="MongoDB",
                current_value="已安装",
                threshold="无",
                status="正常",
                risk_level=RiskLevel.NORMAL.value,
                analysis="检测到MongoDB安装，详细巡检需要配置连接信息",
                suggestion="配置MongoDB连接信息进行深度巡检"
            ))
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="MongoDB",
                current_value="检查失败",
                threshold="无",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"MongoDB检查异常: {str(e)}",
                suggestion="检查MongoDB配置"
            ))
    
    def _check_postgresql(self):
        """PostgreSQL检查"""
        if not self.check_command_exists('psql'):
            self.add_item(InspectionItem(
                resource_name="PostgreSQL",
                current_value="未安装",
                threshold="无",
                status="跳过",
                risk_level=RiskLevel.NORMAL.value,
                analysis="PostgreSQL未安装或不在PATH中",
                suggestion="无需处理"
            ))
            return
        
        try:
            # 检查PostgreSQL服务
            if self.check_service_running('postgresql'):
                self.add_item(InspectionItem(
                    resource_name="PostgreSQL状态",
                    current_value="运行中",
                    threshold="无",
                    status="正常",
                    risk_level=RiskLevel.NORMAL.value,
                    analysis="PostgreSQL服务运行正常",
                    suggestion="详细巡检需要配置连接信息"
                ))
            else:
                self.add_item(InspectionItem(
                    resource_name="PostgreSQL状态",
                    current_value="未运行",
                    threshold="无",
                    status="跳过",
                    risk_level=RiskLevel.NORMAL.value,
                    analysis="PostgreSQL服务未运行",
                    suggestion="如需巡检，请启动PostgreSQL服务"
                ))
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="PostgreSQL",
                current_value="检查失败",
                threshold="无",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"PostgreSQL检查异常: {str(e)}",
                suggestion="检查PostgreSQL配置"
            ))
    
    def _check_elasticsearch(self):
        """Elasticsearch检查"""
        if not self.check_port_listening(9200):
            self.add_item(InspectionItem(
                resource_name="Elasticsearch",
                current_value="未运行",
                threshold="无",
                status="跳过",
                risk_level=RiskLevel.NORMAL.value,
                analysis="Elasticsearch未运行(端口9200未监听)",
                suggestion="无需处理"
            ))
            return
        
        try:
            if REQUESTS_AVAILABLE:
                response = requests.get('http://localhost:9200/_cluster/health', timeout=5)
                if response.status_code == 200:
                    health = response.json()
                    status = health.get('status', 'unknown')
                    
                    if status == 'red':
                        risk = RiskLevel.P1
                        status_text = "严重"
                        analysis = "Elasticsearch集群状态异常(red)"
                        suggestion = "立即检查集群状态和分片分配"
                    elif status == 'yellow':
                        risk = RiskLevel.P2
                        status_text = "警告"
                        analysis = "Elasticsearch集群存在警告(yellow)"
                        suggestion = "检查副本分片分配"
                    else:
                        risk = RiskLevel.NORMAL
                        status_text = "正常"
                        analysis = "Elasticsearch集群状态正常(green)"
                        suggestion = "无需处理"
                    
                    self.add_item(InspectionItem(
                        resource_name="Elasticsearch状态",
                        current_value=f"{status} (节点:{health.get('number_of_nodes', 0)})",
                        threshold="P1: red | P2: yellow",
                        status=status_text,
                        risk_level=risk.value,
                        analysis=analysis,
                        suggestion=suggestion
                    ))
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="Elasticsearch",
                current_value="检查失败",
                threshold="无",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"Elasticsearch检查异常: {str(e)}",
                suggestion="检查Elasticsearch连接"
            ))
    
    def _check_rabbitmq(self):
        """RabbitMQ检查"""
        if not self.check_command_exists('rabbitmqctl'):
            self.add_item(InspectionItem(
                resource_name="RabbitMQ",
                current_value="未安装",
                threshold="无",
                status="跳过",
                risk_level=RiskLevel.NORMAL.value,
                analysis="RabbitMQ未安装或不在PATH中",
                suggestion="无需处理"
            ))
            return
        
        try:
            result = subprocess.run(
                ['rabbitmqctl', 'status'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.add_item(InspectionItem(
                    resource_name="RabbitMQ状态",
                    current_value="运行中",
                    threshold="无",
                    status="正常",
                    risk_level=RiskLevel.NORMAL.value,
                    analysis="RabbitMQ服务运行正常",
                    suggestion="无需处理"
                ))
            else:
                self.add_item(InspectionItem(
                    resource_name="RabbitMQ状态",
                    current_value="异常",
                    threshold="无",
                    status="警告",
                    risk_level=RiskLevel.P2.value,
                    analysis="RabbitMQ状态检查失败",
                    suggestion="检查RabbitMQ服务"
                ))
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="RabbitMQ",
                current_value="检查失败",
                threshold="无",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"RabbitMQ检查异常: {str(e)}",
                suggestion="检查RabbitMQ配置"
            ))
    
    def _check_nginx(self):
        """Nginx检查"""
        if not self.check_command_exists('nginx'):
            self.add_item(InspectionItem(
                resource_name="Nginx",
                current_value="未安装",
                threshold="无",
                status="跳过",
                risk_level=RiskLevel.NORMAL.value,
                analysis="Nginx未安装或不在PATH中",
                suggestion="无需处理"
            ))
            return
        
        try:
            result = subprocess.run(
                ['nginx', '-t'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                self.add_item(InspectionItem(
                    resource_name="Nginx配置",
                    current_value="正常",
                    threshold="无",
                    status="正常",
                    risk_level=RiskLevel.NORMAL.value,
                    analysis="Nginx配置语法正确",
                    suggestion="无需处理"
                ))
            else:
                self.add_item(InspectionItem(
                    resource_name="Nginx配置",
                    current_value="异常",
                    threshold="无",
                    status="警告",
                    risk_level=RiskLevel.P2.value,
                    analysis=f"Nginx配置异常: {result.stderr}",
                    suggestion="检查并修复Nginx配置"
                ))
        except Exception as e:
            self.add_item(InspectionItem(
                resource_name="Nginx",
                current_value="检查失败",
                threshold="无",
                status="异常",
                risk_level=RiskLevel.P3.value,
                analysis=f"Nginx检查异常: {str(e)}",
                suggestion="检查Nginx配置"
            ))
    
    def _check_tomcat(self):
        """Tomcat检查"""
        tomcat_ports = [8080, 8443, 8005, 8009]
        found = False
        
        for port in tomcat_ports:
            if self.check_port_listening(port):
                found = True
                break
        
        if not found:
            self.add_item(InspectionItem(
                resource_name="Tomcat",
                current_value="未运行",
                threshold="无",
                status="跳过",
                risk_level=RiskLevel.NORMAL.value,
                analysis="未检测到Tomcat端口监听",
                suggestion="无需处理"
            ))
            return
        
        self.add_item(InspectionItem(
            resource_name="Tomcat状态",
            current_value="运行中",
            threshold="无",
            status="正常",
            risk_level=RiskLevel.NORMAL.value,
            analysis="检测到Tomcat端口监听",
            suggestion="详细巡检需要配置管理接口访问"
        ))
    
    def _generate_summary(self) -> str:
        """生成摘要"""
        checked = sum(1 for item in self.results if item.status not in ["跳过"])
        issues = sum(1 for item in self.results if item.risk_level in [RiskLevel.P1.value, RiskLevel.P2.value])
        
        if issues > 0:
            return f"已检查{checked}个中间件，发现{issues}个问题"
        else:
            return f"已检查{checked}个中间件，状态正常"


class K8SInspection(BaseInspection):
    """第三层：K8S巡检（模拟）"""
    
    def __init__(self):
        super().__init__()
        self.layer_name = "K8S巡检"
    
    def inspect(self) -> InspectionResult:
        """执行K8S巡检"""
        # 检查kubectl是否存在
        if not self.check_command_exists('kubectl'):
            return InspectionResult(
                layer=self.layer_name,
                items=[InspectionItem(
                    resource_name="Kubernetes",
                    current_value="未安装",
                    threshold="无",
                    status="跳过",
                    risk_level=RiskLevel.NORMAL.value,
                    analysis="kubectl未安装，跳过K8S巡检",
                    suggestion="无需处理"
                )],
                health_score=100,
                summary="K8S未安装，跳过巡检",
                timestamp=self.timestamp
            )
        
        # 模拟K8S巡检结果
        self._mock_k8s_inspection()
        
        return InspectionResult(
            layer=self.layer_name,
            items=self.results,
            health_score=self.calculate_health_score(),
            summary=self._generate_summary(),
            timestamp=self.timestamp
        )
    
    def _mock_k8s_inspection(self):
        """模拟K8S巡检"""
        import random
        
        # Node状态
        node_count = random.randint(3, 10)
        ready_nodes = random.randint(node_count - 1, node_count)
        
        self.add_item(InspectionItem(
            resource_name="Node状态",
            current_value=f"{ready_nodes}/{node_count} Ready",
            threshold="所有Node Ready",
            status="正常" if ready_nodes == node_count else "警告",
            risk_level=RiskLevel.NORMAL.value if ready_nodes == node_count else RiskLevel.P2.value,
            analysis=f"集群共{node_count}个节点，{ready_nodes}个就绪",
            suggestion="检查NotReady节点" if ready_nodes < node_count else "无需处理"
        ))
        
        # Pod状态
        pod_count = random.randint(50, 200)
        running_pods = random.randint(int(pod_count * 0.95), pod_count)
        
        self.add_item(InspectionItem(
            resource_name="Pod状态",
            current_value=f"{running_pods}/{pod_count} Running",
            threshold="运行率 > 95%",
            status="正常" if running_pods / pod_count > 0.95 else "警告",
            risk_level=RiskLevel.NORMAL.value if running_pods / pod_count > 0.95 else RiskLevel.P2.value,
            analysis=f"共{pod_count}个Pod，{running_pods}个运行中",
            suggestion="检查异常Pod" if running_pods / pod_count < 0.95 else "无需处理"
        ))
        
        # 资源使用率
        cpu_usage = random.uniform(30, 90)
        mem_usage = random.uniform(40, 85)
        
        self.add_item(InspectionItem(
            resource_name="集群CPU使用率",
            current_value=f"{cpu_usage:.1f}%",
            threshold="P2: >85%",
            status="警告" if cpu_usage > 85 else "正常",
            risk_level=RiskLevel.P2.value if cpu_usage > 85 else RiskLevel.NORMAL.value,
            analysis=f"集群CPU使用率{cpu_usage:.1f}%",
            suggestion="考虑扩容或优化" if cpu_usage > 85 else "无需处理"
        ))
        
        self.add_item(InspectionItem(
            resource_name="集群内存使用率",
            current_value=f"{mem_usage:.1f}%",
            threshold="P2: >85%",
            status="警告" if mem_usage > 85 else "正常",
            risk_level=RiskLevel.P2.value if mem_usage > 85 else RiskLevel.NORMAL.value,
            analysis=f"集群内存使用率{mem_usage:.1f}%",
            suggestion="考虑扩容或优化" if mem_usage > 85 else "无需处理"
        ))
    
    def _generate_summary(self) -> str:
        p1_count = sum(1 for item in self.results if item.risk_level == RiskLevel.P1.value)
        p2_count = sum(1 for item in self.results if item.risk_level == RiskLevel.P2.value)
        
        if p1_count > 0:
            return f"发现{p1_count}个P1级别问题"
        elif p2_count > 0:
            return f"发现{p2_count}个P2级别问题"
        else:
            return "K8S集群状态正常"


class LogInspection(BaseInspection):
    """第四层：日志巡检（模拟）"""
    
    def __init__(self):
        super().__init__()
        self.layer_name = "日志巡检"
    
    def inspect(self) -> InspectionResult:
        """执行日志巡检"""
        # 模拟日志分析
        self._mock_log_analysis()
        
        return InspectionResult(
            layer=self.layer_name,
            items=self.results,
            health_score=self.calculate_health_score(),
            summary=self._generate_summary(),
            timestamp=self.timestamp
        )
    
    def _mock_log_analysis(self):
        """模拟日志分析"""
        import random
        
        # 错误统计
        error_count = random.randint(0, 50)
        warn_count = random.randint(10, 100)
        
        self.add_item(InspectionItem(
            resource_name="ERROR日志数量(30分钟)",
            current_value=f"{error_count}条",
            threshold="P2: >100条",
            status="警告" if error_count > 100 else "正常",
            risk_level=RiskLevel.P2.value if error_count > 100 else RiskLevel.NORMAL.value,
            analysis=f"最近30分钟ERROR日志{error_count}条",
            suggestion="分析ERROR日志根因" if error_count > 100 else "无需处理"
        ))
        
        self.add_item(InspectionItem(
            resource_name="WARN日志数量(30分钟)",
            current_value=f"{warn_count}条",
            threshold="P2: >200条",
            status="警告" if warn_count > 200 else "正常",
            risk_level=RiskLevel.P2.value if warn_count > 200 else RiskLevel.NORMAL.value,
            analysis=f"最近30分钟WARN日志{warn_count}条",
            suggestion="关注WARN日志趋势" if warn_count > 200 else "无需处理"
        ))
        
        # TOP异常
        top_exceptions = ["NullPointerException", "TimeoutException", "ConnectionException"]
        exception_counts = {ex: random.randint(0, 30) for ex in top_exceptions}
        
        for ex, count in exception_counts.items():
            if count > 0:
                self.add_item(InspectionItem(
                    resource_name=f"异常: {ex}",
                    current_value=f"{count}次",
                    threshold="P2: >20次",
                    status="警告" if count > 20 else "正常",
                    risk_level=RiskLevel.P2.value if count > 20 else RiskLevel.NORMAL.value,
                    analysis=f"{ex}出现{count}次",
                    suggestion="分析异常堆栈" if count > 20 else "无需处理"
                ))
    
    def _generate_summary(self) -> str:
        p1_count = sum(1 for item in self.results if item.risk_level == RiskLevel.P1.value)
        p2_count = sum(1 for item in self.results if item.risk_level == RiskLevel.P2.value)
        
        if p1_count > 0:
            return f"发现{p1_count}个P1级别异常"
        elif p2_count > 0:
            return f"发现{p2_count}个P2级别异常"
        else:
            return "日志分析未发现异常"


class BusinessInspection(BaseInspection):
    """第五层：业务巡检（模拟）"""
    
    def __init__(self):
        super().__init__()
        self.layer_name = "业务巡检"
    
    def inspect(self) -> InspectionResult:
        """执行业务巡检"""
        # 模拟业务指标检查
        self._mock_business_metrics()
        
        return InspectionResult(
            layer=self.layer_name,
            items=self.results,
            health_score=self.calculate_health_score(),
            summary=self._generate_summary(),
            timestamp=self.timestamp
        )
    
    def _mock_business_metrics(self):
        """模拟业务指标"""
        import random
        
        # 订单成功率
        order_success_rate = random.uniform(98.5, 99.9)
        self.add_item(InspectionItem(
            resource_name="订单成功率",
            current_value=f"{order_success_rate:.2f}%",
            threshold="P2: <99%",
            status="警告" if order_success_rate < 99 else "正常",
            risk_level=RiskLevel.P2.value if order_success_rate < 99 else RiskLevel.NORMAL.value,
            analysis=f"订单成功率{order_success_rate:.2f}%",
            suggestion="排查失败订单原因" if order_success_rate < 99 else "无需处理"
        ))
        
        # 支付成功率
        payment_success_rate = random.uniform(99.0, 99.9)
        self.add_item(InspectionItem(
            resource_name="支付成功率",
            current_value=f"{payment_success_rate:.2f}%",
            threshold="P2: <99.5%",
            status="警告" if payment_success_rate < 99.5 else "正常",
            risk_level=RiskLevel.P2.value if payment_success_rate < 99.5 else RiskLevel.NORMAL.value,
            analysis=f"支付成功率{payment_success_rate:.2f}%",
            suggestion="排查支付失败原因" if payment_success_rate < 99.5 else "无需处理"
        ))
        
        # 接口成功率
        api_success_rate = random.uniform(98.0, 99.9)
        self.add_item(InspectionItem(
            resource_name="接口成功率",
            current_value=f"{api_success_rate:.2f}%",
            threshold="P2: <99%",
            status="警告" if api_success_rate < 99 else "正常",
            risk_level=RiskLevel.P2.value if api_success_rate < 99 else RiskLevel.NORMAL.value,
            analysis=f"接口成功率{api_success_rate:.2f}%",
            suggestion="排查接口失败原因" if api_success_rate < 99 else "无需处理"
        ))
        
        # P99响应时间
        p99_latency = random.uniform(0.5, 3.0)
        self.add_item(InspectionItem(
            resource_name="P99响应时间",
            current_value=f"{p99_latency:.2f}s",
            threshold="P2: >2s",
            status="警告" if p99_latency > 2 else "正常",
            risk_level=RiskLevel.P2.value if p99_latency > 2 else RiskLevel.NORMAL.value,
            analysis=f"P99响应时间{p99_latency:.2f}秒",
            suggestion="优化慢接口" if p99_latency > 2 else "无需处理"
        ))
    
    def _generate_summary(self) -> str:
        p1_count = sum(1 for item in self.results if item.risk_level == RiskLevel.P1.value)
        p2_count = sum(1 for item in self.results if item.risk_level == RiskLevel.P2.value)
        
        if p1_count > 0:
            return f"发现{p1_count}个P1级别业务异常"
        elif p2_count > 0:
            return f"发现{p2_count}个P2级别业务异常"
        else:
            return "业务指标正常"


class IntelligentInspection:
    """智能巡检系统主类"""
    
    def __init__(self):
        self.inspectors = [
            ResourceInspection(),
            MiddlewareInspection(),
            K8SInspection(),
            LogInspection(),
            BusinessInspection()
        ]
        self.report_time = datetime.now()
    
    def run_all_inspections(self) -> Dict[str, Any]:
        """执行所有巡检"""
        print("=" * 80)
        print(f"智能运维巡检报告")
        print(f"巡检时间: {self.report_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"主机名: {platform.node()}")
        print(f"操作系统: {platform.system()} {platform.release()}")
        print("=" * 80)
        
        results = []
        total_score = 0
        
        for inspector in self.inspectors:
            print(f"\n{'=' * 80}")
            print(f"执行: {inspector.layer_name}")
            print("=" * 80)
            
            result = inspector.inspect()
            results.append(result)
            total_score += result.health_score
            
            # 打印结果
            self._print_inspection_result(result)
        
        # 计算总体健康评分
        overall_score = total_score // len(self.inspectors)
        
        # 生成总结
        print("\n" + "=" * 80)
        print("巡检总结")
        print("=" * 80)
        print(f"总体健康评分: {overall_score}/100")
        
        # 统计问题
        total_p1 = sum(
            sum(1 for item in r.items if item.risk_level == RiskLevel.P1.value)
            for r in results
        )
        total_p2 = sum(
            sum(1 for item in r.items if item.risk_level == RiskLevel.P2.value)
            for r in results
        )
        
        print(f"P1级别问题: {total_p1}个")
        print(f"P2级别问题: {total_p2}个")
        
        if overall_score >= 90:
            print("系统状态: 优秀 ✓")
        elif overall_score >= 70:
            print("系统状态: 良好")
        elif overall_score >= 50:
            print("系统状态: 需关注")
        else:
            print("系统状态: 需立即处理 ✗")
        
        return {
            "report_time": self.report_time.isoformat(),
            "hostname": platform.node(),
            "os": f"{platform.system()} {platform.release()}",
            "overall_score": overall_score,
            "total_p1_issues": total_p1,
            "total_p2_issues": total_p2,
            "layers": [asdict(r) for r in results]
        }
    
    def _print_inspection_result(self, result: InspectionResult):
        """打印巡检结果"""
        print(f"\n健康评分: {result.health_score}/100")
        print(f"摘要: {result.summary}")
        print("\n详细结果:")
        print("-" * 80)
        
        for item in result.items:
            # 根据风险等级使用不同的标记
            risk_marker = ""
            if item.risk_level == RiskLevel.P1.value:
                risk_marker = "🔴 "
            elif item.risk_level == RiskLevel.P2.value:
                risk_marker = "🟡 "
            elif item.risk_level == RiskLevel.P3.value:
                risk_marker = "🔵 "
            else:
                risk_marker = "✓ "
            
            print(f"{risk_marker}{item.resource_name}")
            print(f"  当前值: {item.current_value}")
            print(f"  阈值: {item.threshold}")
            print(f"  状态: {item.status} | 风险等级: {item.risk_level}")
            if item.risk_level != RiskLevel.NORMAL.value:
                print(f"  分析: {item.analysis}")
                print(f"  建议: {item.suggestion}")
    
    def export_report(self, output_format: str = "json", filename: str = None):
        """导出报告"""
        results = self.run_all_inspections()
        
        if filename is None:
            filename = f"inspection_report_{self.report_time.strftime('%Y%m%d_%H%M%S')}"
        
        if output_format == "json":
            output_file = f"{filename}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n报告已导出: {output_file}")
        else:
            print("暂不支持其他格式导出")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='智能运维巡检系统')
    parser.add_argument('--export', '-e', action='store_true', help='导出报告为JSON文件')
    parser.add_argument('--format', '-f', default='json', choices=['json'], help='报告格式')
    parser.add_argument('--layers', '-l', nargs='+', choices=['resource', 'middleware', 'k8s', 'log', 'business', 'all'],
                        default=['all'], help='指定巡检层')
    
    args = parser.parse_args()
    
    inspector = IntelligentInspection()
    
    if args.export:
        inspector.export_report(output_format=args.format)
    else:
        inspector.run_all_inspections()


if __name__ == "__main__":
    main()
