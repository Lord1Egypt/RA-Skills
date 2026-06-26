#!/usr/bin/env python3
"""
OpenClaw Local Memory Skill 入口文件
"""
import sys
import json
from lib.memory_manager import memory_manager

def handle_message_received(payload):
    """收到用户消息时触发：注入相关记忆到上下文"""
    user_message = payload.get("message", {}).get("content", "")
    if not user_message:
        return payload
    
    # 检查是否是命令
    if user_message.startswith("/remember "):
        content = user_message[len("/remember "):].strip()
        if content:
            mem_id = memory_manager.add_memory(content, source="manual")
            return {
                "reply": f"✅ 已保存记忆，ID: {mem_id}\n内容：{content}"
            }
    elif user_message.startswith("/recall "):
        query = user_message[len("/recall "):].strip()
        if query:
            results = memory_manager.search_memories(query)
            if not results:
                return {"reply": "❌ 没有找到相关记忆"}
            reply = "🔍 相关记忆：\n"
            for i, res in enumerate(results, 1):
                reply += f"{i}. 相似度: {res['similarity']:.2f}\n   内容: {res['content']}\n   创建时间: {res['created_at'][:10]}\n"
            return {"reply": reply}
    elif user_message.startswith("/forget "):
        query = user_message[len("/forget "):].strip()
        if query:
            deleted = memory_manager.delete_by_query(query)
            if not deleted:
                return {"reply": "❌ 没有找到要删除的记忆"}
            reply = "🗑️ 已删除以下记忆：\n"
            for i, res in enumerate(deleted, 1):
                reply += f"{i}. {res['content']}\n"
            return {"reply": reply}
    elif user_message == "/memory-list":
        mems = memory_manager.list_all_memories()
        if not mems:
            return {"reply": "📋 还没有保存任何记忆"}
        reply = "📋 所有记忆列表：\n"
        for i, mem in enumerate(mems, 1):
            reply += f"{i}. ID: {mem['id']}\n   内容: {mem['content']}\n   类型: {mem['type']} | 创建时间: {mem['created_at'][:16]}\n"
        return {"reply": reply}
    
    # 非命令情况，注入上下文
    context = memory_manager.get_relevant_context(user_message)
    if context:
        # 把记忆注入到系统提示词
        if "system_prompt" in payload:
            payload["system_prompt"] = f"{context}\n\n{payload['system_prompt']}"
        else:
            payload["system_prompt"] = context
    
    return payload

def handle_response_sent(payload):
    """回复完成后触发：自动提取记忆保存"""
    user_message = payload.get("user_message", "")
    assistant_reply = payload.get("assistant_reply", "")
    
    if user_message and assistant_reply:
        # 自动提取记忆
        memory_manager.extract_memories_from_conversation(user_message, assistant_reply)
    
    return payload

def main():
    """OpenClaw技能入口"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <event> <payload>")
        sys.exit(1)
    
    event = sys.argv[1]
    payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    
    try:
        if event == "message_received":
            result = handle_message_received(payload)
            print(json.dumps(result))
        elif event == "response_sent":
            result = handle_response_sent(payload)
            print(json.dumps(result))
        else:
            print(json.dumps(payload))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        print(json.dumps(payload))

if __name__ == "__main__":
    main()
