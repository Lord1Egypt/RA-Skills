"""
增强版动态授权监控器

集成：
1. 异常检测与上报
2. 批量审批能力
3. 原有的动态分级 + HTTP/TOTP授权
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

from ..reference_monitor import (
    AccessOperation, AccessDecision, AccessResult, DataLevel
)
from .dynamic_full_integration import DynamicAuthorizationAccessMonitor
from .dynamic_models import AggregationType
from .dynamic_integration import DynamicAccessContext
from ..anomaly_detection import (
    AnomalyDetector, AnomalyEvent, AnomalyType, AnomalySeverity,
    ConsoleReporter, LoggingReporter, create_default_detector
)
from ..bulk_auth import (
    BulkAuthorizationService, BulkAuthRequest, BulkAuthAPI,
    generate_bulk_auth_page
)

logger = logging.getLogger(__name__)


class EnhancedAuthorizationMonitor(DynamicAuthorizationAccessMonitor):
    """
    增强版授权监控器
    
    在原有功能基础上增加：
    - 异常检测与上报
    - 批量审批能力
    """
    
    def __init__(self, *args, enable_anomaly_detection: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 异常检测
        self.enable_anomaly_detection = enable_anomaly_detection
        self.anomaly_detector: Optional[AnomalyDetector] = None
        
        # 批量授权
        self.bulk_service: Optional[BulkAuthorizationService] = None
        self.bulk_api: Optional[BulkAuthAPI] = None
        
        # 检测到的异常记录
        self._detected_anomalies: List[AnomalyEvent] = []
    
    async def initialize(self, http_port: int = 0, totp_password: str = "demo-password"):
        """初始化增强版系统"""
        print("\n" + "="*70)
        print("🚀 初始化增强版动态分级 + 授权联动系统")
        print("="*70)
        
        # 1. 初始化父类
        await super().initialize(http_port, totp_password)
        
        # 2. 初始化异常检测
        if self.enable_anomaly_detection:
            print("\n[4/5] 初始化异常检测...")
            self.anomaly_detector = create_default_detector()
            # 添加自定义上报器，记录到本地
            self.anomaly_detector.add_reporter(self._on_anomaly_detected)
            print("   ✅ 异常检测初始化完成")
        
        # 3. 初始化批量授权
        print("\n[5/5] 初始化批量授权服务...")
        self.bulk_service = BulkAuthorizationService()
        self.bulk_api = BulkAuthAPI(self.bulk_service)
        print("   ✅ 批量授权服务初始化完成")
        
        print("\n" + "="*70)
        print("🎯 增强版系统初始化完成！")
        print("="*70)
    
    def _on_anomaly_detected(self, anomaly: AnomalyEvent):
        """异常检测回调"""
        self._detected_anomalies.append(anomaly)
        
        # 严重异常可以触发额外响应
        if anomaly.severity == AnomalySeverity.CRITICAL:
            logger.critical(f"🚨 严重安全异常: {anomaly.description}")
            # 这里可以添加：锁定Agent、通知CEO等响应
    
    async def check_access_with_anomaly_detection(
        self,
        agent_id: str,
        file_path: str,
        operation: AccessOperation,
        dynamic_context: DynamicAccessContext,
        base_context: Optional[Dict[str, Any]] = None
    ) -> AccessResult:
        """
        带异常检测的访问检查
        
        流程：
        1. 执行标准授权流程
        2. 分析访问行为，检测异常
        3. 如有异常，触发上报
        4. 严重异常可能阻断访问
        """
        # 执行标准授权流程
        result = await self.check_access_with_full_pipeline(
            agent_id=agent_id,
            file_path=file_path,
            operation=operation,
            dynamic_context=dynamic_context,
            base_context=base_context
        )
        
        # 异常检测
        if self.anomaly_detector and self.enable_anomaly_detection:
            # 构建检测上下文
            detection_context = {
                "resource_path": file_path,
                "operation": operation,
                **(base_context or {}),
                "is_bulk_operation": False
            }
            
            # 分析访问
            anomaly = self.anomaly_detector.analyze_access(
                agent_id=agent_id,
                resource_path=file_path,
                operation=operation,
                decision=result.decision,
                data_level=result.level,
                context=detection_context
            )
            
            # 如果检测到严重异常，可以覆盖决策
            if anomaly and anomaly.severity == AnomalySeverity.CRITICAL:
                logger.critical(f"严重异常阻断访问: {anomaly.description}")
                # 创建阻断结果
                return AccessResult(
                    decision=AccessDecision.DENY,
                    token=None,
                    expires_at=None,
                    level=result.level,
                    policy="anomaly_blocked",
                    reason=f"安全异常阻断: {anomaly.anomaly_type.value}",
                    audit_record_id=""
                )
        
        return result
    
    async def check_bulk_with_bulk_auth(
        self,
        agent_id: str,
        file_paths: List[str],
        operation: AccessOperation,
        aggregation_type: AggregationType,
        base_context: Optional[Dict[str, Any]] = None,
        use_bulk_approval: bool = True
    ) -> Dict[str, Any]:
        """
        带批量授权的批量访问检查
        
        Args:
            agent_id: Agent ID
            file_paths: 文件路径列表
            operation: 操作类型
            aggregation_type: 汇聚类型
            base_context: 基础上下文
            use_bulk_approval: 是否使用批量审批（False=逐个审批）
        
        Returns:
            包含访问结果和批量请求信息的字典
        """
        print(f"\n{'='*70}")
        print(f"📦 批量授权流程: {len(file_paths)} 个文件")
        print(f"{'='*70}")
        
        # 1. 批量动态分级
        print("\n📍 Step 1: 批量动态分级")
        results, stats = await self.check_bulk_access(
            agent_id=agent_id,
            file_paths=file_paths,
            operation=operation,
            aggregation_type=aggregation_type,
            base_context=base_context
        )
        
        print(f"   汇总: {stats['total']} 文件, {stats['upgraded']} 升级")
        
        # 2. 异常检测（批量操作）
        if self.anomaly_detector and self.enable_anomaly_detection:
            detection_context = {
                "is_bulk_operation": True,
                "bulk_record_count": len(file_paths),
                "upgraded_count": stats.get('upgraded', 0),
                "operation": operation,
            }
            
            # 使用最高级别进行检测
            max_level = self._get_max_level(results)
            
            anomaly = self.anomaly_detector.analyze_access(
                agent_id=agent_id,
                resource_path="bulk_operation",
                operation=operation,
                decision=AccessDecision.PENDING,  # 批量操作初始为待定
                data_level=max_level,
                context=detection_context
            )
            
            if anomaly and anomaly.severity in (AnomalySeverity.HIGH, AnomalySeverity.CRITICAL):
                print(f"\n⚠️ 检测到批量操作异常: {anomaly.description}")
                # 可以在这里添加额外验证要求
        
        # 3. 批量授权
        if use_bulk_approval and self.bulk_service:
            print("\n📍 Step 2: 创建批量授权请求")
            
            # 构建批量项目
            bulk_items = []
            for i, (path, result) in enumerate(zip(file_paths, results)):
                # 获取动态调整信息
                adjustment_info = self.get_dynamic_adjustment_info(result)
                is_upgraded = adjustment_info and adjustment_info.get('adjustment_type') == 'UPGRADE'
                
                bulk_items.append({
                    "resource_path": path,
                    "data_level": result.level.value,
                    "adjusted_level": result.level.value,
                    "is_upgraded": is_upgraded,
                    "note": adjustment_info.get('adjustment_reason', '') if adjustment_info else ''
                })
            
            # 创建批量请求
            bulk_request = self.bulk_service.create_bulk_request(
                agent_id=agent_id,
                items=bulk_items,
                operation=operation.value,
                context=base_context
            )
            
            print(f"   ✅ 批量请求创建: {bulk_request.request_id}")
            print(f"   📊 摘要: {bulk_request.total_count} 项, {bulk_request.upgraded_count} 升级")
            
            # 构建确认URL
            bulk_url = f"http://127.0.0.1:{self._http_port}/ui/bulk/{bulk_request.request_id}"
            print(f"   🔗 批量审批页面: {bulk_url}")
            
            # 演示模式自动批准
            if self._auto_approve:
                await asyncio.sleep(2)
                self.bulk_service.confirm_bulk(
                    request_id=bulk_request.request_id,
                    user_identifier="demo_user"
                )
                print("   [演示模式] 已自动批准")
            
            return {
                "bulk_request_id": bulk_request.request_id,
                "bulk_url": bulk_url,
                "classifications": results,
                "stats": stats,
                "pending_approval": not self._auto_approve
            }
        else:
            # 使用原有逐个授权逻辑
            results, stats = await self.check_bulk_with_full_pipeline(
                agent_id=agent_id,
                file_paths=file_paths,
                operation=operation,
                aggregation_type=aggregation_type,
                base_context=base_context
            )
            
            return {
                "bulk_request_id": None,
                "classifications": results,
                "stats": stats,
                "pending_approval": False
            }
    
    def get_bulk_request_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """获取批量请求状态"""
        if self.bulk_service:
            return self.bulk_service.get_request_status(request_id)
        return None
    
    def confirm_bulk_request(self, request_id: str, user_identifier: Optional[str] = None,
                            approved_item_ids: Optional[List[str]] = None) -> bool:
        """确认批量请求"""
        if self.bulk_service:
            return self.bulk_service.confirm_bulk(request_id, user_identifier, approved_item_ids)
        return False
    
    def deny_bulk_request(self, request_id: str, user_identifier: Optional[str] = None) -> bool:
        """拒绝批量请求"""
        if self.bulk_service:
            return self.bulk_service.deny_bulk(request_id, user_identifier)
        return False
    
    def get_detected_anomalies(self, severity: Optional[AnomalySeverity] = None) -> List[AnomalyEvent]:
        """获取检测到的异常列表"""
        if severity:
            return [a for a in self._detected_anomalies if a.severity == severity]
        return self._detected_anomalies.copy()
    
    def get_anomaly_stats(self) -> Dict[str, Any]:
        """获取异常检测统计"""
        if self.anomaly_detector:
            stats = self.anomaly_detector.get_stats()
            stats["detected_in_session"] = len(self._detected_anomalies)
            stats["by_severity"] = {
                "critical": len([a for a in self._detected_anomalies if a.severity == AnomalySeverity.CRITICAL]),
                "high": len([a for a in self._detected_anomalies if a.severity == AnomalySeverity.HIGH]),
                "medium": len([a for a in self._detected_anomalies if a.severity == AnomalySeverity.MEDIUM]),
                "low": len([a for a in self._detected_anomalies if a.severity == AnomalySeverity.LOW]),
            }
            return stats
        return {}
    
    def _get_max_level(self, results: List[AccessResult]) -> DataLevel:
        """从结果列表中获取最高级别"""
        level_order = {
            "L1-PUBLIC": 1,
            "L2-INTERNAL": 2,
            "L3-RESTRICTED": 3,
            "L4-CONFIDENTIAL": 4,
            "L5-SECRET": 5,
            "L6-CRITICAL": 6
        }
        
        max_result = max(
            results,
            key=lambda r: level_order.get(r.level.value, 0)
        )
        return max_result.level
    
    def get_enhanced_summary(self) -> Dict[str, Any]:
        """获取增强版系统摘要"""
        base_summary = self.get_authorization_summary()
        
        return {
            **base_summary,
            "anomaly_detection": {
                "enabled": self.enable_anomaly_detection and self.anomaly_detector is not None,
                "stats": self.get_anomaly_stats()
            },
            "bulk_authorization": {
                "enabled": self.bulk_service is not None,
                "pending_requests": len(self.bulk_service.list_requests()) if self.bulk_service else 0
            }
        }
    
    def generate_bulk_auth_page_html(self, request_id: str) -> Optional[str]:
        """生成批量授权页面HTML"""
        if not self.bulk_service:
            return None
        
        request = self.bulk_service.store.get(request_id)
        if not request:
            return None
        
        return generate_bulk_auth_page(request, self._http_port)


def create_enhanced_monitor(enable_anomaly_detection: bool = True) -> EnhancedAuthorizationMonitor:
    """创建增强版监控器"""
    return EnhancedAuthorizationMonitor(enable_anomaly_detection=enable_anomaly_detection)
