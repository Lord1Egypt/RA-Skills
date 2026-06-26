# -*- coding: utf-8 -*-
"""
做梦脚本 - 调用MiniMax M2.7分析MemPalace记忆碎片，提炼精华到核心文档

运行时间：每天凌晨2:00
使用模型：MiniMax M2.7
API：openai-compat

作者：小麦
日期：2026-04-10
版本：v6 (通用版)
"""
import sys
import os
import json
import subprocess
from datetime import datetime
import traceback
from pathlib import Path
import requests

# 设置UTF-8输出
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 查找工作区根目录
def find_workspace_root():
    """查找工作区根目录"""
    current = Path(os.getcwd())

    # 查找包含 .learnings 或 skills 目录的根目录
    for parent in [current] + list(current.parents):
        if (parent / ".learnings").exists() or (parent / "skills").exists():
            return parent

    return current

WORKSPACE = find_workspace_root()

# 加载配置
CONFIG_FILE = WORKSPACE / "skills" / "continuous-learning" / "config" / "dream_config.json"

def load_config():
    """加载配置文件"""
    default_config = {
        'analysis': {
            'model': 'minimax',
            'model_name': 'MiniMax-M2.7',
            'api_url': 'https://api.minimax.chat/v1',
            'api_key': '',
            'timeout_seconds': 120,
            'temperature': 0.3
        },
        'notification': {
            'enabled': True,
            'channel': 'openclaw-weixin',
            'to': '',
            'account_id': '',
            'queue_file': '.notification_queue.json'
        },
        'mempalace': {
            'drawer': 'wing_xiaomai'
        }
    }

    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            # 深度更新
            def deep_update(d, u):
                for k, v in u.items():
                    if isinstance(v, dict):
                        d[k] = deep_update(d.get(k, {}), v)
                    else:
                        d[k] = v
                return d
            deep_update(default_config, user_config)
    except:
        pass

    return default_config

CONFIG = load_config()

# 目标文档
TARGET_DOCS = {
    'SOUL': {
        'path': WORKSPACE / 'SOUL.md',
        'purpose': '行为准则、个性偏好、沟通风格'
    },
    'AGENTS': {
        'path': WORKSPACE / 'AGENTS.md',
        'purpose': '工作流程、代理规则、交互模式'
    },
    'MEMORY': {
        'path': WORKSPACE / 'MEMORY.md',
        'purpose': '用户偏好、项目背景、长期记忆'
    },
    'TOOLS': {
        'path': WORKSPACE / 'TOOLS.md',
        'purpose': '工具配置、集成注意事项、坑'
    },
    'BOOTSTRAP': {
        'path': WORKSPACE / 'BOOTSTRAP.md',
        'purpose': '会话启动规则、预检清单'
    }
}

# 分析提示词
ANALYSIS_PROMPT = """## 做梦任务 - 分析MemPalace记忆碎片

我是OpenClaw AI助手，需要在每天凌晨2:00将记忆宫殿中的碎片记忆整理到我的核心文档。

### 我的核心文档结构
{doc_descriptions}

### 记忆碎片
以下是MemPalace中的日记条目({count}条)：
{entries_text}

### 分析要求

你现在需要完成以下任务：

1. **分类判断**：每个碎片应该归纳到哪个文档（SOUL/AGENTS/MEMORY/TOOLS/BOOTSTRAP）？

2. **价值判断**：这个碎片有无价值？请过滤掉：
   - 错误记录、异常堆栈
   - 临时测试、调试信息
   - 完全无意义的内容

3. **去重判断**：这个碎片是否与已有内容重复？如果是，标记为"重复"。

4. **提取精华**：将碎片的核心信息提炼成简洁的条目：
   - 不超过200字
   - 保持语境但不冗余
   - 如果是配置类，用关键信息表示

### 输出格式

请严格按照以下JSON格式输出，不要有任何额外的文字：

```json
{{
  "updates": [
    {{
      "doc": "SOUL|AGENTS|MEMORY|TOOLS|BOOTSTRAP",
      "content": "精炼后的条目内容",
      "fragment_id": "碎片ID"
    }}
  ],
  "skipped": [
    {{
      "fragment_id": "碎片ID",
      "reason": "无价值|重复|无关"
    }}
  ]
}}
```

注意：
- 只输出JSON，不要添加任何解释
- 如果所有碎片都无价值或重复，updates可以为空数组
- content必须是完整句子，包含必要上下文
"""

def call_minimax_api(messages):
    """调用MiniMax API"""
    api_config = CONFIG.get('analysis', {})
    api_url = api_config.get('api_url', 'https://api.minimax.chat/v1')
    api_key = api_config.get('api_key', '')
    model_name = api_config.get('model_name', 'MiniMax-M2.7')
    timeout = api_config.get('timeout_seconds', 120)

    if not api_key:
        print("[DREAM] 未配置MiniMax API Key，跳过分析")
        return None

    try:
        response = requests.post(
            f"{api_url}/chat/completions",
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': model_name,
                'messages': messages,
                'temperature': api_config.get('temperature', 0.3),
                'max_tokens': 4000
            },
            timeout=timeout
        )

        response.raise_for_status()
        result = response.json()

        return result['choices'][0]['message']['content']

    except Exception as e:
        print(f"[DREAM] API调用失败: {e}")
        return None

def load_mempalace_entries():
    """加载MemPalace中的日记条目"""
    try:
        mempalace_path = WORKSPACE / 'skills' / 'mempalace'
        if not mempalace_path.exists():
            print("[DREAM] MemPalace未安装，无法加载日记条目")
            return []

        sys.path.insert(0, str(mempalace_path))
        from mempalace.mcp_server import handle_request

        drawer = CONFIG.get('mempalace', {}).get('drawer', 'wing_xiaomai')

        result = handle_request({
            "method": "mcp__call",
            "params": {
                "name": "search_entries",
                "arguments": {
                    "drawer": drawer,
                    "limit": 100
                }
            }
        })

        if 'result' in result:
            raw_entries = result['result'].get('entries', [])
            # 去重（只取最近的100条）
            entries = []
            seen_ids = set()
            for entry in raw_entries:
                entry_id = entry.get('id')
                if entry_id and entry_id not in seen_ids:
                    entries.append(entry)
                    seen_ids.add(entry_id)
                if len(entries) >= 100:
                    break
            return entries

    except Exception as e:
        print(f"[DREAM] 加载MemPalace条目失败: {e}")
        traceback.print_exc()

    return []

def apply_updates(updates):
    """应用更新到文档"""
    updated_docs = []

    for update in updates:
        doc_name = update.get('doc')
        content = update.get('content', '')

        if doc_name not in TARGET_DOCS:
            continue

        doc_path = TARGET_DOCS[doc_name]['path']
        fragment_id = update.get('fragment_id', 'unknown')

        try:
            # 读取现有内容
            if doc_path.exists():
                with open(doc_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            else:
                existing_content = '# TODO\n'

            # 检查是否已存在（简单匹配）
            if content in existing_content:
                print(f"[DREAM] [{doc_name}] 已存在，跳过: {content[:50]}...")
                continue

            # 添加内容
            separator = '\n\n---\n\n'
            if not existing_content.endswith('\n'):
                separator = '\n' + separator

            new_content = existing_content + separator + content

            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"[DREAM] [{doc_name}] 已更新: {content[:60]}...")
            updated_docs.append(doc_name)

        except Exception as e:
            print(f"[DREAM] [{doc_name}] 更新失败: {e}")

    return updated_docs

def send_notification(message):
    """发送微信通知"""
    try:
        notification_config = CONFIG.get('notification', {})

        if not notification_config.get('enabled', False):
            return False

        to_user = notification_config.get('to', '')
        account_id = notification_config.get('account_id', '')

        if not to_user:
            print("[DREAM] 未配置通知目标，跳过")
            return False

        cmd = [
            'openclaw',
            'message', 'send',
            '--target', to_user,
            '--message', message,
            '--channel', notification_config.get('channel', 'openclaw-weixin')
        ]

        if account_id:
            cmd.extend(['--account', account_id])

        result = subprocess.run(cmd, timeout=30, cwd=str(WORKSPACE),
                                capture_output=True, text=True,
                                encoding='utf-8', errors='replace')

        return result.returncode == 0

    except Exception as e:
        print(f"[DREAM] 通知发送失败: {e}")
        return False

def queue_notification(message):
    """将通知存入队列"""
    try:
        notification_config = CONFIG.get('notification', {})
        queue_file = WORKSPACE / notification_config.get('queue_file', '.notification_queue.json')
        to_user = notification_config.get('to', '')

        notifications = []
        if queue_file.exists():
            with open(queue_file, 'r', encoding='utf-8') as f:
                notifications = json.load(f)

        notifications.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'to': to_user
        })

        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(notifications, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"[DREAM] 队列写入失败: {e}")
        return False

def main():
    """主函数"""
    print(f"[DREAM] 开始做梦分析 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 加载记忆碎片
    print("[DREAM] 加载MemPalace日记条目...")
    entries = load_mempalace_entries()

    if not entries:
        print("[DREAM] 没有新的日记条目，退出")
        return

    print(f"[DREAM] 找到 {len(entries)} 条日记条目")

    # 准备分析请求
    entries_text = "\n\n".join([
        f"[ID: {e.get('id', 'unknown')}] {e.get('title', '')}\n{e.get('content', '')[:500]}"
        for e in entries[:10]  # 限制数量避免token过多
    ])

    doc_descriptions = "\n".join([
        f"- {name}: {info['purpose']}"
        for name, info in TARGET_DOCS.items()
    ])

    prompt = ANALYSIS_PROMPT.format(
        doc_descriptions=doc_descriptions,
        count=len(entries),
        entries_text=entries_text
    )

    # 调用MiniMax
    print("[DREAM] 调用MiniMax M2.7分析...")
    response = call_minimax_api([
        {"role": "user", "content": prompt}
    ])

    if not response:
        print("[DREAM] 分析失败，跳过文档更新")
        return

    # 解析JSON响应
    try:
        response = response.strip()
        if response.startswith('```json'):
            response = response[7:]
        if response.startswith('```'):
            response = response[3:]
        if response.endswith('```'):
            response = response[:-3]
        response = response.strip()

        result = json.loads(response)
        updates = result.get('updates', [])
        skipped = result.get('skipped', [])

        print(f"[DREAM] 分析完成：{len(updates)}条更新，{len(skipped)}条跳过")

    except Exception as e:
        print(f"[DREAM] 解析响应失败: {e}")
        print(f"[DREAM] 原始响应: {response[:200]}...")
        return

    # 应用更新
    if updates:
        print(f"[DREAM] 应用更新到文档...")
        updated_docs = apply_updates(updates)

        # 发送通知
        doc_list = ", ".join(updated_docs)
        message = (
            f"✅ 做梦完成\n\n"
            f"⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"🔄 更新文档: {doc_list}\n"
            f"✨ 新增条目: {len(updates)}"
        )

        if send_notification(message):
            print("[DREAM] 微信通知已发送")
        else:
            print("[DREAM] 微信通知发送失败，已存入队列")
            queue_notification(message)
    else:
        print("[DREAM] 没有需要更新的内容")

    print(f"[DREAM] 做梦完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    try:
        start_time = datetime.now()
        main()
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"[DREAM] 总耗时: {elapsed:.2f}秒")
    except Exception as e:
        print(f"[DREAM] 做梦失败: {e}")
        traceback.print_exc()
