#!/usr/bin/env python3
"""
多模型对抗引擎 v2.0
集成：Key路由池 + 向量检索 + 代码沙箱 + WebSocket + 收敛判断

作者: 海狸 🦫
日期: 2026-04-02
"""

import json
import time
import sqlite3
import requests
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
import threading
import subprocess
import tempfile

# 添加路径以导入Key路由池
sys.path.insert(0, "/home/admin/.openclaw/workspace/multi_agent_engine")
try:
    from api_key_manager import get_key_router
    HAS_KEY_ROUTER = True
except ImportError:
    HAS_KEY_ROUTER = False
    print("⚠️ Key路由池未找到，使用默认配置")


# =========================
# 配置层
# =========================

BASE_URL = "https://coding.dashscope.aliyuncs.com/v1/chat/completions"
DEFAULT_API_KEY = "sk-sp-2b89d1b9a55d4cb9a8094c9127459aab"

# 四模型角色配置
ROLES = {
    "architect": {
        "model": "qwen3.5-plus",
        "name": "架构师",
        "emoji": "🏗️",
        "persona": "严谨、系统化、追求框架完整性",
        "task": "提出方案框架，设计整体架构",
        "key_type": "primary"
    },
    "engineer": {
        "model": "qwen3-coder-plus",
        "name": "工程师",
        "emoji": "🔧",
        "persona": "务实、高效、代码优先",
        "task": "实现方案，生成可执行代码",
        "key_type": "coder"
    },
    "security": {
        "model": "kimi-k2.5",
        "name": "安全官",
        "emoji": "🔍",
        "persona": "挑剔、攻击性、找漏洞",
        "task": "挑错攻击，指出方案缺陷",
        "key_type": "vision"
    },
    "judge": {
        "model": "MiniMax-M2.5",
        "name": "仲裁者",
        "emoji": "✅",
        "persona": "中立、公正、综合评判",
        "task": "评判辩论，判断是否收敛",
        "key_type": "primary"
    }
}

# WebSocket回调列表
ws_clients = []


# =========================
# 数据结构
# =========================

@dataclass
class DebateRound:
    """单轮辩论记录"""
    round_num: int
    role: str
    model: str
    input_prompt: str
    output_content: str
    reasoning: str = ""
    tokens_used: int = 0
    latency_ms: int = 0
    code_executed: str = ""  # 执行的代码
    code_result: str = ""     # 代码执行结果
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class DebateSession:
    """完整辩论会话"""
    session_id: str
    topic: str
    rounds: List[DebateRound] = field(default_factory=list)
    final_consensus: str = ""
    total_tokens: int = 0
    total_time_ms: int = 0
    status: str = "pending"
    convergence_score: float = 0.0
    knowledge_used: List[str] = field(default_factory=list)


# =========================
# 向量检索增强
# =========================

class VectorEnhancer:
    """向量检索增强器"""
    
    def __init__(self, kb_path: str = "/home/admin/.openclaw/workspace/kb"):
        self.kb_path = kb_path
        self._check_availability()
    
    def _check_availability(self):
        """检查向量检索是否可用"""
        self.available = os.path.exists(self.kb_path)
        if self.available:
            print(f"✅ 知识库路径存在: {self.kb_path}")
        else:
            print(f"⚠️ 知识库路径不存在: {self.kb_path}")
    
    def search(self, query: str, top_k: int = 3) -> List[str]:
        """检索相关知识"""
        if not self.available:
            return []
        
        # 简单关键词匹配（后续可接入ChromaDB）
        results = []
        try:
            for root, dirs, files in os.walk(self.kb_path):
                for file in files:
                    if file.endswith('.md'):
                        filepath = os.path.join(root, file)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if any(kw in content for kw in query.split()[:3]):
                                results.append(f"[{file}]\n{content[:500]}...")
                                if len(results) >= top_k:
                                    return results
        except Exception as e:
            print(f"⚠️ 检索失败: {e}")
        
        return results


# =========================
# 代码沙箱
# =========================

class CodeSandbox:
    """Python代码沙箱执行器"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    def run_safely(self, code: str) -> Tuple[bool, str]:
        """
        安全执行Python代码
        
        Returns:
            (success, output)
        """
        if not code or not code.strip():
            return False, "无代码可执行"
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            result = subprocess.run(
                ['python3', temp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd='/tmp'
            )
            
            if result.returncode == 0:
                return True, result.stdout or "(执行成功，无输出)"
            else:
                return False, f"执行错误:\n{result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, f"执行超时（>{self.timeout}秒）"
        except Exception as e:
            return False, f"执行异常: {str(e)}"
        finally:
            os.unlink(temp_path)


# =========================
# LLM调用层
# =========================

def get_api_key(model: str) -> str:
    """获取API Key（优先使用路由池）"""
    if HAS_KEY_ROUTER:
        router = get_key_router()
        return router.request_key(model)
    return DEFAULT_API_KEY


def release_api_key(model: str, rate_limit_hit: bool = False):
    """释放API Key"""
    if HAS_KEY_ROUTER:
        router = get_key_router()
        # 查找key_type
        for role_config in ROLES.values():
            if role_config["model"] == model:
                router.release_key(role_config["key_type"], rate_limit_hit)
                break


def call_llm(model: str, system_prompt: str, user_prompt: str) -> Dict:
    """调用LLM API"""
    start_time = time.time()
    api_key = get_api_key(model)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    try:
        resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=90)
        
        if resp.status_code != 200:
            release_api_key(model, rate_limit_hit=(resp.status_code == 429))
            return {"success": False, "error": f"API错误 {resp.status_code}", "model": model}
        
        data = resp.json()
        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {})
        
        content = message.get("content", "")
        reasoning = message.get("reasoning_content", "")
        usage = data.get("usage", {})
        total_tokens = usage.get("total_tokens", 0)
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        release_api_key(model)
        
        return {
            "content": content,
            "reasoning": reasoning,
            "tokens": total_tokens,
            "latency_ms": latency_ms,
            "model": model,
            "success": True
        }
        
    except requests.Timeout:
        release_api_key(model)
        return {"success": False, "error": "超时90秒", "model": model}
    except Exception as e:
        release_api_key(model)
        return {"success": False, "error": str(e), "model": model}


# =========================
# 收敛判断器
# =========================

class ConvergenceChecker:
    """收敛判断器"""
    
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold
    
    def check(self, judge_content: str) -> Tuple[bool, float]:
        """
        判断是否收敛
        
        Returns:
            (is_converged, score)
        """
        # 关键词判断
        positive_keywords = ["共识达成", "方案收敛", "最终方案", "一致同意", "无需继续"]
        negative_keywords = ["未收敛", "继续辩论", "仍有分歧", "需要修正"]
        
        score = 0.5  # 基础分
        
        for kw in positive_keywords:
            if kw in judge_content:
                score += 0.15
        
        for kw in negative_keywords:
            if kw in judge_content:
                score -= 0.15
        
        score = max(0.0, min(1.0, score))
        
        return score >= self.threshold, score


# =========================
# 核心引擎
# =========================

class AdversarialEngine:
    """多模型对抗引擎 v2.0"""
    
    def __init__(self, db_path: str = "/home/admin/.openclaw/workspace/data/adversarial_debates.db"):
        self.db_path = db_path
        self.vector_enhancer = VectorEnhancer()
        self.code_sandbox = CodeSandbox()
        self.convergence_checker = ConvergenceChecker()
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS debates (
                session_id TEXT PRIMARY KEY,
                topic TEXT,
                final_consensus TEXT,
                total_tokens INTEGER,
                total_time_ms INTEGER,
                status TEXT,
                convergence_score REAL,
                knowledge_used TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                round_num INTEGER,
                role TEXT,
                model TEXT,
                input_prompt TEXT,
                output_content TEXT,
                reasoning TEXT,
                code_executed TEXT,
                code_result TEXT,
                tokens_used INTEGER,
                latency_ms INTEGER,
                timestamp TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES debates(session_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _build_prompt(self, role_key: str, round_num: int, history: List[DebateRound], 
                      topic: str, knowledge: List[str]) -> Tuple[str, str]:
        """构建提示词"""
        role = ROLES[role_key]
        
        # 系统提示词
        system_prompt = f"""你是{role['emoji']} {role['name']}。

你的性格：{role['persona']}
你的任务：{role['task']}

辩论规则：
1. 必须基于事实和逻辑发言
2. 不得重复自己之前的观点
3. 每轮必须有新内容推进
4. 最终目标是达成共识方案

请用中文回复，保持专业但有个性的风格。"""
        
        # 历史上下文
        history_text = ""
        if history:
            history_text = "\n\n=== 前几轮辩论记录 ===\n"
            for r in history[-4:]:
                role_info = ROLES.get(r.role, {})
                history_text += f"\n{role_info.get('emoji', '?')} {role_info.get('name', r.role)} (Round {r.round_num}):\n{r.output_content[:400]}\n"
                if r.code_result:
                    history_text += f"  💻 代码执行结果: {r.code_result[:200]}\n"
        
        # 知识库上下文
        knowledge_text = ""
        if knowledge:
            knowledge_text = "\n\n=== 知识库检索结果 ===\n" + "\n".join(knowledge[:2])
        
        # 用户提示词
        if role_key == "architect":
            if round_num == 1:
                user_prompt = f"辩论主题：{topic}{knowledge_text}\n\n请你提出完整的方案框架。"
            else:
                user_prompt = f"{history_text}\n\n请根据反馈修正方案。"
                
        elif role_key == "engineer":
            user_prompt = f"{history_text}{knowledge_text}\n\n请实现方案并生成可执行的Python代码（用```python包裹）。"
            
        elif role_key == "security":
            user_prompt = f"{history_text}\n\n请攻击当前方案，找出漏洞。"
            
        elif role_key == "judge":
            user_prompt = f"{history_text}\n\n请评判本轮辩论：\n1. 哪方观点更有说服力？\n2. 方案是否收敛？\n3. 是否达成共识？\n\n明确回答：是否达成共识？"
        
        return system_prompt, user_prompt
    
    def _extract_code(self, content: str) -> str:
        """提取代码块"""
        if "```python" in content:
            start = content.find("```python") + 9
            end = content.find("```", start)
            if end > start:
                return content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            if end > start:
                return content[start:end].strip()
        return ""
    
    async def broadcast_ws(self, data: dict):
        """广播到WebSocket客户端"""
        global ws_clients
        for ws in ws_clients[:]:
            try:
                await ws.send_text(json.dumps(data, ensure_ascii=False))
            except:
                ws_clients.remove(ws)
    
    def run_debate(self, topic: str, max_rounds: int = 5, 
                   enable_code_sandbox: bool = True,
                   enable_vector_search: bool = True) -> DebateSession:
        """执行完整对抗辩论"""
        session_id = f"DEBATE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        session = DebateSession(session_id=session_id, topic=topic)
        
        print(f"\n{'='*60}")
        print(f"🚀 多模型对抗引擎 v2.0 启动")
        print(f"📌 主题: {topic}")
        print(f"🆔 会话ID: {session_id}")
        print(f"🔧 代码沙箱: {'✅' if enable_code_sandbox else '❌'}")
        print(f"📚 向量检索: {'✅' if enable_vector_search else '❌'}")
        print(f"{'='*60}\n")
        
        # 向量检索增强
        if enable_vector_search:
            knowledge = self.vector_enhancer.search(topic)
            session.knowledge_used = knowledge
            if knowledge:
                print(f"📚 检索到 {len(knowledge)} 条相关知识\n")
        
        round_sequence = ["architect", "engineer", "security", "judge"]
        
        for round_num in range(1, max_rounds + 1):
            print(f"\n{'='*20} Round {round_num} {'='*20}")
            
            for role_key in round_sequence:
                role = ROLES[role_key]
                
                system_prompt, user_prompt = self._build_prompt(
                    role_key, round_num, session.rounds, topic, session.knowledge_used
                )
                
                print(f"\n{role['emoji']} {role['name']} ({role['model']}) 正在发言...")
                
                # 调用LLM
                result = call_llm(
                    model=role["model"],
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                )
                
                if not result.get("success"):
                    print(f"❌ 调用失败: {result.get('error')}")
                    session.status = "error"
                    return session
                
                # 提取并执行代码（工程师角色）
                code_executed = ""
                code_result = ""
                if role_key == "engineer" and enable_code_sandbox:
                    code_executed = self._extract_code(result["content"])
                    if code_executed:
                        print(f"💻 执行代码...")
                        success, code_result = self.code_sandbox.run_safely(code_executed)
                        if success:
                            print(f"✅ 代码执行成功")
                        else:
                            print(f"⚠️ 代码执行失败: {code_result[:100]}")
                
                # 记录本轮
                debate_round = DebateRound(
                    round_num=round_num,
                    role=role_key,
                    model=role["model"],
                    input_prompt=user_prompt,
                    output_content=result["content"],
                    reasoning=result.get("reasoning", ""),
                    tokens_used=result["tokens"],
                    latency_ms=result["latency_ms"],
                    code_executed=code_executed,
                    code_result=code_result
                )
                session.rounds.append(debate_round)
                session.total_tokens += result["tokens"]
                session.total_time_ms += result["latency_ms"]
                
                print(f"\n💬 {result['content'][:300]}...")
                print(f"\n⚡ {result['latency_ms']}ms | 📊 {result['tokens']} tokens")
                
                # 收敛判断（仲裁者）
                if role_key == "judge":
                    is_converged, score = self.convergence_checker.check(result["content"])
                    session.convergence_score = score
                    
                    print(f"\n📊 收敛度: {score:.2f}")
                    
                    if is_converged:
                        print(f"\n✅ 共识达成！收敛度 {score:.2f} >= 0.7")
                        session.final_consensus = result["content"]
                        session.status = "done"
                        break
                
                time.sleep(0.3)
            
            if session.status == "done":
                break
        else:
            # 未收敛，取最后仲裁者结论
            last_judge = [r for r in session.rounds if r.role == "judge"][-1]
            session.final_consensus = last_judge.output_content
            session.status = "partial"
        
        # 保存到数据库
        self._save_session(session)
        
        print(f"\n{'='*60}")
        print(f"🎉 辩论完成！")
        print(f"📊 总消耗: {session.total_tokens} tokens, {session.total_time_ms}ms")
        print(f"📈 收敛度: {session.convergence_score:.2f}")
        print(f"📋 状态: {session.status}")
        print(f"{'='*60}\n")
        
        return session
    
    def _save_session(self, session: DebateSession):
        """保存会话到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO debates 
            (session_id, topic, final_consensus, total_tokens, total_time_ms, 
             status, convergence_score, knowledge_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session.session_id,
            session.topic,
            session.final_consensus,
            session.total_tokens,
            session.total_time_ms,
            session.status,
            session.convergence_score,
            json.dumps(session.knowledge_used, ensure_ascii=False)
        ))
        
        for r in session.rounds:
            cursor.execute("""
                INSERT INTO rounds 
                (session_id, round_num, role, model, input_prompt, output_content,
                 reasoning, code_executed, code_result, tokens_used, latency_ms, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id,
                r.round_num,
                r.role,
                r.model,
                r.input_prompt,
                r.output_content,
                r.reasoning,
                r.code_executed,
                r.code_result,
                r.tokens_used,
                r.latency_ms,
                r.timestamp
            ))
        
        conn.commit()
        conn.close()
        print(f"💾 已保存到数据库: {self.db_path}")
    
    def resume_debate(self, session_id: str) -> Optional[DebateSession]:
        """恢复中断的辩论"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM debates WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        # 重建session
        session = DebateSession(
            session_id=row[0],
            topic=row[1],
            final_consensus=row[2] or "",
            total_tokens=row[3],
            total_time_ms=row[4],
            status=row[5],
            convergence_score=row[6] or 0.0,
            knowledge_used=json.loads(row[7]) if row[7] else []
        )
        
        # 加载rounds
        cursor.execute("SELECT * FROM rounds WHERE session_id = ? ORDER BY id", (session_id,))
        for r in cursor.fetchall():
            session.rounds.append(DebateRound(
                round_num=r[2],
                role=r[3],
                model=r[4],
                input_prompt=r[5],
                output_content=r[6],
                reasoning=r[7] or "",
                code_executed=r[8] or "",
                code_result=r[9] or "",
                tokens_used=r[10],
                latency_ms=r[11],
                timestamp=r[12]
            ))
        
        conn.close()
        print(f"🔄 已恢复会话: {session_id}, 已完成 {len(session.rounds)} 轮")
        return session


# =========================
# CLI入口
# =========================

if __name__ == "__main__":
    engine = AdversarialEngine()
    
    topic = "如何设计一个高并发CNC报价系统？"
    
    session = engine.run_debate(
        topic=topic,
        max_rounds=3,
        enable_code_sandbox=True,
        enable_vector_search=True
    )
    
    print("\n" + "="*60)
    print("📋 最终共识：")
    print("="*60)
    print(session.final_consensus[:500])