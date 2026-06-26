"""
记忆维护技能核心脚本
功能：任务执行 + 记忆管理 + 失败重试
版本：2.0.0

【核心优化 v2.0.0】
- ⚡ 独立跟踪主会话和后台子会话，实现精确控制
- 🛑 用户中途停止（session.stop）时立即终止后台大模型调用
- 🎯 任务完成后立即停止后台模型加载，释放内存
- 🧹 定期清理终止/失败的子会话，释放资源
- ⚖️ 更理性的资源分配，减轻内存负担
- 📝 增强进度跟踪：区分执行进度和模型响应进度
"""

import json
import os
import shutil
import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Tuple, Deque
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import uuid
import signal
import traceback
from subprocess import Popen, PIPE, DEVNULL, TimeoutExpired, CallProcessError, SubprocessError
from datetime import datetime, timedelta

# ========== 会话控制器（v2.0.0 新增） =============

class SessionController:
    """会话控制器：管理主会话和后台子会话，实现精确的终止控制
    
    核心功能：
    1. 跟踪所有子会话状态和进程句柄
    2. 用户停止主会话时立即终止所有后台子会话
    3. 主任务完成后立即终止相关子会话
    4. 定期清理终止/失败的子会话
    5. 双进度追踪：执行进度 + 模型响应进度
    
    优化点：
    - ⚡ 异步管理后台会话，不阻塞主流程
    - 🛑 session.stop 立即终止所有后台会话
    - 🎯 任务完成后清理相关会话
    - 🧹 定期清理超时/失败会话，释放资源
    - ⚖️ 更理性的资源分配
    """
    
    # 会话状态定义
    SESSION_STATES = {
        "PENDING": "pending",      # 等待中
        "RUNNING": "running",      # 运行中
        "SUCCESS": "success",      # 成功完成
        "FAILED": "failed",        # 失败
        "TIMEOUT": "timeout",      # 超时
        "STUCK": "stuck",          # 卡死
        "KILLED": "killed"         # 被强制终止
    }
    
    # 模型响应状态
    MODEL_STATES = {
        "NONE": "none",           # 无模型调用
        "WAITING": "waiting",     # 等待模型响应
        "RESPONDING": "responding",  # 模型正在响应
        "COMPLETED": "completed", # 已完成
        "STUCK": "stuck"          # 模型卡死
    }
    
    def __init__(self, workspace: str):
        self.workspace = Path(workspace)
        self.main_session = None  # 主会话 session_key
        self.sub_sessions: Dict[str, Dict] = {}  # subagent_id -> session 信息
        self.exec_sessions: Set[str] = set()  # 正在执行的子会话 ID
        self.completed_tasks: Set[str] = set()  # 已完成的任务 ID
        self.finished_sessions: Set[str] = set()  # 已终止/清理的会话
        self.session_history: Deque[tuple] = deque(maxlen=100)  # 会话事件历史
        
        # 会话超时配置（秒）
        self.session_timeout = timedelta(minutes=60)  # 会话超时 60 分钟
        self.check_interval = timedelta(minutes=15)  # 检查间隔 15 分钟
        
        # 线程池用于异步操作
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # 资源追踪
        self.active_models = set()  # 正在加载的模型
        self.model_tokens = 0  # 累计消耗 tokens
        
    def spawn_session(self, task: str, mode: str = "session", 
                     agent_id: str = "memory-maintenance-2.0.0",
                     timeout_seconds: int = 3600, stream_to: str = "parent",
                     label: str = None,
                     cleanup: str = "keep") -> Optional[str]:
        """异步启动子会话，返回 session_key
        
        Args:
            task: 任务描述
            mode: "session" (持久化) or "run" (一次性)
            agent_id: 代理 ID
            timeout_seconds: 超时时间
            stream_to: "parent" or other session
            label: 会话标签（用于识别）
            cleanup: "keep" (保留) or "delete" (清理)
            
        Returns:
            session_key: 会话标识符
            None: 如果无法创建
        """
        try:
            # 使用 sessions_spawn 创建子会话
            session_key = sessions_spawn(
                task=task,
                mode=mode,
                agent_id=agent_id,
                timeoutSeconds=timeout_seconds,
                streamTo=stream_to,
                label=label,
                cleanup=cleanup
            )
            
            session_id = str(uuid.uuid4())[:8]
            subagent_id = f"sess_{session_id}"
            
            # 记录会话信息
            session_info = {
                "session_key": session_key,
                "task": task,
                "mode": mode,
                "agent_id": agent_id,
                "timeout": timeout_seconds,
                "start_time": datetime.now(),
                "status": "pending",
                "model_tokens": 0,
                "messages": [],
                "tools_called": [],
                "progress": 0,
                "created_by": "system"
            }
            
            self.sub_sessions[subagent_id] = session_info
            self.exec_sessions.add(subagent_id)
            
            # 记录事件
            self._log_event(session_id, "spawned", f"任务：{task[:50]}...")
            
            return session_key
            
        except Exception as e:
            print(f"❌ 会话创建失败：{e}")
            self._log_event("main", "error", f"会话创建失败：{str(e)[:100]}")
            return None
    
    def stop_background_sessions(self, reason: str = "用户中止"):
        """立即终止所有后台子会话，释放资源
        
        触发条件：
        - 用户主动停止主会话
        - 主任务完成后不再需要
        - 会话卡死或超时
        """
        print(f"\n{'='*60}")
        print(f"🛑 终止后台会话：{reason}")
        print(f"{'='*60}")
        
        now = datetime.now()
        terminated_count = 0
        
        for sub_id, info in list(self.sub_sessions.items()):
            if sub_id in self.exec_sessions:
                # 检查会话状态
                if info["status"] in ["pending", "running"]:
                    # 尝试终止
                    try:
                        # 获取会话状态
                        status = self.get_session_status(info["session_key"])
                        
                        if status.is_blocked():
                            print(f"   🚨 强制终止：{sub_id} (状态：{info['status']}, 模型：{status.model})")
                            self._terminate_session(info["session_key"])
                        else:
                            print(f"   ⏸ 等待终止：{sub_id} (状态：{info['status']})")
                            terminated_count += 1
                            
                    except Exception as e:
                        print(f"   ⚠ 无法终止 {sub_id}: {e}")
                
                # 移除执行中的会话
                self.exec_sessions.discard(sub_id)
                
                # 更新状态
                info["status"] = "terminated"
                info["terminated_at"] = now
                info["termination_reason"] = reason
                
                terminated_count += 1
        
        print(f"   ✓ 终止了 {terminated_count} 个会话")
        
        # 清理资源
        self.cleanup_resources(reason)
        
        return terminated_count
    
    def _terminate_session(self, session_key: str):
        """终止单个会话
        
        Args:
            session_key: 会话标识符
        """
        try:
            # 使用 process 工具终止会话
            result = process(action="kill", sessionId=session_key)
            print(f"   🗑 已终止会话：{session_key}")
        except Exception as e:
            print(f"   ⚠ 无法终止会话 {session_key}: {e}")
    
    def stop_main_session(self):
        """终止主会话"""
        if self.main_session:
            print(f"\n⏹️  终止主会话：{self.main_session}")
            self._terminate_session(self.main_session)
            self.main_session = None
    
    def should_keep_session(self, sub_id: str, task_id: str) -> bool:
        """判断是否应保留子会话
        
        保留条件：
        - 会话尚未完成
        - 主任务仍在执行或需要重试
        
        清理条件：
        - 主任务已完成
        - 会话失败/超时/卡死
        - 会话已运行超过阈值
        """
        # 检查会话是否已完成
        if sub_id not in self.sub_sessions:
            return False
        
        session_info = self.sub_sessions[sub_id]
        
        # 已完成
        if session_info["status"] in ["success", "completed"]:
            # 如果主任务需要重试，保留会话
            # 否则清理
            main_completed = task_id in self.completed_tasks
            return not main_completed
        
        # 失败/超时/卡死 - 清理
        if session_info["status"] in ["failed", "timeout", "stuck", "killed"]:
            self._log_failure(task_id, {
                "reason": f"会话{session_info['status']}，{session_info.get('termination_reason', '')}",
                "duration": (datetime.now() - session_info["start_time"]).total_seconds()
            })
            return False
        
        # 检查运行时间
        run_time = (datetime.now() - session_info["start_time"]).total_seconds()
        if run_time > self.session_timeout.total_seconds():
            print(f"   🐌 清理超时会话：{sub_id} ({run_time/60:.0f}分钟)")
            return False
        
        return True
    
    def cleanup_finished_sessions(self):
        """定期清理已完成/失败的会话
        
        清理条件：
        - 会话已完成且不再需要
        - 会话失败/超时/卡死
        - 会话运行超过阈值时间
        """
        now = datetime.now()
        cleaned_count = 0
        
        for sub_id, info in list(self.sub_sessions.items()):
            # 跳过当前正在处理的任务
            current_task = None
            for task_id in self.completed_tasks:
                if not self._task_needs_retry(task_id):
                    current_task = task_id
                    break
            
            if current_task and not self._is_session_for_task(sub_id, current_task):
                continue
            
            # 检查清理条件
            if info["status"] in ["failed", "timeout", "stuck", "killed"]:
                # 失败会话直接清理
                cleaned_count += 1
                self._mark_session_cleaned(sub_id)
                
            elif info["status"] == "success":
                # 成功会话，判断是否保留
                should_keep = self.should_keep_session(sub_id, current_task)
                if not should_keep:
                    cleaned_count += 1
                    self._mark_session_cleaned(sub_id)
                    self._cleanup_session_data(sub_id)
            
            # 检查运行时间
            run_time = (now - info["start_time"]).total_seconds()
            if run_time > self.session_timeout.total_seconds() * 2:
                # 即使成功，超过 2 倍阈值也清理
                if info["status"] == "success" and not should_keep:
                    cleaned_count += 1
                    self._mark_session_cleaned(sub_id)
        
        print(f"\n🧹 清理了 {cleaned_count} 个会话")
    
    def _is_session_for_task(self, sub_id: str, task_id: str) -> bool:
        """判断子会话是否属于指定任务"""
        if sub_id in self.sub_sessions:
            return self.sub_sessions[sub_id]["task"] == task_id
        return False
    
    def _task_needs_retry(self, task_id: str) -> bool:
        """判断任务是否需要重试"""
        # 从记忆中查找
        return False  # 简化处理
    
    def _mark_session_cleaned(self, sub_id: str):
        """标记会话已清理"""
        if sub_id in self.sub_sessions:
            self.sub_sessions[sub_id]["status"] = "cleaned"
            self.sub_sessions[sub_id]["cleaned_at"] = datetime.now()
            self.finished_sessions.add(sub_id)
    
    def _cleanup_session_data(self, sub_id: str):
        """清理会话相关数据"""
        if sub_id in self.sub_sessions:
            del self.sub_sessions[sub_id]
            self.exec_sessions.discard(sub_id)
            
            # 如果有错误日志，记录下来
            self._log_failure(None, {
                "reason": "会话已清理",
                "duration": 0
            })
    
    def get_session_status(self, session_key: str) -> Dict:
        """获取会话状态详情
        
        返回：
        - status: "pending" | "running" | "success" | "failed" | "timeout" | "stuck"
        - progress: 0-100 执行进度
        - model: "none" | "waiting" | "responding" | "completed" | "stuck"
        - model_progress: 0-100 模型响应进度
        - active_models: 当前加载的模型
        - tokens: 累计消耗的 tokens
        """
        try:
            # 获取会话状态
            status_result = session_status(sessionKey=session_key)
            
            # 获取会话历史
            history = sessions_history(
                sessionKey=session_key,
                limit=10,
                includeTools=True
            )
            
            messages = history.get("messages", [])
            
            # 分析状态
            if not messages:
                status = "pending"
                progress = 0
                model = "none"
                model_progress = 0
            else:
                last_msg = messages[-1]
                role = last_msg.get("role", "")
                content = last_msg.get("content", "")
                tool_calls = last_msg.get("tool_calls")
                
                if role == "assistant":
                    if tool_calls:
                        status = "running"
                        model = "responding"
                        model_progress = 50
                    elif content:
                        status = "running"
                        model = "completed"
                        model_progress = 100
                    else:
                        status = "running"
                        model = "waiting"
                        model_progress = 0
                else:
                    status = "running"
                    model = "waiting"
                    model_progress = 0
            
            # 计算执行进度
            if status == "success":
                progress = 100
            elif status == "failed":
                progress = 50  # 执行了部分工作
            elif status == "timeout":
                progress = 70  # 可能接近完成
            elif status == "stuck":
                progress = 30  # 刚刚开始就卡住
            elif status == "running":
                # 根据消息数估算
                progress = min(100, int(len(messages) * 10))
            
            # 统计 tokens
            tokens = status_result.get("usage", {}).get("total_tokens", 0)
            
            return {
                "status": status,
                "progress": progress,
                "model": model,
                "model_progress": model_progress,
                "active_models": self.active_models,
                "tokens": self.model_tokens,
                "tokens_this_turn": tokens,
                "messages_count": len(messages)
            }
            
        except Exception as e:
            print(f"   ⚠ 获取会话状态失败：{e}")
            return {
                "status": "unknown",
                "progress": 0,
                "model": "unknown",
                "model_progress": 0
            }
    
    def check_model_response(self, session_key: str) -> str:
        """检查模型响应状态
        
        返回模型状态字符串：
        - "none": 无模型调用
        - "waiting": 等待模型响应
        - "responding": 模型正在响应
        - "completed": 已完成
        - "stuck": 模型卡死
        """
        try:
            # 获取最近的会话历史
            history = sessions_history(
                sessionKey=session_key,
                limit=50,
                includeTools=True
            )
            
            messages = history.get("messages", [])
            
            if not messages:
                return "none"
            
            # 分析最后一轮对话
            last_msg = messages[-1]
            role = last_msg.get("role", "")
            content = last_msg.get("content", "")
            tool_calls = last_msg.get("tool_calls")
            
            if not content and tool_calls:
                # 刚发送消息，等待模型响应
                return "waiting"
            
            elif content and tool_calls:
                # 模型正在调用工具
                return "responding"
            
            elif content and not tool_calls:
                # 模型已完成响应
                return "completed"
            
            else:
                # 无内容且无工具调用，可能卡死
                return "stuck"
                
        except Exception as e:
            print(f"   ⚠ 检查模型响应失败：{e}")
            return "unknown"
    
    def is_session_terminated(self, session_key: str) -> bool:
        """判断会话是否已终止"""
        return session_key in self.finished_sessions
    
    def can_stop_background(self, task_id: str) -> bool:
        """判断是否可以安全停止后台会话
        
        可以停止：
        - 主会话已终止
        - 相关子会话已完成或失败
        
        不能停止：
        - 主会话仍在运行
        - 相关子会话正在等待模型响应
        """
        # 检查主会话状态
        if self.main_session:
            main_status = self.get_session_status(self.main_session)
            
            if main_status["status"] != "stopped":
                return False  # 主会话仍在运行，不能停止后台
            
            # 检查模型是否还在响应
            if main_status["model"] == "responding":
                print(f"   ⏸ 主会话模型正在响应，等待 {main_status['model_progress']}%")
                return False
        
        return True
    
    def on_task_completed(self, task_id: str):
        """任务完成时，清理相关会话
        
        清理流程：
        1. 停止所有等待模型响应的会话
        2. 停止所有运行中的会话
        3. 保留已完成会话（如果还需要）
        4. 清理失败/超时会话
        """
        print(f"\n✅ 任务 {task_id} 已完成")
        
        # 停止所有相关后台会话
        sessions_to_stop = []
        
        for sub_id, info in self.sub_sessions.items():
            if info.get("task_id") == task_id:
                # 检查是否可以停止
                if self.can_stop_background(task_id):
                    sessions_to_stop.append(sub_id)
        
        # 批量停止会话
        if sessions_to_stop:
            for sub_id in sessions_to_stop:
                self.stop_background_session(sub_id, reason="任务已完成")
        
        # 清理失败会话
        self.cleanup_finished_sessions()
    
    def stop_background_session(self, sub_id: str, reason: str = "用户中止"):
        """停止指定的后台会话"""
        if sub_id not in self.exec_sessions:
            return 0
        
        session_info = self.sub_sessions[sub_id]
        
        # 获取状态
        status = self.get_session_status(session_info["session_key"])
        
        # 检查是否可以停止
        if status["status"] == "failed" or status["model"] == "stuck":
            print(f"   🗑 清理失败/卡死会话：{sub_id}")
        else:
            print(f"   🛑 停止会话：{sub_id} ({reason})")
        
        # 终止会话
        self._terminate_session(session_info["session_key"])
        
        # 更新状态
        session_info["status"] = "terminated"
        session_info["termination_reason"] = reason
        session_info["terminated_at"] = datetime.now()
        
        self.exec_sessions.discard(sub_id)
        self.finished_sessions.add(sub_id)
        
        return 1
    
    def _log_event(self, event_type: str, detail: str = None, extra: dict = None):
        """记录会话事件"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "detail": detail or "",
            "extra": extra or {}
        }
        self.session_history.appendleft(entry)
    
    def _log_failure(self, task_id: str, details: dict):
        """记录失败日志"""
        if not task_id:
            return
        
        log_entry = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        
        # 写入失败日志
        with open(FAILURE_LOG, "a", encoding="utf-8") as f:
            f.write(f"### 失败日志\n")
            f.write(f"任务 ID: {task_id}\n")
            f.write(f"时间：{details.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n")
            f.write(f"原因：{details.get('reason', '未知')}\n")
            f.write(f"持续时间：{details.get('duration', 'N/A')}秒\n")
            f.write("---\n\n")
    
    def cleanup_resources(self, reason: str = "定期清理"):
        """清理资源
        
        清理内容：
        - 终止超时会话
        - 清理失败会话
        - 释放线程池
        - 清理临时文件
        """
        # 清理过期会话
        now = datetime.now()
        expired_sessions = []
        
        for sub_id, info in self.sub_sessions.items():
            if info["status"] not in ["success", "completed"]:
                run_time = (now - info["start_time"]).total_seconds()
                if run_time > self.session_timeout.total_seconds():
                    expired_sessions.append(sub_id)
        
        for sub_id in expired_sessions:
            self.stop_background_session(sub_id, reason=f"超时{reason}")
    
    def get_progress_summary(self, task_id: str) -> Dict:
        """获取任务的进度汇总
        
        返回：
        {
            "stage": "可行性检查 | 执行 | 验证 | 记忆写入"
            "exec_progress": 执行进度 0-100
            "model_progress": 模型响应进度 0-100
            "status": "pending | running | success | failed"
            "blocks": ["blocking_items"]  # 阻塞项
        }
        """
        result = {
            "stage": "可行性检查",
            "exec_progress": 0,
            "model_progress": 0,
            "status": "pending",
            "blocks": [],
            "sessions": {},
            "token_usage": 0
        }
        
        # 获取主会话进度
        if self.main_session:
            main_status = self.get_session_status(self.main_session)
            result["main_status"] = main_status.get("status", "none")
            result["exec_progress"] = main_status.get("progress", 0)
            result["model_status"] = main_status.get("model", "none")
            result["model_progress"] = main_status.get("model_progress", 0)
            result["active_models"] = main_status.get("active_models", [])
            result["tokens"] = self.model_tokens + main_status.get("tokens", 0)
        
        # 获取子会话进度
        if task_id:
            task_sub = self.sub_sessions.get(task_id)
            if task_sub:
                sub_status = self.get_session_status(task_sub["session_key"])
                result["exec_progress"] = max(result["exec_progress"], sub_status.get("progress", 0))
                result["model_progress"] = max(result["model_progress"], sub_status.get("model_progress", 0))
                
                result["sessions"][task_id] = {
                    "status": sub_status.get("status"),
                    "progress": sub_status.get("progress"),
                    "model": sub_status.get("model")
                }
        
        # 判断整体状态
        if result["main_status"] == "terminated":
            result["status"] = "failed"
        elif result["main_status"] == "success" and task_id in self.completed_tasks:
            result["status"] = "success"
        elif result["main_status"] == "running":
            result["status"] = "running"
        
        return result
    
    def monitor(self, interval: int = 60):
        """监控会话状态
        
        Args:
            interval: 检查间隔（秒）
        """
        def _monitor():
            now = datetime.now()
            
            # 检查每个会话
            for sub_id, info in list(self.sub_sessions.items()):
                if sub_id in self.exec_sessions:
                    status = self.get_session_status(info["session_key"])
                    
                    # 检查卡死
                    if status["model"] == "stuck" and status["progress"] < 30:
                        print(f"   🚨 会话 {sub_id} 卡死，准备终止")
                        self.stop_background_session(sub_id, reason="会话卡死")
                    
                    # 检查超时
                    elif (now - info["start_time"]).total_seconds() > self.session_timeout.total_seconds():
                        print(f"   🐌 会话 {sub_id} 超时，准备终止")
                        self.stop_background_session(sub_id, reason="超时")
                    
                    # 记录状态
                    else:
                        self._log_event("status_check", f"{sub_id}: {status['status']}")
            
            # 检查主会话
            if self.main_session:
                main_status = self.get_session_status(self.main_session)
                
                # 用户停止
                if main_status["status"] == "terminated":
                    print(f"   ⏹️  主会话已终止，清理后台")
                    self.stop_all_background_sessions("用户停止")
                
                # 任务完成
                elif main_status["status"] == "success":
                    for sub_id in self.exec_sessions:
                        if sub_id in self.sub_sessions:
                            sub_info = self.sub_sessions[sub_id]
                            if sub_info.get("task_id"):
                                self.on_task_completed(sub_info["task_id"])
        
        while True:
            _monitor()
            self.executor.shutdown(wait=False)
            self.executor = ThreadPoolExecutor(max_workers=4)
            time.sleep(interval)
    
    def shutdown(self):
        """关闭控制器"""
        print(f"\n🔚 关闭会话控制器")
        
        # 停止所有会话
        self.stop_all_background_sessions("控制器关闭")
        self.stop_main_session()
        
        # 关闭线程池
        self.executor.shutdown(wait=True)
        
        print(f"   ✓ 控制器已关闭")


# ========================= 类型定义 =========================

class Task:
    """任务对象"""
    def __init__(self, id: str, type: str, description: str, 
                 parameters: dict = {}, expected_behavior: str = ""):
        self.id = id
        self.type = type  # cron | skill | weather
        self.description = description
        self.parameters = parameters
        self.expected_behavior = expected_behavior
        self.status = "pending"  # pending | running | success | failed | retry | reexec
        self.created_at = datetime.now()
        self.attempts = 0
        self.retry_count = 0
        self.created_by = "user"
        self.session_data = {}  # 任务相关的会话数据
        
    def sub_task(self, sub_id: str) -> "Task":
        """获取子任务（如果是复合任务）"""
        if self.type == "skill_creation":
            return Task(
                id=sub_id,
                type="sub",
                description=self.parameters.get(sub_id, "待定"),
                parameters={},
                expected_behavior="待执行"
            )
        return None
    
    def is_composite(self) -> bool:
        """是否为复合任务（包含子任务）"""
        if self.type in ["skill_creation", "cron_task", "weather_query"]:
            return True
        return False
    
    def needs_execution(self) -> bool:
        """是否需要执行"""
        return self.status in ["pending", "retry", "reexec"]
    
    def can_retry(self) -> bool:
        """是否可以重试"""
        return self.status == "retry"
    
    def mark_completed(self, status: str = "success"):
        """标记任务状态"""
        self.status = status
        self.attempts += 1


# ========================= MemoryMaintainer 类 =========================

class MemoryMaintainer:
    """记忆维护器：负责任务执行和记忆管理
    
    核心功能：
    1. 自动维护 MEMORY.md 文件
    2. 任务分类与优先级调度
    3. 执行进度实时汇报
    4. 失败重试与恢复
    5. 成功结果验证
    6. 每日自动维护
    
    v2.0.0 核心优化：
    - ⚡ 会话独立控制，精确追踪
    - 🛑 session.stop 立即终止后台会话
    - 🎯 任务完成后清理相关会话
    - 🧹 定期清理终止/失败会话
    - ⚖️ 更理性的资源分配
    - 📊 双进度跟踪：执行 + 模型响应
    """
    
    def __init__(self):
        """初始化"""
        self.threads = {}  # 会话 ID -> 会话对象
        self.results = {}  # 会话 ID -> 执行结果
        self.max_retries = 3  # 最大重试次数
        self.task_metadata = {}  # 任务元数据（记录用户请求）
        self.last_progress = {}  # 最后进度记录
        
        # 会话控制器
        self.session_controller = SessionController(WORKSPACE)
        
        # 记忆文件路径
        self.memory_path = MEMORY_PATH
        self.daily_memory_dir = MEMORY_DAILY_DIR
        
        # 分类标记
        self.CATEGORY_SUCCESS = CATEGORY_SUCCESS
        self.CATEGORY_RETRYABLE = CATEGORY_RETRYABLE
        self.CATEGORY_FAILED = CATEGORY_FAILED
        self.CATEGORY_NEVER_USE = CATEGORY_NEVER_USE
        
        # 工作目录
        self.current_dir = os.getcwd()
        self.package_path = WORKSPACE + "/skills"
    """记忆维护器：负责任务执行和记忆管理"""
    
    def __init__(self):
        """初始化"""
        self.threads = {}  # 会话 ID -> 会话对象
        self.results = {}  # 会话 ID -> 执行结果
        self.max_retries = 3  # 最大重试次数
        self.task_metadata = {}  # 任务元数据（记录用户请求）
        self.last_progress = {}  # 最后进度记录
        
    def initialize_memory(self):
        """初始化记忆文件"""
        print(f"📝 正在初始化记忆文件...")
        
        # 确保 MEMORY.md 存在
        if not os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, 'w', encoding='utf-8') as f:
                f.write(self._get_memory_template())
        
        # 确保 memory 目录存在
        if not os.path.exists(Memory_Daily_DIR):
            os.makedirs(Memory_Daily_DIR)
        
        print("✅ 记忆文件初始化完成")
    
    def _get_memory_template(self) -> str:
        """获取记忆模板"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        return f"""# {timestamp} - {datetime.now().strftime("%Y年%m月%d日 - %A")}

## 🧠 记忆文件（长期记忆）

这个文件记录着主人和妹妹一起度过的时光，每一条记忆都承载着重要时刻和成长足迹。

**关于记忆更新**:
- **每日活动**: `memory/YYYY-MM-DD.md` 记录每天的日常
- **长期记忆**: 本文件记录重要决策、习惯、偏好和心得

**记忆分类**:
- 📌 定时任务配置
- 📚 学习成果（知识点、操作流程）
- 💕 用户偏好（称呼、习惯、聊天方式）
- 🛠️ 技能配置和工具使用
- ⏰ 时间相关（时区、常用时间段）

---

*这份记忆会持续更新，记录我们的每一次相遇。*

## 📋 重要配置

### 定时任务
### 技能配置
### 用户偏好

### 学习记录
- **主题**: [主题名称]
- **时间**: [开始时间]
- **时长**: [时长]
- **内容**: [学习内容摘要]
- **状态**: [成功/失败]
"""
    
    def check_feasibility(self, task: str, metadata: Dict = None) -> Dict:
        """检查任务可行性"""
        print(f"🔍 正在检查任务可行性：{task}")
        
        feasibility = {
            "task": task,
            "feasible": False,
            "issues": [],
            "recommendations": []
        }
        
        # 1. 检查记忆维护能力
        if not os.path.exists(MEMORY_PATH):
            feasibility["issues"].append("MEMORY.md 不存在，请先初始化记忆文件")
            feasibility["recommendations"].append("运行 initialize_memory() 初始化记忆文件")
        
        # 2. 检查用户请求
        if metadata:
            if not metadata.get("task"):
                feasibility["issues"].append("缺少任务描述")
                feasibility["recommendations"].append("请提供明确的任务描述")
            
            if not metadata.get("expected_behavior"):
                feasibility["issues"].append("缺少预期行为说明")
                feasibility["recommendations"].append("请描述你希望达到的效果")
        
        # 3. 检查资源
        self._check_resources(task)
        
        # 4. 返回结果
        if len(feasibility["issues"]) == 0:
            feasibility["feasible"] = True
        
        return feasibility
    
    def _check_resources(self, task: str):
        """检查所需资源"""
        print(f"   检查资源：{task}")
        
        # TODO: 根据任务类型检查具体资源
        # - API key
        # - 文件权限
        # - 网络连接
        # - 执行环境
    
    def classify_memory(self, task: str, result: Dict) -> str:
        """分类记忆写入"""
        # 根据任务类型和结果进行分类
        if result.get("success") and task in self._success_categories():
            return CATEGORY_SUCCESS
        elif result.get("retryable"):
            return CATEGORY_RETRY
        else:
            return CATEGORY_FAILED
    
    def _success_categories(self) -> List[str]:
        """成功写入永久记忆的任务类型"""
        return [
            "定时任务", "配置", "学习", "习惯", 
            "偏好", "设备", "决策", "总结"
        ]
    
    def execute_task(self, task: str, metadata: Dict = None, attempts: int = 0) -> Dict:
        """执行任务（带重试机制）"""
        print(f"🚀 开始执行任务：{task}")
        print(f"   尝试次数：{attempts + 1}")
        
        result = {
            "task": task,
            "attempt": attempts + 1,
            "success": False,
            "status": "initializing",
            "steps": [],
            "errors": [],
            "memory_entry": None
        }
        
        try:
            # Step 1: 可行性检查
            feasibility = self.check_feasibility(task, metadata)
            result["feasibility"] = feasibility
            
            if not feasibility["feasible"]:
                if attempts < self.max_retries:
                    attempts += 1
                    result = self.execute_task(task, metadata, attempts)
                    result["attempts"] = attempts
                    return result
                else:
                    result["status"] = "failed"
                    result["status"] = f"不可执行：{', '.join(feasibility['issues'])}"
                    self._log_failure(task, result, reason)
                    return result
            
            # Step 2: 实际执行（根据任务类型）
            result["status"] = "executing"
            print("   步骤 1: 可行性检查通过 ✅")
            
            if task == "配置定时任务":
                result = self._execute_cron_task(task, metadata)
            elif task == "创建技能":
                result = self._execute_skill_creation(task, metadata)
            elif task == "查询天气":
                result = self._execute_weather_query(task, metadata)
            else:
                result = self._execute_generic_task(task, metadata)
            
            result["status"] = "executed"
            print(f"   步骤 2: 任务执行中...")
            
            # Step 3: 实时汇报
            result["progress"] = self._generate_progress_report(result, attempts)
            print("   进度已汇报 ✅")
            
            # Step 4: 验证结果
            result["status"] = "verifying"
            if not self._verify_result(result, task):
                raise Exception(f"任务执行结果验证失败：{result.get('error', '未知错误')}")
            
            print("   步骤 3: 验证通过 ✅")
            
            # Step 5: 记忆写入
            if result.get("success"):
                result["status"] = "completed"
                print("   步骤 4: 记忆写入中...")
                result["memory_entry"] = self._generate_memory_entry(task, result)
                result["memory_path"] = self._save_memory_entry(task, result)
            else:
                result["status"] = "failed"
                print("   步骤 4: 执行失败")
                
        except Exception as e:
            # 内存崩溃或卡死，立即中止
            result["status"] = "crashed"
            result["error"] = str(e)
            result["traceback"] = traceback.format_exc()
            print(f"   🚨 内存崩溃/卡死，任务中止")
            
            if attempts < self.max_retries:
                attempts += 1
                result = self.execute_task(task, metadata, attempts)
                result["attempts"] = attempts
            else:
                # 最终失败
                result["status"] = "failed"
                self._log_failure(task, result, "多次重试后仍失败")
        
        return result
    
    def _execute_cron_task(self, task: str, metadata: Dict) -> Dict:
        """执行定时任务配置"""
        print("   正在配置定时任务...")
        # TODO: 实现 cron 任务配置
        return {"success": True, "method": "cron.add"}
    
    def _execute_skill_creation(self, task: str, metadata: Dict) -> Dict:
        """执行技能创建"""
        print("   正在创建技能...")
        # TODO: 实现技能创建
        return {"success": True, "method": "filesystem.create"}
    
    def _execute_weather_query(self, task: str, metadata: Dict) -> Dict:
        """执行天气查询"""
        print("   正在查询天气...")
        # TODO: 调用天气查询技能
        return {"success": True, "result": "天气查询成功"}
    
    def _execute_generic_task(self, task: str, metadata: Dict) -> Dict:
        """执行通用任务（通过会话）"""
        print("   正在创建子会话执行任务...")
        # TODO: 调用 sessions.spawn 创建子会话
        return {"success": True, "session_id": "xxx"}
    
    def _generate_progress_report(self, result: Dict, attempts: int) -> str:
        """生成进度汇报"""
        lines = [
            f"📊 任务执行进度汇报（尝试 {attempts}）",
            f"任务名称：{result.get('task', '未知')}",
            f"当前状态：{result.get('status', '未知')}",
        ]
        
        if result.get("steps"):
            lines.append("\n执行步骤：")
            for i, step in enumerate(result["steps"][:5], 1):  # 只显示前 5 步
                lines.append(f"  {i}. {step.get('name', '未知')} - {step.get('status', '进行中')}")
        
        if result.get("progress", ""):
            lines.append(f"\n进度说明：{result['progress']}")
        
        return "\n".join(lines)
    
    def _verify_result(self, result: Dict, task: str) -> bool:
        """验证任务执行结果"""
        print("   正在验证执行结果...")
        
        expected_behaviors = self._parse_expected_behaviors(task)
        actual_results = result.get("output", {})
        
        for expectation in expected_behaviors:
            if not self._check_expectation(actual_results, expectation):
                return False
        
        print("   验证通过 ✅")
        return True
    
    def _parse_expected_behaviors(self, task: str):
        """从任务描述中提取预期行为"""
        # TODO: 解析任务描述
        return []
    
    def _check_expectation(self, actual: Any, expectation: Dict) -> bool:
        """检查是否满足预期"""
        for key, expected_value in expectation.items():
            if expected_value == "any":
                continue
            elif not actual.get(key, "") == expected_value:
                return False
        return True
    
    def _generate_memory_entry(self, task: str, result: Dict) -> str:
        """生成记忆条目"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        task_name = result.get("task", task)
        
        entry = f"""---
## {task}

**时间**: {timestamp}

**描述**: {task_name}

**执行状态**: {result.get("status", "未知")}

**关键信息**:
- 方法：{result.get("method", "unknown")}
- 耗时：{result.get("duration", "N/A")}
- 资源：{result.get("resources", [])}

**记忆要点**:
{result.get("memory_content", "")}

---
"""
        return entry
    
    def _save_memory_entry(self, task: str, result: Dict) -> str:
        """保存记忆条目到文件"""
        path = os.path.join(MEMORY_PATH)
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"{timestamp}.md"
        filepath = os.path.join(Memory_Daily_DIR, filename)
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n## 记忆维护记录\n\n{result.get('memory_entry', '')}")
        
        return filepath
    
    def _log_failure(self, task: str, result: Dict, reason: str = "执行失败"):
        """记录失败日志"""
        log_entry = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "status": result.get("status", "unknown"),
            "reason": result.get("reason", reason),
            "error": result.get("error", ""),
            "traceback": result.get("traceback", ""),
            "attempt": result.get("attempt", 1),
            "retried": result.get("retried", False),
            "suggestion": self._generate_suggestion(task, result)
        }
        
        log_file = os.path.join(WORKSPACE, "memory", "failure.log")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n### {task}\n{json.dumps(log_entry, ensure_ascii=False, indent=2)}\n---\n")
    
    def _generate_suggestion(self, task: str, result: Dict) -> str:
        """生成失败处理建议"""
        if result.get("attempts", 0) >= self.max_retries:
            suggestions = []
            
            if "API key 不存在" in result.get("error", ""):
                suggestions.append("请配置对应的 API key")
            elif "权限不足" in result.get("error", ""):
                suggestions.append("请检查权限设置")
            elif "网络连接失败" in result.get("error", ""):
                suggestions.append("请检查网络连接")
            elif "参数错误" in result.get("error", ""):
                suggestions.append("请修正任务参数")
            elif "内存不足" in result.get("error", ""):
                suggestions.append("请降低任务复杂度或重启会话")
            
            if suggestions:
                return "建议：" + ", ".join(suggestions)
            else:
                return "建议：调整任务描述或使用其他执行方式"
        
        # 可重试时返回建议
        return "建议：当前重试，调整参数后再试"
    
    def cleanup_failed_tasks(self, days: int = 7):
        """清理失败的旧任务（保留最近的）"""
        pass
    
    def run_daily_maintenance(self):
        """运行每日维护"""
        # 1. 检查失败任务
        pass
        
        # 2. 更新记忆文件
        pass
        
        # 3. 清理旧文件
        pass


def main():
    """主入口"""
    maintainer = MemoryMaintainer()
    
    print("=" * 50)
    print("🧠 记忆维护技能 v2.0.0")
    print("=" * 50)
    
    # 获取用户输入
    task = input("\n📝 请输入任务描述：")
    metadata = {
        "expected_behavior": input("\n💡 请描述预期效果：")
    }
    
    # 初始化记忆
    maintainer.initialize_memory()
    
    # 检查可行性
    feasibility = maintainer.check_feasibility(task, metadata)
    
    if not feasibility["feasible"]:
        print(f"\n❌ 任务不可行：{', '.join(feasibility['issues'])}")
        print(f"📋 建议：{', '.join(feasibility['recommendations'])}")
        return
    
    print("\n✅ 任务可行，准备执行...")
    
    # 执行任务
    result = maintainer.execute_task(task, metadata)
    
    # 输出结果
    print("\n" + "=" * 50)
    print("📊 执行结果")
    print("=" * 50)
    
    print(f"\n任务：{result['task']}")
    print(f"状态：{result['status']}")
    print(f"尝试次数：{result.get('attempts', 1)}")
    
    if result.get('memory_entry'):
        print(f"\n📌 记忆已写入：{result['memory_path']}")
    
    if result.get('output'):
        print(f"\n💬 执行结果:")
        print(result['output'])
    
    print("\n" + "=" * 50)
    print(f"记忆维护完成！耗时：{result.get('duration', 'N/A')}")
    print("=" * 50)


if __name__ == "__main__":
    main()