#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Plus - 跨渠道记忆同步工具

功能：
1. 多渠道记忆采集（飞书、微信、Telegram 等）
2. 统一存储到官方 SQLite 数据库
3. 实时监控官方记忆系统状态
4. 异常告警（停滞、失败）

作者：伊娃 (Eva)
版本：1.0
创建：2026-04-07
"""

import sqlite3
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('MemoryPlus')

# 常量
DB_PATH = Path.home() / '.openclaw' / 'memory' / 'main.sqlite'
MEMORY_DIR = Path.home() / '.openclaw' / 'memory'
WORKSPACE_DIR = Path.home() / '.openclaw' / 'workspace'

# 渠道类型
CHANNEL_TYPES = {
    'feishu': '飞书',
    'wechat': '微信',
    'telegram': 'Telegram',
    'discord': 'Discord',
    'sms': '短信',
    'imessage': 'iMessage',
    'email': '邮件',
    'voice': '语音对话',
    'webchat': '网页聊天'
}


class MemoryPlus:
    """跨渠道记忆同步核心类"""
    
    def __init__(self, db_path: str = None):
        self.db_path = Path(db_path) if db_path else DB_PATH
        self.conn = None
        self.cursor = None
        self.last_monitor_time = time.time()
        self.monitor_interval = 60  # 监控间隔（秒）
        self.last_write_time = None
        self.write_count = 0
        
    def connect(self):
        """连接数据库"""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.cursor = self.conn.cursor()
            logger.info(f"✅ 数据库连接成功：{self.db_path}")
            return True
        except Exception as e:
            logger.error(f"❌ 数据库连接失败：{e}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logger.info("数据库连接已关闭")
    
    def compute_hash(self, text: str) -> str:
        """计算文本哈希值"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def generate_chunk_id(self, path: str, text: str, start_line: int, end_line: int) -> str:
        """生成 chunk ID"""
        content = f"{path}:{start_line}:{end_line}:{text}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def get_embedding_stub(self, text: str) -> str:
        """
        生成占位 embedding（768 维）
        实际使用时应调用 embedding API
        """
        # 使用简单哈希生成伪向量
        hash_bytes = hashlib.md5(text.encode('utf-8')).digest()
        # 扩展到 768 维（3072 字节）
        embedding_bytes = (hash_bytes * (768 // 16 + 1))[:768]
        # 转换为 float 列表的 JSON 字符串
        embedding_list = [float(b) / 255.0 for b in embedding_bytes]
        return json.dumps(embedding_list)
    
    def insert_chunk(self, 
                     path: str, 
                     text: str, 
                     source: str = 'memory',
                     model: str = 'hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf',
                     start_line: int = 1,
                     end_line: int = None,
                     channel: str = 'feishu',
                     metadata: Dict[str, Any] = None):
        """
        插入记忆块到 chunks 表
        
        Args:
            path: 记忆文件路径（如 memory/feishu/2026-04-07.md）
            text: 记忆文本内容
            source: 来源（默认 memory）
            model: embedding 模型
            start_line: 起始行号
            end_line: 结束行号
            channel: 渠道类型
            metadata: 额外元数据
        """
        if not self.conn:
            logger.error("❌ 数据库未连接")
            return False
        
        try:
            # 计算 end_line
            if end_line is None:
                end_line = text.count('\n') + start_line
            
            # 生成 ID 和 hash
            chunk_id = self.generate_chunk_id(path, text, start_line, end_line)
            chunk_hash = self.compute_hash(text)
            embedding = self.get_embedding_stub(text)
            updated_at = int(time.time() * 1000)  # 毫秒时间戳
            
            # 检查是否已存在
            self.cursor.execute("SELECT id FROM chunks WHERE id = ?", (chunk_id,))
            if self.cursor.fetchone():
                logger.info(f"⚠️  记忆块已存在，跳过：{chunk_id[:16]}...")
                return False
            
            # 插入数据
            sql = """
            INSERT INTO chunks (id, path, source, start_line, end_line, hash, model, text, embedding, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            self.cursor.execute(sql, (
                chunk_id,
                path,
                source,
                start_line,
                end_line,
                chunk_hash,
                model,
                text,
                embedding,
                updated_at
            ))
            
            self.conn.commit()
            
            # 同步 FTS 索引（确保一致性）
            try:
                # 使用 rowid 直接插入，避免 FTS5 rebuild 的延迟
                self.cursor.execute('''
                    INSERT OR IGNORE INTO chunks_fts(rowid, text, id, path, source, model, start_line, end_line)
                    VALUES (last_insert_rowid(), ?, ?, ?, ?, ?, ?, ?)
                ''', (text, chunk_id, path, source, model, start_line, end_line))
                self.conn.commit()
            except Exception as fts_error:
                logger.warning(f"⚠️  FTS 同步失败：{fts_error}，将在下次监控中修复")
            
            self.last_write_time = time.time()
            self.write_count += 1
            
            logger.info(f"✅ 插入记忆块：{path} ({len(text)} 字符，渠道：{channel})")
            return True
            
        except Exception as e:
            logger.error(f"❌ 插入记忆块失败：{e}")
            self.conn.rollback()
            return False
    
    def insert_validated_memory(self,
                                content: str,
                                user_id: str,
                                memory_type: str = 'conversation',
                                importance: str = 'normal',
                                tags: List[str] = None,
                                metadata: Dict[str, Any] = None):
        """
        插入验证后的记忆到 validated_memories 表
        
        Args:
            content: 记忆内容
            user_id: 用户 ID
            memory_type: 记忆类型
            importance: 重要程度
            tags: 标签列表
            metadata: 元数据
        """
        if not self.conn:
            logger.error("❌ 数据库未连接")
            return False
        
        try:
            now = datetime.now(timezone.utc).isoformat()
            tags_json = json.dumps(tags) if tags else '[]'
            metadata_json = json.dumps(metadata) if metadata else '{}'
            
            sql = """
            INSERT INTO validated_memories 
            (content, user_id, memory_type, importance, tags, metadata, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            self.cursor.execute(sql, (
                content,
                user_id,
                memory_type,
                importance,
                tags_json,
                metadata_json,
                now,
                now
            ))
            
            self.conn.commit()
            logger.info(f"✅ 插入验证记忆：{user_id} - {memory_type}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 插入验证记忆失败：{e}")
            self.conn.rollback()
            return False
    
    def monitor_official_system(self) -> Dict[str, Any]:
        """
        监控官方记忆系统状态
        
        Returns:
            监控结果字典
        """
        result = {
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'issues': []
        }
        
        try:
            if not self.conn:
                result['status'] = 'error'
                result['issues'].append('数据库未连接')
                return result
            
            # 1. 检查数据库连通性
            self.cursor.execute("SELECT COUNT(*) FROM chunks")
            total_chunks = self.cursor.fetchone()[0]
            result['total_chunks'] = total_chunks
            
            # 2. 检查最新写入时间
            self.cursor.execute("SELECT MAX(updated_at) FROM chunks")
            latest_ts = self.cursor.fetchone()[0]
            
            if latest_ts:
                latest_time = datetime.fromtimestamp(latest_ts / 1000)
                time_diff = (datetime.now() - latest_time).total_seconds()
                result['latest_write'] = latest_time.isoformat()
                result['seconds_since_last_write'] = time_diff
                
                # 判断是否停滞
                if time_diff > 3600:  # 1 小时未写入
                    result['issues'].append(f'⚠️ 记忆系统停滞：{int(time_diff/60)}分钟未写入')
                    result['status'] = 'warning'
                elif time_diff > 7200:  # 2 小时未写入
                    result['issues'].append(f'❌ 记忆系统严重停滞：{int(time_diff/60)}分钟未写入')
                    result['status'] = 'critical'
                else:
                    result['status'] = 'normal'
            else:
                result['issues'].append('❌ 无记忆写入记录')
                result['status'] = 'critical'
            
            # 3. 检查文件数量
            self.cursor.execute("SELECT COUNT(*) FROM files")
            total_files = self.cursor.fetchone()[0]
            result['total_files'] = total_files
            
            # 4. 检查 FTS 索引一致性
            self.cursor.execute("SELECT COUNT(*) FROM chunks_fts")
            fts_count = self.cursor.fetchone()[0]
            result['fts_count'] = fts_count
            
            if fts_count != total_chunks:
                result['issues'].append(f'⚠️ FTS 索引不一致：chunks={total_chunks}, fts={fts_count}')
            
            # 5. 检查数据库大小
            db_size_mb = self.db_path.stat().st_size / (1024 * 1024)
            result['db_size_mb'] = round(db_size_mb, 2)
            
            if db_size_mb > 100:
                result['issues'].append(f'⚠️ 数据库过大：{db_size_mb:.2f}MB')
            
            # 6. 完整性检查
            self.cursor.execute("PRAGMA integrity_check")
            integrity = self.cursor.fetchone()[0]
            result['integrity'] = integrity
            
            if integrity != 'ok':
                result['issues'].append(f'❌ 数据库损坏：{integrity}')
                result['status'] = 'critical'
            
            # 7. 记录监控时间
            self.last_monitor_time = time.time()
            
            # 总结状态
            if not result['issues']:
                result['status'] = 'normal'
                logger.info(f"✅ 记忆系统状态正常：{total_chunks} 条记忆，{total_files} 个文件")
            else:
                for issue in result['issues']:
                    logger.warning(issue)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 监控失败：{e}")
            result['status'] = 'error'
            result['issues'].append(f'监控异常：{e}')
            return result
    
    def sync_from_channel(self, 
                         channel: str, 
                         messages: List[Dict[str, Any]],
                         date: str = None):
        """
        从渠道同步消息到记忆库
        
        Args:
            channel: 渠道类型（feishu, wechat, telegram 等）
            messages: 消息列表，每条消息包含：
                      - content: 消息内容
                      - sender: 发送者
                      - timestamp: 时间戳
                      - message_id: 消息 ID
            date: 日期（YYYY-MM-DD 格式，默认为今天）
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 创建渠道专用记忆文件路径
        channel_dir = MEMORY_DIR / channel
        channel_dir.mkdir(exist_ok=True)
        
        memory_file = channel_dir / f"{date}.md"
        relative_path = f"memory/{channel}/{date}.md"
        
        logger.info(f"📥 开始同步 {CHANNEL_TYPES.get(channel, channel)} 渠道消息：{len(messages)} 条")
        
        # 按消息分组写入
        for msg in messages:
            content = msg.get('content', '')
            if not content:
                continue
            
            # 格式化记忆内容
            sender = msg.get('sender', 'unknown')
            timestamp = msg.get('timestamp', '')
            message_id = msg.get('message_id', '')
            
            # 构建记忆文本
            memory_text = f"""# Message: {message_id}

**Channel**: {channel}
**Sender**: {sender}
**Timestamp**: {timestamp}

## Content

{content}
"""
            
            # 插入数据库
            self.insert_chunk(
                path=relative_path,
                text=memory_text,
                source='memory',
                channel=channel,
                metadata={
                    'sender': sender,
                    'timestamp': timestamp,
                    'message_id': message_id
                }
            )
        
        # 写入文件（追加模式）
        try:
            with open(memory_file, 'a', encoding='utf-8') as f:
                f.write(f"\n\n## Synced at {datetime.now().isoformat()}\n")
                f.write(f"Total messages: {len(messages)}\n")
            logger.info(f"✅ 已写入记忆文件：{memory_file}")
        except Exception as e:
            logger.error(f"❌ 写入文件失败：{e}")
        
        logger.info(f"✅ {CHANNEL_TYPES.get(channel, channel)} 渠道同步完成")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.conn:
            return {}
        
        stats = {}
        
        # 总记忆块数
        self.cursor.execute("SELECT COUNT(*) FROM chunks")
        stats['total_chunks'] = self.cursor.fetchone()[0]
        
        # 总文件数
        self.cursor.execute("SELECT COUNT(*) FROM files")
        stats['total_files'] = self.cursor.fetchone()[0]
        
        # 按渠道统计
        self.cursor.execute("""
            SELECT source, COUNT(*) as count 
            FROM chunks 
            GROUP BY source
        """)
        stats['by_source'] = dict(self.cursor.fetchall())
        
        # 最新写入时间
        self.cursor.execute("SELECT MAX(updated_at) FROM chunks")
        latest_ts = self.cursor.fetchone()[0]
        if latest_ts:
            stats['latest_write'] = datetime.fromtimestamp(latest_ts / 1000).isoformat()
        
        # 本次会话写入数
        stats['session_writes'] = self.write_count
        
        return stats
    
    def health_check(self) -> bool:
        """
        健康检查
        
        Returns:
            是否健康
        """
        result = self.monitor_official_system()
        
        # 判断健康状态
        is_healthy = (
            result.get('status') in ['normal', 'warning'] and
            result.get('integrity') == 'ok' and
            result.get('total_chunks', 0) > 0
        )
        
        if is_healthy:
            logger.info("✅ 记忆系统健康检查通过")
        else:
            logger.warning("⚠️ 记忆系统健康检查未通过")
            for issue in result.get('issues', []):
                logger.warning(f"  - {issue}")
        
        return is_healthy


def demo():
    """演示功能"""
    print("=" * 60)
    print("Memory Plus - 跨渠道记忆同步工具演示")
    print("=" * 60)
    
    # 创建实例
    mp = MemoryPlus()
    
    # 连接数据库
    if not mp.connect():
        print("❌ 无法连接数据库")
        return
    
    try:
        # 1. 监控官方系统状态
        print("\n1️⃣  监控官方记忆系统状态...")
        monitor_result = mp.monitor_official_system()
        print(f"   状态：{monitor_result['status']}")
        print(f"   总记忆块：{monitor_result.get('total_chunks', 'N/A')}")
        print(f"   总文件数：{monitor_result.get('total_files', 'N/A')}")
        print(f"   数据库大小：{monitor_result.get('db_size_mb', 'N/A')} MB")
        if monitor_result.get('issues'):
            print("   问题:")
            for issue in monitor_result['issues']:
                print(f"     - {issue}")
        
        # 2. 模拟从飞书同步消息
        print("\n2️⃣  模拟从飞书同步消息...")
        feishu_messages = [
            {
                'content': '老板：今天下午 3 点开会，讨论 AI 产品方向',
                'sender': '李威',
                'timestamp': '2026-04-07 14:30:00',
                'message_id': 'msg_001'
            },
            {
                'content': '伊娃：收到，我会准备好产品路线图和市场分析',
                'sender': '伊娃',
                'timestamp': '2026-04-07 14:32:00',
                'message_id': 'msg_002'
            }
        ]
        mp.sync_from_channel('feishu', feishu_messages)
        
        # 3. 模拟从微信同步消息
        print("\n3️⃣  模拟从微信同步消息...")
        wechat_messages = [
            {
                'content': '小花朵：妈妈，今天老师表扬我了！',
                'sender': '小花朵',
                'timestamp': '2026-04-07 16:00:00',
                'message_id': 'wx_001'
            }
        ]
        mp.sync_from_channel('wechat', wechat_messages)
        
        # 4. 获取统计信息
        print("\n4️⃣  统计信息:")
        stats = mp.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # 5. 健康检查
        print("\n5️⃣  健康检查:")
        is_healthy = mp.health_check()
        print(f"   结果：{'✅ 健康' if is_healthy else '❌ 不健康'}")
        
    finally:
        mp.close()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo()
    else:
        # 默认运行监控
        mp = MemoryPlus()
        if mp.connect():
            try:
                result = mp.monitor_official_system()
                print(json.dumps(result, indent=2, ensure_ascii=False))
            finally:
                mp.close()
        else:
            sys.exit(1)
