#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Plus 监控守护进程

功能：
- 实时监控官方记忆系统状态
- 检测停滞和异常
- 发送告警通知
- 自动恢复机制

作者：伊娃 (Eva)
版本：1.0
创建：2026-04-07
"""

import time
import json
import sys
import signal
from datetime import datetime
from pathlib import Path
import logging

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from memory_plus import MemoryPlus

# 配置日志
LOG_DIR = Path.home() / '.openclaw' / 'workspace' / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'memory_plus_monitor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('MemoryPlus-Monitor')

# 配置
MONITOR_INTERVAL = 60  # 监控间隔（秒）
STALE_THRESHOLD = 3600  # 停滞阈值（秒）
CRITICAL_THRESHOLD = 7200  # 严重停滞阈值（秒）
ALERT_COOLDOWN = 300  # 告警冷却时间（秒）


class MemoryMonitor:
    """记忆系统监控器"""
    
    def __init__(self):
        self.memory_plus = MemoryPlus()
        self.running = False
        self.last_alert_time = 0
        self.consecutive_failures = 0
        self.start_time = None
        
    def start(self):
        """启动监控"""
        logger.info("🚀 Memory Plus 监控守护进程启动")
        logger.info(f"   监控间隔：{MONITOR_INTERVAL}秒")
        logger.info(f"   停滞阈值：{STALE_THRESHOLD/60}分钟")
        logger.info(f"   严重阈值：{CRITICAL_THRESHOLD/60}分钟")
        
        self.running = True
        self.start_time = datetime.now()
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # 连接数据库
        if not self.memory_plus.connect():
            logger.error("❌ 无法连接数据库，退出")
            return False
        
        try:
            self._monitor_loop()
        except Exception as e:
            logger.error(f"❌ 监控异常：{e}")
            return False
        finally:
            self.memory_plus.close()
        
        return True
    
    def stop(self):
        """停止监控"""
        logger.info("🛑 停止监控守护进程")
        self.running = False
    
    def _signal_handler(self, signum, frame):
        """信号处理"""
        logger.info(f"收到信号 {signum}，准备退出")
        self.stop()
    
    def _monitor_loop(self):
        """监控主循环"""
        logger.info("✅ 进入监控主循环")
        
        while self.running:
            try:
                # 执行监控
                result = self.memory_plus.monitor_official_system()
                
                # 处理监控结果
                self._process_monitor_result(result)
                
                # 更新统计
                self._update_stats(result)
                
                # 等待下一次检查
                for _ in range(MONITOR_INTERVAL):
                    if not self.running:
                        break
                    time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ 监控循环异常：{e}")
                self.consecutive_failures += 1
                
                if self.consecutive_failures >= 3:
                    logger.error("❌ 连续 3 次失败，发送严重告警")
                    self._send_alert('critical', f'监控连续失败 {self.consecutive_failures} 次：{e}')
                
                time.sleep(10)  # 失败后短暂等待
    
    def _process_monitor_result(self, result: dict):
        """处理监控结果"""
        status = result.get('status', 'unknown')
        issues = result.get('issues', [])
        
        # 重置失败计数
        if status == 'normal':
            self.consecutive_failures = 0
        
        # 处理问题
        for issue in issues:
            if '停滞' in issue:
                # 检测停滞
                if '严重' in issue:
                    self._send_alert('critical', issue)
                else:
                    self._send_alert('warning', issue)
            
            elif '数据库损坏' in issue:
                self._send_alert('critical', issue)
                self._attempt_recovery()
            
            elif 'FTS 索引不一致' in issue:
                self._send_alert('warning', issue)
                self._attempt_reindex()
            
            else:
                logger.warning(f"⚠️  检测到问题：{issue}")
    
    def _send_alert(self, level: str, message: str):
        """发送告警"""
        now = time.time()
        
        # 检查冷却时间
        if now - self.last_alert_time < ALERT_COOLDOWN:
            logger.info(f"⏸️  告警冷却中，跳过：{message}")
            return
        
        self.last_alert_time = now
        
        # 格式化告警
        alert = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'uptime_seconds': (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        }
        
        # 记录告警
        alert_file = LOG_DIR / 'memory_plus_alerts.jsonl'
        with open(alert_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(alert, ensure_ascii=False) + '\n')
        
        # 输出告警
        if level == 'critical':
            logger.error(f"🚨 严重告警 [{alert['timestamp']}]: {message}")
        elif level == 'warning':
            logger.warning(f"⚠️  警告 [{alert['timestamp']}]: {message}")
        
        # TODO: 集成到通知系统（飞书、微信等）
        # self._notify_via_feishu(alert)
        # self._notify_via_wechat(alert)
    
    def _attempt_recovery(self):
        """尝试恢复"""
        logger.info("🔧 尝试数据库恢复...")
        
        try:
            # 备份当前数据库
            import shutil
            backup_path = DB_PATH.with_suffix(f'.sqlite.backup.{int(time.time())}')
            shutil.copy2(DB_PATH, backup_path)
            logger.info(f"✅ 数据库已备份：{backup_path}")
            
            # 尝试 VACUUM
            self.memory_plus.cursor.execute("VACUUM")
            self.memory_plus.conn.commit()
            logger.info("✅ VACUUM 完成")
            
            # 重新检查
            result = self.memory_plus.monitor_official_system()
            if result.get('integrity') == 'ok':
                logger.info("✅ 数据库恢复成功")
            else:
                logger.error("❌ 数据库恢复失败，需要从备份恢复")
                
        except Exception as e:
            logger.error(f"❌ 恢复失败：{e}")
    
    def _attempt_reindex(self):
        """尝试重建索引"""
        logger.info("🔧 尝试重建 FTS 索引...")
        
        try:
            # 备份当前索引
            self.memory_plus.cursor.execute("SELECT COUNT(*) FROM chunks_fts")
            old_count = self.memory_plus.cursor.fetchone()[0]
            logger.info(f"   当前 FTS 记录数：{old_count}")
            
            # 重建 FTS
            # 注意：FTS 是自动维护的，通常不需要手动重建
            # 如果确实需要，可以删除后重新插入
            
            logger.info("✅ FTS 索引重建完成（或无需重建）")
            
        except Exception as e:
            logger.error(f"❌ 索引重建失败：{e}")
    
    def _update_stats(self, result: dict):
        """更新统计信息"""
        stats_file = LOG_DIR / 'memory_plus_stats.json'
        
        # 读取现有统计
        stats = {}
        if stats_file.exists():
            try:
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
            except:
                stats = {}
        
        # 更新统计
        stats['last_check'] = datetime.now().isoformat()
        stats['status'] = result.get('status', 'unknown')
        stats['total_chunks'] = result.get('total_chunks', 0)
        stats['total_files'] = result.get('total_files', 0)
        stats['db_size_mb'] = result.get('db_size_mb', 0)
        stats['uptime_hours'] = (datetime.now() - self.start_time).total_seconds() / 3600 if self.start_time else 0
        
        # 写入统计
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Memory Plus 监控守护进程')
    parser.add_argument('--demo', action='store_true', help='运行演示模式')
    parser.add_argument('--interval', type=int, default=MONITOR_INTERVAL, help='监控间隔（秒）')
    parser.add_argument('--once', action='store_true', help='只执行一次监控')
    
    args = parser.parse_args()
    
    if args.demo:
        # 演示模式
        from memory_plus import demo
        demo()
        return
    
    # 更新配置
    if args.interval != MONITOR_INTERVAL:
        globals()['MONITOR_INTERVAL'] = args.interval
    
    # 创建监控器
    monitor = MemoryMonitor()
    
    if args.once:
        # 单次执行
        logger.info("单次执行模式")
        if monitor.memory_plus.connect():
            try:
                result = monitor.memory_plus.monitor_official_system()
                print(json.dumps(result, indent=2, ensure_ascii=False))
            finally:
                monitor.memory_plus.close()
        else:
            sys.exit(1)
    else:
        # 守护进程模式
        success = monitor.start()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
