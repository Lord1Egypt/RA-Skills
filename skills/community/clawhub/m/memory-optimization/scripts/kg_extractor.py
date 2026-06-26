#!/usr/bin/env python3
"""
KG Extractor - 从 Agent 会话历史中提取知识图谱实体

从 agents/{main,altas}/sessions/*.jsonl 文件中解析对话，
使用 LLM 提取结构化实体并写入知识图谱。

使用方法:
    python3 kg_extractor.py --agents-dir agents/ --dry-run
    python3 kg_extractor.py --agents-dir agents/ --batch-size 5
    python3 kg_extractor.py --agents-dir agents/ --model glm-5
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field

# 导入 memory_ontology 的函数 (在 main() 中动态导入以支持 KG_DIR)

# 路径配置
SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent
ONTOLOGY_DIR = WORKSPACE_ROOT / "ontology"
KG_LOG_FILE = ONTOLOGY_DIR / "kg_extraction_log.jsonl"
sys.path.insert(0, str(SCRIPT_DIR))  # enable utils.llm_client import

from utils.llm_client import LLMClient  # noqa: E402

# 默认配置
DEFAULT_KG_DIR = ""  # 开发环境使用 ontology/
DEFAULT_API_KEY = ""  # 从环境变量 OPENAI_API_KEY 读取
DEFAULT_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"


def load_env_file():
    """从 .env 文件加载环境变量

    查找 WORKSPACE_ROOT/.env 文件并设置环境变量。
    跳过注释和空行，支持带引号的值。
    """
    env_file = WORKSPACE_ROOT / ".env"
    if not env_file.exists():
        return

    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            # 解析 KEY=value
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value:
                os.environ[key] = value


# 加载 .env 文件（如果存在）
load_env_file()


# ========== 数据模型 ==========

@dataclass
class Message:
    """单条消息"""
    role: str  # user, assistant
    content: str
    timestamp: str
    session_id: str = ""
    message_id: str = ""


@dataclass
class Conversation:
    """会话"""
    session_id: str
    messages: List[Message] = field(default_factory=list)
    timestamp: str = ""


@dataclass
class ExtractedEntity:
    """提取的实体"""
    type: str
    title: str
    rationale: str = ""
    content: str = ""
    lesson: str = ""
    description: str = ""
    made_at: str = ""
    discovered_at: str = ""
    learned_at: str = ""
    created_at: str = ""
    confidence: float = 0.5
    source: str = ""
    tags: List[str] = field(default_factory=list)


# ========== 1. JSONL Parser ==========

class JSONLParser:
    """解析 JSONL 会话文件"""

    @staticmethod
    def parse_file(file_path: Path) -> Optional[Conversation]:
        """解析单个 JSONL 文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            messages = []
            session_id = file_path.stem

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # 只处理 message 类型
                if data.get('type') != 'message':
                    continue

                msg_data = data.get('message', {})
                role = msg_data.get('role')

                if role not in ('user', 'assistant'):
                    continue

                # 提取内容
                content_parts = msg_data.get('content', [])
                if isinstance(content_parts, list):
                    content = ""
                    for part in content_parts:
                        if isinstance(part, dict):
                            if part.get('type') == 'text':
                                content += part.get('text', '')
                            elif part.get('type') == 'thinking':
                                # 可以选择包含 thinking 内容
                                pass
                else:
                    content = str(content_parts) if content_parts else ""

                if not content.strip():
                    continue

                timestamp = data.get('timestamp', '')
                message_id = data.get('id', '')

                messages.append(Message(
                    role=role,
                    content=content,
                    timestamp=timestamp,
                    session_id=session_id,
                    message_id=message_id
                ))

            if not messages:
                return None

            return Conversation(
                session_id=session_id,
                messages=messages,
                timestamp=messages[0].timestamp if messages else ""
            )

        except Exception as e:
            print(f"Warning: Failed to parse {file_path}: {e}")
            return None

    @staticmethod
    def scan_directory(agents_dir: Path) -> List[Path]:
        """扫描目录下所有 JSONL 文件"""
        jsonl_files = []

        if not agents_dir.exists():
            return jsonl_files

        # 扫描所有子目录
        for subdir in agents_dir.rglob('sessions'):
            if subdir.is_dir():
                jsonl_files.extend(subdir.glob('*.jsonl'))

        return sorted(jsonl_files)


# ========== 2. Message Filter ==========

class MessageFilter:
    """消息过滤和处理"""

    # 需要过滤的系统消息关键词
    SYSTEM_KEYWORDS = [
        'system', 'bootstrap', 'soUL', 'identity',
        'conversation info', 'sender (untrusted'
    ]

    # 错误消息标记
    ERROR_MARKERS = [
        'error', 'failed', 'exception', '429', '500',
        '暂未开放', '权限', 'throttled'
    ]

    @classmethod
    def is_system_message(cls, content: str) -> bool:
        """判断是否为系统消息"""
        content_lower = content.lower()
        return any(kw in content_lower for kw in cls.SYSTEM_KEYWORDS)

    @classmethod
    def is_error_message(cls, content: str) -> bool:
        """判断是否为错误消息"""
        # 检查是否没有实际内容
        if not content or len(content.strip()) < 5:
            return True

        content_lower = content.lower()
        # 如果主要是错误信息
        error_count = sum(1 for marker in cls.ERROR_MARKERS if marker in content_lower)
        if error_count >= 2:
            return True

        return False

    @classmethod
    def filter_messages(cls, messages: List[Message]) -> List[Message]:
        """过滤消息"""
        filtered = []

        for msg in messages:
            # 跳过系统消息
            if cls.is_system_message(msg.content):
                continue

            # 跳过纯错误消息
            if cls.is_error_message(msg.content):
                continue

            filtered.append(msg)

        return filtered

    @classmethod
    def merge_consecutive(cls, messages: List[Message]) -> List[Message]:
        """合并相邻的同类消息"""
        if not messages:
            return []

        merged = [messages[0]]

        for msg in messages[1:]:
            last_msg = merged[-1]

            # 如果是同一角色且间隔很短，合并
            if (msg.role == last_msg.role and
                msg.session_id == last_msg.session_id):
                last_msg.content += "\n" + msg.content
            else:
                merged.append(msg)

        return merged


# (LLMClient imported from utils.llm_client above)

# ========== 4. Entity Extractor ==========

EXTRACTION_PROMPT = """你是一个知识提取专家。分析以下对话，提取结构化实体。

对话内容：
{messages}

请提取以下类型的实体（JSON 格式）：
1. Decision: 重要决策（为什么做、替代方案、影响）
2. Finding: 发现/洞察（技术发现、流程改进、问题识别）
3. LessonLearned: 经验教训（错误、成功、最佳实践）
4. Commitment: 承诺（对用户的承诺、任务约定）
5. Concept: 高频术语（重要概念、专有名词）

输出格式（必须是有效 JSON）：
{{
  "entities": [
    {{
      "type": "Decision|Finding|LessonLearned|Commitment|Concept",
      "title": "实体标题",
      "rationale": "决策理由（仅 Decision）",
      "content": "发现内容（仅 Finding）",
      "lesson": "经验教训（仅 LessonLearned）",
      "description": "承诺内容（仅 Commitment）",
      "made_at": "决策时间 ISO 格式",
      "discovered_at": "发现时间 ISO 格式",
      "learned_at": "学习时间 ISO 格式",
      "created_at": "创建时间 ISO 格式",
      "confidence": 0.0-1.0,
      "tags": ["#tag1", "#tag2"]
    }}
  ]
}}

注意：
- 只输出 JSON，不要有其他内容
- 如果没有发现任何实体，返回空的 entities 数组
- 确保时间格式为 ISO 8601"""


class EntityExtractor:
    """实体提取器"""

    def __init__(self, client: LLMClient,
                 create_entity_fn=None, validate_entity_fn=None):
        self.client = client
        self._create_entity = create_entity_fn
        self._validate_entity = validate_entity_fn

    def extract(self, conversation: Conversation, dry_run: bool = False) -> List[ExtractedEntity]:
        """从会话中提取实体"""
        # 过滤消息
        filtered_messages = MessageFilter.filter_messages(conversation.messages)
        filtered_messages = MessageFilter.merge_consecutive(filtered_messages)

        if not filtered_messages:
            return []

        # 限制消息数量（避免过长）
        max_messages = 20
        if len(filtered_messages) > max_messages:
            filtered_messages = filtered_messages[-max_messages:]

        # 构建消息文本
        messages_text = self._format_messages(filtered_messages)

        # 调用 LLM
        prompt = EXTRACTION_PROMPT.format(messages=messages_text)

        llm_messages = [
            {"role": "system", "content": "你是一个专业的知识提取助手，只输出 JSON 格式。"},
            {"role": "user", "content": prompt}
        ]

        response = self.client.call(llm_messages)

        if not response:
            return []

        # 解析响应
        return self._parse_response(response, conversation.session_id, dry_run)

    def _format_messages(self, messages: List[Message]) -> str:
        """格式化消息为文本"""
        lines = []
        for msg in messages:
            role = "用户" if msg.role == "user" else "助手"
            # 截断过长内容
            content = msg.content[:500] + "..." if len(msg.content) > 500 else msg.content
            lines.append(f"[{role}]: {content}")

        return "\n".join(lines)

    def _parse_response(self, response: str, session_id: str,
                       dry_run: bool) -> List[ExtractedEntity]:
        """解析 LLM 响应"""
        entities = []

        try:
            # 尝试提取 JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
            else:
                data = json.loads(response)

            for item in data.get('entities', []):
                entity_type = item.get('type')

                # 映射到 schema 中的类型
                if entity_type == 'Concept':
                    # Concept 映射为 Finding
                    entity_type = 'Finding'
                    item['content'] = f"概念: {item.get('title')}"

                if entity_type not in ['Decision', 'Finding', 'LessonLearned', 'Commitment']:
                    continue

                # 提取时间字段
                time_field = None
                for tf in ['made_at', 'discovered_at', 'learned_at', 'created_at']:
                    if tf in item:
                        time_field = item[tf]
                        break

                if not time_field:
                    time_field = datetime.now().astimezone().isoformat()

                # 构建实体属性
                confidence_value = item.get('confidence', 0.5)

                props = {
                    'title': item.get('title', ''),
                    'tags': item.get('tags', ['#extracted']),
                    'source': f"session:{session_id}"
                }

                if entity_type == 'Decision':
                    # Decision 的 confidence 是数字类型
                    props['confidence'] = confidence_value if isinstance(confidence_value, (int, float)) else 0.5
                    props['rationale'] = item.get('rationale', '')
                    props['made_at'] = time_field
                    props['status'] = 'tentative'

                elif entity_type == 'Finding':
                    # Finding 的 confidence 是枚举字符串
                    if isinstance(confidence_value, (int, float)):
                        if confidence_value >= 0.8:
                            confidence_str = 'confirmed'
                        elif confidence_value >= 0.6:
                            confidence_str = 'likely'
                        elif confidence_value >= 0.4:
                            confidence_str = 'speculation'
                        else:
                            confidence_str = 'verified'
                    else:
                        confidence_str = confidence_value
                    props['confidence'] = confidence_str
                    props['content'] = item.get('content', '')
                    props['discovered_at'] = time_field
                    props['type'] = 'insight'

                elif entity_type == 'LessonLearned':
                    # LessonLearned 的 confidence 是枚举字符串
                    if isinstance(confidence_value, (int, float)):
                        if confidence_value >= 0.8:
                            confidence_str = 'confirmed'
                        elif confidence_value >= 0.6:
                            confidence_str = 'likely'
                        elif confidence_value >= 0.4:
                            confidence_str = 'speculation'
                        else:
                            confidence_str = 'verified'
                    else:
                        confidence_str = confidence_value
                    props['confidence'] = confidence_str
                    props['lesson'] = item.get('lesson', '')
                    props['learned_at'] = time_field
                    props['mistake_or_success'] = 'observation'

                elif entity_type == 'Commitment':
                    # Commitment 没有 confidence 评估，使用默认值
                    props['confidence'] = 0.5
                    props['description'] = item.get('description', '')
                    props['created_at'] = time_field
                    props['status'] = 'pending'

                # 验证实体
                errors = self._validate_entity(entity_type, props)
                if errors:
                    print(f"  Warning: Validation failed for {item.get('title')}: {errors}")
                    continue

                # Phase 8: 写入时门控检查
                gate_result = None
                try:
                    from write_time_gating import WriteTimeGating
                    gating = WriteTimeGating()
                    # 构建待评估实体
                    entity_for_gating = {
                        'type': entity_type,
                        'properties': props.copy()
                    }
                    gate_result = gating.gate(entity_for_gating, 'kg_extractor')

                    if gate_result.status == "REJECT":
                        print(f"  ⊘ Rejected by gating (score={gate_result.score.total_score:.3f})")
                        continue

                    if gate_result.status == "ARCHIVE":
                        print(f"  ⇢ Archived (score={gate_result.score.total_score:.3f})")
                        props['is_archived'] = True

                    # 将显著性评分添加到属性
                    props['significance_score'] = gate_result.score.total_score

                except Exception as gate_error:
                    print(f"  Warning: Gating check failed: {gate_error}")
                    # 门控失败时默认允许通过（不阻止实体创建）

                # 写入 KG（如果不是 dry-run）
                if not dry_run:
                    try:
                        entity = self._create_entity(entity_type, props)
                        score_str = f" (sig={gate_result.score.total_score:.2f})" if gate_result else ""
                        print(f"  ✓ Created {entity_type}: {props['title']}{score_str}")
                    except Exception as e:
                        print(f"  ✗ Failed to create entity: {e}")
                        continue

                entities.append(ExtractedEntity(
                    type=entity_type,
                    title=props['title'],
                    confidence=props['confidence'],
                    tags=props['tags']
                ))

        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse LLM response as JSON: {e}")
            print(f"Response: {response[:200]}...")

        return entities


# ========== 5. Batch Processor ==========

class BatchProcessor:
    """批量处理器"""

    def __init__(self, extractor: EntityExtractor):
        self.extractor = extractor
        self.stats = {
            'files_processed': 0,
            'files_with_entities': 0,
            'total_entities': 0,
            'by_type': {},
            'processed_files': []
        }

    def process_directory(self, agents_dir: Path, batch_size: int = 5,
                         dry_run: bool = False, limit: int = None,
                         log: bool = False) -> Dict:
        """处理目录下所有会话文件"""
        jsonl_files = JSONLParser.scan_directory(agents_dir)

        if limit:
            jsonl_files = jsonl_files[:limit]

        print(f"\n📁 Found {len(jsonl_files)} JSONL files")

        for i, file_path in enumerate(jsonl_files):
            print(f"\n[{i+1}/{len(jsonl_files)}] Processing: {file_path.name}")

            # 解析文件
            conversation = JSONLParser.parse_file(file_path)

            if not conversation:
                print(f"  ✗ No valid messages found")
                continue

            # 提取实体
            entities = self.extractor.extract(conversation, dry_run)

            # 更新统计
            self.stats['files_processed'] += 1

            if entities:
                self.stats['files_with_entities'] += 1
                self.stats['total_entities'] += len(entities)

                for entity in entities:
                    entity_type = entity.type
                    self.stats['by_type'][entity_type] = \
                        self.stats['by_type'].get(entity_type, 0) + 1

                print(f"  ✓ Extracted {len(entities)} entities")
            else:
                print(f"  - No entities extracted")

            # 记录已处理的文件
            self.stats['processed_files'].append({
                'file': str(file_path),
                'session_id': conversation.session_id,
                'entities_count': len(entities)
            })

            # 批量处理间隔
            if (i + 1) % batch_size == 0:
                print(f"\n--- Processed {i+1} files, pausing ---")
                if log:
                    _append_to_log(self.stats['processed_files'], batch_size)

        return self.stats


# ========== 6. Report Generator ==========

class ReportGenerator:
    """报告生成器"""

    @staticmethod
    def print_stats(stats: Dict):
        """打印统计信息"""
        print("\n" + "="*60)
        print("📊 KG Extractor Report")
        print("="*60)

        print(f"\n处理统计:")
        print(f"  文件总数: {stats['files_processed']}")
        print(f"  包含实体的文件: {stats['files_with_entities']}")
        print(f"  提取实体总数: {stats['total_entities']}")

        if stats['by_type']:
            print(f"\n按类型分布:")
            for entity_type, count in sorted(stats['by_type'].items(),
                                              key=lambda x: -x[1]):
                print(f"  {entity_type}: {count}")

        if stats.get('processed_files'):
            print(f"\n已处理文件列表 ({len(stats['processed_files'])}):")
            for pf in stats['processed_files']:
                print(f"  - {pf['file']} (session: {pf['session_id']}, entities: {pf['entities_count']})")

        print()


def _append_to_log(processed_files: list, batch_size: int = 5):
    """追加已处理文件到日志"""
    if not processed_files:
        return
    KG_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    # 只写入最新批次
    recent_files = processed_files[-batch_size:] if len(processed_files) > batch_size else processed_files
    with open(KG_LOG_FILE, 'a', encoding='utf-8') as f:
        for pf in recent_files:
            log_entry = {
                'timestamp': datetime.now().astimezone().isoformat(),
                **pf
            }
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')


# ========== Main ==========

def main():
    parser = argparse.ArgumentParser(
        description='KG Extractor - 从 Agent 会话中提取知识图谱实体'
    )

    parser.add_argument(
        '--agents-dir', '-d',
        type=Path,
        default=Path(os.environ.get('KG_AGENTS_DIR', WORKSPACE_ROOT / 'agents')),
        help='Agent 会话目录路径 (默认: KG_AGENTS_DIR 环境变量或 WORKSPACE_ROOT/agents)'
    )

    parser.add_argument(
        '--kg-dir',
        default='',
        help='知识图谱目录 (默认: ontology/, 生产: /root/.openclaw/workspace/memory/ontology/)'
    )

    parser.add_argument(
        '--model', '-m',
        default=None,
        help='LLM 模型名称 (默认从 OPENAI_MODEL 环境变量读取)'
    )

    parser.add_argument(
        '--api-key',
        default='',
        help='API Key (默认从环境变量 OPENAI_API_KEY 读取)'
    )

    parser.add_argument(
        '--base-url',
        default=None,
        help='API 基础 URL (默认从环境变量 OPENAI_BASE_URL 读取)'
    )

    parser.add_argument(
        '--batch-size', '-b',
        type=int,
        default=5,
        help='每批处理文件数'
    )

    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=None,
        help='限制处理文件数量（用于测试）'
    )

    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='仅模拟运行，不写入 KG'
    )

    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='输出报告到文件'
    )

    parser.add_argument(
        '--log',
        action='store_true',
        help='将处理记录写入日志文件 (ontology/kg_extraction_log.jsonl)'
    )

    args = parser.parse_args()

    # 设置知识图谱目录（必须在导入 memory_ontology 之前）
    if args.kg_dir:
        os.environ['KG_DIR'] = str(args.kg_dir)
        print(f"   KG目录: {args.kg_dir}")
    else:
        print(f"   KG目录: {WORKSPACE_ROOT / 'ontology'} (默认)")

    # 重新导入以应用 KG_DIR 配置
    if 'memory_ontology' in sys.modules:
        del sys.modules['memory_ontology']
    sys.path.insert(0, str(SCRIPT_DIR))
    from memory_ontology import create_entity, load_schema, validate_entity

    print("🚀 KG Extractor")
    print(f"   Agents目录: {args.agents_dir}")
    print(f"   模型: {args.model}")
    print(f"   Dry-run: {args.dry_run}")

    # 初始化组件
    llm_client = LLMClient(
        model=args.model,
        api_key=args.api_key,
        base_url=args.base_url
    )

    extractor = EntityExtractor(llm_client, create_entity, validate_entity)
    processor = BatchProcessor(extractor)

    # 处理
    stats = processor.process_directory(
        args.agents_dir,
        batch_size=args.batch_size,
        dry_run=args.dry_run,
        limit=args.limit,
        log=args.log
    )

    # 输出报告
    ReportGenerator.print_stats(stats)

    # 保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"✓ Report saved to: {args.output}")


if __name__ == '__main__':
    main()
