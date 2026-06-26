#!/usr/bin/env python3
"""
合规审计日志模块
满足等保 2.0、个保法、数据安全法要求
"""

import os
import json
import hashlib
import base64
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


@dataclass
class AuditLogEntry:
    """审计日志条目"""
    timestamp: str
    log_id: str
    user_id: str
    action: str  # parse/ask/summarize/extract/search
    file_name: str
    file_size: int
    file_hash: str
    result: str  # success/failed
    metadata: Dict[str, Any]
    error_message: str = ""
    ip_address: str = "127.0.0.1"
    session_id: str = ""


class ComplianceLogger:
    """
    合规审计日志器
    加密存储、不可篡改、支持审计报告导出
    """
    
    def __init__(self, log_dir: str = None, 
                 encryption_key: str = None,
                 retention_days: int = 90):
        """
        初始化日志器
        
        Args:
            log_dir: 日志目录
            encryption_key: 加密密钥
            retention_days: 日志保留天数
        """
        if log_dir is None:
            base_dir = Path(__file__).parent.parent
            log_dir = base_dir / "data" / "audit_logs"
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.retention_days = retention_days
        
        # 初始化加密
        self.encryption_key = encryption_key or self._generate_key()
        self.cipher = Fernet(self.encryption_key)
        
        # 当前日志文件
        self.current_log_file = self._get_current_log_file()
        
        # 清理过期日志
        self._cleanup_old_logs()
    
    def _generate_key(self) -> bytes:
        """生成加密密钥"""
        password = b"local_data_ai_secret_key"
        salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def _get_current_log_file(self) -> Path:
        """获取当前日志文件"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.log_dir / f"audit_{today}.log"
    
    def log_operation(self, user_id: str, action: str, 
                     file_name: str, file_size: int,
                     result: str, metadata: Dict = None,
                     error_message: str = "",
                     session_id: str = "") -> str:
        """
        记录操作日志
        
        Args:
            user_id: 用户标识
            action: 操作类型
            file_name: 文件名
            file_size: 文件大小
            result: 操作结果
            metadata: 额外元数据
            error_message: 错误信息
            session_id: 会话标识
            
        Returns:
            日志 ID
        """
        # 计算文件哈希
        file_hash = self._calculate_file_hash(file_name)
        
        # 创建日志条目
        entry = AuditLogEntry(
            timestamp=datetime.now().isoformat(),
            log_id=self._generate_log_id(),
            user_id=user_id,
            action=action,
            file_name=file_name,
            file_size=file_size,
            file_hash=file_hash,
            result=result,
            metadata=metadata or {},
            error_message=error_message,
            session_id=session_id
        )
        
        # 加密存储
        self._write_log_entry(entry)
        
        return entry.log_id
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """计算文件哈希（如果文件存在）"""
        if not os.path.exists(file_path):
            return ""
        
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return ""
    
    def _generate_log_id(self) -> str:
        """生成日志 ID"""
        import uuid
        return f"log_{uuid.uuid4().hex[:16]}_{int(datetime.now().timestamp())}"
    
    def _write_log_entry(self, entry: AuditLogEntry):
        """写入日志条目（加密）"""
        # 转换为字典
        entry_dict = asdict(entry)
        
        # 添加完整性校验
        entry_dict['integrity_hash'] = self._calculate_integrity_hash(entry_dict)
        
        # JSON 序列化
        json_data = json.dumps(entry_dict, ensure_ascii=False)
        
        # 加密
        encrypted_data = self.cipher.encrypt(json_data.encode())
        
        # 写入文件
        with open(self.current_log_file, 'ab') as f:
            f.write(encrypted_data + b"\n")
    
    def _calculate_integrity_hash(self, entry_dict: Dict) -> str:
        """计算完整性校验哈希"""
        # 排除已有的 integrity_hash
        data = {k: v for k, v in entry_dict.items() if k != 'integrity_hash'}
        json_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def read_logs(self, start_date: str = None, end_date: str = None,
                  user_id: str = None, action: str = None) -> List[AuditLogEntry]:
        """
        读取日志
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            user_id: 用户过滤
            action: 操作类型过滤
            
        Returns:
            日志条目列表
        """
        logs = []
        
        # 确定日期范围
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # 遍历日志文件
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current <= end:
            log_file = self.log_dir / f"audit_{current.strftime('%Y-%m-%d')}.log"
            
            if log_file.exists():
                day_logs = self._read_log_file(log_file)
                logs.extend(day_logs)
            
            current += timedelta(days=1)
        
        # 过滤
        if user_id:
            logs = [log for log in logs if log.user_id == user_id]
        if action:
            logs = [log for log in logs if log.action == action]
        
        return logs
    
    def _read_log_file(self, log_file: Path) -> List[AuditLogEntry]:
        """读取单个日志文件"""
        logs = []
        
        with open(log_file, 'rb') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # 解密
                    decrypted_data = self.cipher.decrypt(line)
                    entry_dict = json.loads(decrypted_data.decode())
                    
                    # 验证完整性
                    stored_hash = entry_dict.pop('integrity_hash', '')
                    calculated_hash = self._calculate_integrity_hash(entry_dict)
                    
                    if stored_hash != calculated_hash:
                        print(f"[ComplianceLogger] 警告: 日志完整性校验失败")
                        continue
                    
                    logs.append(AuditLogEntry(**entry_dict))
                    
                except Exception as e:
                    print(f"[ComplianceLogger] 读取日志条目失败: {e}")
        
        return logs
    
    def export_audit_report(self, start_date: str, end_date: str,
                           format: str = "pdf",
                           include_watermark: bool = True) -> str:
        """
        导出审计报告
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            format: 导出格式 (pdf/excel/json)
            include_watermark: 是否添加水印
            
        Returns:
            报告文件路径
        """
        # 读取日志
        logs = self.read_logs(start_date, end_date)
        
        # 生成报告
        report_data = self._generate_report_data(logs, start_date, end_date)
        
        # 导出
        if format == "json":
            return self._export_json(report_data, include_watermark)
        elif format == "excel":
            return self._export_excel(report_data, include_watermark)
        else:
            return self._export_pdf(report_data, include_watermark)
    
    def _generate_report_data(self, logs: List[AuditLogEntry],
                             start_date: str, end_date: str) -> Dict:
        """生成报告数据"""
        total_operations = len(logs)
        success_count = sum(1 for log in logs if log.result == "success")
        failed_count = total_operations - success_count
        
        # 按操作类型统计
        action_stats = {}
        for log in logs:
            action_stats[log.action] = action_stats.get(log.action, 0) + 1
        
        # 按用户统计
        user_stats = {}
        for log in logs:
            user_stats[log.user_id] = user_stats.get(log.user_id, 0) + 1
        
        return {
            "report_info": {
                "title": "LocalDataAI 审计报告",
                "generated_at": datetime.now().isoformat(),
                "period": f"{start_date} 至 {end_date}",
                "retention_days": self.retention_days
            },
            "summary": {
                "total_operations": total_operations,
                "success_count": success_count,
                "failed_count": failed_count,
                "success_rate": f"{(success_count/total_operations*100):.2f}%" if total_operations > 0 else "0%"
            },
            "action_statistics": action_stats,
            "user_statistics": user_stats,
            "details": [asdict(log) for log in logs]
        }
    
    def _export_json(self, report_data: Dict, 
                    include_watermark: bool) -> str:
        """导出 JSON 报告"""
        if include_watermark:
            report_data['watermark'] = {
                "text": f"审计报告 - 生成时间: {datetime.now().isoformat()}",
                "generated_by": "LocalDataAI Compliance Logger"
            }
        
        output_file = self.log_dir / f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        return str(output_file)
    
    def _export_excel(self, report_data: Dict,
                     include_watermark: bool) -> str:
        """导出 Excel 报告"""
        try:
            import pandas as pd
            
            # 创建 Excel writer
            output_file = self.log_dir / f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # 摘要
                summary_df = pd.DataFrame([report_data['summary']])
                summary_df.to_excel(writer, sheet_name='摘要', index=False)
                
                # 操作统计
                action_df = pd.DataFrame([
                    {"操作类型": k, "次数": v} 
                    for k, v in report_data['action_statistics'].items()
                ])
                action_df.to_excel(writer, sheet_name='操作统计', index=False)
                
                # 详细记录
                if report_data['details']:
                    details_df = pd.DataFrame(report_data['details'])
                    details_df.to_excel(writer, sheet_name='详细记录', index=False)
            
            return str(output_file)
            
        except ImportError:
            print("[ComplianceLogger] 未安装 pandas/openpyxl，改用 JSON 导出")
            return self._export_json(report_data, include_watermark)
    
    def _export_pdf(self, report_data: Dict,
                   include_watermark: bool) -> str:
        """导出 PDF 报告"""
        # 简化实现：先导出 JSON，实际项目中可使用 ReportLab 生成 PDF
        return self._export_json(report_data, include_watermark)
    
    def _cleanup_old_logs(self):
        """清理过期日志"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        for log_file in self.log_dir.glob("audit_*.log"):
            try:
                # 从文件名提取日期
                date_str = log_file.stem.replace("audit_", "")
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                
                if file_date < cutoff_date:
                    log_file.unlink()
                    print(f"[ComplianceLogger] 已清理过期日志: {log_file.name}")
            except:
                pass
    
    def verify_log_integrity(self, log_file: Path = None) -> bool:
        """
        验证日志完整性
        
        Args:
            log_file: 日志文件路径，默认检查当前日志
            
        Returns:
            是否通过验证
        """
        if log_file is None:
            log_file = self.current_log_file
        
        if not log_file.exists():
            return True
        
        valid_count = 0
        invalid_count = 0
        
        with open(log_file, 'rb') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    decrypted_data = self.cipher.decrypt(line)
                    entry_dict = json.loads(decrypted_data.decode())
                    
                    stored_hash = entry_dict.pop('integrity_hash', '')
                    calculated_hash = self._calculate_integrity_hash(entry_dict)
                    
                    if stored_hash == calculated_hash:
                        valid_count += 1
                    else:
                        invalid_count += 1
                        
                except:
                    invalid_count += 1
        
        print(f"[ComplianceLogger] 日志完整性验证: 有效 {valid_count}, 无效 {invalid_count}")
        return invalid_count == 0


# 单例模式
_logger_instance = None


def get_logger() -> ComplianceLogger:
    """获取日志器单例"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = ComplianceLogger()
    return _logger_instance
